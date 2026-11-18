# Acme Signals model evaluation: project rules

## Scope

Evaluate the releases of the contact-ranking model in `releases.yml` on the UCI Bank
Marketing data (`data/bank-full.csv`, documented in `data/README.md`) and publish the results
as documents. Acme Signals is a fictional company: say so wherever it is named. The bank data
are real; `data/synthetic_business.csv` is SYNTHETIC and must be labelled so wherever it is used.

## Rules

- `data/` is read-only. Never edit, re-save or replace a file in it.
- Results are computed once, by `scripts/evaluate.py`, into `outputs/`. Documents read
  `outputs/` and never fit a model.
- Every number in a document comes from `outputs/` through code (inline `{python}` or a
  cell). Never type a number by hand.
- A sentence whose wording depends on the results (best, higher, lower, most) gets a guard
  from `acme_eval.claims.claim` in the cell before it, so the render stops if it becomes false.
- `duration` is known only after the call: no model may use it.
- `outputs/`, `.venv/` and rendered files (`*.html`, `*.docx`, `*.pdf`, `*_files/`) are never
  committed.

## Commands

The Python environment is `pyproject.toml` and `uv.lock`. Run `python`, `pytest` and
`quarto` through `uv run`, which builds `.venv/` on first use:

- `uv run python scripts/evaluate.py` (writes `outputs/`)
- `uv run pytest -q`
- `uv run quarto render report.qmd` (html, docx and pdf)
