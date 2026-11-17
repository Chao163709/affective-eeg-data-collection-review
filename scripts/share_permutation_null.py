"""Within-participant shuffle reference for the share (review Section VI-B).

Null: within each participant, the observed ratings are reassigned across the
stimuli that participant actually rated.  This holds the participant's rating
distribution and the design's missing-cell pattern fixed and changes only which
stimulus a rating is attached to.  Shuffling within a stimulus would leave every
stimulus mean unchanged and is not a null for this statistic.

Output: results/share_permutation_null.json (back up before rerunning).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

import verified_analysis as va

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261102
BOOT = 2000


def permute_within_participant(y, rng, n_perm):
    """Reassign each participant's observed ratings across their rated stimuli."""
    i, s = y.shape
    out = np.full((n_perm, i, s), np.nan)
    for r in range(i):
        row = y[r]
        obs = np.isfinite(row)
        n = int(obs.sum())
        if n < 2:
            out[:, r, obs] = row[obs]
            continue
        vals = row[obs]
        order = np.argsort(rng.random((n_perm, n)), axis=1)
        out[:, r, obs] = vals[order]
    return out


def main():
    rng = np.random.default_rng(SEED)
    result = {
        "seed": SEED,
        "n_permutations": BOOT,
        "statistic": "unequal-group one-way moment estimate (R2_stim)",
        "null": "ratings reassigned across stimuli within participant; "
                "participant distribution and missing-cell pattern held fixed",
        "p_rule": "(1 + #{null >= observed}) / (B + 1)",
        "corpora": {},
    }
    for name, a in va.rating_matrices().items():
        result["corpora"][name] = {}
        for j, dim in enumerate(("valence", "arousal")):
            y = a[..., j]
            observed = float(va.icc_batch(y))
            null = va.icc_batch(permute_within_participant(y, rng, BOOT))
            if not np.isfinite(null).all():
                raise ValueError(f"Non-finite shuffle statistic: {name} {dim}")
            p = (1.0 + float((null >= observed).sum())) / (BOOT + 1.0)
            result["corpora"][name][dim] = {
                "observed": observed,
                "null_q50": float(np.percentile(null, 50)),
                "null_q95": float(np.percentile(null, 95)),
                "null_q99": float(np.percentile(null, 99)),
                "null_max": float(null.max()),
                "n_null_ge_observed": int((null >= observed).sum()),
                "p": p,
            }
            print(f"{name:12s} {dim:8s} obs={observed:.4f} "
                  f"null95={result['corpora'][name][dim]['null_q95']:.4f} "
                  f"max={null.max():.4f} p={p:.4f}", flush=True)

    result["input_sha256"] = va.verified_input_hashes()
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    target = ROOT / "results" / "share_permutation_null.json"
    target.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
