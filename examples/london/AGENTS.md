# London guide: project rules

## Scope

A London visitor guide for the city's tourism office, written once in Markdown and Quarto
and reused for every audience: web page, documents, slides, dashboard, flyer and website.

## Rules

- Every number comes from a cited file in `data/`: each row carries `source`, `url` and
  `retrieved`. Never estimate or invent a figure or a fact.
- ALVA counts only its member sites: write "ALVA member attractions".
- Photos are openly licensed, credited from `images/ATTRIBUTION.md`, and show no people.
- Keep `data/` and `images/` unchanged.

## Commands

The Python environment is `pyproject.toml` and `uv.lock`. Run `quarto` and `python`
through `uv run`, which builds `.venv/` on first use:

- `uv run quarto preview <file>` for a live preview
- `uv run quarto render <file>`, or `uv run quarto render` once `_quarto.yml` exists
