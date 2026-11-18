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
- `outputs/`, `reports/`, `.venv/`, `_site/` and rendered files (`*.html`, `*.docx`, `*.pdf`, `*.pptx`,
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
  model card, the white paper and the deck, rendered together into `_site/`. Its `render` list is explicit;
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

## White paper rules (`whitepaper.qmd`)

- Every reference in `references.bib` is verified before a release: run
  `uv run python scripts/check_refs.py` (it needs the network) and fix every mismatch. An
  entry without a DOI is checked by hand at its URL; record the date in the file's comment.
- Cite a source only for what you have read in it (its text, or at least its abstract). If a
  source cannot be opened, do not cite it; never add a reference from memory.
- Every figure, table and equation has a label (`fig-`, `tbl-`, `eq-`) and is referred to in
  the text (`@fig-roc`); sections are referred to as `@sec-`. A rendered "??" or "?@" is a
  broken reference.
- Citations use `csl: csl/apa.csl` in every format; for Typst that needs `citeproc: true`
  under `typst:`, or Typst formats them itself in another style. Keep the style file as
  downloaded, with its licence line.
- The PDF uses the house template, `templates/whitepaper/typst-show.typ`, named under
  `template-partials`. Change the look there, in `brand-color` roles, not in the document.
- No inline code in YAML (`abstract`, `description`, `title`): the abstract is the body's
  first paragraph, between the two raw Typst blocks that open and close `whitepaper-abstract`.
- Figures in the PDF are vector (`fig-format: svg` under `typst:`).

## Parameter rules (`update.qmd`, `segment.qmd`)

- A parameterised document keeps its parameters and their defaults in one cell tagged
  `parameters` (`#| tags: [parameters]`), the first cell after the YAML. Each default must
  render on its own (`month = "latest"` means the last month in the data), so a plain
  `uv run quarto render update.qmd` works.
- Check every value before using it, with `acme_eval.params`: a month or segment that is not
  in the data stops the render with a message that lists the values that are.
- Name every output by its parameters (`update-2026-10.pdf`, `segment-age-60plus.pdf`), with
  `-M output-file:<name>` (each format adds its extension) or `--output <name>.<ext>`, so one
  value never overwrites another's file. `scripts/render_params.py` renders every value into
  `reports/` and checks that each file contains its value; run it after changing either one.
- Every wording that depends on the value (up or down, above or below, first, best so far,
  new this month) is chosen by code from the numbers as printed, and guarded with `claim`. A
  sentence that only some values need comes from an `output: asis` cell; a caption that names
  the value is computed (the last paragraph of a `::: {#tbl-…}` div, with inline code).
- Every number from `data/synthetic_business.csv` is labelled SYNTHETIC: the document opens
  with a "SYNTHETIC: invented for teaching" callout, each number in the text is marked
  "(synthetic)", and the table caption and column headings say so. Figures from `outputs/`
  are said to be real.
- `-P` and `--execute-params` need `papermill` (in `pyproject.toml`). Keep `echo: false`: it
  also hides the cell papermill injects with the values.
- The parameterised documents are not in `project.render` or the navbar: the site's home page
  says every number on it comes from the real bank data, and a site page could show only one
  value. Quarto therefore renders each as a single file, next to the source, not in `_site/`.
  `reports/` is never committed.

## Team rules (branches, pull requests, CI)

- Work on a branch, never on `main`: `git switch -c <short-name>` before the first edit.
  Never push to `main`, never force-push, and never merge a pull request: a person reviews
  and merges it.
- One coherent change per branch and pull request: a new section, a fix, a dependency
  update. Unrelated fixes you notice go in your report, not in this change.
- Never commit `outputs/`, `reports/`, `_site/`, `.venv/` or rendered files; CI computes them.
  Check `git status` before every commit: it lists only the files this change needs.
- Before saying a change is done, run the commands CI runs, in order, and say which passed:
  `uv run python scripts/evaluate.py`, `uv run pytest -q`, `uv run quarto render`,
  `uv run python scripts/check_site.py`. Never weaken a test, delete a `claim` guard or
  change its condition to make a step pass: report the failure instead.
- Report what you could not verify: a step you did not run (no network for
  `check_refs.py`, no Chrome for `deck_pdf.py`), a page you did not open, a number you did not
  check against `outputs/`. The pull request template has a line for it.
- CI is the source of truth for "it builds": `.github/workflows/check.yml` runs on every pull
  request from a fresh clone. A change is ready for review when that check is green, not when
  it builds on your machine. Change the workflows in `.github/workflows/` only when asked,
  and keep their commands the same as the ones listed here.

## Commands

The Python environment is `pyproject.toml` and `uv.lock`. Run `python`, `pytest` and
`quarto` through `uv run`, which builds `.venv/` on first use:

- `uv run python scripts/evaluate.py` (writes `outputs/`)
- `uv run pytest -q`
- `uv run quarto render` (the whole site into `_site/`: every page, the report's, the
  card's and the white paper's docx and pdf, the deck's pptx with its alt text), then
  `uv run python scripts/check_site.py`
- `uv run quarto render report.qmd` (or any one page) renders that page alone, into `_site/`
- `uv run python scripts/deck_pdf.py` (`_site/slides.pdf`, checked page by page; needs Chrome)
- `uv run python scripts/make_reference_docs.py` (after changing `_brand.yml`)
- `uv run python scripts/check_refs.py` (every DOI in `references.bib`; before a release)
- `uv run quarto render update.qmd -P month:2026-06 -M output-file:update-2026-06` (one month,
  html, docx and pdf, next to the source); `segment.qmd` takes `-P factor:job -P segment:retired`
- `uv run python scripts/render_params.py` (every month and age band into `reports/`, checked;
  `2026-06 2026-10` for those two months only, `--formats pdf` for PDFs only)
