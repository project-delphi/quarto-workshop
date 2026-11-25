# Acme Signals: model evaluation (worked example)

Acme Signals is a fictional two-person machine-learning company. Its model ranks a bank's
marketing contacts by how likely each is to subscribe to a term deposit, so that a call
centre calls the likeliest first. This project evaluates three fictional releases of the
model (v1 to v3, `releases.yml`) on real public data, the UCI Bank Marketing dataset
(`data/README.md`), and publishes the results as a small website: an evaluation report, a
model card, a technical white paper and a slide deck, each also as Word or PowerPoint and
PDF, in one brand. Two parameterised documents, rendered once per value by a script, give a
monthly investor update and a one-page report per customer segment. GitHub Actions workflows rebuild
and check it on every pull request, publish the site from `main`, and render the reports
each month.

This folder is the finished project: the state of `checkpoints/20-eval-ci/` with this
README. It starts from `starters/eval-repo/`, the repository as a team would have it before
Quarto.

## Layout

| Path | What it holds |
|---|---|
| `AGENTS.md` | The project's rules for a coding agent |
| `data/` | `bank-full.csv` (real, unchanged, CC BY 4.0), `synthetic_business.csv` (SYNTHETIC), `README.md` |
| `releases.yml` | The three fictional releases and their months |
| `src/acme_eval/` | `data.py` (loading, checks, split, age bands), `models.py` (one pipeline per release), `metrics.py` (metrics, bootstrap intervals, calibration, slices), `claims.py` (guards), `brand.py` (brand colours and WCAG contrast), `params.py` (parameter checks, words chosen from numbers) |
| `scripts/evaluate.py` | Fits every release once and writes `outputs/` |
| `scripts/make_synthetic_business.py` | Writes the synthetic business figures (fixed seed) |
| `tests/` | pytest: checksum and shape, no `duration`, metric definitions, output schema, brand contrast, parameter checks |
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
| `scripts/deck_pdf.py` | Prints `_site/slides.html` to `_site/slides.pdf` in Chrome, driven by Playwright, and checks every page |
| `scripts/check_site.py` | Checks the rendered pages: alt text, language, title, description, heading levels, brand contrast |
| `update.qmd` | Monthly investor update, parameter `month` (default `"latest"`): the month's SYNTHETIC business figures and the release live that month, with its real metrics; html, docx and Typst PDF; not on the site |
| `segment.qmd` | One page per customer segment, parameters `factor` (`age_band` or `job`) and `segment` (default `60+`): the best release in that segment, real data; html, docx and Typst PDF; not on the site |
| `scripts/render_params.py` | Renders `update.qmd` for every month and `segment.qmd` for every age band into `reports/`, and checks each file contains its value |
| `.github/workflows/check.yml` | CI: on every pull request and push to `main`, computes `outputs/`, runs the tests, renders the site and checks it |
| `.github/workflows/publish.yml` | The same build on `main`, then deploys `_site/` to GitHub Pages |
| `.github/workflows/monthly.yml` | On the 2nd of each month: the build, every report as PDF (kept as an artifact), and the reference check |
| `.github/pull_request_template.md` | The three checks for reviewing a change, and a line on what an agent did not verify |

## Rebuild

