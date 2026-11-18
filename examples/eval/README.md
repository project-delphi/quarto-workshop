# Acme Signals: model evaluation (worked example)

Acme Signals is a fictional two-person machine-learning company. Its model ranks a bank's
marketing contacts by how likely each is to subscribe to a term deposit, so that a call
centre calls the likeliest first. This project evaluates three fictional releases of the
model (v1 to v3, `releases.yml`) on real public data, the UCI Bank Marketing dataset
(`data/README.md`), and publishes the results as an evaluation report and a model card.

This folder is the finished project so far: the state of `checkpoints/15-eval-results/`
with this README. It starts from `starters/eval-repo/`, the repository as a team would have
it before Quarto. Slides, a website, a white paper and a parameterised update are planned
for later chapters and are not here yet.

## Layout

| Path | What it holds |
|---|---|
| `AGENTS.md` | The project's rules for a coding agent |
| `data/` | `bank-full.csv` (real, unchanged, CC BY 4.0), `synthetic_business.csv` (SYNTHETIC), `README.md` |
| `releases.yml` | The three fictional releases and their months |
| `src/acme_eval/` | `data.py` (loading, checks, split, age bands), `models.py` (one pipeline per release), `metrics.py` (metrics, bootstrap intervals, calibration, slices), `claims.py` (guards) |
| `scripts/evaluate.py` | Fits every release once and writes `outputs/` |
| `scripts/make_synthetic_business.py` | Writes the synthetic business figures (fixed seed) |
| `tests/` | pytest: checksum and shape, no `duration`, metric definitions, output schema |
| `notebooks/explore.ipynb` | The team's first exploration, saved without outputs |
| `report.qmd` | Evaluation report: html, docx and Typst PDF |
| `model-card.qmd` | Model card for the best release: html, docx and Typst PDF |
| `references.bib` | Sources cited by both documents |

## Rebuild

From this folder, with [uv](https://docs.astral.sh/uv/) and Quarto installed:

```bash
uv run python scripts/evaluate.py      # writes outputs/ (about 20 s)
uv run pytest -q                       # every test passes
uv run quarto render report.qmd        # report.html, report.docx, report.pdf
uv run quarto render model-card.qmd    # model-card.html, .docx, .pdf
```

`outputs/` and the rendered files are not committed. If a user-level Jupyter kernel
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
