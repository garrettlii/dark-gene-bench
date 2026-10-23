"""Scoring for probabilistic answers.

Primary metric: multi-class Brier skill relative to a reference forecast (the
label frequencies of the scored set; uniform when labels are balanced).
Uncertainty: bootstrap that resamples genes within each density bin, since
questions about the same gene are not independent.
"""
from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd


def brier(probs: np.ndarray, onehot: np.ndarray) -> np.ndarray:
    return ((probs - onehot) ** 2).sum(axis=1)


def to_arrays(df: pd.DataFrame, labels: Sequence[str]) -> tuple[np.ndarray, np.ndarray]:
    probs = df[[f"p_{lab}" for lab in labels]].to_numpy(dtype=float)
    onehot = np.stack([(df["label"] == lab).to_numpy(dtype=float) for lab in labels], axis=1)
    return probs, onehot


def reference_probs(df: pd.DataFrame, labels: Sequence[str]) -> np.ndarray:
    freq = df["label"].value_counts(normalize=True)
    return np.array([freq.get(lab, 0.0) for lab in labels])


def skill(df: pd.DataFrame, labels: Sequence[str], ref: np.ndarray) -> float:
    probs, onehot = to_arrays(df, labels)
    b_model = brier(probs, onehot).mean()
    b_ref = brier(np.tile(ref, (len(df), 1)), onehot).mean()
    return float(1.0 - b_model / b_ref) if b_ref > 0 else float("nan")


def accuracy(df: pd.DataFrame, labels: Sequence[str]) -> float:
    probs, onehot = to_arrays(df, labels)
    return float((probs.argmax(axis=1) == onehot.argmax(axis=1)).mean())


def ece(df: pd.DataFrame, labels: Sequence[str], n_bins: int = 10) -> float:
    """Top-label expected calibration error."""
    probs, onehot = to_arrays(df, labels)
    conf = probs.max(axis=1)
    correct = (probs.argmax(axis=1) == onehot.argmax(axis=1)).astype(float)
    edges = np.linspace(0, 1, n_bins + 1)
    which = np.clip(np.digitize(conf, edges[1:-1]), 0, n_bins - 1)
    total = 0.0
    for b in range(n_bins):
        mask = which == b
        if mask.any():
            total += mask.mean() * abs(correct[mask].mean() - conf[mask].mean())
    return float(total)


def _gene_rows(sub: pd.DataFrame) -> list[np.ndarray]:
    return [np.asarray(ix) for ix in sub.groupby("GeneID").indices.values()]


def by_bin(df: pd.DataFrame, labels: Sequence[str], n_boot: int = 2000, seed: int = 0) -> tuple[pd.DataFrame, dict]:
    """Per-bin skill with 95% CIs, plus a bootstrap CI for the slope of skill on bin index.

    The bootstrap resamples genes (with all their questions) within each bin.
    """
    rng = np.random.default_rng(seed)
    ref = reference_probs(df, labels)
    bins = sorted(int(b) for b in df["density_bin"].unique())
    rows, boot = [], np.full((n_boot, len(bins)), np.nan)
    for j, b in enumerate(bins):
        sub = df[df["density_bin"] == b].reset_index(drop=True)
        probs, onehot = to_arrays(sub, labels)
        b_model = brier(probs, onehot)
        b_ref = brier(np.tile(ref, (len(sub), 1)), onehot)
        genes = _gene_rows(sub)
        for i in range(n_boot):
            draw = rng.integers(0, len(genes), size=len(genes))
            ix = np.concatenate([genes[k] for k in draw])
            denom = b_ref[ix].mean()
            boot[i, j] = 1.0 - b_model[ix].mean() / denom if denom > 0 else np.nan
        lo, hi = np.nanpercentile(boot[:, j], [2.5, 97.5])
        rows.append({
            "density_bin": b, "n_questions": len(sub), "n_genes": len(genes),
            "skill": skill(sub, labels, ref), "ci_low": float(lo), "ci_high": float(hi),
            "accuracy": accuracy(sub, labels), "ece": ece(sub, labels),
            "parse_fail_rate": float(sub["parse_failed"].mean()) if "parse_failed" in sub else float("nan"),
        })
    table = pd.DataFrame(rows)
    x = np.array(bins, dtype=float)
    if len(bins) > 1:
        point_slope = float(np.polyfit(x, table["skill"].to_numpy(), 1)[0])
        ok = np.all(np.isfinite(boot), axis=1)
        slopes = np.array([np.polyfit(x, boot[i], 1)[0] for i in np.flatnonzero(ok)])
    else:
        point_slope, slopes = float("nan"), np.array([np.nan])
    slope = {"slope": point_slope,
             "ci_low": float(np.nanpercentile(slopes, 2.5)),
             "ci_high": float(np.nanpercentile(slopes, 97.5)),
             "reference_probs": dict(zip(labels, map(float, ref)))}
    return table, slope


def verdicts(table: pd.DataFrame, slope: dict, predictions: dict) -> dict[str, bool]:
    """Apply the pre-registered decision rules (see prereg/phase0_prior_probe.md)."""
    top = table.loc[table["density_bin"].idxmax()]
    bottom = table.loc[table["density_bin"].idxmin()]
    return {
        "P1a_top_bin_ci_low_at_least": bool(top["ci_low"] >= float(predictions["top_bin_min_skill"])),
        "P1b_bottom_bin_at_most": bool(bottom["skill"] <= float(predictions["bottom_bin_max_skill"])),
        "P1c_slope_ci_low_above": bool(slope["ci_low"] > float(predictions["min_slope"])),
    }
