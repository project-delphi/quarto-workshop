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
- `outputs/`, `.venv/`, `_site/` and rendered files (`*.html`, `*.docx`, `*.pdf`, `*.pptx`,
  `*_files/`) are never committed; the reference documents in `templates/` are source files
  and are.

## Deck rules (`slides.qmd`)

- One claim per slide, and the slide's title states it. A number in a title is computed
  (inline `{python}`), and the title's wording gets a `claim` guard like any sentence.
- Detail goes in the speaker notes (`::: {.notes}`), on every slide; the slide keeps the claim
  and its evidence. The title slide's notes go before the first `##` heading.
- The last slide says what is decided.
- Figures are static matplotlib images with `fig-alt`, in the report's colour-blind-safe
  palette: PowerPoint cannot run JavaScript.
- Colours and fonts come from `_brand.yml` (see below); `acme.scss` keeps only what the brand
  cannot say for Reveal.js (muted text, title sizes, layout rules), using `$brand-*` colours
  and no colour of its own. The deck's theme lists `brand` last so those variables exist.
- The PowerPoint deck uses `templates/acme-reference.pptx` as its `reference-doc`, and
  `scripts/pptx_alt_text.py` (run after every render by `_quarto.yml`) gives its figures
  their alt text.

## Site and brand rules

- The folder is a Quarto website (`_quarto.yml`): `index.qmd`, `about.qmd`, the report, the
  model card and the deck, rendered together into `_site/`. Its `render` list is explicit;
  add a page there and to the navbar together.
- One `_brand.yml` drives the colours, fonts and logo of the web pages, the Reveal.js deck
  and the Typst PDFs. Change a brand colour or font there, never in a page or in
  `acme.scss`; code that needs one reads it with `acme_eval.brand` (the deck's figures take
  their ink and paper so). The figures' Okabe-Ito palette is not the brand's and stays in
  the documents.
- Word and PowerPoint ignore `_brand.yml`: they get the same colours and font through
  `templates/acme-reference.docx` and `.pptx`, made from `_brand.yml` by
  `uv run python scripts/make_reference_docs.py`. Rerun it after changing the brand; never
  edit the templates by hand.
- Every page has a `description` in its YAML (search results, link previews and the home
  page's table of documents use it). A description never contains a number: numbers are
  computed, and YAML cannot compute.
- The home page's first sentence states the headline result, computed and guarded.
- `brand/logo.svg` is a fictional company's logo, drawn for teaching. Every image has alt text.
- `tests/test_deck_contrast.py` checks the brand's text colours (WCAG contrast of at least
  4.5:1), and `scripts/check_site.py` must pass after every render: alt text, `lang`,
  title and description on every page, no skipped heading levels, and the brand's contrast.

## Commands

The Python environment is `pyproject.toml` and `uv.lock`. Run `python`, `pytest` and
`quarto` through `uv run`, which builds `.venv/` on first use:

- `uv run python scripts/evaluate.py` (writes `outputs/`)
- `uv run pytest -q`
- `uv run quarto render` (the whole site into `_site/`: every page, the report's and the
  card's docx and pdf, the deck's pptx with its alt text), then
  `uv run python scripts/check_site.py`
- `uv run quarto render report.qmd` (or any one page) renders that page alone, into `_site/`
- `uv run python scripts/deck_pdf.py` (`_site/slides.pdf`, checked page by page; needs Chrome)
- `uv run python scripts/make_reference_docs.py` (after changing `_brand.yml`)
