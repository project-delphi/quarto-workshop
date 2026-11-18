# Acme Signals: model evaluation (worked example)

Acme Signals is a fictional two-person machine-learning company. Its model ranks a bank's
marketing contacts by how likely each is to subscribe to a term deposit, so that a call
centre calls the likeliest first. This project evaluates three fictional releases of the
model (v1 to v3, `releases.yml`) on real public data, the UCI Bank Marketing dataset
(`data/README.md`), and publishes the results as a small website: an evaluation report, a
model card and a slide deck, each also as Word or PowerPoint and PDF, in one brand.

This folder is the finished project so far: the state of `checkpoints/17-eval-site/`
with this README. It starts from `starters/eval-repo/`, the repository as a team would have
it before Quarto. A white paper and a parameterised update are planned for later chapters
and are not here yet.

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
| `references.bib` | Sources cited by both documents |
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
```

`uv run quarto render` writes every page and format into `_site/`: `index.html`,
`about.html`, `report.html`, `.docx` and `.pdf`, `model-card.html`, `.docx` and `.pdf`,
`slides.html` and `slides.pptx`, plus `search.json` for the site's search. After it,
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
  the three documents with the `description` each one declares, so a description is written
  once and serves the listing, search results and link previews.
- **The site checks itself.** `scripts/check_site.py` reads every rendered page and fails
  on an image without alt text, a page without `lang`, title or description, or a heading
  that skips a level, and on brand colours with too little contrast. Quarto's Reveal.js
  template writes no description tag, so `filters/description-meta.lua` adds the deck's.
