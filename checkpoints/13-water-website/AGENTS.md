# Water quality and infant mortality: project rules

## Scope

Describe drinking-water quality, water services and infant mortality in Colombian
municipalities from `data/water_municipal.csv` (documented in `data/README.md`), then
publish one analysis as a report, slides, a blog post, a dashboard and a website.

## Rules

- Keep `data/` unchanged. Compute every number from it, in `scripts/analysis.py`, and never
  type a result by hand.
- IRCA here is the utility-supplied ("prestadores") IRCA from the INS open table: label it so.
- Cluster on water, service and context features only. Outcomes (infant mortality,
  Saber 11, school dropout) describe the clusters and never define them.
- Comparisons between clusters are descriptive: say that they do not establish causal
  effects of water quality.
- Follow the caveats in `data/README.md`: method changes, the capitals' coverage and the
  years each source covers.

## Commands

The Python environment is `pyproject.toml` and `uv.lock`. Run `quarto` and `python`
through `uv run`, which builds `.venv/` on first use:

- `uv run python scripts/analysis.py`
- `uv run quarto render <file>`, `uv run quarto render` and `uv run quarto preview`
