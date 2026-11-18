# Checkpoint 15 · Model card and results

Checkpoint 14 plus `model-card.qmd` (html, docx and Typst PDF), which follows the sections of
Mitchell et al. (2019), *Model Cards for Model Reporting*, and `references.bib`. The card
describes the best release: details, intended and out-of-scope uses, factors (age band and
`job`), metrics with intervals, evaluation and training data, slice tables from
`outputs/segments.csv`, a calibration figure, ethical considerations and caveats.
`report.qmd` gains numbered sections, a "Who is called" section with recall by age band,
a calibration section and figure, and citations. Each sentence whose wording depends on
the results has a guard (`acme_eval.claims.claim`). Acme Signals is a fictional company; the
bank data are real (`data/README.md`).

Sources and data only: no `outputs/` and no rendered files. `uv run` builds `.venv/` from
`uv.lock` on first use.

## Catch up

Ask your coding agent, started in `acme-eval/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/15-eval-results/README.md
```

The steps, run inside `acme-eval/` (by the agent, or by you in a terminal):

1. Keep your work, all but the `.venv/` environment (`uv run` rebuilds it from `uv.lock`): `b="../acme-eval-backup-15-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"` (a new time-stamped copy beside `acme-eval/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/15-eval-results/. .`
3. Compute and test: `uv run python scripts/evaluate.py && uv run pytest -q` (about 20 seconds; every test passes).
4. Render, one file at a time: `uv run quarto render report.qmd && uv run quarto render model-card.qmd`.
5. Check: `model-card.html` has nine numbered sections, two slice tables (age band and job), the calibration figure and a References list with Mitchell et al. (2019); `report.html` has Tables 1 and 2 and Figures 1 and 2; each document also has a `.docx` and a `.pdf`.
6. Rejoin: your folder now holds the end of these steps. Continue at the box in Chapter 3.
