# Acme Signals: model evaluation (worked example)

Acme Signals is a fictional two-person machine-learning company. Its model ranks a bank's
marketing contacts by how likely each is to subscribe to a term deposit, so that a call
centre calls the likeliest first. This project evaluates three fictional releases of the
model (v1 to v3, `releases.yml`) on real public data, the UCI Bank Marketing dataset
(`data/README.md`), and publishes the results as a small website: an evaluation report, a
model card, a technical white paper and a slide deck, each also as Word or PowerPoint and
PDF, in one brand.

This folder is the finished project so far: the state of `checkpoints/18-eval-whitepaper/`
with this README. It starts from `starters/eval-repo/`, the repository as a team would have
it before Quarto. A parameterised update is planned for a later chapter and is not here yet.

## Layout

| Path | What it holds |
|---|---|
| `AGENTS.md` | The project's rules for a coding agent |
| `data/` | `bank-full.csv` (real, unchanged, CC BY 4.0), `synthetic_business.csv` (SYNTHETIC), `README.md` |
| `releases.yml` | The three fictional releases and their months |
| `src/acme_eval/` | `data.py` (loading, checks, split, age bands), `models.py` (one pipeline per release), `metrics.py` (metrics, bootstrap intervals, calibration, slices), `claims.py` (guards), `brand.py` (brand colours and WCAG contrast) |
| `scripts/evaluate.py` | Fits every release once and writes `outputs/` |
| `scripts/make_synthetic_business.py` | Writes the synthetic business figures (fixed seed) |
| `tests/` | pytest: checksum and shape, no `duration`, metric definitions, output schema, brand contrast |
| `notebooks/explore.ipynb` | The team's first exploration, saved without outputs |
| `_quarto.yml` | The website: pages, navbar, footer, social cards, post-render step |
| `index.qmd` | Home page: the headline result, then a table of the documents |
| `about.qmd` | About the fictional company (`about` template `trestles`) |
| `report.qmd` | Evaluation report: html, docx and Typst PDF |
| `model-card.qmd` | Model card for the best release: html, docx and Typst PDF |
| `whitepaper.qmd` | Technical white paper for clients and investors: html, docx and a Typst PDF in the house template |
| `references.bib` | Sources the documents cite, each checked against its DOI record |
| `csl/apa.csl` | The APA 7th edition citation style, from the official CSL repository (CC BY-SA 3.0) |
| `templates/whitepaper/typst-show.typ` | The white paper's house template for Typst: title block, running header, footer |
| `scripts/check_refs.py` | Checks every DOI in `references.bib` against Crossref or DataCite (needs the network) |
| `slides.qmd` | Eight-slide deck for the product team and investors: Reveal.js and PowerPoint |
| `_brand.yml` | Acme's brand: palette and colour roles, system fonts, logo |
| `brand/logo.svg` | The logo, drawn for this fictional company |
| `acme.scss` | What the brand cannot say for the Reveal.js deck: muted text, title sizes, layout |
| `filters/title-notes.lua` | Puts the title slide's speaker notes on the Reveal.js title slide |
| `filters/description-meta.lua` | Gives the deck the `<meta name="description">` HTML pages get |
| `templates/acme-reference.docx`, `.pptx` | Word and PowerPoint templates in the brand's colours (made by `scripts/make_reference_docs.py`) |
| `scripts/pptx_alt_text.py` | Copies each figure's `fig-alt` into `_site/slides.pptx` (after every render) |
| `scripts/deck_pdf.py` | Prints `_site/slides.html` to `_site/slides.pdf` with headless Chrome and checks every page |
| `scripts/check_site.py` | Checks the rendered pages: alt text, language, title, description, heading levels, brand contrast |

## Rebuild

