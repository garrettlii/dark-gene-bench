"""Read the perturbation differential-expression results (AnnData .h5ad).

Column and layer names are not hard-coded: they come from config/columns.yaml,
which is filled in after running scripts/01_inspect_perturb.py on the real file.
Matrices are sliced column-wise with h5py so the full layers never load.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import h5py
import numpy as np
import pandas as pd


def _read_elem(node):
    try:
        from anndata.io import read_elem  # anndata >= 0.11
    except ImportError:  # pragma: no cover
        from anndata.experimental import read_elem
    return read_elem(node)


def read_obs_var(path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    with h5py.File(path, "r") as f:
        obs = _read_elem(f["obs"])
        var = _read_elem(f["var"])
    return obs, var


def _node_summary(name: str, node) -> str:
    if isinstance(node, h5py.Dataset):
        return f"{name}: dense {node.shape} {node.dtype}"
    enc = node.attrs.get("encoding-type", "group")
    shape = node.attrs.get("shape")
    return f"{name}: {enc} shape={tuple(shape) if shape is not None else '?'}"


def _column_summary(df: pd.DataFrame, max_examples: int = 3) -> list[str]:
    lines = []
    for col in df.columns:
        s = df[col]
        try:
            n_unique = s.nunique(dropna=True)
        except TypeError:
            n_unique = -1
        examples = ", ".join(map(str, s.dropna().unique()[:max_examples]))
        lines.append(f"  {col!r}: {s.dtype}, {n_unique} unique, e.g. {examples}")
    return lines


def describe(path: str | Path) -> str:
    """Human-readable structure of an .h5ad file, for filling config/columns.yaml."""
    lines = [f"file: {path}"]
    with h5py.File(path, "r") as f:
        lines.append("top-level keys: " + ", ".join(f.keys()))
        if "X" in f:
            lines.append(_node_summary("X", f["X"]))
        for group in ("layers", "obsm", "varm", "obsp", "varp"):
            if group in f and len(f[group]):
                for key in f[group]:
                    lines.append(_node_summary(f"{group}/{key}", f[group][key]))
        if "uns" in f:
            lines.append("uns keys: " + ", ".join(f["uns"].keys()))
    obs, var = read_obs_var(path)
    lines.append(f"obs: {obs.shape[0]} rows; index e.g. {', '.join(map(str, obs.index[:3]))}")
    lines += _column_summary(obs)
    lines.append(f"var: {var.shape[0]} rows; index e.g. {', '.join(map(str, var.index[:3]))}")
    lines += _column_summary(var)
    return "\n".join(lines)


def _as_bool(s: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(s):
        return s.fillna(False).astype(bool)
    if pd.api.types.is_numeric_dtype(s):
        return s.fillna(0).astype(float) != 0
    return s.astype(str).str.strip().str.lower().isin({"true", "1", "yes", "t"})


def perturbation_table(obs: pd.DataFrame, cols: dict, min_cells: int | None = None) -> pd.DataFrame:
    """One row per (perturbation, condition) with QC decisions. Raises if configured columns are missing."""
    oc = cols["obs"]
    required = {"target_gene": oc.get("target_gene"), "condition": oc.get("condition")}
    for key, name in required.items():
        if not name:
            raise ValueError(f"config/columns.yaml: obs.{key} is not set (run scripts/01_inspect_perturb.py)")
        if name not in obs.columns:
            raise KeyError(f"obs column {name!r} (obs.{key}) not found; available: {list(obs.columns)}")
    flag_cols = list(oc.get("flags_exclude_true") or []) + list(oc.get("flags_require_true") or [])
    missing = [c for c in flag_cols if c not in obs.columns]
    if missing:
        raise KeyError(f"QC flag columns not found in obs: {missing}")

    out = pd.DataFrame({
        "obs_index": np.arange(len(obs)),
        "obs_name": obs.index.astype(str),
        "target": obs[oc["target_gene"]].astype(str).to_numpy(),
        "condition": obs[oc["condition"]].astype(str).to_numpy(),
    })
    ens_col = oc.get("target_gene_id")
    out["target_ensembl"] = obs[ens_col].astype(str).to_numpy() if ens_col else None

    qc = pd.Series(True, index=out.index)
    for c in oc.get("flags_exclude_true") or []:
        flag = _as_bool(obs[c]).to_numpy()
        out[f"flag_{c}"] = flag
        qc &= ~flag
    for c in oc.get("flags_require_true") or []:
        flag = _as_bool(obs[c]).to_numpy()
        out[f"require_{c}"] = flag
        qc &= flag
    ncell_col = oc.get("n_cells")
    if ncell_col and min_cells:
        n = pd.to_numeric(obs[ncell_col], errors="coerce").to_numpy()
        out["n_cells"] = n
        qc &= pd.Series(n >= min_cells, index=out.index)
    eff_col = oc.get("effect_size")
    if eff_col:
        out["effect_size"] = pd.to_numeric(obs[eff_col], errors="coerce").to_numpy()
    out["qc_pass"] = qc.to_numpy()
    return out


def _matrix_key(name: str | None) -> str:
    if not name or name == "X":
        return "X"
    return f"layers/{name}"


def read_columns(path: str | Path, matrix: str | None, col_idx: Iterable[int]) -> np.ndarray:
    """Read selected columns (all rows) of X or a layer without loading the whole matrix."""
    col_idx = np.asarray(list(col_idx), dtype=np.int64)
    if len(np.unique(col_idx)) != len(col_idx):
        raise ValueError("column indices must be unique")
    order = np.argsort(col_idx)
    with h5py.File(path, "r") as f:
        node = f[_matrix_key(matrix)]
        if isinstance(node, h5py.Dataset):
            data = node[:, col_idx[order]]
            return data[:, np.argsort(order)]
        mat = _read_elem(node)  # sparse: loads the matrix
        return np.asarray(mat[:, col_idx].todense())


def readout_long(path: str | Path, var: pd.DataFrame, cols: dict, readouts: list[str]) -> tuple[pd.DataFrame, list[str]]:
    """Long table (obs_index, readout, lfc, padj) for the readout panel. Returns (table, missing readouts)."""
    vc, lc = cols.get("var", {}), cols["layers"]
    if not lc.get("lfc") or not lc.get("padj"):
        raise ValueError("config/columns.yaml: layers.lfc and layers.padj must be set")
    symbols = var[vc["gene_symbol"]].astype(str) if vc.get("gene_symbol") else pd.Series(var.index.astype(str))
    pos = {s: i for i, s in enumerate(symbols.to_numpy())}
    present = [r for r in readouts if r in pos]
    missing = [r for r in readouts if r not in pos]
    if not present:
        return pd.DataFrame(columns=["obs_index", "readout", "lfc", "padj"]), missing
    idx = [pos[r] for r in present]
    lfc = read_columns(path, lc["lfc"], idx)
    padj = read_columns(path, lc["padj"], idx)
    n_obs = lfc.shape[0]
    table = pd.DataFrame({
        "obs_index": np.repeat(np.arange(n_obs), len(present)),
        "readout": np.tile(present, n_obs),
        "lfc": lfc.reshape(-1).astype("float64"),
        "padj": padj.reshape(-1).astype("float64"),
    })
    return table, missing
