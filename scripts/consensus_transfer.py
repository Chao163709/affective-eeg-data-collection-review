"""Recompute Table V: LOSO losses and paired participant-loss intervals.

Bootstrap fixed held-out losses, not refitted predictors or a crossed design.
Outputs retain the historical list schema used by the review's figure builder.
"""
from __future__ import annotations

import hashlib
import json
import zlib
from pathlib import Path

import numpy as np

from verified_analysis import input_paths, rating_matrices

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261104
REPLICATES = 2000


def participant_losses(y):
    losses = []
    for i in range(len(y)):
        train = np.delete(y, i, axis=0)
        valid = np.isfinite(y[i])
        assert valid.any(), f'Participant {i} has no observations'
        pred = np.nanmean(train, axis=0)[valid]
        assert np.isfinite(pred).all(), 'A held-out stimulus has no training rating'
        null = np.nanmean(train)
        losses.append([np.mean((y[i, valid] - pred)**2),
                       np.mean((y[i, valid] - null)**2)])
    return np.asarray(losses)


def consensus_q(losses):
    means = np.mean(losses, axis=-2)
    assert np.all(means[..., 1] > 0)
    return 1 - means[..., 0] / means[..., 1]


def main():
    # Hand-check self-exclusion, missing ratings and ratio-of-means aggregation.
    np.testing.assert_allclose(participant_losses(np.array([[1., 2.], [3., 4.]])),
                               [[4., 4.25], [4., 4.25]])
    np.testing.assert_allclose(participant_losses(np.array([[1., np.nan], [3., 4.], [5., 6.]]))[0],
                               [9., 12.25])
    np.testing.assert_allclose(consensus_q(np.array([[1., 2.], [3., 6.]])), .5)
    previous = {r['corpus']: r for r in json.loads((ROOT / 'results/step1_consensus.json').read_text())}
    output = []
    for name, a in rating_matrices().items():
        seed = SEED + zlib.crc32(name.encode('utf-8'))
        draws = np.random.default_rng(seed).integers(0, len(a), size=(REPLICATES, len(a)))
        for j, dim in enumerate(['valence', 'arousal']):
            key = name.replace('-HCI', '') + '_' + dim
            losses = participant_losses(a[:, :, j])
            lc, ln = losses.mean(axis=0)
            q = float(consensus_q(losses))
            np.testing.assert_allclose([lc, ln, q],
                [previous[key]['L_ref'], previous[key]['L_null'], previous[key]['R2_consensus']],
                rtol=0, atol=1e-12)
            lo, hi = np.quantile(consensus_q(losses[draws]), [.025, .975], method='linear')
            row = dict(corpus=key, n=len(a), L_ref=float(lc), L_null=float(ln),
                       R2_consensus=q, lo=float(lo), hi=float(hi), seed=seed,
                       replicates=REPLICATES, per_participant_losses=losses.tolist(),
                       matrix_sha256=hashlib.sha256(a[:, :, j].copy().tobytes()).hexdigest())
            output.append(row)
            print(f'{key}: {q:.3f} [{lo:.3f}, {hi:.3f}] (point matches archive)')
    metadata = dict(script='scripts/consensus_transfer.py',
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        numpy_version=np.__version__, base_seed=SEED, replicates=REPLICATES,
        seed_rule='base_seed + crc32(UTF-8 corpus name)',
        bootstrap='paired resampling of fixed participant loss pairs, with replacement',
        scope='descriptive participant variation; predictors not refitted; stimuli fixed',
        quantile_method='linear',
        inputs={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):
                hashlib.sha256(p.read_bytes()).hexdigest()
                for p in [ROOT / 'scripts/verified_analysis.py',
                          ROOT / 'results/rating_input_manifest_20261108.json',
                          *input_paths().values()]})
    (ROOT / 'results/step1_consensus.json').write_text(json.dumps(output, indent=2, allow_nan=False), encoding='utf-8')
    (ROOT / 'results/consensus_transfer_provenance.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
