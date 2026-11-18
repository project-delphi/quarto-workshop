# Checkpoint 19 · Reports that run themselves

Checkpoint 18 plus two parameterised documents and the script that renders them. `update.qmd`
is a monthly investor update with one parameter, `month` (`"YYYY-MM"`, default `"latest"`,
the last month in `data/synthetic_business.csv`): the month's business figures, which are
SYNTHETIC and say so (a "SYNTHETIC: invented for teaching" callout, "(synthetic)" after each
number, the table's caption and headings), then the release live that month with its real
metrics from `outputs/`. `segment.qmd` is one page per customer segment, with parameters
`factor` (`age_band` or `job`) and `segment` (default `60+`): the best release's figures in
that segment from `outputs/segments.csv`. Both hold their defaults in a cell tagged
`parameters`, check the value with `src/acme_eval/params.py` before using it, choose every
value-dependent word ("up", "below", "the first release") in code and guard it, and render as
html, Word and a Typst PDF.

Neither is on the site: they are not in `project.render`, so Quarto renders each as a single
file next to the source. `scripts/render_params.py` renders `update.qmd` for every month and
`segment.qmd` for every age band, one Quarto run per value with
`-P month:2026-10 -M output-file:update-2026-10`, moves the files into `reports/`, and checks
that each contains its value. `pyproject.toml` adds `papermill`, which Quarto needs for `-P`;
`tests/test_params.py` tests the checks. Acme Signals is a fictional company; the bank data
are real (`data/README.md`).

Sources and data only: no `outputs/`, no `reports/` and no rendered files. `uv run` builds
`.venv/` from `uv.lock` on first use.

## Catch up

Ask your coding agent, started in `acme-eval/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/19-eval-params/README.md
```

The steps, run inside `acme-eval/` (by the agent, or by you in a terminal):

1. Keep your work, all but the `.venv/` environment (`uv run` rebuilds it from `uv.lock`): `b="../acme-eval-backup-19-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"` (a new time-stamped copy beside `acme-eval/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/19-eval-params/. .`
3. Compute and test: `uv run python scripts/evaluate.py && uv run pytest -q` (about 20 seconds; every test passes).
4. Build the site and check it: `uv run quarto render && uv run python scripts/check_site.py` (about 50 seconds; the check ends "6 pages checked, 0 problems").
5. Render every month and age band: `uv run python scripts/render_params.py` (about 5 minutes; it ends "45 files, 0 problems").
6. Check: open `reports/update-2026-10.pdf`; it says "This update covers October 2026", shows the "SYNTHETIC: invented for teaching" box, marks each business number "(synthetic)" and names v3 as the release live that month. `reports/update-2026-01.pdf` says no release was live yet, and `reports/segment-age-60plus.pdf` covers the contacts aged 60+.
7. Rejoin: your folder now holds the end of these steps. Continue at the catch-up box of the parameters chapter, "Reports That Run Themselves".
