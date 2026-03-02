# AI Evaluation Harness (Lightweight, Reproducible)

A small, production‑minded evaluation harness you can use to assess rule/LLM outputs against a gold test set. Designed for **Solution Architects with applied AI responsibilities**.

## What it does
- Loads a CSV **test set** (inputs + expected labels)
- Calls a **model client** (LLM or rule‑based; easily swappable)
- Produces **metrics** (accuracy, precision, recall, F1) and a **confusion matrix**
- Writes an **evaluation report** (CSV + JSON) suitable for tickets/UAT

> No external services required by default. The included `ModelClient` is a mock to keep everything offline and PHI‑free. Swap it with a real API call when ready.

## Quickstart

From repo root (no PHI in test data):

```bash
python -m src.run_eval \
  --test-cases data/test_cases.csv \
  --gold data/gold.csv \
  --out-dir out

## Sample Output

Running:

```bash
python -m src.run_eval --test-cases data/test_cases.csv --gold data/gold.csv --out-dir out

{
  "accuracy": 0.8,
  "per_label": {
    "IGNORE": {"precision": 1.0, "recall": 1.0, "f1": 1.0},
    "POST": {"precision": 1.0, "recall": 0.5, "f1": 0.66},
    "REVIEW": { "precision": 1.0, "recall": 1.0, "f1": 1.0 }
  }
}

## Interpreting Metrics

- **Accuracy**: % of all cases where predicted label == expected (`gold`) label.
- **Precision (per label)**: Of what the model predicted as this label, how many were actually correct.
- **Recall (per label)**: Of all cases that *should* be this label, how many the model found.
- **F1**: Harmonic mean of precision and recall (balances the two).

### Scenario Slices
The harness also reports metrics by `scenario` (e.g., `supply_present`, `post_required`, `ambiguous`) in `metrics.json` → `by_scenario`. This helps isolate false positives/negatives to specific conditions and write targeted acceptance criteria.

### How I use this in UAT / tickets
1) Run the harness on a fixed test set.
2) If **accuracy < target** or a label’s **F1** is low, open a defect with:
   - failing `case_id`s from `out/evaluation_report.csv`
   - the per‑label metrics from `out/metrics.json`
3) Re-run after fixes and attach the updated artifacts.

### Defect Export
If any cases fail, the harness writes `out/jira_defects.csv` with the minimal fields needed to open a defect (case_id, scenario, expected vs predicted, input_text). Attach this file to tickets for faster triage.
