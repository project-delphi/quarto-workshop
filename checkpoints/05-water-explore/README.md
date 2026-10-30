# Checkpoint 05 · Explore

`explore.qmd`: rows and columns, missing values by column and zone, IRCA by risk band and zone, and IRCA by year. Sources only: the data come from `examples/water/data/`.

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/05-water-explore/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../water-quality-backup-05-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `water-quality/`, so earlier backups are kept).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/05-water-explore/. .`
4. Render: `quarto render explore.qmd`.
5. Check: `explore.html` shows missing values by zone and IRCA by band, zone and year for 2010–2023.
