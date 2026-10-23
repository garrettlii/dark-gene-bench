"""Probe v2: prior-only questions asked twice, with the gene named and with it hidden.

Families (no data shown to the model):
- readout: does readout R decrease, stay unchanged or increase when G is knocked down?
  Readouts come from the whole transcriptome; "unchanged" readouts respond to at least R
  other perturbations in the same condition, so silence cannot be guessed from the readout.
- gene: which of two knockdowns (same bin and condition, matched on target expression)
  changes more genes?
- neighbour: which of four knockdowns has the LFC profile most similar to G's?

Truth must agree in both halves of the chosen donor split(s). Inputs come from
scripts/07_build_probe2_inputs.py; nothing here reads files.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .donors import LAB_DOWN, LAB_UNCHANGED, LAB_UP, CODE_TO_LABEL

HIDDEN = "a gene whose identity is hidden"
READOUT_LABELS = ("decreased", "unchanged", "increased")
GENE_LABELS = ("A", "B")
NEIGHBOUR_LABELS = ("A", "B", "C", "D")

INTRO = ("You are answering a question about a CRISPR interference (CRISPRi) Perturb-seq screen in primary human "
         "CD4+ T cells from healthy donors. Each targeted gene was knocked down, and gene expression was measured by "
         "single-cell RNA sequencing and compared with cells carrying non-targeting control guides.")
TAIL = "Answer from your own knowledge, without tools. Reply with only a JSON object giving your probability for each option, for example {example}."

READOUT_TEMPLATE = INTRO + """

Condition: {condition_text}
Knocked-down gene: {target}
Readout gene: {readout}

In this screen, how did expression of the readout gene change when the knocked-down gene was knocked down?
- "decreased": a statistically detectable decrease
- "unchanged": no detectable change
- "increased": a statistically detectable increase

Across this question set, the three answers occur about equally often.
""" + TAIL

GENE_TEMPLATE = INTRO + """

Condition: {condition_text}
Knockdown A: {gene_a}
Knockdown B: {gene_b}

Which of these two knockdowns changed the expression of more genes (more genes with a statistically detectable change)?
- "A": knockdown A changed more genes
- "B": knockdown B changed more genes

Across this question set, A and B are correct about equally often.
""" + TAIL

NEIGHBOUR_TEMPLATE = INTRO + """

Condition: {condition_text}
Knocked-down gene: {target}

Which of the following knockdowns produced a transcriptome-wide expression change most similar to that of the knocked-down gene?
- "A": {opt_a}
- "B": {opt_b}
- "C": {opt_c}
- "D": {opt_d}

