# Acme Signals: model evaluation

Acme Signals is a fictional two-person machine-learning company. Its model ranks a bank's
marketing contacts by how likely each is to subscribe to a term deposit, so that a call
centre calls the likeliest first. This repository evaluates each released version of the
model on real public data, the UCI Bank Marketing dataset (`data/README.md`), and writes the
results to `outputs/`.

The company, its releases and `data/synthetic_business.csv` are invented for teaching; the
bank data are real.

## Run it

You need [uv](https://docs.astral.sh/uv/). It builds `.venv/` from `uv.lock` on first use.

```bash
uv run python scripts/evaluate.py   # fit v1-v3, write outputs/ (about 20 s)
uv run pytest -q                    # data, leakage, metrics and output checks
```

Run both from this folder: the code reads `data/` and `releases.yml` by relative path.
`tests/test_outputs.py` is skipped until `outputs/` exists.

To look at the exploratory notebook (`notebooks/explore.ipynb`, saved without outputs):

```bash
uv run --with jupyter jupyter lab notebooks/explore.ipynb
```

## What is where

| Path | What it holds |
|---|---|
| `releases.yml` | The three fictional releases: v1 (2026-03), v2 (2026-06), v3 (2026-09) |
| `src/acme_eval/data.py` | Loading with column and type checks, the split, age bands; drops `duration` |
| `src/acme_eval/models.py` | One scikit-learn pipeline per release |
| `src/acme_eval/metrics.py` | ROC AUC, average precision, Brier score, top-10% recall, precision and lift, calibration; bootstrap intervals |
| `scripts/evaluate.py` | Fits every release once and writes `outputs/` |
| `scripts/make_synthetic_business.py` | Writes the synthetic monthly business figures |
| `tests/` | pytest checks |
| `data/` | `bank-full.csv` (real, unchanged), `synthetic_business.csv` (SYNTHETIC), `README.md` |

## Outputs

`scripts/evaluate.py` writes five files, the same bytes on every run:

- `metrics.csv`: one row per version and metric, with a 95% bootstrap interval (`low`, `high`).
- `segments.csv`: metrics by age band and by `job`, with group sizes.
- `calibration.csv`: mean predicted probability and observed rate in ten equal-count bins.
- `curves.csv`: ROC and precision-recall points for plotting.
- `summary.json`: the best version by ROC AUC, the test-set size, the base rate, the split
  seed, the data checksum and the package versions.

`outputs/` is computed, so it is not committed: rerun the script to rebuild it.
