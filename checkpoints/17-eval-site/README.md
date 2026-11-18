# Checkpoint 17 · A site and one brand

Checkpoint 16 plus a website and a brand. `_quarto.yml` makes the folder a Quarto website
with an explicit `render` list: a home page (`index.qmd`) whose first sentence is the
headline result, computed and guarded, above a listing (type `table`) of the documents with
their descriptions; the report, the model card and the deck; and `about.qmd` (the `trestles`
template) about Acme Signals, a fictional company. The navbar carries the logo, the footer
the fictional-company notice and the data credit (CC BY 4.0), every page a `description`,
and `open-graph: true` with a placeholder `site-url` gives link previews; search is on.
`uv run quarto render` builds it all into `_site/`, with the report's and the card's Word and
PDF files and the deck's PowerPoint file beside them; `_quarto.yml` then runs
`scripts/pptx_alt_text.py`.

`_brand.yml` holds Acme's palette and colour roles, system fonts (Helvetica, Arial) and the
logo (`brand/logo.svg`, drawn for this fictional company). Quarto applies it to the web
pages, the Reveal.js deck and the Typst PDFs; `acme.scss` keeps only the deck's muted text,
title sizes and layout, in `$brand-*` colours. Word and PowerPoint ignore the brand, so
`scripts/make_reference_docs.py` (replacing `make_pptx_reference.py`) makes
`templates/acme-reference.docx` and `.pptx` from its colours. `src/acme_eval/brand.py` reads
the brand and computes WCAG contrast for `tests/test_deck_contrast.py` and
`scripts/check_site.py`, which checks every rendered page for alt text, `lang`, a title, a
description and skipped heading levels. `filters/description-meta.lua` gives the deck its
description tag. The bank data are real (`data/README.md`).

Sources and data only: no `outputs/` and no rendered files. `uv run` builds `.venv/` from
`uv.lock` on first use.

## Catch up

Ask your coding agent, started in `acme-eval/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/17-eval-site/README.md
```

The steps, run inside `acme-eval/` (by the agent, or by you in a terminal):

1. Keep your work, all but the `.venv/` environment (`uv run` rebuilds it from `uv.lock`): `b="../acme-eval-backup-17-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"` (a new time-stamped copy beside `acme-eval/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/17-eval-site/. .`
3. Remove what the site replaces (it is in the backup): the old template script and the documents rendered beside the sources, since the site renders into `_site/`: `rm -f scripts/make_pptx_reference.py && find . -maxdepth 1 \( -name '*.html' -o -name '*.docx' -o -name '*.pdf' -o -name '*.pptx' -o -name '*_files' \) -exec rm -rf {} +`.
4. Compute and test: `uv run python scripts/evaluate.py && uv run pytest -q` (about 20 seconds; every test passes, including the brand's contrast test).
5. Build the site and check it: `uv run quarto render && uv run python scripts/check_site.py` (about 40 seconds; the check ends "5 pages checked, 0 problems").
6. Check: open `_site/index.html`; its first sentence names the best release with its recall, the table lists the report, the model card and the slides, and the navbar shows the logo with Report, Model card, Slides and About. `_site/` also holds `report.docx`, `report.pdf`, `model-card.docx`, `model-card.pdf` and `slides.pptx`.
7. Rejoin: your folder now holds the end of these steps. Continue at the catch-up box of the site chapter, "A Site and One Brand".
