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
- Cite sources from `references.bib` with `[@key]`; verify each entry at its DOI or URL.
- `outputs/`, `.venv/` and rendered files (`*.html`, `*.docx`, `*.pdf`, `*.pptx`, `*_files/`)
  are never committed; `templates/acme-reference.pptx` is a source file and is.

## Deck rules (`slides.qmd`)

- One claim per slide, and the slide's title states it. A number in a title is computed
  (inline `{python}`), and the title's wording gets a `claim` guard like any sentence.
- Detail goes in the speaker notes (`::: {.notes}`), on every slide; the slide keeps the claim
  and its evidence. The title slide's notes go before the first `##` heading.
- The last slide says what is decided.
- Figures are static matplotlib images with `fig-alt`, in the report's colour-blind-safe
  palette: PowerPoint cannot run JavaScript.
- Colours and fonts live in `acme.scss`; `tests/test_deck_contrast.py` checks that the body, heading, link and muted text colours have WCAG contrast of at least 4.5:1 on the background. Change a colour there and in
  `scripts/make_pptx_reference.py` together.
- The PowerPoint deck uses `templates/acme-reference.pptx` as its `reference-doc`. Remake it
  with `uv run python scripts/make_pptx_reference.py`; never edit it by hand.

## Commands

The Python environment is `pyproject.toml` and `uv.lock`. Run `python`, `pytest` and
`quarto` through `uv run`, which builds `.venv/` on first use:

- `uv run python scripts/evaluate.py` (writes `outputs/`)
- `uv run pytest -q`
- `uv run quarto render report.qmd` and `uv run quarto render model-card.qmd` (html, docx
  and pdf each)
- `uv run quarto render slides.qmd` (revealjs and pptx), then
  `uv run python scripts/pptx_alt_text.py` (alt text for the pptx figures) and
  `uv run python scripts/deck_pdf.py` (slides.pdf, checked page by page)