From this folder, with [uv](https://docs.astral.sh/uv/) and Quarto installed:

```bash
uv run python scripts/evaluate.py      # writes outputs/ (about 20 s)
uv run pytest -q                       # every test passes
uv run quarto render                   # the whole site into _site/ (about 40 s)
uv run python scripts/check_site.py    # every page passes
uv run python scripts/deck_pdf.py      # _site/slides.pdf, one page per slide, needs Chrome
uv run python scripts/check_refs.py    # every DOI in references.bib, before publishing; needs the network
uv run python scripts/render_params.py # every month and age band into reports/, checked (about 5 min)
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

`scripts/render_params.py` writes `reports/update-2026-01.pdf`, `.docx` and `.html` to
`reports/update-2026-10.*` and `reports/segment-age-18-29.*` to `reports/segment-age-60plus.*`
(`2026-06 2026-10` renders those two months only; `--formats pdf` only PDFs). One month renders by
hand with `uv run quarto render update.qmd -P month:2026-06 -M output-file:update-2026-06`,
next to the source.

`outputs/`, `reports/`, `_site/` and the rendered files are not committed. If a user-level Jupyter kernel
shadows the project's environment, prefix the render with
`JUPYTER_PATH="$PWD/.venv/share/jupyter"`.

## CI and publishing

When this folder is its own GitHub repository, `.github/` holds three workflows that run the
Rebuild commands above on GitHub's machines (`ubuntu-24.04`, Quarto 1.10.20, uv 0.11.32),
from a fresh clone, so "it builds" means it builds there, not only on one laptop.

| Workflow | Runs on | Does | Results appear |
|---|---|---|---|
| `check.yml` (*Check*) | every pull request, every push to `main` | `evaluate.py`, `pytest`, `quarto render`, `check_site.py`; read-only | a green tick or red cross on the pull request and commit; the log under *Actions* |
| `publish.yml` (*Publish*) | every push to `main`, or *Run workflow* | the same build, then uploads `_site/` and deploys it to GitHub Pages | the site at `https://<owner>.github.io/<repository>/`, linked from the run's *deploy* job |
| `monthly.yml` (*Monthly reports*) | 06:17 UTC on the 2nd of each month (`cron: "17 6 2 * *"`), or *Run workflow* | the same build, `render_params.py --formats pdf`, then `check_refs.py` | the PDFs as an artifact, `reports-<run number>`, at the foot of the run's page (kept 90 days) |

A guard that the results no longer support (`ClaimError`) stops `quarto render`, so the
check fails and the pull request shows which sentence to fix; *Publish* runs the same steps,
so such a page is never published. Each run caches uv's downloads, keyed on `uv.lock`.

- **One-time setting.** Before the first *Publish*, on GitHub: Settings → Pages → Build and
  deployment → Source: **GitHub Actions**. It deploys without a `gh-pages` branch and without
  `quarto publish`. Set `site-url` in `_quarto.yml` to the Pages address at the same time.
- **Protect `main`.** Settings → Branches (or Rules): require a pull request and the *Check*
  job to pass before merging, so every change to `main` has been reviewed and rebuilt.
- **The schedule.** Cron reads UTC (unless a `timezone:` line names another) and runs on the default branch's latest commit; GitHub may
  start it late when busy, and turns schedules off in a public repository after 60 days with
  no activity (re-enable it under *Actions*). The reference check runs last and fails the run
  on a mismatch, after the reports are saved.
- **Pull requests.** `pull_request_template.md` fills each new pull request with the three
  checks (scope, correctness, rebuild) and asks which coding agent, if any, made the change
  and what it did not verify.

In this book's repository, `.github/` sits inside `examples/eval/`, where GitHub does not
read it: the workflows run only once the folder is a repository of its own.

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
  Reveal.js has no PDF export in Quarto, so `scripts/deck_pdf.py` opens the deck's print view in
  Chrome with Playwright, waits until it holds a page per slide, prints it, and retries when a
  page comes out blank.
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
- **Parameterised documents are rendered by a script, not by the site.** `update.qmd` and
  `segment.qmd` hold their parameters and defaults in a cell tagged `parameters`; Quarto
  passes `-P name:value` to Jupyter through papermill (a dependency for that alone), which
  adds a cell after it with the values. They are left out of `project.render`: the home page
  says every number on the site comes from the real bank data, which the update's synthetic
  business figures would make false, and a site page could show only one month. Quarto 1.10.20
  then renders each as a single file, writing next to the source (in `_site/` only if it were
  in `project.render`); `--output-dir` is refused for a single file and `--output` takes no
  folder, so `scripts/render_params.py` names each output by its value with
  `-M output-file:update-2026-10` (one run, one execution, every format) and moves it into
  `reports/`. The html is self-contained (`embed-resources`), so each file can be sent alone.
- **A parameter is checked before it is used.** `acme_eval.params` stops the render on a month
  or segment that is not in the data and lists the ones that are. Words that depend on the
  value (up or down, above or below, first, best so far) come from `params.direction` and
  `params.relation` on the numbers as printed, guarded by `claim`; sentences only some values
  need come from `output: asis` cells, and captions that name the value are computed.
- **Synthetic figures say so, every time.** The update opens with a "SYNTHETIC: invented for
  teaching" callout, marks each business number "(synthetic)", and starts its table caption
  with the label; its model figures are said to be real. `render_params.py` fails an update
  whose text lacks "SYNTHETIC".
