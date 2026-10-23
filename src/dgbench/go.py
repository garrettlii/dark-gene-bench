"""Gene Ontology annotations (GOA human GAF) as a model could have seen them.

Each model uses the archived GOA release published closest before its cutoff (D-021);
annotations that cite the dataset paper are dropped. A no-IEA variant drops electronic
annotations. (An older date-column filter is kept for reference: GAF dates are
last-modified dates, so it also removes annotations re-dated by later releases.)
"""
from __future__ import annotations

import gzip
from collections import defaultdict
from pathlib import Path

import pandas as pd

GAF_COLUMNS = ["db", "db_id", "symbol", "qualifier", "go_id", "reference", "evidence", "with_from", "aspect",
               "name", "synonyms", "type", "taxon", "date", "assigned_by", "extension", "product_form"]
COMPLEX_ROOT = "GO:0032991"  # protein-containing complex


def read_gaf(path: str | Path) -> pd.DataFrame:
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt") as fh:
        rows = [ln.rstrip("\n").split("\t") for ln in fh if not ln.startswith("!")]
    df = pd.DataFrame([r[:17] + [""] * (17 - len(r)) for r in rows], columns=GAF_COLUMNS)
    return df[~df["qualifier"].str.contains("NOT", na=False)]


def filter_annotations(gaf: pd.DataFrame, exclude_refs: list[str], cutoff_date: str | None = None,
                       exclude_evidence: tuple[str, ...] = ()) -> pd.DataFrame:
    """Drop annotations citing any of exclude_refs, with an evidence code in exclude_evidence,
    or (if cutoff_date is given, YYYY-MM-DD) dated on or after the cutoff."""
    cited = gaf["reference"].str.split("|").apply(lambda rs: any(r in exclude_refs for r in rs))
    keep = ~cited & ~gaf["evidence"].isin(exclude_evidence)
    if cutoff_date:
        keep &= gaf["date"] < cutoff_date.replace("-", "")
    return gaf[keep]


def gene_terms(gaf: pd.DataFrame, symbol_to_gid: dict[str, int]) -> dict[int, frozenset[str]]:
    out: dict[int, set[str]] = defaultdict(set)
    for sym, go_id in gaf[["symbol", "go_id"]].itertuples(index=False):
        gid = symbol_to_gid.get(sym)
        if gid is not None:
            out[gid].add(go_id)
    return {g: frozenset(t) for g, t in out.items()}


def term_sizes(terms: dict[int, frozenset[str]]) -> dict[str, int]:
    sizes: dict[str, int] = defaultdict(int)
    for ts in terms.values():
        for t in ts:
            sizes[t] += 1
    return dict(sizes)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    union = len(a | b)
    return len(a & b) / union if union else 0.0


def read_obo_parents(path: str | Path) -> dict[str, set[str]]:
    """is_a and part_of parents per term from an OBO file."""
    parents: dict[str, set[str]] = defaultdict(set)
    term = None
    with open(path) as fh:
        for ln in fh:
            ln = ln.strip()
            if ln == "[Term]":
                term = None
            elif ln.startswith("id: GO:"):
                term = ln[4:]
            elif term and ln.startswith("is_a: "):
                parents[term].add(ln.split()[1])
            elif term and ln.startswith("relationship: part_of "):
                parents[term].add(ln.split()[2])
    return parents


def descendants(root: str, parents: dict[str, set[str]]) -> set[str]:
    children: dict[str, set[str]] = defaultdict(set)
    for child, ps in parents.items():
        for p in ps:
            children[p].add(child)
    out, stack = set(), [root]
    while stack:
        for c in children[stack.pop()]:
            if c not in out:
                out.add(c)
                stack.append(c)
    return out


def pairwise(gids, terms: dict[int, frozenset[str]], restrict: set[str] | None = None):
    """(jaccard, shares_any) matrices over genes ``gids`` using their terms (optionally only ``restrict``)."""
    import numpy as np
    from scipy import sparse

    vocab: dict[str, int] = {}
    r, c = [], []
    for i, g in enumerate(gids):
        for t in terms.get(g, ()):
            if restrict is None or t in restrict:
                r.append(i)
                c.append(vocab.setdefault(t, len(vocab)))
    X = sparse.csr_matrix((np.ones(len(r), dtype=np.float32), (r, c)), shape=(len(gids), max(len(vocab), 1)))
    inter = (X @ X.T).toarray()
    n = np.asarray(X.sum(axis=1)).ravel()
    union = n[:, None] + n[None, :] - inter
    jac = np.divide(inter, union, out=np.zeros_like(inter), where=union > 0)
    return jac, inter > 0
