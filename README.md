# dark-gene-bench

Does an AI research agent's skill at analysing experimental data depend on how much has been written about the subject?

This benchmark holds the task and the dataset fixed and varies literature density: from heavily studied genes to genes with almost no papers. Each task is answered three ways: with no data (prior knowledge only), with data, and with data but the gene's identity hidden. The comparison separates what agents conclude from the data from what they already knew.

- **Data:** genome-scale CRISPRi Perturb-seq in primary human CD4+ T cells (Zhu et al. 2026, *Cell*): four donors, three stimulation conditions. Truth comes from held-out donors.
- **Density:** fractional PubMed counts per gene from NCBI gene2pubmed, cut off at the evaluated models' training cutoff.
- **Questions:** direct effects, signature neighbours, context shifts and unseen perturbations, answered with probabilities and scored with Brier skill against scripted baselines.

See [`docs/DESIGN.md`](docs/DESIGN.md) for the full design, [`docs/DATA.md`](docs/DATA.md) for sources and licences, and [`docs/RELATED_WORK.md`](docs/RELATED_WORK.md) for context.

## Status

Phase 0 (prior-only probe) is implemented and tested on synthetic data. It is the go/no-go check: if models' no-data accuracy does not fall as literature density falls, the density axis carries no signal and the design stops. Phases 1–3 are specified in the design doc.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,api]"
pytest -q

python scripts/00_fetch_ncbi.py                   # NCBI files -> ~/benchmarks/dgb/dgb-data/raw/ncbi
# download the DE results file (docs/DATA.md), set its path in config/columns.yaml
python scripts/01_inspect_perturb.py              # then fill config/columns.yaml
python scripts/02_build_density.py --resolve-pmid-cutoff
python scripts/03_build_gene_table.py             # -> reports/feasibility.md
python scripts/04_make_probe_batch.py --dry-run
# fill in, commit and push prereg/phase0_prior_probe.md
python scripts/04_make_probe_batch.py --prereg prereg/phase0_prior_probe.md
python scripts/05_run_probe.py --batch <id> --limit 5
python scripts/05_run_probe.py --batch <id>
python scripts/06_score_probe.py --batch <id>     # -> reports/phase0_<id>.md
```

## Rules

- **Pre-registration first.** A batch can only be generated from a filled-in, committed and pushed pre-registration; each batch is recorded in a ledger, and a second batch under the same pre-registration needs a recorded reason. See [`prereg/README.md`](prereg/README.md).
- **Aggregates only in the repo.** Question sets, responses and truth stay outside the repository.
- **Everything evaluation-related lives outside the repo tree** (`~/benchmarks/dgb/dgb-data`, `~/benchmarks/dgb/dgb-runs`, `~/benchmarks/dgb/dgb-truth` by default), so agents under evaluation can never read the design or the answers.

## Layout

| Path | Contents |
|---|---|
| `config/` | main config, dataset column map, genes named in the dataset paper |
| `docs/` | design, data, related work, decision log |
| `prereg/` | pre-registration templates and committed predictions |
| `scripts/` | numbered pipeline steps |
| `src/dgbench/` | density, identifiers, dataset reader, questions, model backends, scoring, pre-registration guard |
| `tests/` | synthetic-data tests |
| `reports/` | aggregate results only |
