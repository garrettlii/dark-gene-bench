# Decision log

Append-only. Any change to truth definitions, thresholds, scoring or binning after a batch exists needs a dated entry here and a new pre-registration.

## 2026-10-22

- **D-001 Manipulated variable.** Literature density per gene, holding task and dataset fixed. Reason: post-cutoff designs saturate (BioStudyBench best closed model 94.7%) and planted faults saturated in planted-fault-bench.
- **D-002 Domain.** Genes over neuroimaging: measurable density for ~10,000 uniformly perturbed genes; neuro entities lack a clean density axis.
- **D-003 Primary dataset.** Zhu et al. 2026 CD4+ T-cell genome-scale CRISPRi Perturb-seq: donor replication (truth from held-out donors) and three conditions (context shift). Virtual Cell Challenge 2026 data as contingent replication.
- **D-004 Density measure.** Fractional gene2pubmed counts, papers linking >100 genes dropped, Entrez IDs, PMID cutoff at the earliest evaluated model's training cutoff.
- **D-005 Phase 0 truth.** Combined-donor differential-expression results with fixed thresholds as provisional truth; held-out-donor truth starts in Phase 1.
- **D-006 Integrity.** Batches require a filled, committed and pushed pre-registration; one batch per pre-registration commit unless a reason is recorded in the ledger; only aggregates are committed; data, runs and truth live outside the repository.
