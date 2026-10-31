# Checkpoint 12 · ePub

The ⭐ optional ePub step: checkpoint 11 plus `epub` in `report.qmd` (`lang: en`, an ePub download link on the HTML page).

`AGENTS.md` holds the project's rules for the coding assistant, and `pyproject.toml` with `uv.lock` its Python environment, which `uv run` builds on first use.

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/12-water-epub/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../water-quality-backup-12-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `water-quality/`, so earlier backups are kept).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/12-water-epub/. .`
4. Run: `uv run python scripts/analysis.py && uv run quarto render report.qmd`.
5. Check: `report.epub` opens in an e-book reader with the three figures and the sources.
6. Rejoin: your folder now holds the ⭐ ePub step. Start pasting prompts again at ✍️🌐 *2:55 · Blog + website* ([slide](https://project-delphi.github.io/quarto-workshop/#/water-website)).
