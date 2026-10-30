# Checkpoint 04 · Five audiences

State at the end of the audiences block: checkpoint 03 plus `london-email.qmd` (docx), `london-flyer.qmd` (A5 Typst PDF) and `london-social.qmd` (12 cm square Typst PDF; optional on the slides).

## Catch up

Ask your coding assistant, started in `london-guide/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/04-london-audiences/README.md
```

The steps, run inside `london-guide/` (by the assistant, or by you in a terminal):

1. Keep your work: `cp -R . ../london-guide-backup-04` (a copy beside `london-guide/`).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/04-london-audiences/. .`
3. Remove `london.md` if it is still there: `london.qmd` replaces it, and both would write `london.html`.
4. Render: `quarto render london-email.qmd && quarto render london-flyer.qmd && quarto render london-social.qmd`.
5. Check: `london-email.docx` opens with headings and working links, `london-flyer.pdf` is one A5 page and `london-social.pdf` is one 12 cm square page.
