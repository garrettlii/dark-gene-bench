# Probe v2 runbook

Prior-only probe with each question asked twice, with the gene named and with it hidden. Design: `docs/DESIGN.md` and D-015 to D-022 in `docs/DECISIONS.md`. Data, runs and truth stay outside the repository (`config/default.yaml`).

1. For each model's `cutoff_date`: `python scripts/02_build_density.py --cutoff-date <D> --tcell`. Then `python scripts/03_build_gene_table.py`.
2. `python scripts/07_build_probe2_inputs.py` builds labels, DE counts and correlations from the combined and donor-pair fits into `data_root/derived/probe2/`.
3. `python scripts/08_make_probe2_batch.py --dry-run` writes `reports/probe2_dryrun.md` (aggregate counts only). Fill in `prereg/probe2.md` and the probe v2 FILL values in `config/default.yaml`, then commit and push.
4. `python scripts/08_make_probe2_batch.py --prereg prereg/probe2.md` generates the batch. It refuses to run unless the pre-registration is committed and pushed, `config/` is clean, and every FILL value is set.
5. Smoke test each model: `python scripts/05_run_probe.py --batch <id> --models <name> --limit 5`. Check parse failures and raw responses, then run without `--limit`. Rerun until every model has 0 infrastructure errors; a call that fails within seconds is usually authentication or quota.
6. `python scripts/09_score_probe2.py --batch <id>` writes `reports/probe2_<id>.md`. The report is marked INTERIM until every model has 0 unanswered calls and 0 infrastructure errors.

Before any run, check that no assistant instruction files (for example `CLAUDE.md` or `AGENTS.md`) exist in `runs_root`, its subdirectories, or any parent directory. Each CLI model runs in its own empty directory under `runs_root/_empty_cwd/`.

## Phase 1 backlog item added by probe v2

- Program-level questions (deferred from probe v2): programs must be derived from donors 1–2 only.
