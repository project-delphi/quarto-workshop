# Checkpoint 06 · Prepare

State at the end of the Prepare block (both steps): checkpoint 05 plus `scripts/analysis.py` with `prepare()`: row selection, nine features, the capital fill, imputation flags and within-year z-scores beside the original-unit columns. It writes `outputs/prepared.parquet`.

`AGENTS.md` holds the project's rules for the coding assistant, and `pyproject.toml` with `uv.lock` its Python environment, which `uv run` builds on first use.

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/06-water-prepare/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../water-quality-backup-06-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `water-quality/`, so earlier backups are kept).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/06-water-prepare/. .`
4. Run: `uv run python scripts/analysis.py`.
5. Check: the printed `kept` count matches the 🧮 *What we keep* slide and `outputs/prepared.parquet` exists.
6. Rejoin: your folder now holds the end of this block, so skip the block's remaining prompts and follow the slides. Start pasting prompts again at 🧩 *Cluster* (⏱️ 1:55) ([slide](https://project-delphi.github.io/quarto-workshop/#/water-cluster)).
