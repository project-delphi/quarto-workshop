# Checkpoint 08 · Interpret

State at the end of the Interpret block (both steps): checkpoint 07 plus the outcome rules, `outputs/outcomes_by_year.csv`, cluster profiles with rule-based names (`outputs/cluster_profiles.csv`), and a centroid heatmap and outcome lines in `clusters.qmd`.

`AGENTS.md` holds the project's rules for the coding assistant, and `pyproject.toml` with `uv.lock` its Python environment, which `uv run` builds on first use.

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/08-water-interpret/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../water-quality-backup-08-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `water-quality/`, so earlier backups are kept).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/08-water-interpret/. .`
4. Run: `uv run python scripts/analysis.py && uv run quarto render clusters.qmd`.
5. Check: the script prints one name per cluster and `clusters.html` shows the heatmap and the outcomes by cluster and year.
6. Rejoin: your folder now holds the end of this block, so skip the block's remaining prompts and follow the slides. Start pasting prompts again at ⚠️ *Correlation ≠ causation* (⏱️ 2:30) ([slide](https://project-delphi.github.io/quarto-workshop/#/water-causation)).