From this folder, with [uv](https://docs.astral.sh/uv/) and Quarto installed:

```bash
uv run python scripts/evaluate.py      # writes outputs/ (about 20 s)
uv run pytest -q                       # every test passes
uv run quarto render                   # the whole site into _site/ (about 40 s)
uv run python scripts/check_site.py    # every page passes
uv run python scripts/deck_pdf.py      # _site/slides.pdf, one page per slide, needs Chrome
uv run python scripts/check_refs.py    # every DOI in references.bib, before publishing; needs the network
```

`uv run quarto render` writes every page and format into `_site/`: `index.html`,
`about.html`, `report.html`, `.docx` and `.pdf`, `model-card.html`, `.docx` and `.pdf`,
`whitepaper.html`, `.docx` and `.pdf`, `slides.html` and `slides.pptx`, plus `search.json` for the site's search. After it,
`_quarto.yml` runs `scripts/pptx_alt_text.py`, which gives the PowerPoint figures their alt
text. One page renders alone with `uv run quarto render report.qmd` (into `_site/` too);
`uv run quarto preview` serves the site and re-renders a page when it is saved.

The templates in `templates/` are committed; after changing `_brand.yml`, remake them with
`uv run python scripts/make_reference_docs.py` (it needs Quarto on PATH).
`scripts/deck_pdf.py` finds Chrome from the `CHROME` environment variable, the macOS default
location, or `google-chrome`/`chromium` on PATH. Before publishing, set `site-url` in
`_quarto.yml` to the site's own address (it is a placeholder, `https://example.org/acme-eval/`):
the social cards' image links are made from it.

`outputs/`, `_site/` and the rendered files are not committed. If a user-level Jupyter kernel
shadows the project's environment, prefix the render with
`JUPYTER_PATH="$PWD/.venv/share/jupyter"`.

## Design decisions

- **`duration` is excluded.** It is the length of the call, known only once the call has
  ended and the outcome is known. The dataset's own documentation says it "should be
  discarded if the intention is to have a realistic predictive model" (`data/README.md`).
  `acme_eval.data.load()` drops it and `tests/test_models.py` checks that no release uses it.
- **Top-10% recall is the business metric.** The call centre calls the top 10% of the
  ranked list (`acme_eval.metrics.TOP_SHARE`), so what matters is the share of all
  subscribers those calls reach. ROC AUC summarises the whole ranking and picks the "best"
  release; the Brier score and the calibration table check the probabilities; lift compares
  the called list with calling at random.
- **Results are computed once.** `scripts/evaluate.py` is the only code that fits a model.
  It writes plain CSV and JSON to `outputs/`, deterministically (rerunning it gives the same
  bytes), and every document reads those files. A number in a document is therefore the
  number in `outputs/`, and the documents render in seconds.
- **Guards protect wording.** Inline code keeps numbers right, but not words such as "best"
  or "smallest". Each such sentence has a `claim(condition, sentence)` before it; if new
  results make it false, the render stops with that sentence.
- **Intervals are paired bootstraps.** 1,000 resamples of the test set
  (`metrics.N_BOOTSTRAP`, seed `metrics.BOOTSTRAP_SEED`), the same resamples for every
  release, give 95% percentile intervals. They reflect test-set sampling only.
- **Fixed settings.** One stratified split, 25% test, seed 2026 (`data.TEST_SIZE`,
  `data.SPLIT_SEED`); `random_state` 2026 for every model (`models.MODEL_SEED`); age bands
  18-29, 30-39, 40-49, 50-59 and 60+ (`data.AGE_EDGES`); ten equal-count calibration bins.
  `outputs/summary.json` records them with the data checksum and package versions.
- **The deck states one claim per slide.** Each title is the claim, with its number
  computed and its wording guarded, so the deck can be re-rendered for the next release
  without rewriting it; the detail is in the speaker notes and the last slide is the decision.
  Figures are static images because PowerPoint cannot run JavaScript.
  Reveal.js has no PDF export in Quarto, so `scripts/deck_pdf.py` prints the deck's print view
  with headless Chrome and retries when a page comes out blank.
- **One brand file.** `_brand.yml` holds Acme's colours (a palette and the roles
  `background`, `foreground`, `primary`, `secondary`), fonts and logo. Quarto applies it to
  the web pages (Bootstrap), the Reveal.js deck and the Typst PDFs (page colour, text and
  heading colours, fonts, the logo at the top of each page), so a colour changes in one
  place. It does not reach Word or PowerPoint, so `scripts/make_reference_docs.py` reads the
  same colours from it into their reference documents. `acme.scss` keeps only the deck's
  muted text, title sizes and layout rules, in `$brand-*` colours; the theme lists `brand`
  last, because Quarto puts a later theme's variables first and `$brand-slate` must exist
  before `acme.scss` uses it.
