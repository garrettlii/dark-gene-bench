# Data

All data lives under `paths.data_root` (default `~/dgb-data`), outside the repository. Record every download's checksum; manifests are written next to the files.

## NCBI Gene (literature density and identifiers)

Downloaded by `python scripts/00_fetch_ncbi.py`:

| File | Source | Use |
|---|---|---|
| `gene2pubmed.gz` | https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz | gene–paper links |
| `Homo_sapiens.gene_info.gz` | https://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz | symbols, synonyms, Ensembl cross-references |

These files are updated daily; the manifest records the download time and SHA-256.

**Time cutoff.** gene2pubmed has no dates. We keep papers whose PMID is below the first PMID entered in PubMed on `density.cutoff_date` (`scripts/02_build_density.py --resolve-pmid-cutoff`, via NCBI E-utilities). PMIDs are assigned roughly in entry order, so this approximates "entered PubMed before the cutoff"; older papers indexed late are a known, small exception. Ranking by density is insensitive to the exact cutoff; it matters mainly for genes whose first papers are very recent. Set `NCBI_API_KEY` in the environment for higher rate limits (optional).

## Perturbation data: Zhu et al. 2026 (primary)

- Paper: Zhu, Dann, Yan et al., "Genome-scale perturb-seq in primary human CD4+ T cells maps context-specific regulators of T cell programs and human immune traits", *Cell* (2026), DOI 10.1016/j.cell.2026.08.002. Preprint: bioRxiv 2025.12.23.696273.
- Data: CZI Virtual Cells Platform, https://virtualcellmodels.cziscience.com/dataset/genome-scale-tcell-perturb-seq
- Licence: the dataset page lists the MIT License and an Acceptable Use Policy; the article is CC BY-NC. Confirm both before redistribution of any derived files.

**Phase 0 needs only the differential-expression results object** (one row per perturbation × condition; the dataset page lists 33,983 rows × 10,282 measured genes, plus per-perturbation QC flags). Download it manually to `~/dgb-data/raw/czi_tcell/`, set `de_results.path` in `config/columns.yaml`, then run `scripts/01_inspect_perturb.py` and fill in the column names. Record its SHA-256 (the batch manifest also records it).

**Phase 1 needs the per-donor single-cell objects** (one per donor × condition; 22 million cells in total). Check first whether per-donor pseudobulk is provided. If not, compute pseudobulk once on a cluster (e.g. Sherlock) and store only the pseudobulk matrices under `data_root`.

QC flags described on the dataset page (confirm exact names and semantics with `01_inspect_perturb.py`):
- `neighboring_gene_KD`: a gene adjacent to the target locus is also knocked down (cis off-target)
- `distal_offtarget_flag`: possible distal off-target effect
- `low_target_gex`: low baseline target expression; knockdown estimate may be unreliable
- `keep_test_genes`: perturbation passes the authors' criteria for differential-expression analysis

## Replication data (contingent): Virtual Cell Challenge 2026

Arc Institute, six cancer cell lines (A549, MCF7, HT29, HAP1, BxPC3, K562), CRISPRi with 10x Flex. https://virtualcellchallenge.org/ — final submissions close 5 November 2026; results expected late November 2026. Only control-cell profiles and perturbation lists are public during the challenge. Check for a full release after results are announced, and check its licence.

## Other public perturbation screens (background, likely in training data)

- Replogle et al. 2022, genome-scale CRISPRi Perturb-seq in K562 and RPE1: https://gwps.wi.mit.edu/
- Nadig et al., TRADE, with essential-gene screens in Jurkat and HepG2 (PMC11244993).

## What may be committed

Only aggregate summaries (counts, per-bin statistics) go in `reports/`. Gene lists, question sets, model outputs and truth stay under `data_root`, `runs_root` and `truth_root`.
