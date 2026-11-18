# Checkpoint 14 · Evaluation report

The evaluation starter (`starters/eval-repo/`) after the fast path's steps: `AGENTS.md` with
the project's rules, the Quarto execution packages (`ipykernel`, `nbclient`, `nbformat`) added
to `pyproject.toml` and `uv.lock`, the guard helper `src/acme_eval/claims.py`, and
`report.qmd` (html, docx and Typst PDF). The report reads `outputs/` only: one sentence names
the best release and its ROC AUC with its interval, a cross-referenced table (`tbl-metrics`)
compares the three releases and a figure (`fig-roc`) shows their ROC curves. A guard stops
the render if the release the sentence names is not the best in `outputs/metrics.csv`. Acme Signals is a fictional company; the bank data are
real (`data/README.md`).

Sources and data only: no `outputs/` and no rendered files. `uv run` builds `.venv/` from
`uv.lock` on first use.

## Catch up

Ask your coding agent, started in `acme-eval/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/14-eval-start/README.md
```

The steps, run inside `acme-eval/` (by the agent, or by you in a terminal):

1. Keep your work, all but the `.venv/` environment (`uv run` rebuilds it from `uv.lock`): `b="../acme-eval-backup-14-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"` (a new time-stamped copy beside `acme-eval/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/14-eval-start/. .`
3. Compute and test: `uv run python scripts/evaluate.py && uv run pytest -q` (about 20 seconds; every test passes).
4. Render every format: `uv run quarto render report.qmd`.
5. Check: `report.html` opens with the sentence naming the best release and its ROC AUC, then Table 1 (three releases) and Figure 1 (three ROC curves); `report.docx` and `report.pdf` exist.
6. Rejoin: your folder now holds the end of these steps. Continue at the box in Chapter 3.
