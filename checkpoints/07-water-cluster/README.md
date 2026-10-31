# Checkpoint 07 · Cluster

State at the end of the Cluster block (both steps): checkpoint 06 with k-means in `scripts/analysis.py` (k = 2–8, elbow + silhouette, ARI across seeds, clusters numbered by centroid IRCA) and `clusters.qmd` (elbow, silhouette, PCA scatter).

`AGENTS.md` holds the project's rules for the coding assistant, and `pyproject.toml` with `uv.lock` its Python environment, which `uv run` builds on first use.

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/07-water-cluster/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../water-quality-backup-07-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `water-quality/`, so earlier backups are kept).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/07-water-cluster/. .`
4. Run: `uv run python scripts/analysis.py && uv run quarto render clusters.qmd`.
5. Check: `outputs/clusters.parquet` exists and `clusters.html` shows the elbow, the silhouette and the PCA picture.
6. Rejoin: your folder now holds the end of this block, so skip the block's remaining prompts and follow the slides. Start pasting prompts again at 🏷️ *Interpret* (⏱️ 2:15) ([slide](https://project-delphi.github.io/quarto-workshop/#/water-interpret)).
