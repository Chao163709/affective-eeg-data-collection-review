"""Recompute the manuscript's descriptive label analyses from one entry point.

No EEG training or significance claims.  Bootstrap units and effective sample
sizes are recorded explicitly.  Run from any directory with numpy and pandas.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261101
INPUT_NAMES = ("deap_subj32_8d65c6_y.npy", "mahnob_meta.csv", "dens_ratings.csv",
               "met_ratings.tsv", "faced_ratings_long.csv")


def input_paths():
    paths = {name: ROOT / "cache" / name for name in INPUT_NAMES}
    paths["faced_ratings_long.csv"] = Path(os.environ.get(
        "FACED_RATINGS", str(paths["faced_ratings_long.csv"])))
    return paths


def verified_input_hashes():
    """Reject inputs differing from the frozen analysis before reading ratings."""
    frozen = ROOT / "results" / "rating_input_manifest_20261108.json"
    expected = json.loads(frozen.read_text(encoding="utf-8"))["input_sha256"]
    actual = {}
    for name, path in input_paths().items():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected[name]:
            raise ValueError(f"Input SHA-256 mismatch: {name} ({path})")
        actual[name] = digest
    return actual


def rating_matrices():
    verified_input_hashes()
    cache = ROOT / "cache"
    y = np.load(cache / "deap_subj32_8d65c6_y.npy")
    out = {"DEAP": y[:, :2].reshape(32, 40, 2).astype(float)}
    d = pd.read_csv(cache / "mahnob_meta.csv")
    subjects, stimuli = sorted(d.subject.unique()), sorted(d.media.unique())
    out["MAHNOB-HCI"] = np.stack([
        d.pivot_table(index="subject", columns="media", values=dim)
        .reindex(index=subjects, columns=stimuli).to_numpy(float)
        for dim in ("valence", "arousal")], axis=-1)
    d = pd.read_csv(cache / "dens_ratings.csv")
    # Repeated keys are identical export records, not extra observations.
    if (d.groupby(["subject", "stimulus", "dim"])["y"].nunique(dropna=False) > 1).any():
        raise ValueError("DENS has conflicting ratings for a participant/stimulus/dimension")
    d = d.drop_duplicates(["subject", "stimulus", "dim"])
    p = d.groupby(["subject", "stimulus", "dim"])["y"].mean().unstack("dim")
    p = p.dropna(subset=["valence", "arousal"])
    subjects = sorted(p.index.get_level_values(0).unique())
    stimuli = sorted(p.index.get_level_values(1).unique())
    out["DENS"] = np.stack([
        p[dim].unstack().reindex(index=subjects, columns=stimuli).to_numpy(float)
        for dim in ("valence", "arousal")], axis=-1)
    d = pd.read_csv(cache / "met_ratings.tsv", sep="\t")
    d.columns = d.columns.str.strip()
    out["MET"] = np.stack([
        d.pivot_table(index="participant_id", columns="song_id", values=dim)
        .to_numpy(float) for dim in ("Valence", "Arousal")], axis=-1)
    faced_path = input_paths()["faced_ratings_long.csv"]
    if not faced_path.exists():
        raise FileNotFoundError("Set FACED_RATINGS or supply cache/faced_ratings_long.csv")
    d = pd.read_csv(faced_path)
    subjects, stimuli = sorted(d.subject.unique()), sorted(d.video_index.unique())
    a = np.stack([
        d[d.item.eq(dim)].pivot_table(index="subject", columns="video_index", values="score")
        .reindex(index=subjects, columns=stimuli).to_numpy(float)
        for dim in ("Valence", "Arousal")], axis=-1)
    out["FACED"] = a[np.isfinite(a).any(axis=(1, 2))]
    return out


def icc_batch(a):
    """One-way unequal-group moment estimate; last two axes = raters, stimuli.

    This is a descriptive ICC(1) calculation, not a fitted crossed model.
    Missing cells are excluded; bootstrap duplicates remain distinct rows/columns.
    """
    valid = np.isfinite(a)
    counts = valid.sum(axis=-2)
    sums = np.nansum(a, axis=-2)
    n = counts.sum(axis=-1)
    k = (counts > 0).sum(axis=-1)
    means = np.divide(sums, counts, out=np.zeros_like(sums), where=counts > 0)
    grand = sums.sum(axis=-1) / n
    ssb = (counts * (means - grand[..., None]) ** 2).sum(axis=-1)
    ssw = np.maximum(0., np.nansum(a * a, axis=(-2, -1)) - (counts * means**2).sum(axis=-1))
    m0 = (n - (counts**2).sum(axis=-1) / n) / (k - 1)
    msw = ssw / (n - k)
    vb = np.maximum(0., (ssb / (k - 1) - msw) / m0)
    return vb / (vb + msw)


def balanced_components(a):
    """Correct two-way random-intercept moments, complete rectangular blocks."""
    if not np.isfinite(a).all():
        raise ValueError("Balanced moments require a complete block")
    i, s = a.shape[-2:]
    grand = a.mean(axis=(-2, -1))
    mi, ms = a.mean(axis=-1), a.mean(axis=-2)
    msi = s * ((mi - grand[..., None])**2).sum(axis=-1) / (i-1)
    mss = i * ((ms - grand[..., None])**2).sum(axis=-1) / (s-1)
    residual = a - mi[..., :, None] - ms[..., None, :] + grand[..., None, None]
    mse = (residual**2).sum(axis=(-2, -1)) / ((i-1)*(s-1))
    vi, vs = np.maximum(0., (msi-mse)/s), np.maximum(0., (mss-mse)/i)
    v = np.stack([vi, vs, mse], axis=-1)
    return v / v.sum(axis=-1, keepdims=True)


def binary_scores(a):
    """LOSO known-stimulus and training-majority baselines for fixed labels.

    a may have a leading bootstrap axis.  NaN denotes an absent rating.
    """
    present = np.isfinite(a)
    labels = np.nan_to_num(a)
    total_pos = labels.sum(axis=-2, keepdims=True)
    total_n = present.sum(axis=-2, keepdims=True)
    others_n = total_n - present
    clip_pred = (total_pos - labels) * 2 > others_n
    all_pos, all_n = labels.sum(axis=(-2, -1)), present.sum(axis=(-2, -1))
    own_pos, own_n = labels.sum(axis=-1), present.sum(axis=-1)
    majority = 2*(all_pos[..., None]-own_pos) > (all_n[..., None]-own_n)
    clip_pred = np.where(others_n > 0, clip_pred, majority[..., :, None])
    known = ((clip_pred == labels)*present).sum(axis=(-2, -1)) / all_n
    baseline = ((majority[..., :, None] == labels)*present).sum(axis=(-2, -1)) / all_n
    return known, baseline


def interval(x):
    return [float(v) for v in np.percentile(x, [2.5, 97.5])]


def recompute(boot=2000):
    rng = np.random.default_rng(SEED)
    out = {"seed": SEED, "bootstrap": boot,
           "method": "unequal-group one-way moments; descriptive percentile intervals",
           "calibration": "not established for the unbalanced observed designs",
           "corpora": {}}
    for name, a in rating_matrices().items():
        i, s, _ = a.shape
        result = {"n_subjects": i, "n_stimuli": s,
                  "n_cells": [int(np.isfinite(a[..., j]).sum()) for j in range(2)],
                  "n_complete": int(np.isfinite(a).all(axis=(1, 2)).sum()),
                  "dimensions": {}}
        points = [float(icc_batch(a[..., j])) for j in range(2)]
        result["contrast"] = {"point": points[0]-points[1], "frames": {}}
        frame_values = {}
        for frame in ("stimulus", "participant", "crossed"):
            pi = rng.integers(i, size=(boot, i)) if frame != "stimulus" else np.broadcast_to(np.arange(i), (boot, i))
            si = rng.integers(s, size=(boot, s)) if frame != "participant" else np.broadcast_to(np.arange(s), (boot, s))
            values = [icc_batch(a[..., j][pi[:, :, None], si[:, None, :]]) for j in range(2)]
            frame_values[frame] = values
            result["contrast"]["frames"][frame] = {"ci": interval(values[0]-values[1])}
        for j, dim in enumerate(("valence", "arousal")):
            y = a[..., j]
            counts = np.isfinite(y).sum(axis=0)
            n = counts.sum()
            mbar = n / len(counts)
            m0 = (n-(counts**2).sum()/n)/(len(counts)-1)
            med = float(np.nanmedian(y))
            lab = np.where(np.isfinite(y), y > med, np.nan)
            known, baseline = binary_scores(lab)
            si = rng.integers(s, size=(boot, s))
            known_b, baseline_b = binary_scores(lab[:, si].transpose(1, 0, 2))
            fixed = np.where(np.isfinite(y), y > 5, np.nan)
            strengths = {}
            for rule, ll in (("fixed", fixed), ("median", lab)):
                p = np.nanmean(ll, axis=0)
                strengths[rule] = float(np.maximum(p, 1-p).mean())
            result["dimensions"][dim] = {
                "point": points[j], "mean_count": float(mbar), "effective_count": float(m0),
                "ci": {f: interval(frame_values[f][j]) for f in frame_values},
                "binary": {"threshold": med, "rule": "y > full-corpus median, held fixed during resampling",
                           "aggregation": "micro over observed participant-stimulus cells",
                           "stimulus_baseline": float(known), "training_majority_baseline": float(baseline),
                           "class_balance_reference": float(max(np.nanmean(lab), 1-np.nanmean(lab))),
                           "stimulus_ci": interval(known_b), "excess_ci": interval(known_b-baseline_b)},
                "majority_strength": strengths}
        if name in ("DEAP", "MAHNOB-HCI", "MET"):
            complete = np.isfinite(a).all(axis=(1, 2))
            block = a[complete]
            result["crossed_complete_block"] = {"n_subjects": len(block), "n_stimuli": s, "dimensions": {}}
            pi = rng.integers(len(block), size=(boot, len(block)))
            for j, dim in enumerate(("valence", "arousal")):
                point = balanced_components(block[..., j])
                bs = balanced_components(block[..., j][pi])
                result["crossed_complete_block"]["dimensions"][dim] = {
                    "point": point.tolist(), "ci_participant": interval(bs[:, 0])}
        out["corpora"][name] = result
        print(name, "subjects", i, "cells", result["n_cells"], "ICC", points, flush=True)
    out["input_sha256"] = verified_input_hashes()
    out["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", type=int, default=2000)
    args = parser.parse_args()
    result = recompute(args.bootstrap)
    target = ROOT / "results" / "verified_revision_20261101.json"
    target.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    print(target)
