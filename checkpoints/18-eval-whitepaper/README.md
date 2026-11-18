# Checkpoint 18 · White papers and references

Checkpoint 17 plus a technical white paper. `whitepaper.qmd` is three to five A4 pages for
clients and investors: an abstract, numbered sections (Introduction, Data, Method, Results,
Limitations, Conclusion), three numbered equations, a table and two figures, each referred to
in the text with `@eq-`, `@tbl-`, `@fig-` or `@sec-`. Every number comes from `outputs/`
and every result-dependent sentence has a guard. It renders as html (on the site, in the
navbar and the home page's table of documents), Word (`templates/acme-reference.docx`) and a
Typst PDF in Acme's house template, `templates/whitepaper/typst-show.typ`, a replacement for
one of Quarto's Typst template partials: a title block with the logo, a "Technical white
paper" label, the company and the date, a running header and a page-numbered footer, in the
brand's colours. Its figures are SVG in the PDF.

`references.bib` adds three sources, each checked against its DOI record: Fawcett (2006) on
ROC analysis, Efron (1979) on the bootstrap and Niculescu-Mizil and Caruana (2005) on
calibration. `csl/apa.csl` (the APA 7th edition style from the official CSL repository,
CC BY-SA 3.0) formats the citations alike in all three formats; the Typst PDF needs
`citeproc: true` for that. `scripts/check_refs.py` compares every DOI's year, first author
and title with Crossref or DataCite; it needs the network and is run before publishing, not
by the render. Acme Signals is a fictional company; the bank data are real
(`data/README.md`).

Sources and data only: no `outputs/` and no rendered files. `uv run` builds `.venv/` from
`uv.lock` on first use.

## Catch up

Ask your coding agent, started in `acme-eval/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/18-eval-whitepaper/README.md
```

The steps, run inside `acme-eval/` (by the agent, or by you in a terminal):

1. Keep your work, all but the `.venv/` environment (`uv run` rebuilds it from `uv.lock`): `b="../acme-eval-backup-18-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"` (a new time-stamped copy beside `acme-eval/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/18-eval-whitepaper/. .`
3. Compute and test: `uv run python scripts/evaluate.py && uv run pytest -q` (about 20 seconds; every test passes).
4. Build the site and check it: `uv run quarto render && uv run python scripts/check_site.py` (about 50 seconds; the check ends "6 pages checked, 0 problems").
5. Check the references (needs the network): `uv run python scripts/check_refs.py` (it ends "0 problems").
6. Check: open `_site/whitepaper.pdf`; page 1 shows the logo, "TECHNICAL WHITE PAPER", the title and the abstract, the sections are numbered, "Equation 1", "Table 1" and "Figure 1" appear in the text, and the references are in APA style, as in `_site/whitepaper.html` and `_site/whitepaper.docx`. The navbar of `_site/index.html` shows White paper.
7. Rejoin: your folder now holds the end of these steps. Continue at the catch-up box of the white-paper chapter, "White Papers and References".
