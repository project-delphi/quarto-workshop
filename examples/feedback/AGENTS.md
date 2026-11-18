# Section feedback sheets: project rules

## Scope

One feedback sheet per section of a fictional course, from `data/gradebook.csv`. The gradebook
is SYNTHETIC, invented for teaching: say so on every output, in the text, the table caption,
the figure caption and the axis label.

## Rules

- `data/` is read-only. To change the gradebook, change `scripts/make_gradebook.py` and rerun
  it; never edit the CSV by hand.
- Students are ids (`S001`), never names, and a sheet shows only section totals (mean, spread,
  number submitted), never one student's mark. Never describe a group smaller than
  `MIN_STUDENTS` in `feedback.qmd`.
- The parameter, `section`, and its default live in the cell tagged `parameters`
  (`#| tags: [parameters]`), the first cell after the YAML. The document checks the value
  before using it and stops on a section that is not in the gradebook.
- Every number is computed from the gradebook. Never type a number by hand.
- Every wording that depends on the marks ("above the course mean", "wider than the course's")
  is chosen by code from the numbers as printed (rounded to one decimal) and guarded with
  `claim`, so the words and the figures beside them never disagree.
- Each output is named by its parameter: `feedback-A.pdf`. Never let one section's file
  overwrite another's.
- Every figure has `fig-alt` and a caption; the alt text describes the chart without stating
  a result, because it is the same for every section.
- `reports/`, `.venv/` and rendered files are never committed.

## Commands

The Python environment is `pyproject.toml` and `uv.lock` (papermill is needed for `-P`). Run
`python` and `quarto` through `uv run`:

- `uv run python scripts/make_gradebook.py` (rewrites `data/gradebook.csv`, the same bytes)
- `uv run quarto render feedback.qmd -P section:B --to typst --output feedback-B.pdf` (one sheet)
- `uv run python scripts/render_sections.py` (every section into `reports/`, checked)
