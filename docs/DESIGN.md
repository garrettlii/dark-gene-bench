# Design

## Question

How much of an AI research agent's ability to draw correct conclusions from experimental data depends on what it already knows about the subject?

We hold the task and the dataset fixed and vary one thing: how much has been written about the subject, from heavily studied genes to genes with almost no literature. For every task we measure performance with no data, with data, and with data but the gene's identity hidden.

## Why this design

- **Post-cutoff is not the same as scarce.** BioStudyBench uses biomedical studies first published after the evaluated models' cutoffs and runs each task with and without data; the best closed model already passes 94.7%. New findings in well-studied areas can still be reached largely from priors.
- **Freshness is already the field's default.** RECLAIM is built to be rebuilt each year from new conferences, and the ICML 2026 Open Reproductions challenge covered about a third of the conference.
- **Planted-fault benchmarks saturate.** In planted-fault-bench, both evaluated agents reached behavior d′ ≈ 2.9 on a textbook fault class.
- **Recall studies exist; analysis studies don't.** SciHorizon-Gene shows LLM knowledge-QA accuracy drops for genes with little research attention. No benchmark asks whether *data analysis* holds up as the literature thins, while separating prior knowledge from what the data shows.

Either outcome is informative. If agents on the least-studied genes, with names shown, match well-studied genes with names hidden, and beat a scripted baseline on the harder families, that is direct evidence of capability without training data. If performance falls to the baseline, their apparent skill was mostly memory.

## Why genes rather than neuroimaging

- **Signal.** Literature density is measurable per gene with standard tools (NCBI gene2pubmed), spans orders of magnitude, and covers ~10,000 perturbed genes measured identically in one assay. Brain cell-type clusters have opaque IDs with no literature to count; brain regions number in the hundreds, and their density is confounded with size and recording yield.
- **Difficulty from science, not plumbing.** Gene effects in T cells depend on stimulation context, so textbook priors can mislead. Predicting unseen perturbations is hard: simple linear baselines have matched or beaten deep models on perturbation-effect prediction (Ahlmann-Eltze et al. 2025; verify citation). Neuroimaging tasks would mostly be hard because the data is messy, which other benchmarks already measure.
- **Cost.** This leaves the neuroimaging home field; a computational-biology collaborator should review question templates and truth definitions.

## Data

### Primary: genome-scale CRISPRi Perturb-seq in primary human CD4+ T cells

Zhu et al. 2026, *Cell* (DOI 10.1016/j.cell.2026.08.002; preprint bioRxiv 2025.12.23.696273). All expressed genes perturbed across 22 million cells from four donors under three conditions (rest, 8 h and 48 h after re-stimulation). The authors recovered ~575 cells per perturbed gene per condition and report that active regulators change substantially across stimulation conditions. The data page lists QC flags for cis off-target knockdown of neighbouring genes, distal off-target effects, and low baseline target expression. Data: CZI Virtual Cells Platform (see docs/DATA.md).

Why this dataset:
- **Donors give biological replicates**, so truth can come from held-out people rather than resampled cells.
- **Conditions give context-shift questions**, where priors are most likely to mislead.
- **Contamination note:** the preprint (December 2025) predates the training cutoffs of current models. Genes the paper discusses by name go in `config/flagged_genes.txt` and are excluded from Phase 0 and reported separately later.

### Replication (contingent): Virtual Cell Challenge 2026

Arc Institute profiled CRISPRi knockdowns in six cancer cell lines (10x Flex). Final submissions close 5 November 2026 and results are due late November. If Arc releases the measurements afterwards, they give a second, post-cutoff dataset across six contexts. No release has been announced.

### Splits

- **Phase 0:** combined-donor differential-expression results, used as provisional truth.
- **Phase 1 onward:** donors 1–2 are visible to the agent; donors 3–4 are truth and never enter an agent workspace. Agents receive pseudobulk effect matrices per donor and condition (log fold change, standard error, cells per perturbation) and a subsample of control cells, not raw single-cell data, so difficulty comes from inference rather than file handling. Gene programs used in questions are derived from donors 1–2 only.

## Entities

**QC exclusions:** cis neighbour knockdown, distal off-target, low target expression, too few cells per donor, and (Phase 1) an effect that does not replicate between donors 1 and 2.

**Literature density:**
- *Primary:* fractional PubMed count from gene2pubmed. Each paper contributes 1/k to each of the k human genes it links; papers linking more than 100 genes (screens, atlases) are dropped; only papers entered before the earliest evaluated model's training cutoff are counted (PMID cutoff, docs/DATA.md). Counted by Entrez GeneID so renamed genes keep their history.
- *Context-specific (Phase 1):* the same count restricted to T-cell papers (MeSH).
- *Empirical:* each model's own no-data score per gene.

**Bins:** quintiles of log density over QC-passing genes (0 = least studied); genes with no papers fall in the lowest quintile, and tied genes share a bin. A separate zero-paper bin (`density.zero_bin`, D-007) is implemented but off (D-010). Ties can merge bins; the feasibility report flags this, and the binning rule is fixed in the pre-registration.

**Matching (Phase 1):** within each bin, match genes on cross-donor reliability, effect size, knockdown efficiency and baseline expression. Without matching, a falling curve could mean "noisier data" rather than "less known".

## Question families

All answers are probabilities over pre-defined outcomes. Truth comes from held-out donors (Phase 1+). Each gene is assigned one family at random within its density bin.

