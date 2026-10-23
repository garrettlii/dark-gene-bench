"""Donor-pair differential-expression fits (GWCD4i.DE_stats.by_donors.h5mu) and the derived
matrices probe v2 needs: labels, DE counts and LFC-profile correlations per fit.

Labels are int8 codes so a perturbation x readout matrix fits in memory:
LAB_NONE (borderline or missing), LAB_UNCHANGED, LAB_DOWN, LAB_UP.
"""
from __future__ import annotations

from pathlib import Path

import h5py
import numpy as np

LAB_NONE, LAB_UNCHANGED, LAB_DOWN, LAB_UP = -1, 0, 1, 2
CODE_TO_LABEL = {LAB_UNCHANGED: "unchanged", LAB_DOWN: "decreased", LAB_UP: "increased"}


def label_codes(lfc: np.ndarray, padj: np.ndarray, alpha: float, lfc_min: float,
                none_padj_min: float, none_lfc_max: float) -> np.ndarray:
    """Same thresholds as questions.label_effects, as an int8 matrix."""
    out = np.full(lfc.shape, LAB_NONE, dtype=np.int8)
    ok = np.isfinite(lfc) & np.isfinite(padj)
    sig = ok & (padj < alpha)
    out[sig & (lfc <= -lfc_min)] = LAB_DOWN
    out[sig & (lfc >= lfc_min)] = LAB_UP
    out[ok & (padj >= none_padj_min) & (np.abs(lfc) <= none_lfc_max)] = LAB_UNCHANGED
    return out


def changed_mask(lfc: np.ndarray, padj: np.ndarray, alpha: float, lfc_min: float) -> np.ndarray:
    return np.isfinite(lfc) & np.isfinite(padj) & (padj < alpha) & (np.abs(lfc) >= lfc_min)


def read_rows(path: str | Path, dataset: str, rows: np.ndarray, cols: np.ndarray | None = None) -> np.ndarray:
    """float32 rows (and optionally columns) of a dense 2-D dataset; rows need not be sorted."""
    rows = np.asarray(rows, dtype=np.int64)
    order = np.argsort(rows)
    with h5py.File(path, "r") as f:
        data = f[dataset][rows[order], :]
    data = data[np.argsort(order)].astype(np.float32)
    return data if cols is None else data[:, cols]


def obs_keys(path: str | Path, group: str) -> np.ndarray:
    """Row keys of an AnnData obs (its index column)."""
    with h5py.File(path, "r") as f:
        g = f[f"{group}/obs" if group else "obs"]
        return g[g.attrs["_index"]][:].astype(str)


def var_index(path: str | Path, group: str) -> np.ndarray:
    with h5py.File(path, "r") as f:
        g = f[f"{group}/var" if group else "var"]
        return g[g.attrs["_index"]][:].astype(str)


def row_corr(a: np.ndarray, b: np.ndarray | None = None) -> np.ndarray:
    """Pearson correlation between rows of a (and rows of b), NaNs treated as 0 after centring."""
    def z(m):
        m = np.nan_to_num(m - np.nanmean(m, axis=1, keepdims=True))
        sd = np.sqrt((m ** 2).sum(axis=1, keepdims=True))
        return m / np.where(sd > 0, sd, 1)
    za = z(a.astype(np.float32))
    zb = za if b is None else z(b.astype(np.float32))
    return za @ zb.T


def paired_row_corr(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Correlation of row i of a with row i of b (a perturbation's profile across two fits)."""
    a = np.nan_to_num(a - np.nanmean(a, axis=1, keepdims=True))
    b = np.nan_to_num(b - np.nanmean(b, axis=1, keepdims=True))
    den = np.sqrt((a ** 2).sum(1) * (b ** 2).sum(1))
    return np.where(den > 0, (a * b).sum(1) / np.where(den > 0, den, 1), np.nan)
