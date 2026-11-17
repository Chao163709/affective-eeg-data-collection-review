"""Sensitivity of rating shares to crossed participant/stimulus REML.

Profiles the residual variance and intercept using the determinant lemma and
Woodbury identity. Reports point estimates, not calibrated confidence bounds.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize
from scipy.sparse.csgraph import connected_components

from verified_analysis import balanced_components, icc_batch, rating_matrices, verified_input_hashes

ROOT = Path(__file__).resolve().parents[1]


def design(y):
    people, clips = np.where(np.isfinite(y))
    values = y[people, clips]
    i, s = y.shape
    z = np.zeros((len(values), i+s))
    z[np.arange(len(values)), people] = 1
    z[np.arange(len(values)), i+clips] = 1
    graph = z.T@z
    if connected_components(graph, directed=False, return_labels=False) != 1:
        raise ValueError('Participant/stimulus graph is disconnected')
    return values, z


def profile(values, z):
    n, q = z.shape
    mean = values.mean()
    y = values-mean
    ztz, zy, z1 = z.T@z, z.T@y, z.sum(axis=0)
    y2, sum_y = float(y@y), float(y.sum())

    def evaluate(ratios, n_people):
        scale = np.sqrt(np.r_[np.full(n_people, ratios[0]),
                               np.full(q-n_people, ratios[1])])
        m = np.eye(q) + scale[:, None]*ztz*scale[None, :]
        factor = cho_factor(m, lower=True, check_finite=False)
        rhs = np.column_stack((scale*z1, scale*zy))
        correction = rhs.T@cho_solve(factor, rhs, check_finite=False)
        xx, xy, yy = n-correction[0, 0], sum_y-correction[0, 1], y2-correction[1, 1]
        residual = yy-xy*xy/xx
        if residual <= 0 or xx <= 0:
            raise ValueError('Degenerate REML scale or intercept information')
        variance = residual/(n-1)
        score = (n-1)*np.log(variance) + 2*np.log(np.diag(factor[0])).sum()+np.log(xx)
        return float(score), float(variance), float(mean+xy/xx)

    return evaluate


def fit(y):
    values, z = design(y)
    evaluate = profile(values, z)
    candidates = []
    score, residual, mean = evaluate([0., 0.], y.shape[0])
    candidates.append(dict(score=score, ratios=[0., 0.], residual=residual, mean=mean,
                           success=True, model='residual only'))
    for active in [(0,), (1,), (0, 1)]:
        for start in [-2., 0., 2.]:
            def objective(log_ratios):
                ratios = np.zeros(2)
                ratios[list(active)] = np.exp(log_ratios)
                return evaluate(ratios, y.shape[0])[0]
            result = minimize(objective, np.full(len(active), start), method='L-BFGS-B',
                              bounds=[(-12., 12.)]*len(active),
                              options={'ftol': 1e-12, 'gtol': 1e-6, 'maxiter': 500})
            ratios = np.zeros(2)
            ratios[list(active)] = np.exp(result.x)
            score, residual, mean = evaluate(ratios, y.shape[0])
            candidates.append(dict(score=score, ratios=ratios.tolist(), residual=residual,
                mean=mean, success=bool(result.success), model=str(active)))
    best = min(candidates, key=lambda c: c['score'])
    if not best['success']:
        raise RuntimeError('Best REML optimization did not converge')
    parts = np.r_[np.array(best['ratios'])*best['residual'], best['residual']]
    shares = parts/parts.sum()
    return dict(components=parts.tolist(), shares=shares.tolist(), mean=best['mean'],
                restricted_profile_objective=best['score'], boundary_model=best['model'],
                converged=best['success'])


def check():
    rng = np.random.default_rng(20261108)
    balanced = rng.normal(size=(8, 11)) + np.arange(8)[:, None]*.7 + np.arange(11)[None, :]*.5
    np.testing.assert_allclose(fit(balanced)['shares'], balanced_components(balanced), atol=2e-5)
    toy = balanced[:4, :5].copy()
    toy[1, 2] = np.nan
    values, z = design(toy)
    evaluate = profile(values, z)
    # Independent dense covariance likelihood verifies the low-rank identity.
    for ratios in [(0., 0.), (.2, 2.), (0., 1.)]:
        v = np.eye(len(values)) + ratios[0]*z[:, :4]@z[:, :4].T + ratios[1]*z[:, 4:]@z[:, 4:].T
        inverse = np.linalg.inv(v)
        one = np.ones(len(values))
        mean = (one@inverse@values)/(one@inverse@one)
        resid = values-mean
        variance = (resid@inverse@resid)/(len(values)-1)
        score = (len(values)-1)*np.log(variance)+np.linalg.slogdet(v)[1]+np.log(one@inverse@one)
        np.testing.assert_allclose(evaluate(ratios, 4), [score, variance, mean], atol=1e-10)


def main():
    check()
    output = dict(method='crossed random-intercept Gaussian REML; profiled intercept/residual scale',
        component_order=['participant', 'stimulus', 'residual (interaction plus measurement error)'],
        uncertainty='point-estimate sensitivity only; no confidence intervals',
        assumptions='independent random intercepts, common residual variance, ignorable observed-cell pattern',
        input_sha256=verified_input_hashes(), numpy_version=np.__version__, scipy_version=scipy.__version__,
        loader_sha256=hashlib.sha256((ROOT/'scripts/verified_analysis.py').read_bytes()).hexdigest(),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), corpora={})
    for name, a in rating_matrices().items():
        output['corpora'][name] = {}
        for j, dim in enumerate(('valence', 'arousal')):
            result = fit(a[..., j])
            result['one_way_share'] = float(icc_batch(a[..., j]))
            result['n_observations'] = int(np.isfinite(a[..., j]).sum())
            output['corpora'][name][dim] = result
            print(name, dim, 'one-way', round(result['one_way_share'], 4),
                  'crossed', np.round(result['shares'], 4).tolist(), flush=True)
    (ROOT/'results/crossed_rating_reml_20261108.json').write_text(
        json.dumps(output, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
