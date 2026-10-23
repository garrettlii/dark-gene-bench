# Working rules for this repository

This repo builds a benchmark that measures how much an AI research agent's skill at analysing perturbation data depends on how much has been written about the gene. Read `docs/DESIGN.md` before changing anything substantive.

## Hard rules

1. **No AI attribution, anywhere.** Never add `Co-Authored-By` trailers, "Generated with …" lines, session links, or any mention of an AI assistant to commit messages, PR titles or descriptions, issues, code comments, docs or file headers. Commit messages describe the change and nothing else. `.claude/settings.json` disables automatic attribution; this rule covers everything the setting does not.
2. **Pre-register before every batch.** Never generate a batch unless its pre-registration file is filled in, committed and pushed; `scripts/04_make_probe_batch.py` enforces this. Never bypass the guard, edit it to pass, or use `--additional-batch-reason` unless the human explicitly asks and supplies the reason.
3. **Aggregates only in the repo.** Committed files may contain counts and per-bin statistics. Gene lists, question sets, model responses, per-question scores and truth stay under `data_root`, `runs_root` and `truth_root`. Never paste per-question results into chat summaries either; report aggregates.
4. **Nothing evaluation-related inside the repo tree.** Data, task workspaces, model outputs and answer keys live outside it (`config/default.yaml`, enforced at load). Agents under evaluation must never run inside this repo, because they would read this file and the design docs. Before any run, check that no `CLAUDE.md` or `AGENTS.md` exists in `runs_root`, its subdirectories, or any parent directory (including the home directory).
5. **Conflict of interest.** Claude models are among the evaluated models, possibly including the model reading this. Produce numbers; do not interpret Claude results, do not propose thresholds, binning or scoring changes after seeing results, and flag any such question for the human.
6. **Frozen after generation.** Truth definitions, thresholds, binning and scoring do not change after a batch exists without a new dated entry in `docs/DECISIONS.md` and a new pre-registration.
7. **Ask instead of guessing** about dataset semantics: column meanings, condition labels, which layer holds which statistic, whether p-values are adjusted.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,api]"
pytest -q
```

## Phase 0 runbook (prior-only probe)

1. `python scripts/00_fetch_ncbi.py` — gene2pubmed and gene_info into `~/dgb-data/raw/ncbi`.
2. Download the differential-expression results object for Zhu et al. 2026 (see `docs/DATA.md`) into `~/dgb-data/raw/czi_tcell/` and set `de_results.path` in `config/columns.yaml`.
3. `python scripts/01_inspect_perturb.py` — fill in `config/columns.yaml` and make the `probe.condition_text` keys in `config/default.yaml` match the condition labels. Show the human the mapping and get confirmation.
4. `python scripts/02_build_density.py --resolve-pmid-cutoff` — needs network access to NCBI E-utilities.
5. `python scripts/03_build_gene_table.py` — writes `reports/feasibility.md`. Stop and show the human the per-bin counts and any bin-collapse warning.
6. `python scripts/04_make_probe_batch.py --dry-run` — check quotas per bin. The human fills in `prereg/phase0_prior_probe.md`, commits and pushes it.
7. `python scripts/04_make_probe_batch.py --prereg prereg/phase0_prior_probe.md`
8. Smoke test: `python scripts/05_run_probe.py --batch <id> --limit 5`; check parse failures and the raw responses. Then run without `--limit`. Infrastructure errors (quota, auth, timeouts) are retried on the next run; a run that fails within seconds is almost always auth or quota, not a model answer.
9. `python scripts/06_score_probe.py --batch <id>` — writes `reports/phase0_<id>.md` (aggregates only, safe to commit).

CLI backends: confirm flags with `claude --help` and `codex exec --help` before the first run. Each CLI model runs in its own empty directory under `runs_root/_empty_cwd/`.

## Phase 1 backlog (not started)

- Per-donor pseudobulk (donors 1–2 for agents, 3–4 for truth), computed once on a cluster.
- Gene programs derived from donors 1–2 only.
- Generators for families F2–F4; anonymizer with the identity-guess leakage probe.
- Truth under at least three pipelines; drop disagreements.
- Scripted baselines per family and the donor ceiling.
- Neutral agent harness: same scaffold for every model, no internet, fixed budget, workspaces outside this repo, truth never mounted.
- Matching of genes within density bins on reliability, effect size, knockdown efficiency and expression.

## Conventions

- Python ≥ 3.10, `src/` layout, pytest; tests use synthetic data and never touch the network.
- Scripts read `config/default.yaml` (override with `--config`); keep new parameters in config, not code.
- Prefer small, tested functions in `src/dgbench/`; scripts stay thin.
