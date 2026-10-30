# Checkpoint 12 · ePub

Checkpoint 11 plus `epub` in `report.qmd` (`lang: en`, an ePub download link on the HTML page).

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/12-water-epub/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . ../water-quality-backup-12` (a copy beside `water-quality/`).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/12-water-epub/. .`
4. Run: `python3 scripts/analysis.py && quarto render report.qmd`.
5. Check: `report.epub` opens in an e-book reader with the three figures and the sources.
