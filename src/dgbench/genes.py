"""Map perturbation targets to Entrez GeneIDs using NCBI Homo_sapiens.gene_info."""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import pandas as pd

_ENSEMBL_VERSION = re.compile(r"\.\d+$")


def read_gene_info(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", compression="infer", dtype=str, keep_default_na=False)
    df = df.rename(columns={"#tax_id": "tax_id"})
    df["GeneID"] = df["GeneID"].astype("int64")
    return df[["GeneID", "Symbol", "Synonyms", "dbXrefs", "type_of_gene", "description"]]


def strip_version(ensembl_id: str) -> str:
    return _ENSEMBL_VERSION.sub("", ensembl_id.strip())


@dataclass
class GeneMaps:
    symbol: dict[str, int] = field(default_factory=dict)
    symbol_upper: dict[str, int] = field(default_factory=dict)
    synonym: dict[str, int] = field(default_factory=dict)  # unambiguous synonyms only
    ensembl: dict[str, int] = field(default_factory=dict)


def build_maps(gene_info: pd.DataFrame) -> GeneMaps:
    maps = GeneMaps()
    upper_seen: dict[str, set[int]] = defaultdict(set)
    syn_seen: dict[str, set[int]] = defaultdict(set)
    ens_seen: dict[str, set[int]] = defaultdict(set)
    for gid, sym, syns, xrefs in gene_info[["GeneID", "Symbol", "Synonyms", "dbXrefs"]].itertuples(index=False):
        maps.symbol[sym] = gid
        upper_seen[sym.upper()].add(gid)
        if syns and syns != "-":
            for s in syns.split("|"):
                syn_seen[s.strip().upper()].add(gid)
        if xrefs and xrefs != "-":
            for x in xrefs.split("|"):
                if x.startswith("Ensembl:"):
                    ens_seen[strip_version(x.split(":", 1)[1])].add(gid)
    maps.symbol_upper = {k: next(iter(v)) for k, v in upper_seen.items() if len(v) == 1}
    official_upper = set(upper_seen)
    maps.synonym = {k: next(iter(v)) for k, v in syn_seen.items() if len(v) == 1 and k not in official_upper}
    maps.ensembl = {k: next(iter(v)) for k, v in ens_seen.items() if len(v) == 1}
    return maps


def map_targets(symbols: Iterable[str], maps: GeneMaps, ensembl_ids: Iterable[str] | None = None) -> pd.DataFrame:
    """Map each target. Order of preference: Ensembl, exact symbol, case-insensitive symbol, unambiguous synonym."""
    symbols = list(symbols)
    ens = list(ensembl_ids) if ensembl_ids is not None else [None] * len(symbols)
    rows = []
    for sym, eid in zip(symbols, ens):
        gid, method = None, "unmapped"
        if eid and isinstance(eid, str) and strip_version(eid) in maps.ensembl:
            gid, method = maps.ensembl[strip_version(eid)], "ensembl"
        elif sym in maps.symbol:
            gid, method = maps.symbol[sym], "symbol"
        elif isinstance(sym, str) and sym.upper() in maps.symbol_upper:
            gid, method = maps.symbol_upper[sym.upper()], "symbol_case"
        elif isinstance(sym, str) and sym.upper() in maps.synonym:
            gid, method = maps.synonym[sym.upper()], "synonym"
        rows.append({"target": sym, "target_ensembl": eid, "GeneID": gid, "map_method": method})
    out = pd.DataFrame(rows)
    out["GeneID"] = out["GeneID"].astype("Int64")
    return out
