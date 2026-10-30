# Checkpoint 11 · Council slides

Checkpoint 10 plus `slides.qmd` (six slides, as revealjs and pptx).

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/11-water-slides/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../water-quality-backup-11-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `water-quality/`, so earlier backups are kept).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/11-water-slides/. .`
4. Run: `python3 scripts/analysis.py && quarto render slides.qmd`.
5. Check: `slides.html` and `slides.pptx` both have six slides.