- **System fonts.** Helvetica, then Arial: nothing is downloaded when a page opens. Typst
  warns about a listed font the machine lacks, so the list leaves out the generic
  `sans-serif`, which Typst never knows; on a machine without Helvetica, Typst warns once
  and uses Arial. Office gets Arial, the last named font.
- **Contrast is tested.** `tests/test_deck_contrast.py` checks that every text colour in the
  brand, and the deck's muted text, has WCAG contrast of at least 4.5:1 on the background,
  and that `acme.scss` sets no colour of its own.
- **The home page states the result.** Its first sentence is the headline, computed from
  `outputs/` and guarded like the report's. Below it, a Quarto listing of type `table` lists
  the four documents with the `description` each one declares, so a description is written
  once and serves the listing, search results and link previews.
- **The site checks itself.** `scripts/check_site.py` reads every rendered page and fails
  on an image without alt text, a page without `lang`, title or description, or a heading
  that skips a level, and on brand colours with too little contrast. Quarto's Reveal.js
  template writes no description tag, so `filters/description-meta.lua` adds the deck's.
- **The white paper is short and cited.** `whitepaper.qmd` is for clients and investors:
  three to five A4 pages with an abstract, numbered sections (Introduction, Data, Method,
  Results, Limitations, Conclusion), numbered equations, one table and two figures, each
  referred to in the text (`@eq-`, `@tbl-`, `@fig-`, `@sec-`). Its numbers and guarded
  wording follow the report's rules. The only typed numbers are the source's campaign dates
  and the definitions' constants (one half in the AUC, one over n in the Brier score).
- **The abstract is in the body.** Inline code in a YAML `abstract:` does run in Quarto
  1.10.20 (tried in html, docx and Typst), but the project keeps numbers out of YAML, as it
  does for `description`: metadata is read by tools that compute nothing, and a long YAML
  string is hard to review. The abstract is the first paragraph, wrapped for the PDF in two raw Typst blocks that call
  the house template's `whitepaper-abstract`; for html and docx an `## Abstract` heading
  (hidden in Typst) introduces it.
- **APA everywhere.** `csl: csl/apa.csl` styles the citations in html and docx (Pandoc's
  citeproc). In Typst, Quarto would hand citations to Typst's own processor, which prints its
  own "Bibliography" heading and title-cases titles; `citeproc: true` under `typst:` makes
  Pandoc format them, so all three formats cite alike. The style is
  <https://github.com/citation-style-language/styles/blob/3c6698d791a83016d699f50cbbea857f6ee3d2f8/apa.csl>
  (retrieved 2026-11-18, unchanged), licensed CC BY-SA 3.0 as its `<rights>` line says.
- **References are checked, and cited only for what was read.** `scripts/check_refs.py`
  asks doi.org which agency registered each DOI and compares the year, first author and title
  with Crossref's or DataCite's record. It needs the network, so it is a check before
  publishing, not part of the render. Each source is cited only for what its text or abstract,
  as opened, says. Brier (1950) was not cited: its DOI checks, but neither its publisher's
  page nor Crossref offered its text or abstract, so the Brier score is defined without it.
- **A house template for the PDF.** Quarto 1.10.20 lets a document replace any of its Typst
  template partials (`template-partials:`; the names are Quarto's, such as `typst-show.typ`
  and `typst-template.typ`). `templates/whitepaper/typst-show.typ` replaces the partial that
  applies the page style: it draws the title block (logo, a "Technical white paper" label,
  title, subtitle, company, date), a running header from page 2 and a "page n of N" footer,
  in `brand-color`, which Quarto defines from `_brand.yml` before the partial. Quarto's own
  `article` still sets the fonts and section numbers. `_brand.yml`'s `meta.name` does not
  reach Pandoc templates, so the company name is the document's `company` field.
- **Vector figures in the PDF.** `fig-format: svg` under `typst:` writes the figures as SVG,
  which Typst draws as vector paths; html and docx get PNG at `fig-dpi: 200`.
