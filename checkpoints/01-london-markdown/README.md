# Checkpoint 01 · London in Markdown

State at the end of the Markdown block (steps 1–5, the first render, the project rules and the Python environment): `london.md` with a heading, lists, a link, the Big Ben photo, a quote, a table and a code fence, plus `images/`. No YAML and no code yet.

`AGENTS.md` holds the project's rules for the coding assistant, and `pyproject.toml` with `uv.lock` its Python environment, which `uv run` builds on first use.

## Catch up

Ask your coding assistant, started in `london-guide/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/01-london-markdown/README.md
```

The steps, run inside `london-guide/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../london-guide-backup-01-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `london-guide/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/01-london-markdown/. .`
3. Render: `uv run quarto render london.md`.
4. Check: `london.html` shows both lists, the photo with its credit, the five-row table and the checklist.
5. Rejoin: your folder now holds the end of this block, so skip the block's remaining prompts and follow the slides. Start pasting prompts again at 🧪 *From .md to .qmd* (⏱️ 0:35) ([slide](https://project-delphi.github.io/quarto-workshop/#/md-to-qmd)).
