"""Probabilistic baseline forecasts for probe v2 (the "fame-only" and "annotation-only" rungs).

Every rung is a calibrated forecast fitted on questions about genes outside the scored set:
- F-readout and F-gene: multinomial logistic regression on a few features.
- F-neighbour: conditional logit over the four options; for annotation-only the single
  feature is GO Jaccard with the target, so the fit is a softmax over Jaccard whose
  temperature is 1 / coefficient.
Inputs are plain frames; GO terms come from the archived release for a model's cutoff.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .genes import strip_version
from .go import jaccard
from .probe2 import LABELS
from .scoring2 import fit_conditional_logit, fit_softmax, predict_conditional_logit, predict_softmax


@dataclass
class Context:
    log_density: pd.Series           # GeneID -> log density at the model's cutoff
    base_mean: dict                  # (GeneID, condition) -> target baseMean
    terms: dict                      # GeneID -> frozenset of GO terms
    ensembl: dict                    # Ensembl ID -> GeneID
    floor: float                     # log density of a gene with no papers


def _ld(ctx, g):
    return ctx.log_density.reindex(np.asarray(g)).fillna(ctx.floor).to_numpy(float)


def _lbm(ctx, g, c):
    return np.log2([ctx.base_mean.get((x, y), np.nan) for x, y in zip(g, c)])


def _nterms(ctx, g):
    return np.log1p([len(ctx.terms.get(x, ())) for x in g])


def features(family: str, ctx: Context, df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """(fame, annotation) features. Neighbour features are (n, 4, d) option tensors."""
    c = df["condition"].to_numpy()
    if family == "readout":
        g = df["GeneID"].to_numpy()
        r = [ctx.ensembl.get(strip_version(x)) for x in df["readout_id"]]
        fame = np.column_stack([_ld(ctx, g), _lbm(ctx, g, c)])
        ann = np.column_stack([[jaccard(ctx.terms.get(a, frozenset()), ctx.terms.get(b, frozenset())) for a, b in zip(g, r)],
                               _nterms(ctx, g), _nterms(ctx, r)])
        return np.nan_to_num(fame), ann
    if family == "gene":
        a, b = df["GeneID_a"].to_numpy(), df["GeneID_b"].to_numpy()
        fame = np.column_stack([_ld(ctx, a) - _ld(ctx, b), _lbm(ctx, a, c) - _lbm(ctx, b, c)])
        return np.nan_to_num(fame), (_nterms(ctx, a) - _nterms(ctx, b))[:, None]
    t = df["GeneID"].to_numpy()
    opts = np.array([list(o) for o in df["option_GeneIDs"]])
    fame = np.stack([np.column_stack([_ld(ctx, o), _lbm(ctx, o, c)]) for o in opts.T], axis=1)
    jac = np.array([[jaccard(ctx.terms.get(x, frozenset()), ctx.terms.get(o, frozenset())) for o in os_] for x, os_ in zip(t, opts)])
    return np.nan_to_num(fame), jac[:, :, None]


def label_index(family: str, df: pd.DataFrame) -> np.ndarray:
    return df["label"].map({lab: i for i, lab in enumerate(LABELS[family])}).to_numpy()


def forecasts(family: str, ctx: Context, train: pd.DataFrame, test: pd.DataFrame) -> dict[str, np.ndarray]:
    """Fame-only and annotation-only probabilities for ``test``, fitted on ``train``."""
    K = len(LABELS[family])
    y = label_index(family, train)
    f_tr, a_tr = features(family, ctx, train)
    f_te, a_te = features(family, ctx, test)
    if family == "neighbour":
        return {"fame_only": predict_conditional_logit(fit_conditional_logit(f_tr, y), f_te),
                "annotation_only": predict_conditional_logit(fit_conditional_logit(a_tr, y), a_te)}
    return {"fame_only": predict_softmax(fit_softmax(f_tr, y, K), f_te),
            "annotation_only": predict_softmax(fit_softmax(a_tr, y, K), a_te)}


def crossfit(family: str, ctx: Context, df: pd.DataFrame, cluster: str, folds: int = 5, seed: int = 0) -> dict[str, np.ndarray]:
    """Out-of-fold forecasts with folds split by ``cluster`` (a gene), so no gene is in both sides."""
    rng = np.random.default_rng(seed)
    genes = df[cluster].unique()
    fold_of = dict(zip(genes, rng.integers(0, folds, len(genes))))
    f = df[cluster].map(fold_of).to_numpy()
    out = {}
    for k in range(folds):
        te = f == k
        if te.any() and (~te).any():
            for name, P in forecasts(family, ctx, df[~te], df[te]).items():
                out.setdefault(name, np.zeros((len(df), len(LABELS[family]))))[te] = P
    return out


def balanced_pool(df: pd.DataFrame, cells: list[str], max_total: int, seed: int) -> pd.DataFrame:
    """Equal count in every cell (the smallest cell's size, capped so the total stays under
    max_total), so a fitted rung sees the scored set's label proportions."""
    groups = list(df.groupby(cells))
    if not groups:
        return df.iloc[0:0]
    per = min(min(len(g) for _, g in groups), max(1, max_total // len(groups)))
    return pd.concat([g.sample(per, random_state=seed) for _, g in groups], ignore_index=True)
