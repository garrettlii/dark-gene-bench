"""Family 1 (direct effect) questions for the Phase 0 prior-only probe.

Question: when gene G is knocked down in condition C, does readout gene R go
down, stay unchanged, or go up? Truth comes from differential-expression
statistics with pre-registered thresholds; borderline cases are dropped.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

LABELS = ("decreased", "unchanged", "increased")

PROMPT_TEMPLATE = """You are answering a question about a CRISPR interference (CRISPRi) Perturb-seq screen in primary human CD4+ T cells from healthy donors. Each targeted gene was knocked down, and gene expression was measured by single-cell RNA sequencing and compared with cells carrying non-targeting control guides.

Condition: {condition_text}
Knocked-down gene: {target}
Readout gene: {readout}

In this screen, how did expression of {readout} change when {target} was knocked down?
- "decreased": a statistically detectable decrease
- "unchanged": no detectable change
- "increased": a statistically detectable increase
{balance_note}
Answer from your own knowledge, without tools. Reply with only a JSON object giving your probability for each option, for example {{"decreased": 0.2, "unchanged": 0.5, "increased": 0.3}}."""

BALANCE_NOTE = "\nAcross this question set, the three answers occur about equally often.\n"


def label_effects(lfc: np.ndarray, padj: np.ndarray, alpha: float, lfc_min: float,
                  none_padj_min: float, none_lfc_max: float) -> np.ndarray:
    """Vectorized labels; None marks borderline or missing values (excluded from questions)."""
    lfc = np.asarray(lfc, dtype=float)
    padj = np.asarray(padj, dtype=float)
    out = np.full(lfc.shape, None, dtype=object)
    ok = np.isfinite(lfc) & np.isfinite(padj)
    sig = ok & (padj < alpha)
    out[sig & (lfc <= -lfc_min)] = "decreased"
    out[sig & (lfc >= lfc_min)] = "increased"
    out[ok & (padj >= none_padj_min) & (np.abs(lfc) <= none_lfc_max)] = "unchanged"
    return out


def build_prompt(target: str, readout: str, condition_text: str, balanced: bool) -> str:
    return PROMPT_TEMPLATE.format(target=target, readout=readout, condition_text=condition_text,
                                  balance_note=BALANCE_NOTE if balanced else "\n")


def sample_questions(candidates: pd.DataFrame, per_bin: int, max_per_gene: int,
                     rng: np.random.Generator, balance: bool = True) -> pd.DataFrame:
    """Pick questions per density bin.

    ``candidates`` needs columns GeneID, density_bin, label. With ``balance`` each
    bin gets per_bin // 3 questions of each label. A gene contributes at most
    ``max_per_gene`` questions. Bins that cannot fill their quota are returned
    short; the caller reports this rather than silently topping up.
    """
    candidates = candidates.reset_index(drop=True)
    picked = []
    for _, group in candidates.groupby("density_bin", sort=True):
        order = rng.permutation(len(group))
        group = group.iloc[order]
        per_gene: dict[int, int] = {}
        if balance:
            quota = {lab: per_bin // len(LABELS) for lab in LABELS}
        else:
            quota = None
        taken, n = [], 0
        for row in group.itertuples(index=True):
            if n >= per_bin:
                break
            if per_gene.get(row.GeneID, 0) >= max_per_gene:
                continue
            if quota is not None:
                if quota.get(row.label, 0) <= 0:
                    continue
                quota[row.label] -= 1
            per_gene[row.GeneID] = per_gene.get(row.GeneID, 0) + 1
            taken.append(row.Index)
            n += 1
        picked.append(group.loc[taken])
    out = pd.concat(picked) if picked else candidates.iloc[0:0]
    out = out.iloc[rng.permutation(len(out))].reset_index(drop=True)
    out["qid"] = make_ids(len(out), rng)
    return out


def make_ids(n: int, rng: np.random.Generator) -> list[str]:
    ids: set[str] = set()
    out = []
    while len(out) < n:
        candidate = "q" + "".join(rng.choice(list("0123456789abcdef"), size=10))
        if candidate not in ids:
            ids.add(candidate)
            out.append(candidate)
    return out
