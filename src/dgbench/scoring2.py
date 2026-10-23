"""Probe v2 scoring: named-minus-hidden gain, secondary measures and cross-fitted baselines.

Primary estimand per question: Brier(hidden) - Brier(named), i.e. how much naming the gene
helps. With k samples per prompt it is computed both ways: the mean of per-sample Briers
("mean_brier") and the Brier of the mean forecast ("brier_of_mean"). Uncertainty comes from
bootstraps that resample genes (a question's first GeneID) with all their questions.
"""
from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd
from scipy.optimize import minimize

COMBINE = ("mean_brier", "brier_of_mean")


def brier(p: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Multi-class Brier per row; p is (n, K) probabilities, y is (n,) label indices."""
    onehot = np.zeros_like(p)
    onehot[np.arange(len(y)), y] = 1
    return ((p - onehot) ** 2).sum(1)


def combine_samples(probs: list[np.ndarray], y: int) -> dict[str, float]:
    """Both ways of combining k sampled forecasts for one question."""
    P = np.stack(probs)
    ys = np.full(len(P), y)
    return {"mean_brier": float(brier(P, ys).mean()), "brier_of_mean": float(brier(P.mean(0, keepdims=True), ys[:1])[0])}


def cluster_boot(df: pd.DataFrame, stat, cluster: str = "cluster", n_boot: int = 2000, seed: int = 0) -> tuple[float, float, float]:
    """(point, ci_low, ci_high) resampling clusters with all their rows."""
    rng = np.random.default_rng(seed)
    groups = df.groupby(cluster).indices
    keys = list(groups)
    point = float(stat(df))
    vals = []
    for _ in range(n_boot):
        ix = np.concatenate([groups[keys[k]] for k in rng.integers(0, len(keys), len(keys))])
        vals.append(stat(df.iloc[ix]))
    lo, hi = np.nanpercentile(vals, [2.5, 97.5])
    return point, float(lo), float(hi)


def slope(df: pd.DataFrame, y: str, x: str, covariates: Sequence[str] = ()) -> float:
    """OLS coefficient of x in y ~ x + covariates (rows with missing values dropped)."""
    d = df[[y, x, *covariates]].dropna()
    if len(d) < len(covariates) + 3:
        return float("nan")
    X = np.column_stack([np.ones(len(d)), d[x].to_numpy(float)] + [d[c].to_numpy(float) for c in covariates])
    coef, *_ = np.linalg.lstsq(X, d[y].to_numpy(float), rcond=None)
    return float(coef[1])


def auc(score: np.ndarray, positive: np.ndarray) -> float:
    """Mann-Whitney AUC with ties counted half."""
    pos, neg = score[positive], score[~positive]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    ranks = pd.Series(np.concatenate([pos, neg])).rank().to_numpy()
    return float((ranks[: len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def ece(p: np.ndarray, y: np.ndarray, n_bins: int = 10) -> float:
    conf, pred = p.max(1), p.argmax(1)
    which = np.clip(np.digitize(conf, np.linspace(0, 1, n_bins + 1)[1:-1]), 0, n_bins - 1)
    return float(sum(abs((pred[which == b] == y[which == b]).mean() - conf[which == b].mean()) * (which == b).mean()
                     for b in range(n_bins) if (which == b).any()))


def murphy(p: np.ndarray, y: np.ndarray, n_bins: int = 10) -> dict[str, float]:
    """Murphy decomposition of the Brier score summed over classes (one-vs-rest), 10 forecast bins:
    brier ~= reliability - resolution + uncertainty (exact up to within-bin variation)."""
    rel = res = unc = 0.0
    edges = np.linspace(0, 1, n_bins + 1)[1:-1]
    for k in range(p.shape[1]):
        o = (y == k).astype(float)
        base = o.mean()
        unc += base * (1 - base)
        b = np.digitize(p[:, k], edges)
        for j in np.unique(b):
            m = b == j
            w = m.mean()
            rel += w * (p[m, k].mean() - o[m].mean()) ** 2
            res += w * (o[m].mean() - base) ** 2
    return {"reliability": rel, "resolution": res, "uncertainty": unc, "brier": float(brier(p, y).mean())}


# ---------------------------------------------------------------- cross-fitted baselines

def fit_softmax(X: np.ndarray, y: np.ndarray, K: int, l2: float = 1.0) -> np.ndarray:
    """Multinomial logistic regression (intercept added); returns weights (d+1, K)."""
    Xb = np.column_stack([np.ones(len(X)), X])
    mu, sd = Xb[:, 1:].mean(0), Xb[:, 1:].std(0) + 1e-9
    Xs = Xb.copy()
    Xs[:, 1:] = (Xb[:, 1:] - mu) / sd

    def loss(w):
        W = w.reshape(Xs.shape[1], K)
        Z = Xs @ W
        Z -= Z.max(1, keepdims=True)
        lp = Z - np.log(np.exp(Z).sum(1, keepdims=True))
        return -lp[np.arange(len(y)), y].mean() + l2 * (W[1:] ** 2).sum() / len(y)

    W = minimize(loss, np.zeros(Xs.shape[1] * K), method="L-BFGS-B").x.reshape(Xs.shape[1], K)
    return np.vstack([W[:1] - (mu / sd) @ W[1:], W[1:] / sd[:, None]])


def predict_softmax(W: np.ndarray, X: np.ndarray) -> np.ndarray:
    Z = np.column_stack([np.ones(len(X)), X]) @ W
    Z -= Z.max(1, keepdims=True)
    e = np.exp(Z)
    return e / e.sum(1, keepdims=True)


def fit_conditional_logit(F: np.ndarray, y: np.ndarray, l2: float = 1.0) -> np.ndarray:
    """Choice model over options: F is (n, n_options, d) option features, y the chosen option."""
    mu, sd = F.reshape(-1, F.shape[2]).mean(0), F.reshape(-1, F.shape[2]).std(0) + 1e-9
    Fs = (F - mu) / sd

    def loss(b):
        Z = Fs @ b
        Z -= Z.max(1, keepdims=True)
        lp = Z - np.log(np.exp(Z).sum(1, keepdims=True))
        return -lp[np.arange(len(y)), y].mean() + l2 * (b ** 2).sum() / len(y)

    return minimize(loss, np.zeros(F.shape[2]), method="L-BFGS-B").x / sd


def predict_conditional_logit(b: np.ndarray, F: np.ndarray) -> np.ndarray:
    Z = F @ b
    Z -= Z.max(1, keepdims=True)
    e = np.exp(Z)
    return e / e.sum(1, keepdims=True)


def argmax_forecast(scores: np.ndarray) -> np.ndarray:
    """One-hot on the highest score per row, ties split evenly."""
    top = scores == scores.max(1, keepdims=True)
    return top / top.sum(1, keepdims=True)


def completeness(responses: pd.DataFrame, expected: pd.DataFrame) -> dict[str, int]:
    """Unanswered expected calls and infrastructure errors (latest record per call)."""
    key = ["qid", "version", "sample"]
    latest = responses.drop_duplicates(key, keep="last") if len(responses) else responses
    merged = expected.merge(latest, on=key, how="left", indicator=True)
    return {"unanswered": int((merged["_merge"] == "left_only").sum()),
            "infra_errors": int(merged["error"].notna().sum()) if "error" in merged else 0}


# ---------------------------------------------------------------- skill-point normalization (D-024)

UNIFORM_BRIER = {"readout": 2 / 3, "gene": 1 / 2, "neighbour": 3 / 4}


def normalized_gain(brier_hidden, brier_named, family) -> np.ndarray:
    """(Brier(hidden) - Brier(named)) / uniform Brier for the family: the gain in skill points."""
    u = np.asarray(pd.Series(family).map(UNIFORM_BRIER), dtype=float)
    return (np.asarray(brier_hidden, dtype=float) - np.asarray(brier_named, dtype=float)) / u


def family_balanced_mean(df: pd.DataFrame, col: str, families: Sequence[str] = ("readout", "gene")) -> float:
    """Mean of the per-family means of ``col`` over ``families`` present in df (equal family weight)."""
    means = [df.loc[df["family"] == f, col].mean() for f in families if (df["family"] == f).any()]
    return float(np.mean(means)) if means else float("nan")
