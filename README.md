# Quarto Workshop

A hands-on workshop on [Quarto](https://quarto.org): write markdown, execute code inside it, and publish a
blog to GitHub Pages.

**Slides:** https://project-delphi.github.io/quarto-workshop/

By the end you will have a live blog, built from `.qmd` source, with a post whose charts are generated from
code every time it renders.

---

## For attendees

### Do this before the workshop

The environment is the slowest part and the most common place to get stuck. Getting it done in advance is
the single best thing you can do.

Install:

| Tool | Notes |
|---|---|
| [Quarto](https://quarto.org/docs/get-started/) | The binary, not the pip package |
| [GitHub CLI](https://cli.github.com) (`gh`) | Used to create the repo and publish; run `gh auth login` |
| Conda | [Miniconda](https://docs.conda.io/projects/miniconda/) is fine |
| Git | Configured with your name and email |
| VSCode | Plus the Quarto extension |
| A GitHub account | |

You need a POSIX shell: macOS, Linux, or **WSL2** on Windows — not git bash, PowerShell or cygwin. On
Windows, run `wsl --install`, then install everything above *inside* WSL and work from your Linux home
directory, not `/mnt/c` (rendering across the filesystem boundary is slow and hits permission errors).

Then check it all worked:

```bash
quarto --version && gh auth status && conda --version
```

### Set up the environment

```bash
curl -fsSL -o environment.yml \
  https://raw.githubusercontent.com/project-delphi/quarto-workshop/main/environment.yml
head -3 environment.yml   # expect YAML, not "<!DOCTYPE html>"
conda env create -f environment.yml -p "$PWD/.conda"
conda activate "$PWD/.conda"
```

Takes about two minutes. It is Python-only — R is a separate, optional environment
(`environment-r.yml`) used by the RStudio section, so you do not pay for it unless you want it.

That `head -3` is worth actually running. If a download fails, `curl -o` will happily save the error page
under the right filename and the next command fails with a confusing YAML error.

### Checkpoint

Do not move past this until all four look right:

```bash
which quarto                 # a path, not "not found"
quarto check                 # Python and Jupyter both OK
which python                 # .../.conda/bin/python, inside your project
jupyter kernelspec list      # python3 -> your .conda, not some other project
```

### If you get stuck

Clone a known-good blog and rejoin the session — sort your environment out afterwards, in the break. Do not
spend the workshop debugging conda while everyone else is writing posts.

```bash
git clone https://github.com/project-delphi/quarto-blog-starter my-blog
cd my-blog
conda env create -f environment.yml -p "$PWD/.conda"
conda activate "$PWD/.conda"
quarto preview
```

It contains a post with an executing `{python}` cell, so if it renders a chart, your whole toolchain works —
Quarto, Python **and** the Jupyter kernel.

### Common errors

| You see | It means | Do this |
|---|---|---|
| `quarto: command not found` | Not installed, or env not activated | `which quarto`, then `quarto check` |
| `CondaError: Run 'conda init'` | Shell not set up for conda | `conda init "$(basename $SHELL)"`, restart shell |
| `conda env create` fails parsing YAML | You downloaded an error page, not the file | `head -3 environment.yml` |
| `ModuleNotFoundError` for a package you *know* is installed | A user-level Jupyter kernel is shadowing your env | `jupyter kernelspec list`; prefix with `JUPYTER_PATH="$PWD/.conda/share/jupyter"` |
| `Address already in use` on preview | An old preview is still running | `quarto preview --port 4201` |
| `gh: please run: gh auth login` | Not authenticated | `gh auth login` |
| Published but 404s | Pages is still building | Wait a minute, check the repo's Actions tab |

The fourth row is the sneaky one: the package really is installed, just not in the interpreter Quarto is
using.

### Publishing your blog

Publishing is a **command**, not configuration — there is no `publish:` key in `_quarto.yml`:

```bash
gh repo create my-blog --public --source=. --push
quarto publish gh-pages
```

Quarto renders, creates the `gh-pages` branch, adds `.nojekyll`, pushes, and prints your URL.

---

## For instructors

### Repo layout

| Path | What it is |
|---|---|
| `index.qmd` | The entire deck. reveal.js format is set in this file's YAML header, not `_quarto.yml` |
| `_quarto.yml` | Project type and `output-dir: docs`, plus a `render:` list limiting the build to the deck |
| `environment.yml` | Slim Python environment, also what attendees download |
| `environment-r.yml` | Optional R environment for the RStudio section |
| `docs/` | Rendered output, committed — GitHub Pages serves `main:/docs` |
| `CLAUDE.md` | Notes for Claude Code |

### Building

```bash
conda activate "$PWD/.conda"
quarto render          # writes docs/
quarto preview         # live reload while editing
```

The deck contains an executing `{python}` cell, so rendering needs the environment active — a bare
`quarto render` outside it fails on a missing Jupyter.

Re-render and commit `docs/` in the same change as any `index.qmd` edit. Pages serves whatever is in
`main:/docs`, so an un-rendered edit silently publishes nothing. Note this is a different mechanism from
the `quarto publish gh-pages` flow the workshop teaches — don't mix them up.

### Editing the deck

- `##` starts a slide, `#` a section slide; `{.smaller}` after a heading shrinks dense ones.
- The deck teaches code-block syntax, so it deliberately contains both executed blocks (`` ```{python} ``)
  and display-only ones (`` ```{.python} ``). The leading dot decides whether code runs — changing one to
  the other changes behaviour, not just formatting.
- To *show* cell syntax without executing it, write `{{python}}`. A longer outer fence is not enough;
  Quarto's cell scanner finds the nested block and runs it anyway.
- `code-line-numbers="1|2|3"` drives progressive highlighting and refers to *physical* lines. Re-check the
  ranges after adding or removing a line, including line continuations.
- Most sections end in an `### Exercise`. Keep that shape.

### Known quirks

- **`.gitignore` and `docs/`** — the inherited Python template has a `dist/` rule that also matches
  `docs/site_libs/revealjs/dist/`. There is a negation for `docs/site_libs/**` further down; if output
  files mysteriously will not stage, check `git check-ignore -v <path>`.
- **A failed render empties `docs/`** — Quarto cleans the output directory before it builds, so if the
  render dies (most often: environment not activated) you are left with a deleted `docs/`, not the previous
  build. It is only ever a `git checkout -- docs` away, but do not commit in that state.
- **`site_libs` churn** — the deck is `embed-resources: true`, so `docs/index.html` is a self-contained
  ~3.6MB file and is all the published site needs. `docs/site_libs/` is also tracked but vestigial, and
  renders rewrite parts of it. Incidental churn there is expected.
