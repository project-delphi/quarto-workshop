# Checkpoint 04 · Five audiences

The ⭐ optional audience versions: checkpoint 03 plus `london-email.qmd` (docx), `london-email-message.md` (the email that carries it), `london-flyer.qmd` (A5 Typst PDF) and `london-social.qmd` (12 cm square Typst PDF).

`AGENTS.md` holds the project's rules for the coding assistant, and `pyproject.toml` with `uv.lock` its Python environment, which `uv run` builds on first use.

## Catch up

Ask your coding assistant, started in `london-guide/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/04-london-audiences/README.md
```

The steps, run inside `london-guide/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../london-guide-backup-04-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `london-guide/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/04-london-audiences/. .`
3. Remove `london.md` if it is still there: `london.qmd` replaces it, and both would write `london.html`.
4. Render: `uv run quarto render london-email.qmd && uv run quarto render london-flyer.qmd && uv run quarto render london-social.qmd`.
5. Check: `london-email.docx` opens with headings and working links, `london-email-message.md` holds the email in one text block, `london-flyer.pdf` is one A5 page and `london-social.pdf` is one 12 cm square page.
6. Rejoin: your folder now holds every ⭐ audience version. Start pasting prompts again at 🌍 *Publish to GitHub Pages* (⏱️ 0:50) ([slide](https://project-delphi.github.io/quarto-workshop/#/publish-london)).
