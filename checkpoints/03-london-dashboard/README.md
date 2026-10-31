# Checkpoint 03 · Dashboard

Checkpoint 02 plus `london-dashboard.qmd`: an Attractions page (three value boxes and two Plotly charts) and the optional Churches page (Visit London's ten churches from `data/churches.csv`, each linked to its Visit London page).

`AGENTS.md` holds the project's rules for the coding assistant, and `pyproject.toml` with `uv.lock` its Python environment, which `uv run` builds on first use.

## Catch up

Ask your coding assistant, started in `london-guide/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/03-london-dashboard/README.md
```

The steps, run inside `london-guide/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../london-guide-backup-03-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `london-guide/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/03-london-dashboard/. .`
3. Remove `london.md` if it is still there: `london.qmd` replaces it, and both would write `london.html`.
4. Render: `uv run quarto render london-dashboard.qmd`.
5. Check: `london-dashboard.html` has an Attractions page with three value boxes, a bar chart and a line chart, and a Churches page listing ten churches with Visit London links.
