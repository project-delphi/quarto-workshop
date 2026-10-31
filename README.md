# Quarto Workshop

Create reproducible content you can share with the world, using Quarto. In a hands-on
3 h 20 min session (with a 10-minute break), participants turn plain-text Markdown into **docx, pdf,
pptx, revealjs slides, a website, a blog and a dashboard** (and, optionally, epub), with a coding assistant (Claude Code, Codex or Antigravity)
writing the computations. The slides are the course resource: everything needed to follow along alone is
on them.

- **[Quarto workshop](https://project-delphi.github.io/quarto-workshop/)**: Part 1 builds a
  London tourist guide from Markdown to a published dashboard. Part 2 clusters Colombian
  municipalities by drinking-water risk and context, then publishes one analysis many ways.
- **[AI workflows](https://project-delphi.github.io/quarto-workshop/ai-workflows.html)**: an
  optional 90-minute graduate lab built on a real randomized email-marketing experiment, with a
  report in PDF (Typst), DOCX and IPYNB, eight slides, and verified revisions.

## For attendees

Before the workshop, install [Quarto](https://quarto.org/docs/get-started/),
[uv](https://docs.astral.sh/uv/getting-started/installation/) (it brings Python), Git,
an editor, the [GitHub CLI](https://cli.github.com/) (signed in with `gh auth login`), and one
coding assistant ([Claude Code](https://code.claude.com/docs/en/setup),
[Codex](https://github.com/openai/codex) or Google's
[Antigravity CLI](https://antigravity.google/docs/getting-started?tab=cli), `agy`). Then clone this repository next to your working
folders; it holds the checkpoints and the data:

```bash
cd ~ && git clone https://github.com/project-delphi/quarto-workshop.git
```

Also before the workshop: run the setup check on the slides, do the 🧪 test run (your assistant
renders a tiny Quarto document with a Python calculation to HTML and PDF through `uv run`) and
tell the organiser it worked, and read
[Markdown in Y minutes](https://learnxinyminutes.com/markdown/). PDFs in both decks use
Quarto's bundled Typst engine, so no LaTeX install is needed. Each project creates its own
Python environment with uv during the workshop (one prompt, a few seconds), and its Quarto
and Python commands run through `uv run`. To follow the slides
in another language such as Spanish, use the
[Google Translate extension](https://chromewebstore.google.com/detail/google-translate/aapbdbdomjkkjkaonfhkkikfgjllcleb);
code blocks are marked not to be translated, and prompts are translated with the file
names, columns, options and commands in them kept in English. Shell examples assume
macOS, Linux, or WSL.

### How the slides work

Hands-on slides use three coloured boxes:

| Box | Meaning |
|---|---|
| 🤖 **Ask your coding assistant** (violet) | The exact prompt to paste |
| 👀 **Expect it to run** (amber) | Commands the assistant will probably run for you |
| ⌨️ **You type** (green) | The few things only you can do: start the assistant, sign in, approve its commands, run `quarto preview`, open results |

Every exercise shows a ⏱️ time box and a ✅ "you're done when…" check. 🏠 slides are
pre-work and ⭐ slides are optional and self-paced. Stuck for two minutes? Copy the
exercise's 😰 **Catch me up** prompt into your assistant, for example:

```text
Catch me up: follow ../quarto-workshop/checkpoints/02-london-qmd/README.md
```

Each checkpoint README lists the steps, which also work by hand from inside your project
folder: back up the folder to a new time-stamped `../<folder>-backup-NN-<time>` (earlier
backups are kept), copy the checkpoint in, copy the water `data/` if it is missing (Part 2
checkpoints hold sources only), render, check a named output, and rejoin at the slide the
README names. A checkpoint is the state at the end of its block, so it can be ahead of the
step you are on: skip the block's remaining prompts and follow the slides until the next ⏱️
block, where everyone is hands-on together again. The finished projects, `examples/london/`
and `examples/water/`, have the same catch-up section in their READMEs.

From Part 2's Cluster block on, the analysis has two routes. The normal 📤 route copies each
block's finished `scripts/analysis.py` from its checkpoint and spends the time on the pages;
the ⭐ challenge route writes the analysis with the ⭐ prompts. Both write the same
`outputs/`, so everyone builds the same report, slides, blog and dashboard.

Prompts are examples, not transcripts: assistants vary, so check the rendered result and read
the diff.

### Agenda

| Time | Block |
|---|---|
| 0:00 | 👋 Welcome · 🎯 objective · 🏁 outcome |
| 0:05 | 🧭 What is Quarto? |
| 0:10 | 🛠️ Setup check · 🧰 boxes · 🗣️ prompting (install, the test run and [Markdown in Y minutes](https://learnxinyminutes.com/markdown/) are pre-work) |
| 0:15 | 🇬🇧 Part 1 · London: Markdown → HTML, rules, environment |
| 0:35 | 🧪 Part 1 · `.md` → `.qmd`: YAML, code, docx + PDF |
| 0:45 | 🗂️ Part 1 · Four audiences, 🤖 sub-agents in parallel |
| 0:55 | 🌍 Part 1 · Publish to GitHub Pages |
| 1:05 | ☕ Break · 🛟 catch up |
| 1:15 | 💧 Part 2 · Colombia water quality and infant mortality (125 min) |
| 3:20 | 🏁 Done |

## For instructors and contributors

| Path | Purpose |
|---|---|
| `index.qmd` | Workshop deck: Part 0 intro and setup; includes the two parts below |
| `slides/_london.qmd`, `slides/_water.qmd` | Part 1 and Part 2 slides, included from `index.qmd` |
| `ai-workflows.qmd` | Optional marketing-experiment lab on agent-assisted Quarto authoring |
| `examples/london/` | Finished Part 1 project: cited London data, guide, dashboard, audience versions, website |
| `examples/water/` | Finished Part 2 project: municipal water dataset, build pipeline, analysis and outputs |
| `checkpoints/` | The state at the end of each hands-on block, with catch-up steps in each README (no rendered output; water ones need `examples/water/data/`) |
| `assets/` | Hub and publishing diagrams (SVG); `deck-3d/` builds the three.js bundle for the two 3-D slides in Part 2 |
| `theme.scss` | Dark theme additions: agent boxes, clocks, cards, previews, progress bar |
| `section-progress.html` | Coloured section progress bar and navigation |
| `_quarto.yml` | Explicit render list, execution defaults, shared Reveal.js settings |
| `examples/marketing-context/`, `examples/ai-context/` | Inputs for the AI workflows lab |
| `AGENTS.md` / `CLAUDE.md` | Repository instructions, slide conventions, data contracts, delegation roles |
| `environment.yml`, `environment-r.yml` | Python (and optional R) environment recipes |
| `docs/` | Committed rendered output; GitHub Pages serves `main:/docs` |

`examples/`, `checkpoints/` and `slides/` stay outside `project.render`; the examples and
checkpoints are rendered separately when they change.

### Build and preview

```bash
quarto render
quarto preview
# Or preview a single deck:
quarto preview ai-workflows.qmd
```

The deck executes Python. If you use this checkout's `.conda/` environment (built from
`environment.yml`), select it explicitly:

```bash
QUARTO_PYTHON="$PWD/.conda/bin/python" \
  JUPYTER_PATH="$PWD/.conda/share/jupyter" quarto render
```

Preview does not open a browser automatically: open the URL printed in the terminal.
Quarto 1.6.40 (with bundled Typst 0.11) is the locally validated baseline; dashboards and
Typst need Quarto ≥ 1.4.

The bottom bar divides the deck into coloured sections that match the agenda. The active
segment has a white marker, and a label shows the current section and its slide count. Click a
segment to jump to its start. Level-one headings start segments; `data-progress-label` on a
slide heading starts a task segment (used for the eight marketing turns).

### Editing and verification

- Follow the slide conventions in `AGENTS.md`: one concept per slide, ≤ ~30 words of prose,
  emoji over words, notes for detail, the three agent boxes, ⏱️ and ✅ on every exercise, and a
  😰 catch-up prompt naming a checkpoint README.
- Exercise times are planning estimates that leave each block a few minutes for showing
  results and recovering from a failed command. Rehearse with a stopwatch and keep the
  agenda slides, section clocks, exercise labels and this README consistent.
- Use executable `{python}` cells only for code that should run during rendering, and
  display-only fences for examples. Never run install, network, publish or agent commands
  while rendering.
- Every number on a slide is computed from committed data or carries a citation.
- Render the whole project, inspect every changed slide at 1280 × 720, 1366 × 768 and
  1440 × 1000, check links between both decks, and run `git diff --check`.

Re-render and include `docs/` alongside source edits. Do not hand-edit generated HTML or switch
this repository to `quarto publish gh-pages` (participants use that command for their own
repositories). A failed clean render can remove existing output; fix the failure and complete a
successful full render before delivering changes. The `.gitignore` exception for
`docs/site_libs/**` prevents the generic `dist/` rule from hiding Reveal.js assets.
