# Checkpoint 05 · Explore

`explore.qmd`: rows and columns, missing values by column and zone, IRCA by risk band and zone, and IRCA by year. Sources only: the data come from `examples/water/data/`.

`AGENTS.md` holds the project's rules for the coding assistant, and `pyproject.toml` with `uv.lock` its Python environment, which `uv run` builds on first use.

## Catch up

Ask your coding assistant, started in `water-quality/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/05-water-explore/README.md
```

The steps, run inside `water-quality/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../water-quality-backup-05-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `water-quality/`, so earlier backups are kept).
2. Copy the data if `data/water_municipal.csv` is missing (checkpoints hold sources only): `cp -R ../quarto-workshop/examples/water/data .`
3. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/05-water-explore/. .`
4. Render: `uv run quarto render explore.qmd`.
5. Check: `explore.html` shows missing values by zone and IRCA by band, zone and year for 2010–2023.
6. Rejoin: your folder now holds the end of this block, so skip the block's remaining prompts and follow the slides. Start pasting prompts again at 🧹 *Prepare* (⏱️ 1:45) ([slide](https://project-delphi.github.io/quarto-workshop/#/water-prepare)).
