# Quarto Workshop

Create reproducible content you can share with the world, using Quarto. In a hands-on
3 h 10 min session, participants turn plain-text Markdown into **docx, pdf, pptx, xlsx, a
website, a blog and a dashboard**, with a coding assistant (Claude Code or Codex) writing the
computations. The slides are the course resource: everything needed to follow along alone is
on them.

- **[Quarto workshop](https://project-delphi.github.io/quarto-workshop/)**: Part 1 builds a
  London tourist guide from Markdown to a published dashboard. Part 2 clusters Colombian
  municipalities by drinking-water risk and context, then publishes one analysis many ways.
- **[AI workflows](https://project-delphi.github.io/quarto-workshop/ai-workflows.html)**: an
  optional graduate lab built on a real randomized email-marketing experiment, with a report in
  PDF, DOCX and IPYNB, eight slides, and verified revisions.

## For attendees

Before the workshop, install [Quarto](https://quarto.org/docs/get-started/), Python, Git,
an editor, the [GitHub CLI](https://cli.github.com/) (signed in with `gh auth login`), and one
coding assistant ([Claude Code](https://code.claude.com/docs/en/setup) or
[Codex](https://github.com/openai/codex)). Then clone this repository next to your working
folders; it holds the checkpoints and the data:

```bash
git clone https://github.com/project-delphi/quarto-workshop.git
```

PDFs use Quarto's bundled Typst engine, so no LaTeX install is needed
(`quarto install tinytex` is the LaTeX alternative). Shell examples assume macOS, Linux, or WSL.

### How the slides work

Hands-on slides use three coloured boxes:

| Box | Meaning |
|---|---|
| 🤖 **Ask your coding assistant** (violet) | The exact prompt to paste |
| 👀 **Expect it to run** (amber) | Commands the assistant will probably run for you |
| ⌨️ **You type** (green) | The few commands and clicks you do yourself: accounts, `git push`, `quarto publish`, opening files |

Every exercise shows a ⏱️ time box and a ✅ "you're done when…" check. If you fall behind,
copy the matching checkpoint into your folder and carry on, for example:

```bash
cp -R quarto-workshop/checkpoints/02-london-qmd/. london-guide/
```

Part 2 checkpoints hold sources only, so copy the data first:

```bash
mkdir -p water-quality && cp -R quarto-workshop/examples/water/data water-quality/
cp -R quarto-workshop/checkpoints/07-water-cluster/. water-quality/
```

Prompts are examples, not transcripts: assistants vary, so check the rendered result and read
the diff.

### Agenda

| Time | Block |
|---|---|
| 0:00 | 👋 Welcome · 🎯 objective · 🏁 outcome |
| 0:05 | 🧭 What is Quarto? |
| 0:10 | 🛠️ Setup check |
| 0:15 | 📖 Read: [Markdown in Y minutes](https://learnxinyminutes.com/markdown/) |
| 0:20 | 🇬🇧 Part 1 · London: Markdown → HTML |
| 0:30 | 🧪 Part 1 · `.md` → `.qmd`: YAML, code, many formats |
| 0:40 | 🗂️ Part 1 · One guide, five audiences + dashboard |
| 0:50 | 🌍 Part 1 · Publish to GitHub Pages |
| 1:00 | 💧 Part 2 · Water quality in Colombian municipalities (130 min) |
| 3:10 | 🏁 Done |

## For instructors and contributors

| Path | Purpose |
|---|---|
| `index.qmd` | Workshop deck: Part 0 intro and setup; includes the two parts below |
| `slides/_london.qmd`, `slides/_water.qmd` | Part 1 and Part 2 slides, included from `index.qmd` |
| `ai-workflows.qmd` | Optional marketing-experiment lab on agent-assisted Quarto authoring |
| `examples/london/` | Finished Part 1 project: cited London data, guide, dashboard, audience versions, website |
| `examples/water/` | Finished Part 2 project: municipal water dataset, build pipeline, analysis and outputs |
| `checkpoints/` | The state after each hands-on step (no rendered output; water ones need `examples/water/data/`) |
| `assets/` | Hub and publishing diagrams (SVG) |
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
  emoji over words, notes for detail, the three agent boxes, ⏱️ and ✅ on every exercise.
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