1. **F1 Direct effect.** The gene's knockdown is visible in all conditions. "In 48 h-stimulated cells, does knocking down G raise, lower or not change program P?" A script computing the same statistic on donors 1–2 is near-optimal, so F1 is a control: it checks the agent can read the data and measures **prior override** (answers that contradict the agent's own data in favour of what it "knows"). Phase 0 uses a single-readout version of F1.
2. **F2 Signature neighbours.** "Which of these four genes has the knockdown signature most similar to G's?" For well-studied genes the options include known biological partners, so priors can help or mislead. Keep only questions with a clear margin in held-out donors.
3. **F3 Context shift.** G's 48 h data is removed for all donors; the agent sees rest and 8 h. "At 48 h, is G's effect on P the same sign, reversed or absent?"
4. **F4 Unseen perturbation.** G's knockdown is removed entirely. The agent still has G as a readout under other perturbations, its co-expression in control cells, and everything else. "Will knocking G down change P at 48 h?" Hardest and most prior-dependent.

## Conditions

- **Prior only:** gene name and question; no data, no tools. One call per question; run on every QC-passing gene.
- **Data, named.**
- **Data, anonymized:** G's symbol is replaced by a random token everywhere, including its own readout column (so on-target knockdown can still be checked); guide coordinates are stripped. After answers are locked, the agent is asked to guess G's identity (top 3). Hit rate is reported by bin; correctly identified runs are analysed separately.

All conditions: no internet, the same neutral harness for every model, fixed budget, task workspaces outside this repository. This also removes the model/harness confound from planted-fault-bench.

## Truth, baselines and scoring

**Truth:** computed under at least three reasonable pipelines (e.g. mean z-scored pseudobulk, a DESeq2-style model, limma-voom); questions where pipelines disagree are dropped.

**Baselines:**
- *Scripted pipeline per family:* F1/F2 compute the same statistic on donors 1–2, calibrated on a separate set of genes; F3 assumes 48 h looks like 8 h; F4 is a linear prediction from the knockdown profiles of G's co-expression neighbours.
- *Donor ceiling:* how well donors 1–2 predict donors 3–4 when G's data is fully visible.

**Metrics:** multi-class Brier skill relative to a reference forecast (log score secondary), top-label calibration error per bin. Bootstrap CIs resample genes within bins.

**Estimands:**
- *Data-attributable skill* = named − prior-only.
- *Prior reliance* = named − anonymized.

**Analysis model (pre-registered):** mixed effects, skill ~ log density × condition × family + matching covariates + (1 | gene) + (1 | template).

**Main figure:** skill against log density, one line per condition, per family, with the scripted baseline and donor ceiling as references.

## Phases

- **Phase 0 — prior-only probe (implemented).** F1 single-readout questions, provisional combined-donor truth, all models, no data. Go/no-go: if prior-only skill does not fall with density, the axis does nothing and the design stops.
- **Phase 1 — pilot.** 40 genes (8 per quintile, 10 per family) × 2 data conditions × 2 models × k = 1. Builds donor-split pseudobulk, programs, F2–F4 generators, anonymizer and leakage probe, multi-pipeline truth, baselines and the neutral harness.
- **Phase 2 — full batch.** Size set from pilot variance and cost per run; k ≥ 3 on a subset. If budget is tight, keep F3–F4 plus a small F1 control.
- **Phase 3 — replication** on the Virtual Cell Challenge 2026 data, if released.

## Draft predictions (to be set by the authors before each batch)

1. Prior-only skill rises with log density; the bottom bin is near zero. **Stop rule** if this fails.
2. Anonymized skill does not depend on density once genes are matched; correct identity guesses are rare in the bottom three bins.
3. The named − anonymized gap is positive in the top bin and near zero in the bottom.
4. On F4, agents do no better than the linear baseline in the bottom bin.
5. Prior override on F1 rises with density.
6. Overconfidence is highest in the bottom bin with names shown.

## Threats to validity

1. **Density correlates with data quality** → matching, the anonymized condition, reliability covariates.
2. **Density measurement** → screen papers dropped, fractional counting, Entrez IDs; PMID cutoff is approximate.
3. **Truth depends on the pipeline** → multi-pipeline agreement.
4. **Preprint contamination** → flagged genes excluded or reported separately.
5. **Deanonymization** → identity-guess probe; report by bin.
6. **CRISPRi specifics** (knockdown ≠ knockout, cis effects, variable efficiency) → QC flags, on-target checks.
7. **Label balance** → Phase 0 tells models the answers are roughly equally common, so skill reflects discrimination; consistent across bins.
8. **Model/harness confound** → one neutral harness; CLI backends are acceptable only for Phase 0 and are labelled as such.
9. **An evaluated model also helps build the benchmark** → humans set thresholds and interpret results for that model's family.

## Timeline (target: NeurIPS 2027 Evaluations & Datasets track; 2026 deadline was 6 May)

- **By mid-November 2026:** data, density, QC, feasibility report, Phase 0 probe; go/no-go.
- **Late November–December:** Phase 1 infrastructure and pilot.
- **January 2027:** commit predictions; full batch.
- **February–March:** runs; k ≥ 3 on a subset; replication if data is available.
- **April–May:** analysis and writing.

## Open decisions

- Binning rule when ties collapse bins.
- Final model list and backends (API keys vs. CLI sign-ins).
- Program definitions for F1/F3/F4 (data-derived on donors 1–2).
- Matching method and covariates.
- Whether F2 stays in the full batch.
- Compute and API budget.
