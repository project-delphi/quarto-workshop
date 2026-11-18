# Section feedback sheets (worked example)

An educator's parameterised report: one document, `feedback.qmd`, rendered once per section
of a course, gives each section a one-page sheet comparing its marks with the whole course.
The gradebook, `data/gradebook.csv`, is **SYNTHETIC: invented for teaching**; no student,
course or mark is real (`data/README.md`). It is the small companion of `examples/eval/`'s
monthly update, for the same chapter.

## Layout

| Path | What it holds |
|---|---|
| `AGENTS.md` | The project's rules for a coding agent |
| `data/gradebook.csv` | SYNTHETIC gradebook: 60 student ids in sections A, B and C, four assignments |
| `data/README.md` | What the gradebook holds, and that it is invented |
| `scripts/make_gradebook.py` | Writes the gradebook, with a fixed seed |
| `feedback.qmd` | The sheet, parameter `section` (default `"A"`): mean and spread per assignment against the course, a chart, guarded wording; Typst PDF (and html) |
| `scripts/render_sections.py` | Renders every section into `reports/feedback-<section>.pdf` and checks each |
| `pyproject.toml`, `uv.lock` | The Python environment: pandas, matplotlib, papermill, Jupyter |

## Build

From this folder, with [uv](https://docs.astral.sh/uv/) and Quarto installed:

```bash
uv run python scripts/render_sections.py   # reports/feedback-A.pdf, -B.pdf, -C.pdf (about 30 s)
```

One sheet: `uv run quarto render feedback.qmd -P section:B --to typst --output feedback-B.pdf`
(next to the source). Without `-P`, the default section, `A`, renders. If a user-level Jupyter
kernel shadows the project's environment, prefix the commands with
`JUPYTER_PATH="$PWD/.venv/share/jupyter"`.

## Design decisions

- **One parameter, checked.** `section` and its default sit in the cell tagged `parameters`;
  Quarto passes `-P section:B` to Jupyter through papermill, which adds a cell with the value
  after it (hidden by `echo: false`). The document stops on a section the gradebook lacks.
- **Words follow the printed numbers.** "Above", "below" or "level with" the course mean, and
  "wider" or "narrower" spread, are chosen from the means and standard deviations rounded to
  one decimal, as printed, and guarded, so the text never contradicts its table.
- **Totals only.** The sheet gives each section's mean, standard deviation and number
  submitted, never a student's mark, and refuses a group smaller than five. The course
  figures include the section; a mean leaves out work not submitted. Differences between
  sections of about twenty students may be chance: the sheet describes, it tests nothing.
- **Labelled everywhere.** The callout, the opening sentence, the table and figure captions
  and the chart's axis say SYNTHETIC; `render_sections.py` fails a sheet whose text lacks it.
- **Not a website.** There is no `_quarto.yml`, so each render is a single file written next
  to `feedback.qmd`; `render_sections.py` names it with `--output feedback-<section>.pdf` and
  moves it into `reports/`.
