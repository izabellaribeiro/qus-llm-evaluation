# Beyond Accuracy — Evaluating LLM User-Story Quality Assessments

This repository evaluates LLM user-story quality assessments against the final human reference for **all 13 QUS criteria**, using one shared metric implementation. It includes model outputs, qualitative ratings, and reproducible analyses for RQ1–RQ4.

## How to run

Use Python 3.13. From this directory, on Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m scripts.reproduce --output-root replication_runs/check
.\.venv\Scripts\python.exe -m scripts.verify_package --reproduced-root replication_runs/check
```

On Linux/macOS, create the environment with `python3.13 -m venv .venv` and use `.venv/bin/python` in the remaining commands.

Execution reads saved outputs; it makes **no model API calls** and needs no credentials. Results go into `replication_runs/check/`. The `results/` directory contains the corresponding reference exports. Undefined metrics remain undefined. The environment manifest records the installed dependency versions.

## Contents

| Path | Purpose |
|---|---|
| `config/` | Collection configuration and criterion definitions |
| `data/ground_truth/gold_standard_qus13_final.csv` | Authoritative final binary reference |
| `data/raw/`, `data/processed/` | Source backlogs, execution datasets, story-ID maps |
| `data/qualitative_sample/` | Final coding workbook, codebook, original selection provenance and candidate source matches |
| `prompts/` | Executed prompts and demonstrations |
| `outputs/` | Frozen raw responses, parsed outputs, normalized predictions |
| `scripts/` | Collection utilities and RQ1–RQ4 analyses |
| `results/` | Final analysis exports |
| `vendor/aqusa-core/` | Baseline implementation and its license |
| `manifest.json` | File integrity hashes |

The final reference has **2,366 story–criterion pairs: 385 Violation and 1,981 No Violation**. There are 182 stories, three models, three prompts, five runs, and 106,470 saved LLM predictions. The decision column is authoritative; annotation notes retain their original context. Independent uses the implementation-prerequisite definition: a violation occurs when another story must be implemented first.

## Analysis and interpretation

- RQ1: precision, recall, F1, MCC, specificity, balanced accuracy and accuracy by model, prompt, project, dimension and criterion. Model summaries average five-run configuration means across prompts.
- RQ2: descriptive prompt summaries and existing Friedman/Wilcoxon diagnostics. Repeated runs and story–criterion pairs are not independent population samples; nominal p-values do not establish population-level superiority.
- RQ3: run stability, majority voting, ordinal confidence versus correctness, and unanimous incorrect units with High confidence in all five runs. Confidence is not probability calibration.
- RQ4: the 30-case sample was selected manually for approximately balanced original TP/TN/FP/FN coverage and diversity across models, prompts, criteria and projects. It is exploratory; no random seed was used. Original selection quadrants and ambiguous run matches are preserved as provenance. Current quadrants use the final reference.

Reported rater agreement is calculated from the final ratings of the two evaluators.

Expected results include **1,542 persistent High-confidence incorrect units**. Final RQ4 counts are RC0/RC1/RC2 = **6/10/14** and ES0/ES1/ES2 = **3/9/18**. Model-only outputs have not been changed or re-executed to obtain these results.

## Notes

The optional collection utilities under `scripts/execution/` require provider credentials for new model runs. They are not invoked by `scripts.reproduce`. AQUSA re-execution additionally requires the NLTK resources installed by `scripts/setup_aqusa_nltk.py`. Original baseline licensing is preserved under `vendor/`.
