# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-deck Quarto workshop presentation teaching Quarto itself. All slide content lives in `index.qmd`
(reveal.js format, defined in that file's YAML header, not in `_quarto.yml`). Published at
https://project-delphi.github.io/quarto-workshop/

## Commands

```bash
conda env create -f environment.yml -p "$PWD/.conda"   # first-time setup
conda activate "$PWD/.conda"

quarto preview index.qmd    # live-reload while editing slides
quarto render               # writes docs/ (output-dir set in _quarto.yml)
```

`_quarto.yml` carries a `render:` list limiting the build to `index.qmd`. Without it the website
project also renders `README.md` and `CLAUDE.md` into `docs/`. A failed render (usually: env not
activated) leaves `docs/` deleted rather than untouched — `git checkout -- docs` to recover.

There are no tests or linters.

## Build output

`_quarto.yml` sets `output-dir: docs`, and GitHub Pages serves from `main:/docs` — so rendered output is
committed, not ignored. Re-render and commit `docs/` in the same change as any `index.qmd` edit.

Because `index.qmd` sets `embed-resources: true`, `docs/index.html` is a fully self-contained ~3.7MB file;
that alone is what the published site needs. `docs/site_libs/` is also tracked (45 files) but vestigial —
`quarto render` rewrites some of it every time, so expect incidental churn there.

Gotcha: `.gitignore` line 13 is `dist/` (inherited from GitHub's Python template) and it matches
`docs/site_libs/revealjs/dist/`. Those files are only in the index because they predate the rule; `git add`
skips them silently. Use `git add -f` if they genuinely need updating.

## Editing slides

- `##` starts a new slide; `#` starts a section slide. `{.smaller}` after a heading shrinks dense slides.
- The deck teaches code-block syntax, so it contains both *executed* blocks (```` ```{python} ````) and
  *display-only* blocks (```` ```{.python} ````). The leading dot is meaningful — changing one to the other
  changes whether code runs at render time. Blocks demonstrating `#|` options are deliberately display-only.
- `code-line-numbers="1|2|3"` drives progressive line highlighting; the ranges must match the block's actual
  lines, so re-check them after adding or removing a line.
- Content is exercise-driven: most sections end with an `### Exercise` heading. Keep that shape when adding
  material.

## Conventions

Commit messages are `type(scope): lowercase description`; the repo uses `feat`, `fix`, `chore`, `refactor`,
plus local types `update` and `cruft` (removing dead files). Work on branches (`rk/slides` style), never
directly on `main`.

`main` is a protected branch, enforced for admins: no direct pushes, no force pushes, no deletion. Changes
reach it through a PR (self-merge is fine, no approval required). `.claude/settings.json` denies the
matching git commands locally as a first line of defence, but GitHub is what actually enforces it.

When several PRs are stacked, merge them strictly bottom-up. Merging a child into its stacked parent after
the parent has already merged to `main` silently strands the child's work on a branch no longer in `main`'s
path — verify by diffing branch contents, not by trusting merged/closed status.