Exactly one option is correct, and each letter is correct about equally often.
""" + TAIL

EXAMPLES = {
    "readout": '{"decreased": 0.2, "unchanged": 0.5, "increased": 0.3}',
    "gene": '{"A": 0.6, "B": 0.4}',
    "neighbour": '{"A": 0.4, "B": 0.2, "C": 0.3, "D": 0.1}',
}
LABELS = {"readout": READOUT_LABELS, "gene": GENE_LABELS, "neighbour": NEIGHBOUR_LABELS}


def build_prompts(family: str, condition_text: str, **genes: str) -> dict[str, str]:
    """{"named": ..., "hidden": ...}; only the knocked-down gene line(s) differ."""
    ex = EXAMPLES[family]
    if family == "readout":
        named = READOUT_TEMPLATE.format(condition_text=condition_text, target=genes["target"], readout=genes["readout"], example=ex)
        hidden = READOUT_TEMPLATE.format(condition_text=condition_text, target=HIDDEN, readout=genes["readout"], example=ex)
    elif family == "gene":
        named = GENE_TEMPLATE.format(condition_text=condition_text, gene_a=genes["gene_a"], gene_b=genes["gene_b"], example=ex)
        hidden = GENE_TEMPLATE.format(condition_text=condition_text, gene_a=HIDDEN, gene_b=HIDDEN, example=ex)
    elif family == "neighbour":
        opts = {f"opt_{k}": genes[f"opt_{k}"] for k in "abcd"}
        named = NEIGHBOUR_TEMPLATE.format(condition_text=condition_text, target=genes["target"], example=ex, **opts)
        hidden = NEIGHBOUR_TEMPLATE.format(condition_text=condition_text, target=HIDDEN, example=ex, **opts)
    else:
        raise ValueError(family)
    return {"named": named, "hidden": hidden}


def wrong_names(rows: pd.DataFrame, question_rows: list[list[int]], exclude_symbols: list[set[str]], log2_tol: float,
                pool: np.ndarray, rng: np.random.Generator) -> list[list[int] | None]:
    """For each question, one substitute row per named gene: same condition and density bin,
    |log2 target_baseMean difference| <= log2_tol, from ``pool`` (row mask), and not any gene or
    symbol already in the question. None when no substitute exists."""
    cond, bins = rows["condition"].to_numpy(), rows["density_bin"].to_numpy()
    lbm = np.log2(rows["target_baseMean"].to_numpy(dtype=float))
    sym, gid = rows["symbol"].to_numpy(), rows["GeneID"].to_numpy()
    out = []
    for qrows, excl in zip(question_rows, exclude_symbols):
        used = {gid[r] for r in qrows}
        picks = []
        for r in qrows:
            ok = pool & (cond == cond[r]) & (bins == bins[r]) & (np.abs(lbm - lbm[r]) <= log2_tol)
            ok &= ~np.isin(gid, list(used)) & ~np.isin(sym, list(excl))
            cand = np.flatnonzero(ok)
            if not len(cand):
                picks = None
                break
            pick = int(rng.choice(cand))
            used.add(gid[pick])
            picks.append(pick)
        out.append(picks)
    return out


def run_order(items: list[tuple[str, str, int]], rng: np.random.Generator) -> list[tuple[str, str, int]]:
    """Shuffle (qid, version, sample) calls so no two adjacent calls share a qid.

    Raises if impossible (one qid holds more than half the calls)."""
    items = [items[i] for i in rng.permutation(len(items))]
    for i in range(1, len(items)):
        if items[i][0] != items[i - 1][0]:
            continue
        nxt = items[i + 1][0] if i + 1 < len(items) else None
        for j in list(range(i + 1, len(items))) + list(range(0, i - 1)):
            cand = items[j]
            ok_here = cand[0] != items[i - 1][0] and cand[0] != nxt
            ok_there = all(items[k][0] != items[i][0] for k in (j - 1, j + 1) if 0 <= k < len(items) and k != i)
            if ok_here and ok_there:
                items[i], items[j] = items[j], items[i]
                break
        else:
            raise ValueError("cannot separate calls that share a qid")
    return items


# ---------------------------------------------------------------- agreement

def agrees(labels_comb: np.ndarray, halves: list[np.ndarray]) -> np.ndarray:
    """True where every donor-pair half gives the same label as the combined fit."""
    ok = np.ones(labels_comb.shape, dtype=bool)
    for h in halves:
        ok &= h == labels_comb
    return ok


# ---------------------------------------------------------------- F-readout

def effect_terciles(rows: pd.DataFrame) -> np.ndarray:
    """Terciles (0, 1, 2) of target effect size (n_downstream) within each condition, over the given rows (D-019)."""
    out = np.zeros(len(rows), dtype=np.int8)
    for _, ix in rows.groupby("condition").indices.items():
        ranks = pd.Series(rows["n_downstream"].to_numpy()[ix]).rank(method="average")
        out[ix] = pd.qcut(ranks, 3, labels=False).to_numpy()
    return out


def readout_candidates(rows: pd.DataFrame, labels_comb: np.ndarray, resp: np.ndarray, conditions: list[str],
                       target_cols: np.ndarray, R: int, agree: np.ndarray | None = None,
                       zrank: np.ndarray | None = None, top_k: int | None = None) -> pd.DataFrame:
    """Long table of candidate (row, readout) questions.

    ``rows`` (one per labels_comb row) needs condition and eff_class; ``target_cols[r]`` is the
    readout column of row r's own target (-1 if not measured). ``resp[k, j]`` counts
    perturbations changing readout j in condition k. "Unchanged" needs resp >= R (the target
    itself is unchanged, so it is not in the count). ``agree`` masks rows x readouts whose
    donor-pair labels agree. With ``top_k``, changed readouts must be among the target's
    ``top_k`` strongest effects by |z| (``zrank``: 0 = strongest in the row).
    """
    cond_k = rows["condition"].map({c: k for k, c in enumerate(conditions)}).to_numpy()
    lab = labels_comb.copy()
    rr = np.arange(len(lab))
    has_t = target_cols >= 0
    lab[rr[has_t], target_cols[has_t]] = -1
    changed = (lab == LAB_DOWN) | (lab == LAB_UP)
    if top_k is not None:
        changed &= zrank < top_k
    keep = changed | ((lab == LAB_UNCHANGED) & (resp[cond_k] >= R))
    if agree is not None:
        keep &= agree
    r_idx, j_idx = np.nonzero(keep)
    out = pd.DataFrame({"row": r_idx, "readout_col": j_idx, "label": [CODE_TO_LABEL[c] for c in lab[r_idx, j_idx]]})
    out["condition"] = rows["condition"].to_numpy()[r_idx]
    out["eff_class"] = rows["eff_class"].to_numpy()[r_idx]
    return out


# ---------------------------------------------------------------- F-gene

def gene_pairs(rows: pd.DataFrame, nde_comb: np.ndarray, nde_halves: list[np.ndarray], ratio: float,
               log2_tol: float, eligible: np.ndarray, one_of: np.ndarray | None = None) -> pd.DataFrame:
    """Candidate pairs (row_a < row_b) in the same condition and density bin, matched on
    log2 target_baseMean within log2_tol, whose DE counts differ by at least ``ratio`` and are
    ordered the same way in every donor-pair half. ``larger`` is 0 for row_a, 1 for row_b.
    With ``one_of`` (a row mask, e.g. flagged genes), keep only pairs with exactly one such row."""
    lbm = np.log2(rows["target_baseMean"].to_numpy(dtype=float))
    out = []
    for (_, _), grp in rows[eligible].groupby(["condition", "density_bin"]):
        ix = grp.index.to_numpy()
        a, b = np.triu_indices(len(ix), k=1)
        ra, rb = ix[a], ix[b]
        na, nb = nde_comb[ra].astype(float), nde_comb[rb].astype(float)
        ok = (np.abs(lbm[ra] - lbm[rb]) <= log2_tol) & (np.maximum(na, nb) >= ratio * np.maximum(np.minimum(na, nb), 1))
        sign = np.sign(na - nb)
        for h in nde_halves:
            ok &= np.sign(h[ra].astype(float) - h[rb].astype(float)) == sign
        ok &= sign != 0
        if one_of is not None:
            ok &= one_of[ra] != one_of[rb]
        out.append(pd.DataFrame({"row_a": ra[ok], "row_b": rb[ok], "larger": (sign[ok] < 0).astype(int)}))
    cols = ["row_a", "row_b", "larger"]
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=cols)


# ---------------------------------------------------------------- F-neighbour

@dataclass
class NeighbourSpec:
    min_de: int
    min_self_corr: float
    margin: float
    go_max_genes: int
    match_log2_tol: float


def neighbour_items(rows: pd.DataFrame, cond_rows: np.ndarray, corr: np.ndarray, half_corrs: list[np.ndarray],
                    nde: np.ndarray, selfcorr: np.ndarray, targets: np.ndarray, option_ok: np.ndarray,
                    jac: np.ndarray, share_small: np.ndarray, share_complex: np.ndarray,
                    spec: NeighbourSpec, rng: np.random.Generator) -> pd.DataFrame:
    """One candidate item per target and tier within one condition.

    ``cond_rows`` are the row ids (into ``rows``) of this condition, aligned with ``corr``
    (combined), each matrix in ``half_corrs``, and the GO matrices (``jac``: Jaccard;
    ``share_small``: share a term with at most go_max_genes genes; ``share_complex``: share a
    protein-containing-complex term). ``nde``, ``selfcorr``, ``targets`` and ``option_ok`` are
    aligned with cond_rows. Distractors have similarity to the target below its median over
    the condition and come from the correct option's density bin.
    """
    bins = rows["density_bin"].to_numpy()[cond_rows]
    lbm = np.log2(rows["target_baseMean"].to_numpy(dtype=float))[cond_rows]
    informative = (nde >= spec.min_de) & (selfcorr >= spec.min_self_corr)
    out = []
    for t in np.flatnonzero(targets & informative):
        sims = corr[t].copy()
        sims[t] = np.nan
        cand = np.flatnonzero(option_ok & informative)
        cand = cand[cand != t]
        if len(cand) == 0:
            continue
        correct = cand[np.nanargmax(sims[cand])]
        median = np.nanmedian(sims)
        pool = np.flatnonzero(option_ok & (sims < median) & (bins == bins[correct]))
        pool = pool[(pool != t) & (pool != correct)]
        hard_pool = pool[(jac[t, pool] >= jac[t, correct]) & (np.abs(lbm[pool] - lbm[correct]) <= spec.match_log2_tol)]
        tiers = {"easy": pool, "hard": hard_pool}
        if not share_small[t, correct] and not share_complex[t, correct]:
            tiers["discovery"] = hard_pool
        for tier, p in tiers.items():
            if len(p) < 3:
                continue
            dis = rng.choice(p, size=3, replace=False)
            if sims[correct] - np.nanmax(sims[dis]) < spec.margin:
                continue
            opts = np.concatenate([[correct], dis])
            if not all(np.nanargmax(h[t, opts]) == 0 for h in half_corrs):
                continue
            order = rng.permutation(4)
            out.append({"target": cond_rows[t], "tier": tier, "options": cond_rows[opts[order]].tolist(),
                        "label": NEIGHBOUR_LABELS[int(np.flatnonzero(order == 0)[0])],
                        "margin": float(sims[correct] - np.nanmax(sims[dis]))})
    return pd.DataFrame(out, columns=["target", "tier", "options", "label", "margin"])


# ---------------------------------------------------------------- stratified sampling

def stratified_sample(cand: pd.DataFrame, cell_cols: list[str], per_cell: int, max_per_gene: int,
                      rng: np.random.Generator, gene_col: str = "GeneID", bin_col: str = "density_bin",
                      bins: list | None = None) -> tuple[pd.DataFrame, list]:
    """Same count per cell in every bin. Cells that cannot fill in every bin are dropped.

    A gene contributes at most ``max_per_gene`` items across the family. Returns
    (selected rows, dropped cells)."""
    bins = sorted(cand[bin_col].unique()) if bins is None else bins
    cells = sorted(cand.groupby(cell_cols).groups)
    keep, dropped = [], []
    used: dict = {}
    shuffled = cand.iloc[rng.permutation(len(cand))]
    plan = {}
    for cell in cells:
        cell_key = cell if isinstance(cell, tuple) else (cell,)
        mask = np.logical_and.reduce([shuffled[c].to_numpy() == v for c, v in zip(cell_cols, cell_key)])
        plan[cell_key] = shuffled[mask]
    for cell_key, sub in plan.items():
        trial, trial_used = [], dict(used)
        ok = True
        for b in bins:
            got = 0
            for idx, g in zip(sub.index[sub[bin_col].to_numpy() == b], sub[gene_col].to_numpy()[sub[bin_col].to_numpy() == b]):
                genes = g if isinstance(g, tuple) else (g,)
                if any(trial_used.get(x, 0) >= max_per_gene for x in genes):
                    continue
                for x in genes:
                    trial_used[x] = trial_used.get(x, 0) + 1
                trial.append(idx)
                got += 1
                if got == per_cell:
                    break
            if got < per_cell:
                ok = False
                break
        if ok:
            keep += trial
            used = trial_used
        else:
            dropped.append(cell_key)
    return cand.loc[keep], dropped


def cell_capacity(cand: pd.DataFrame, cell_cols: list[str], gene_col: str = "GeneID",
                  bin_col: str = "density_bin") -> pd.DataFrame:
    """Candidates and distinct genes per bin x cell (what each cell could hold at one item per gene)."""
    g = cand.groupby([bin_col] + cell_cols)
    return pd.DataFrame({"candidates": g.size(), "genes": g[gene_col].nunique()}).reset_index()
