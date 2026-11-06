# Quarto & Coding Agent Cheatsheet

A concise reference guide for the patterns, options, and commands taught in the Quarto workshop.

---

## 1. Document Front Matter (YAML)

### Multi-Format Document
Render a single `.qmd` into multiple document and presentation formats:

```yaml
---
title: "Project Report"
subtitle: "Executive Summary"
author: "Author Name"
date: today
format:
  html:
    toc: true
    code-fold: true
    embed-resources: true
  typst:
    papersize: a4
    margin:
      x: 2cm
      y: 2.5cm
  docx: default
  pptx: default
  revealjs:
    theme: [dark, custom.scss]
    slide-number: true
  epub:
    toc: true
---
```

---

## 2. Python Code Cell Options

Quarto uses special comments (`#|`) at the top of executable code cells:

| Option | Purpose | Example |
|---|---|---|
| `#| echo: false` | Hide the code; display only the output (charts/tables) | `#| echo: false` |
| `#| echo: true` | Display code alongside the output | `#| echo: true` |
| `#| eval: false` | Show code without running it | `#| eval: false` |
| `#| warning: false` | Suppress execution warnings | `#| warning: false` |
| `#| fig-cap: "..."` | Caption below figure or plot | `#| fig-cap: "Annual visits 2015–2025"` |
| `#| fig-alt: "..."` | Screen-reader accessible alternative text | `#| fig-alt: "Bar chart showing..."` |
| `#| fig-width: N` | Figure width in inches (for static formats) | `#| fig-width: 8` |
| `#| tbl-cap: "..."` | Caption for Markdown or DataFrame tables | `#| tbl-cap: "Summary statistics"` |

### Inline Python Code
Embed computed values directly into narrative text:
```markdown
The dataset contains `{python} len(df)` records across `{python} df['year'].nunique()` years.
```

---

## 3. Dashboards (`format: dashboard`)

Quarto transforms headings into interactive rows, columns, and tabsets:

```markdown
---
title: "Operations Dashboard"
format: dashboard
---

# Overview

## Row {height=30%}

::: {.valuebox icon="water" color="primary"}
Municipalities
`{python} f"{df['divipola'].nunique():,}"`
:::

::: {.valuebox icon="droplet" color="warning"}
High Risk Zones
`{python} f"{(df['irca'] > 35).sum():,}"`
:::

## Row {height=70%}

### Column {width=60%}

```{python}
#| title: Geographic Distribution
fig = px.scatter(...)
fig
```

### Column {width=40%}

```{python}
#| title: Priority Municipalities
show(priority_table, maxBytes=0)
```
```

---

## 4. Website Configuration (`_quarto.yml`)

Manage multi-page websites, blogs, and publishing settings:

```yaml
project:
  type: website
  output-dir: _site
  pre-render: scripts/analysis.py  # Optional: run computation before render

website:
  title: "Drinking Water Analysis"
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: explore.qmd
        text: Explore
      - href: clusters.qmd
        text: Clusters
      - href: dashboard.qmd
        text: Dashboard
      - href: report.pdf
        text: "Download PDF"

execute:
  echo: true
  warning: true
  freeze: false   # false = always recompute; auto = cache unchanged pages
```

---

## 5. Essential CLI Commands

Each project uses [uv](https://docs.astral.sh/uv/) to manage dependencies deterministically:

```bash
# 1. Initialize environment & add dependencies
uv init --bare
uv add pandas numpy matplotlib plotly scikit-learn itables tabulate

# 2. Preview & Render
uv run quarto preview <file.qmd>
uv run quarto render <file.qmd>
uv run quarto render

# 3. Publish to GitHub Pages
uv run quarto publish gh-pages
uv run quarto publish gh-pages --no-prompt
```

`preview` reloads live in the browser. `render` with a file renders that document; without one, the whole website or project. The first `publish` is interactive (Enter to confirm); use `--no-prompt` for later updates.

---

## 6. Prompting Coding Assistants Effectively

To get reliable, reproducible results when working with agents (Claude Code, Codex, Antigravity):

1. **Be explicit about inputs and outputs**:
   - Name source files, target files, and specific columns in backticks (`data/visits.csv`, `year`, `visits`).
2. **Specify verification criteria**:
   - Always end prompts with an observable check:
   - *"Render with `uv run quarto render report.qmd` and verify `report.pdf` has 3 charts and no missing values."*
3. **Guard against dashboard duplication**:
   - Remind the assistant: *"Assign Plotly charts to `fig` and end the cell with `fig` (no `fig.show()`)."*
4. **Protect data contracts**:
   - Instruct the assistant: *"Never fabricate numbers; compute all values from the cited CSV tables."*
