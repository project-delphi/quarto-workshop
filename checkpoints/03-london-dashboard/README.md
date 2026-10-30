# Checkpoint 03 · Dashboard

Checkpoint 02 plus `london-dashboard.qmd`: three value boxes and two Plotly charts from `data/`.

## Catch up

Ask your coding assistant, started in `london-guide/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/03-london-dashboard/README.md
```

The steps, run inside `london-guide/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../london-guide-backup-03-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `london-guide/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/03-london-dashboard/. .`
3. Remove `london.md` if it is still there: `london.qmd` replaces it, and both would write `london.html`.
4. Render: `quarto render london-dashboard.qmd`.
5. Check: `london-dashboard.html` shows three value boxes, a bar chart and a line chart.
