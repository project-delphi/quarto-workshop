# Repository instructions

## Scope and architecture

This repository is a Quarto website containing Reveal.js teaching decks. Read `_quarto.yml`,
`README.md`, and the affected `.qmd` files before editing. `index.qmd` teaches foundations;
`ai-workflows.qmd` teaches graduate-level agent-assisted authoring. Preserve the dark theme
and exercise-driven structure. The main learning path delegates dependency setup to agents;
do not reintroduce lengthy Conda or kernel troubleshooting lessons.

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

The foundations deck executes Python through Jupyter. Inspect the existing runtime before
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
changed slide in a browser, including narrow/mobile view, and verify links between both decks.
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
