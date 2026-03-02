# AI Evaluation Harness (Lightweight, Reproducible)

A small, production‑minded evaluation harness you can use to assess rule/LLM outputs against a gold test set. Designed for **Solution Architects with applied AI responsibilities**.

## What it does
- Loads a CSV **test set** (inputs + expected labels)
- Calls a **model client** (LLM or rule‑based; easily swappable)
- Produces **metrics** (accuracy, precision, recall, F1) and a **confusion matrix**
- Writes an **evaluation report** (CSV + JSON) suitable for tickets/UAT

> No external services required by default. The included `ModelClient` is a mock to keep everything offline and PHI‑free. Swap it with a real API call when ready.

## Quickstart
```bash
# From repo root (no PHI in test data)
python src/run_eval.py \
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
