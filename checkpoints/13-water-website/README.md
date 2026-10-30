# Checkpoint 13 · Website and blog

Checkpoint 12 as a Quarto website: `_quarto.yml` (pre-render, `freeze: false`, render list, navbar), `index.qmd` with a post listing and `posts/four-kinds-of-municipal-zone/`.

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/13-water-website/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . ../water-quality-backup-13` (a copy beside `water-quality/`).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/13-water-website/. .`
4. Render the site: `quarto render` (the pre-render step runs `scripts/analysis.py` first).
5. Check: `_site/index.html` lists one post whose title states the real k.
