import os
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

from dgbench.backends import CLIBackend, parse_probs
from dgbench.prereg import PreregError, check_prereg
from dgbench.questions import LABELS, build_prompt, label_effects, sample_questions
from dgbench.scoring import by_bin, skill, verdicts


def test_label_effects_thresholds():
    lfc = np.array([-0.5, 0.5, 0.05, 0.2, -0.5, np.nan])
    padj = np.array([0.01, 0.01, 0.9, 0.01, 0.2, 0.01])
    got = label_effects(lfc, padj, alpha=0.05, lfc_min=0.25, none_padj_min=0.5, none_lfc_max=0.1)
    assert list(got) == ["decreased", "increased", "unchanged", None, None, None]


def _candidates(n_genes=40, per_gene=6, n_bins=2, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for g in range(n_genes):
        for _ in range(per_gene):
            rows.append({"GeneID": g, "density_bin": g % n_bins, "label": rng.choice(LABELS)})
    return pd.DataFrame(rows)


def test_sampling_balances_labels_and_caps_genes():
    cand = _candidates()
    picked = sample_questions(cand, per_bin=30, max_per_gene=2, rng=np.random.default_rng(1))
    for _, sub in picked.groupby("density_bin"):
        assert len(sub) == 30
        assert sub["label"].value_counts().to_dict() == {lab: 10 for lab in LABELS}
        assert sub.groupby("GeneID").size().max() <= 2
    assert picked["qid"].is_unique


def test_sampling_reports_shortfall_instead_of_padding():
    cand = _candidates(n_genes=4, per_gene=3)
    picked = sample_questions(cand, per_bin=30, max_per_gene=1, rng=np.random.default_rng(1))
    assert picked.groupby("density_bin").size().max() <= 2


def test_prompt_renders_json_example():
    p = build_prompt("AAA1", "IL2", "48 hours after re-stimulation", balanced=True)
    assert '{"decreased": 0.2, "unchanged": 0.5, "increased": 0.3}' in p
    assert "AAA1" in p and "equally often" in p


def _scored(n_genes=60, n_bins=3, seed=0, good_bins=(2,)):
    rng = np.random.default_rng(seed)
    rows = []
    for g in range(n_genes):
        b = g % n_bins
        for _ in range(3):
            lab = rng.choice(LABELS)
            if b in good_bins:
                p = {k: (0.8 if k == lab else 0.1) for k in LABELS}
            else:
                p = {k: 1 / 3 for k in LABELS}
            rows.append({"GeneID": g, "density_bin": b, "label": lab, "parse_failed": False,
                         **{f"p_{k}": v for k, v in p.items()}})
    return pd.DataFrame(rows)


def test_skill_reference_cases():
    df = _scored(good_bins=())
    ref = np.array([1 / 3] * 3)
    assert skill(df, LABELS, ref) == pytest.approx(0.0, abs=1e-9)
    perfect = df.copy()
    for k in LABELS:
        perfect[f"p_{k}"] = (perfect["label"] == k).astype(float)
    assert skill(perfect, LABELS, ref) == pytest.approx(1.0)


def test_by_bin_and_verdicts():
    df = _scored()
    table, slope = by_bin(df, LABELS, n_boot=200, seed=0)
    assert list(table["density_bin"]) == [0, 1, 2]
    top = table.iloc[-1]
    assert top["ci_low"] <= top["skill"] <= top["ci_high"] and top["skill"] > 0.5
    assert slope["slope"] > 0
    v = verdicts(table, slope, {"top_bin_min_skill": 0.3, "bottom_bin_max_skill": 0.05, "min_slope": 0.0})
    assert all(v.values())


def test_parse_probs():
    labs = LABELS
    assert parse_probs('example {"decreased": 0.2, "unchanged": 0.5, "increased": 0.3} '
                       'answer {"decreased": 2, "unchanged": 1, "increased": 1}', labs) == {
        "decreased": 0.5, "unchanged": 0.25, "increased": 0.25}
    assert parse_probs('{"decreased": -1, "unchanged": 1, "increased": 1}', labs) is None
    assert parse_probs("no json here", labs) is None
    assert parse_probs('{"down": 1}', labs) is None


def test_cli_backend_runs_in_empty_dir(tmp_path):
    cmd = [sys.executable, "-c", "import sys; print(len(sys.argv[1])); "
           "print('{\"decreased\": 1, \"unchanged\": 0, \"increased\": 0}')", "{prompt}"]
    backend = CLIBackend(cmd, workdir=str(tmp_path / "cwd"))
    out = backend.complete("hello")
    assert parse_probs(out, LABELS)["decreased"] == 1.0
    (tmp_path / "cwd" / "stray.txt").write_text("x")
    with pytest.raises(RuntimeError):
        CLIBackend(cmd, workdir=str(tmp_path / "cwd"))


PREREG = """# Pre-registration

```yaml
predictions:
  top_bin_min_skill: {top}
  bottom_bin_max_skill: 0.05
  min_slope: 0.0
```
"""


def _git(repo, *args):
    env = {**os.environ, "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.com",
           "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.com"}
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)


def test_prereg_guard(tmp_path):
    repo, remote = tmp_path / "repo", tmp_path / "remote.git"
    repo.mkdir()
    _git(tmp_path, "init", "--bare", "-b", "main", str(remote))
    _git(repo, "init", "-b", "main")
    f = repo / "prereg.md"
    f.write_text(PREREG.format(top="<<FILL: number>>"))
    with pytest.raises(PreregError, match="placeholder"):
        check_prereg("prereg.md", repo=repo)
    f.write_text(PREREG.format(top="0.1"))
    with pytest.raises(PreregError):
        check_prereg("prereg.md", repo=repo)  # untracked
    _git(repo, "add", "prereg.md")
    _git(repo, "commit", "-m", "Add pre-registration")
    with pytest.raises(PreregError, match="remote"):
        check_prereg("prereg.md", repo=repo)
    info = check_prereg("prereg.md", repo=repo, require_pushed=False)
    assert info["predictions"]["top_bin_min_skill"] == 0.1
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")
    info = check_prereg("prereg.md", repo=repo)
    assert info["pushed_to"] == ["origin/main"]
    f.write_text(PREREG.format(top="0.2"))
    with pytest.raises(PreregError, match="uncommitted"):
        check_prereg("prereg.md", repo=repo)


def test_prereg_guard_requires_clean_config(tmp_path):
    repo = tmp_path / "repo"
    (repo / "config").mkdir(parents=True)
    _git(repo, "init", "-b", "main")
    (repo / "prereg.md").write_text(PREREG.format(top="0.1"))
    cfg = repo / "config" / "default.yaml"
    cfg.write_text("a: 1\n")
    _git(repo, "add", "prereg.md", "config/default.yaml")
    _git(repo, "commit", "-m", "Add pre-registration")
    check_prereg("prereg.md", repo=repo, require_pushed=False)
    cfg.write_text("a: 2\n")
    with pytest.raises(PreregError, match="config/"):
        check_prereg("prereg.md", repo=repo, require_pushed=False)  # modified tracked file
    _git(repo, "checkout", "--", "config/default.yaml")
    (repo / "config" / "new.txt").write_text("x\n")
    with pytest.raises(PreregError, match="config/"):
        check_prereg("prereg.md", repo=repo, require_pushed=False)  # new untracked file
