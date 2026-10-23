"""Load YAML configuration and resolve the three external directories.

Data, run outputs and truth files must live outside the repository so that
agents under evaluation can never read them (or this repo's docs) from a
task workspace.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "config" / "default.yaml"
PATH_KEYS = ("data_root", "runs_root", "truth_root")


def _expand(path: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(path))).resolve()


def _is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def _substitute(obj: Any, tokens: dict[str, str]) -> Any:
    """Replace {data_root}-style tokens in every string, leaving other braces alone."""
    if isinstance(obj, str):
        for key, value in tokens.items():
            obj = obj.replace("{" + key + "}", value)
        return obj
    if isinstance(obj, list):
        return [_substitute(v, tokens) for v in obj]
    if isinstance(obj, dict):
        return {k: _substitute(v, tokens) for k, v in obj.items()}
    return obj


def resolve_paths(cfg: dict, repo_root: Path = REPO_ROOT) -> dict:
    cfg = copy.deepcopy(cfg)
    paths = {k: _expand(cfg["paths"][k]) for k in PATH_KEYS}
    for key, path in paths.items():
        if _is_within(path, repo_root.resolve()):
            raise ValueError(
                f"paths.{key} ({path}) is inside the repository. Keep data, runs and "
                "truth outside the repo so evaluated agents cannot reach them."
            )
    if _is_within(paths["truth_root"], paths["runs_root"]):
        raise ValueError("paths.truth_root must not be inside paths.runs_root.")
    tokens = {k: str(v) for k, v in paths.items()}
    tokens["repo_root"] = str(repo_root.resolve())
    cfg = _substitute(cfg, tokens)
    cfg["paths"] = tokens
    return cfg


def load_config(path: str | Path | None = None) -> dict:
    path = Path(path) if path else DEFAULT_CONFIG
    with open(path) as fh:
        cfg = yaml.safe_load(fh)
    cfg = resolve_paths(cfg)
    columns_file = cfg.get("perturb", {}).get("columns_file")
    if columns_file:
        cpath = Path(columns_file)
        if not cpath.is_absolute():
            cpath = REPO_ROOT / cpath
        with open(cpath) as fh:
            cfg["columns"] = _substitute(yaml.safe_load(fh), cfg["paths"])
    return cfg


def config_hash(cfg: dict) -> str:
    blob = json.dumps(cfg, sort_keys=True, default=str).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def derived_path(cfg: dict, name: str) -> Path:
    out = Path(cfg["paths"]["data_root"]) / "derived"
    out.mkdir(parents=True, exist_ok=True)
    return out / name
