# Checkpoint 09 · Correlation ≠ causation

Checkpoint 08 plus the within-cluster IRCA vs infant mortality check (Spearman ρ and n per cluster, one row per municipality-year) and the descriptive-only caveat in `clusters.qmd`.

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/09-water-causation/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . ../water-quality-backup-09` (a copy beside `water-quality/`).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/09-water-causation/. .`
4. Run: `python3 scripts/analysis.py && quarto render clusters.qmd`.
5. Check: `clusters.html` shows ρ and n for every cluster and says the check is descriptive.
