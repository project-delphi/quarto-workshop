# Checkpoint 16 · Slides

Checkpoint 15 plus `slides.qmd`, an eight-slide deck for Acme's product team and its
investors in two formats, Reveal.js (`slides.html`) and PowerPoint (`slides.pptx`). Each
slide states one claim in its title, with the title's numbers computed from `outputs/` and
its wording guarded by `acme_eval.claims.claim`; the detail is in the speaker notes, and the
last slide is the decision. The deck has a two-column v2-against-v3 slide, the ROC figure,
who is called by age band, calibration, and caveats that appear one at a time (fragments).
Its theme is `acme.scss` (Acme's colours, system fonts), checked by
`tests/test_deck_contrast.py` (WCAG contrast of at least 4.5:1); the PowerPoint deck uses
`templates/acme-reference.pptx`, made by `scripts/make_pptx_reference.py` with the same
colours. `filters/title-notes.lua` puts the title slide's notes on the Reveal.js title slide,
`scripts/pptx_alt_text.py` gives the PowerPoint figures their alt text, and
`scripts/deck_pdf.py` prints `slides.pdf` with headless Chrome and checks it page by page
(`pypdf`, added to the `dev` group of `pyproject.toml` and `uv.lock`). Acme Signals is a
fictional company; the bank data are real (`data/README.md`).

Sources and data only: no `outputs/` and no rendered files. `uv run` builds `.venv/` from
`uv.lock` on first use.

## Catch up

Ask your coding agent, started in `acme-eval/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/16-eval-slides/README.md
```

The steps, run inside `acme-eval/` (by the agent, or by you in a terminal):

1. Keep your work, all but the `.venv/` environment (`uv run` rebuilds it from `uv.lock`): `b="../acme-eval-backup-16-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"` (a new time-stamped copy beside `acme-eval/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/16-eval-slides/. .`
3. Compute and test: `uv run python scripts/evaluate.py && uv run pytest -q` (about 20 seconds; every test passes, including the deck's contrast test).
4. Render the deck, then give the PowerPoint figures their alt text: `uv run quarto render slides.qmd && uv run python scripts/pptx_alt_text.py`.
5. Print the PDF (needs Google Chrome or Chromium; set `CHROME` to its path if it is not found): `uv run python scripts/deck_pdf.py`.
6. Check: `slides.html` has eight slides, the last titled "We decide: …", and pressing `S` opens the speaker view with notes; `slides.pptx` has eight slides with notes; `slides.pdf` has eight pages and the script says so.
7. Rejoin: your folder now holds the end of these steps. Continue at the catch-up box of the slides chapter, "Slides That Carry a Decision".
