"""Literature density per gene from NCBI gene2pubmed.

Primary measure: fractional paper count. Each paper contributes 1/k to each of
the k human genes it is linked to; papers linked to more than
``max_genes_per_paper`` genes (screens, atlases) are dropped. Counting is by
Entrez GeneID so renamed genes keep their history.

Time cutoff: papers are kept if their PMID is below ``pmid_cutoff``. PMIDs are
assigned roughly in order of PubMed entry date, so this approximates "entered
PubMed before the cutoff date". See docs/DATA.md.
"""
from __future__ import annotations

import datetime as dt
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


def read_gene2pubmed(path: str | Path, tax_id: int = 9606, chunksize: int = 5_000_000) -> pd.DataFrame:
    """Return unique (GeneID, pmid) links for one species, read in chunks."""
    parts = []
    reader = pd.read_csv(
        path,
        sep="\t",
        compression="infer",
        chunksize=chunksize,
        dtype={"#tax_id": "int64", "GeneID": "int64", "PubMed_ID": "int64"},
    )
    for chunk in reader:
        chunk = chunk[chunk["#tax_id"] == tax_id]
        parts.append(chunk[["GeneID", "PubMed_ID"]])
    links = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=["GeneID", "PubMed_ID"])
    links = links.rename(columns={"PubMed_ID": "pmid"}).drop_duplicates(ignore_index=True)
    return links.astype({"GeneID": "int64", "pmid": "int64"})


def compute_density(
    links: pd.DataFrame,
    max_genes_per_paper: int = 100,
    pmid_cutoff: int | None = None,
    epsilon: float = 0.01,
) -> tuple[pd.DataFrame, dict]:
    """Per-gene paper counts. Returns (table, summary). Genes with no papers are absent."""
    n_links_in = len(links)
    if pmid_cutoff is not None:
        links = links[links["pmid"] < int(pmid_cutoff)]
    genes_per_paper = links.groupby("pmid")["GeneID"].nunique()
    kept_papers = genes_per_paper[genes_per_paper <= max_genes_per_paper]
    links = links[links["pmid"].isin(kept_papers.index)]
    weights = 1.0 / links["pmid"].map(kept_papers).astype("float64")
    table = (
        links.assign(weight=weights)
        .groupby("GeneID")
        .agg(n_papers=("pmid", "nunique"), frac_papers=("weight", "sum"))
        .reset_index()
    )
    table["log_density"] = np.log10(table["frac_papers"] + epsilon)
    summary = {
        "links_in": int(n_links_in),
        "papers_after_cutoff_filter": int(len(genes_per_paper)),
        "papers_dropped_high_throughput": int((genes_per_paper > max_genes_per_paper).sum()),
        "papers_kept": int(len(kept_papers)),
        "genes_with_papers": int(len(table)),
        "max_genes_per_paper": int(max_genes_per_paper),
        "pmid_cutoff": None if pmid_cutoff is None else int(pmid_cutoff),
        "epsilon": float(epsilon),
    }
    return table, summary


def attach_density(genes: pd.DataFrame, density: pd.DataFrame, epsilon: float) -> pd.DataFrame:
    """Left-join density onto a table with a GeneID column; genes without papers get zeros."""
    out = genes.merge(density, on="GeneID", how="left")
    out["n_papers"] = out["n_papers"].fillna(0).astype("int64")
    out["frac_papers"] = out["frac_papers"].fillna(0.0)
    out["log_density"] = out["log_density"].fillna(np.log10(epsilon))
    return out


def assign_bins(values: pd.Series, n_bins: int) -> pd.Series:
    """Equal-count bins (0 = least studied). Tied values share a bin via average ranks."""
    ranks = values.rank(method="average")
    return pd.qcut(ranks, q=n_bins, labels=False, duplicates="drop").astype("int64")


def resolve_pmid_cutoff(date_str: str, max_days_forward: int = 7, api_key: str | None = None,
                        email: str | None = None, retmax: int = 10_000) -> dict:
    """Smallest PMID whose PubMed entry date (edat) falls on the first non-empty day at or after date_str.

    Approximation: if more than ``retmax`` records share that day, the minimum is
    taken over the returned subset and ``truncated`` is set.
    """
    day = dt.date.fromisoformat(date_str)
    for offset in range(max_days_forward + 1):
        d = (day + dt.timedelta(days=offset)).strftime("%Y/%m/%d")
        params = {"db": "pubmed", "datetype": "edat", "mindate": d, "maxdate": d,
                  "retmax": str(retmax), "retmode": "json"}
        if api_key:
            params["api_key"] = api_key
        if email:
            params["email"] = email
        url = EUTILS + "?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=60) as resp:
            data = json.load(resp)
        result = data["esearchresult"]
        ids = [int(x) for x in result.get("idlist", [])]
        count = int(result.get("count", 0))
        if ids:
            return {"date_requested": date_str, "date_used": d, "pmid_cutoff": min(ids),
                    "records_that_day": count, "truncated": count > len(ids)}
        time.sleep(0.4)
    raise RuntimeError(f"No PubMed records found within {max_days_forward} days after {date_str}")
