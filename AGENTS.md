# Repository instructions

## Scope and architecture

This repository is a Quarto website containing Reveal.js teaching decks. Read `_quarto.yml`,
`README.md`, and the affected `.qmd` files before editing. `index.qmd` is the 3 h 10 min
hands-on workshop: Part 0 (intro, setup), Part 1 (London guide, included from
`slides/_london.qmd`) and Part 2 (Colombian water quality, included from `slides/_water.qmd`).
`ai-workflows.qmd` teaches graduate-level agent-assisted authoring. Preserve the dark theme
(`theme: [dark, theme.scss]`) and exercise-driven structure. The main learning path delegates dependency setup to agents;
do not reintroduce lengthy Conda or kernel troubleshooting lessons.

The workshop audience uses desktop computers and modern laptops. Design and
validate the teaching decks at desktop and laptop presentation sizes. Mobile
layout review is not a completion requirement unless explicitly requested.

Shared presentation and execution settings live in `_quarto.yml`; document headers contain
metadata and only necessary overrides. Keep `project.render` explicit so README, agent
instructions, and lab inputs never become published pages accidentally.

## Build and preview

From the repository root:

```bash
quarto --version
quarto render
quarto preview
quarto preview ai-workflows.qmd
```

Preview prints a local URL and does not launch a browser automatically. Open that URL for
visual inspection. Stop only preview processes you started.

The workshop deck executes Python through Jupyter. Inspect the existing runtime and any required PDF/TeX engine before
installing dependencies; prepare a local environment if needed and record the commands used.
`environment.yml` and `environment-r.yml` are optional reproducibility recipes. When the
existing `.conda/` environment is usable, select it explicitly:

```bash
QUARTO_PYTHON="$PWD/.conda/bin/python" \
  JUPYTER_PATH="$PWD/.conda/share/jupyter" quarto render
```

Do not disable execution or hide errors to make a build pass. `freeze: false` and `cache: false`
keep teaching computations fresh. Changes to external data are not automatically detected by
`freeze: auto`; any future caching policy must document invalidation.

## Technical Markdown and scientific content

- Use two-space YAML indentation and valid Quarto option names, checked against official docs.
- Use `#` for section slides, `##` for slides, and `### Exercise` for embedded activities.
- Keep slides focused. Move detail into `::: {.notes}`; split content before shrinking type.
- Executable cells use `{python}`; display-only fences use `python` or `{.python}`.
  Show literal cell syntax with `{{python}}` inside a longer outer fence. Never accidentally
  execute installation, network, publishing, or agent commands while rendering a deck.
- Check progressive highlighting against physical code lines, including continuations.
- Use relative links to local `.qmd` files so Quarto resolves output links correctly.
- Define notation, units, assumptions, and the unit of analysis near technical results.
- Compute numerical claims from the input data. Keep raw inputs unchanged; label synthetic data.
- Verify citations against primary sources. Link current CLI and installation claims to official
  documentation and record the verification date. Never invent results or references.
- Give meaningful figures captions and alternative text; inspect code wrapping and tables.

## Workshop slide conventions

The slides are the course resource: participants follow them alone and do most work by
prompting a coding assistant.

- One concept per slide, introduced in order (Markdown → render → YAML → code cells →
  formats → projects → publishing). Never use a concept before its slide.
- Emoji over words: at most about 30 words of prose per slide; detail goes in `::: {.notes}`.
  Build examples progressively with fragments (`. . .`, `.fragment`) instead of walls of text.
- Section dividers are `# <emoji> Title {#id}` followed by `[⏱️ h:mm]{.clock}` matching the agenda.
- Hands-on slides use the three boxes defined in `theme.scss`: `::: {.prompt}` holds the exact
  prompt in a fenced `text` block (copyable, 1–4 lines, one task, concrete file/column names,
  a verification ask); `::: {.agent}` lists what the assistant will likely run; `::: {.you}`
  lists what participants type or click themselves (accounts, `git push`, `quarto publish`).
- Exercises use `### Exercise · ⏱️ N min` and a `::: {.done}` block whose text completes
  "You're done when …". Each hands-on step has a copyable checkpoint in `checkpoints/`.

## Worked examples and report deliverables

`examples/london/` is the finished Part 1 project and `examples/water/` the finished Part 2
project; `checkpoints/NN-*/` hold intermediate states (sources only, no data or rendered
output). Keep all three outside `project.render`; they are rendered separately for testing.

London figures must be real and cited: every data row carries `source`, `url`, and
`retrieved` columns (ALVA attraction visits, VisitBritain/ONS inbound visits). Images must be
openly licensed, attributed, and contain no people. If a figure cannot be verified at its
source, stop and report rather than estimating it.

