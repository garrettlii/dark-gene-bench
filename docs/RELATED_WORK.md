# Related work

## Reproduction and verification of fresh papers

- **RECLAIM** (arXiv 2609.28850, Sept 2026). 100 NeurIPS 2025 papers in Run / Retrain / Reimplement tiers with fixed targets and GPU budgets, graded from logs; designed to be rebuilt yearly. Best agent: 41% / 27% / 15%. Most common error: not checking against the paper's numbers. https://arxiv.org/abs/2609.28850
- **ICML 2026 Open Reproductions** (Hugging Face and alphaXiv, July–Aug 2026). Community agents reproduced 2,226 ICML 2026 papers claim by claim; an LLM judge issued per-claim verdicts; 23% of examined papers had at least one falsified or contested claim, and 242 papers drew opposite verdicts from independent teams. https://huggingface.co/blog/icml-2026-open-reproductions

## Separating analysis from prior knowledge

- **BioStudyBench** (arXiv 2610.07614, Oct 2026). 25 long-horizon tasks from biomedical studies first published July–September 2026; each run with and without data and tools. Data access adds 47 points on average; best closed model passes 94.7%. Closest prior work; it fixes the date split but does not vary literature density. https://arxiv.org/abs/2610.07614
- **SciHorizon-Gene** (arXiv 2601.12805). Large gene-centric knowledge benchmark; performance falls for genes with low research attention. Tests recall, not analysis of data. https://arxiv.org/abs/2601.12805

## Agentic science benchmarks (recent)

- **Autonomous Science Bench** (arXiv 2610.18449, Oct 2026). Budgeted design-build-test-learn campaigns against a lab service, with discovery and held-out-ranking gates. https://arxiv.org/abs/2610.18449
- **Into the Unknown** (arXiv 2610.19159, Oct 2026). Agents write follow-up papers on unpublished directions from national-lab scientists; rubric grading; none of 135 submissions met all conditions. https://arxiv.org/abs/2610.19159
- **BixBench3** (arXiv 2608.25286). Reconstructing published computational-biology analyses; agents score worse on larger raw datasets. https://arxiv.org/abs/2608.25286
- **GeneBench / GeneBench-Pro** (bioRxiv 2026.04.22.720113; OpenAI). Multi-stage genomics inference problems; Pro uses fully simulated data-generating processes.

## Perturbation biology

- **Zhu et al. 2026, *Cell*.** Genome-scale CRISPRi Perturb-seq in primary human CD4+ T cells; primary dataset. DOI 10.1016/j.cell.2026.08.002
- **Virtual Cell Challenge 2026** (Arc Institute). Zero-shot prediction of knockdown responses in unseen cell lines. https://virtualcellchallenge.org/
- **Replogle et al. 2022.** Genome-scale Perturb-seq in K562 and RPE1. https://gwps.wi.mit.edu/
- **Nadig et al. (TRADE).** Transcriptome-wide impact of perturbations; Jurkat and HepG2 essential screens. https://pmc.ncbi.nlm.nih.gov/articles/PMC11244993/

## To verify before citing (from memory)

- Ahlmann-Eltze, Huber & Anders (2025), *Nature Methods*: deep-learning perturbation-effect predictors did not outperform simple linear baselines.
- Stoeger, Gerlach, Morimoto & Amaral (2018), *PLoS Biology*: a small set of biological features predicts which genes get studied.
- Tanzer et al. (2024), MTOB: translating Kalamang from a single grammar book.
- Kandpal et al. (2023): LLMs struggle with long-tail knowledge.
