# Checkpoint 02 · From .md to .qmd

State at the end of the `.md` → `.qmd` block, so it already includes every step of that block: `london.qmd` with YAML front matter, a Python cell with inline code, a captioned figure and six formats (html, docx, typst PDF, pptx, epub, and revealjs slides in `london-slides.html`), plus the `data/` and `images/` it reads.

## Catch up

Ask your coding assistant, started in `london-guide/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/02-london-qmd/README.md
```

The steps, run inside `london-guide/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . "../london-guide-backup-02-$(date +%Y%m%d-%H%M%S)"` (a new time-stamped copy beside `london-guide/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/02-london-qmd/. .`
3. Remove `london.md` if it is still there: `london.qmd` replaces it, and both would write `london.html`.
4. Render every format: `quarto render london.qmd`.
5. Check: `london.html` shows the title block, the sentence with computed visit numbers and the numbered bar chart; `london.docx`, `london.pdf`, `london.pptx`, `london.epub` and `london-slides.html` exist.
