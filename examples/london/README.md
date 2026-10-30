# London guide: finished Part 1 project

The finished Part 1 project: `london.qmd` in six formats, the dashboard, the partner brief, the flyer and the social card, published as one website by `_quarto.yml`. Every number comes from `data/` (cited ALVA tables); photo credits are in `images/ATTRIBUTION.md`.

## Catch up

Ask your coding assistant, started in `london-guide/`:

```text
Catch me up: follow ../quarto-workshop/examples/london/README.md
```

The steps, run inside `london-guide/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../london-guide-backup-final-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `london-guide/`, so earlier backups are kept).
2. Copy the finished project here: `cp -R ../quarto-workshop/examples/london/. .`
3. Remove `london.md` if it is still there: `london.qmd` replaces it, and both would write `london.html`.
4. Render the site: `quarto render` (writes `_site/`).
5. Check: `_site/index.html` opens with Guide, Dashboard and Downloads in the navbar.
