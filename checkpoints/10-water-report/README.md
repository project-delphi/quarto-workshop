# Checkpoint 10 · Report

Checkpoint 09 plus `report.qmd` (html, docx and Typst PDF).

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/10-water-report/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . ../water-quality-backup-10` (a copy beside `water-quality/`).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/10-water-report/. .`
4. Run: `python3 scripts/analysis.py && quarto render report.qmd`.
5. Check: `report.docx` and `report.pdf` open with the heatmap and the outcomes figure.