The water dataset (`examples/water/data/`) is real public data joined on DANE DIVIPOLA codes
by `scripts/build_dataset.py`; never generate synthetic data presented as real. One row is a
municipality × zone (urban/rural) × year. The INS open IRCA table (datos.gov.co `nxt2-39c3`)
corresponds to utility-supplied ("prestadores") IRCA, not INS's national total; label it so.
Profile features are clustered; outcomes (infant mortality, Saber 11, dropout) are only used
to describe clusters and are never clustered on. Cluster comparisons are descriptive:
state that they do not establish causal effects of water quality. Record missing sources as
TODOs with URLs rather than filling them.

The marketing workflow names inputs and deliverables on its opening content
slide. Inputs are `context/hillstrom.csv`, `notes.md`, and `sources.bib`.
Deliverables are `report.pdf`, `report.docx`, a runnable `report.ipynb`, and
`slides.html` with exactly eight slides including the title, plus sources,
unchanged inputs, and build instructions. Keep the brief, prompts, commands,
review criteria, README, and submission checklist consistent with this contract.

Build the reports from one `report.qmd`. Render PDF and DOCX with Quarto. For a
runnable notebook with saved results, use the tested conversion/execution route:

```bash
quarto convert report.qmd --output report.ipynb
jupyter nbconvert --to notebook --execute --inplace report.ipynb
```

Run from the lab root with the selected Python/Jupyter environment. Do not assume
`quarto render --to ipynb` preserves executable cells: the locally validated
Quarto 1.6.40 export can turn analysis code into Markdown. Check notebook cell
types, saved outputs, and execution from a fresh kernel. Include readable
reference links in notebook Markdown and verify bibliography rendering in PDF
and DOCX. Test changed instructional commands in a disposable workspace without
running a paid agent session. Official [conversion](https://quarto.org/docs/cli/convert.html)
and [notebook execution](https://nbconvert.readthedocs.io/en/latest/usage.html)
documentation checked 2026-10-07.

## New modules and custom sub-agent workflows

Before authoring a module, define audience, prerequisites, objectives, an exercise, and observable
completion criteria. Add the module to `_quarto.yml`, README, and relevant deck navigation.

When delegation is requested, use the following custom role contracts. If sub-agents are not
available, perform the same stages sequentially; do not claim independent review occurred.

1. Evidence reviewer: read-only inspection of sources; return supported claims, source locations,
   and gaps. No edits to generated output.
2. Module author: own one explicitly assigned `.qmd` and any agreed module-specific assets;
   return the draft, exercise, assumptions, and validation performed.
3. Render reviewer: inspect rendered slides and links; report defects by slide ID and viewport.
4. Lead integrator: own shared configuration, README, and final `docs/` generation; reconcile
   findings, verify scientific content, and run the full build after integration.

Give each delegated task a bounded file scope, expected output, and checks. Do not let multiple
agents write the same file or render concurrently into `docs/`. Use separate worktrees or output
directories if independent builds are required. Agent definition formats are tool-specific:
inspect the installed tool's official documentation before adding `.claude/agents/` or Codex
configuration. This role contract alone does not install or launch custom agents.

## Validation and generated output

Run `quarto render` and `git diff --check` after source/configuration changes. Inspect every
changed slide in a browser at desktop and laptop presentation sizes, and verify
links between both decks. Use viewports such as 1440 × 1000 for desktop, 1366 × 768 for
laptop, and 1280 × 720 for a projector, checking code wrapping and caption visibility.
Check executed output, captions, citations, math, and code overflow; a clean render alone is
insufficient. Test instructional commands in a disposable directory when their behavior changes.
Never run paid agent sessions merely to test a displayed command.

GitHub Pages serves `main:/docs`. Include rendered output with source changes when preparing a
commit. Do not hand-edit `docs/` or use `quarto publish gh-pages` for this repository. A failed
render can clean the output directory: fix the failure and re-render; do not commit missing
output or blindly restore over someone else's changes. `.gitignore` explicitly permits
`docs/site_libs/**` despite the generic `dist/` rule.

## Git and handoff

Work on a feature branch, preserve unrelated changes, and use `type(scope): lowercase description`
for commits when requested. Main is protected: do not force-push, bypass protection, or push
changes directly to main. For stacked PRs, integrate bottom-up and verify branch contents.

Report source changes, checks actually run, and any remaining limitations. Distinguish local
rendering from publishing. Do not commit, push, or publish unless the task authorizes it.
