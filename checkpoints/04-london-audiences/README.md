# Checkpoint 04 · Three audience versions

State at the end of the audiences block, the four files that one prompt's three sub-agents write: checkpoint 02 plus `london-dashboard.qmd` (an Attractions page with three value boxes and two Plotly charts, and a Churches page listing Visit London's ten churches from `data/churches.csv`, each linked to its Visit London page), `london-email.qmd` (docx partner brief), `london-email-message.md` (the email that carries it), `london-flyer.qmd` (A5 Typst PDF); the ⭐ 12 cm square ad, `london-social.qmd`, is optional and not in this checkpoint. There is no checkpoint 03: the block is a single prompt.

`AGENTS.md` holds the project's rules for the coding assistant, and `pyproject.toml` with `uv.lock` its Python environment, which `uv run` builds on first use.

## Catch up

Ask your coding assistant, started in `london-guide/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/04-london-audiences/README.md
```

The steps, run inside `london-guide/` (by the assistant, or by you in a terminal):

1. Keep your work, all but the `.venv/` environment (`uv run` rebuilds it from `uv.lock`): `b="../london-guide-backup-04-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"` (a new time-stamped copy beside `london-guide/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/04-london-audiences/. .`
3. Remove `london.md` if it is still there: `london.qmd` replaces it, and both would write `london.html`.
4. Render, one file at a time: `uv run quarto render london-dashboard.qmd && uv run quarto render london-email.qmd && uv run quarto render london-flyer.qmd`.
5. Check: `london-dashboard.html` has an Attractions page with three value boxes, a bar chart and a line chart, and a Churches page listing ten churches with Visit London links; `london-email.docx` opens with headings and working links; `london-email-message.md` holds the email in one text block; `london-flyer.pdf` is one A5 page.
6. Rejoin: your folder now holds the end of this block, so skip the block's remaining prompts and follow the slides. Start pasting prompts again at 🌍 *Publish to GitHub Pages* (⏱️ 0:54) ([slide](https://project-delphi.github.io/quarto-workshop/#/publish-london)).
