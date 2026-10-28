# Quarto Workshop

Build technical documents, Reveal.js slides, sites, and blogs by asking a coding agent in plain English.
Learn the Quarto commands and source syntax alongside the requests. The same prompts work with Claude Code, Codex, or Antigravity CLI.

- **[Quarto foundations](https://project-delphi.github.io/quarto-workshop/)** — four UCI wine-data tasks: introduction slides, a three-page essay, a runnable Jupyter notebook, and a separate blog, with explicit outputs and review checks.
- **[AI workflows](https://project-delphi.github.io/quarto-workshop/ai-workflows.html)** — a real marketing experiment covering email promotions, incremental sales, a report in PDF, DOCX, and IPYNB, eight slides, and verified revisions.

## Lab Setup (Admin)

English: On each Ubuntu WSL computer, copy this script to a working directory and run `./setup_wsl_es.sh` while connected to the internet, ahead of the workshop. This installs and downloads the main tools and repository before attendees arrive on a slow connection. The final `claude` command starts an interactive session.

Español: En cada equipo con Ubuntu en WSL, copie el script a un directorio de trabajo y ejecute `./setup_wsl_es.sh` con conexión a internet antes del taller. Así se instalan y descargan las herramientas principales y el repositorio antes de que lleguen los participantes con una conexión lenta. El comando final `claude` inicia una sesión interactiva.

## For attendees

Install [Quarto](https://quarto.org/docs/get-started/), Git, an editor, and one coding agent.
The [foundations source](index.qmd) shows installation of Claude Code, Codex,
and Google's Antigravity CLI. The instructions were checked against
[Claude Code documentation](https://code.claude.com/docs/en/setup) and
[Codex documentation](https://developers.openai.com/codex/cli/) on 2026-10-06,
and the [Antigravity CLI guide](https://antigravity.google/docs/getting-started?tab=cli)
on 2026-10-28.
Use a GitHub account and [GitHub CLI](https://cli.github.com/) when you reach publishing.
The foundations deck has an early agent-guided `gh auth login` step; verify the
intended account with `gh auth status` before creating a remote repository.
Shell examples assume macOS, Linux, or WSL on Windows.

Environment setup used to be a workshop bottleneck. Now the coding agent handles dependencies
and verifies the build; attendees focus on the source material and the resulting publication.
The existing environment recipes remain available for reproducibility.

### Learning through a conversation

Each major activity pairs **Ask your coding agent**, **Commands** (or a source pattern), and a
**Check**. Enter the prompt in a coding agent session opened in the exercise folder. The coding agent can
edit files and run tools there, subject to its permissions. Commands show what performs
the work and provide a manual route; do not rerun a scaffold command the agent already ran.

For example, ask: “Create hello.qmd, a short HTML page introducing Quarto. Show
a Markdown source example beside its rendered result and add a simple, self-contained Mermaid
graphic showing a .qmd file becoming HTML. Render it, fix build errors, and tell me
which file to open.” Then inspect both files and follow up:
“Add a reading list with a link to the Quarto guide. Render it again.”

The foundations tasks can span multiple sessions, beginning with short source exercises
and ending with review and optional blog publication. The 60-minute marketing lab uses
eight conversation turns, from inspecting evidence to reviewing the complete deliverable.
Its website and blog adaptations are optional extensions.
The marketing case uses Kevin Hillstrom's [published randomized email experiment](https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html)
(2008), with two-week customer purchase and spending outcomes. The classroom brief asks for a
campaign recommendation; campaign cost, margin, and long-term outcomes are unavailable.
Prompt examples are suggested tasks, not transcripts or guarantees of an agent's output.
See [official Codex prompting guidance](https://developers.openai.com/codex/prompting/)
and [CLI documentation](https://developers.openai.com/codex/cli/) (checked 2026-10-06).

### The directory method

1. Create a new local directory for one question or publication.
2. Move selected working copies of notes, raw data, and references into `context/`.
3. Launch `codex` or `claude` **inside that directory** and ask it to read the selected files.
4. Ask it to write `brief.md`: audience, question, inputs, outputs, and acceptance criteria. Review the brief.
5. Have the agent implement, render, inspect, and revise. Audit the evidence yourself.

The [wine context bundle](examples/wine-context/) supplies a local CSV copy of the
[UCI Wine recognition dataset](https://archive.ics.uci.edu/dataset/109/wine),
provenance notes, source records, and a worked notebook source, `notebook.qmd`.
Copy it into `~/code/quarto-play/context/` before starting the four tasks.
The 178 rows represent wine samples from three anonymous cultivars. The labels
are categories, not quality scores. The CSV was exported from scikit-learn 1.6.1
on 2026-10-21, with sample IDs added and target labels converted to UCI's 1–3.

### Four foundations tasks

The early `hello.qmd` / `hello.html` exercises teach source syntax. They do not
replace the runnable research Jupyter notebook required by Task 3.

| Task | Editable source | Required final output and check |
|---|---|---|
| 1. Wine chemistry introduction | `intro.qmd` | `intro.html`, exactly six Reveal.js slides including title and sources |
| 2. Evidence essay | `essay.qmd` | `essay.pdf`, exactly three pages including references, no separate cover |
| 3. Data Jupyter notebook | `notebook.qmd` | `notebook.ipynb`, executable from a fresh kernel with saved results |
| 4. Separate wine blog | Blog configuration and `posts/wine-chemistry/index.qmd` | `_site/index.html` linking to `_site/posts/wine-chemistry/index.html` |

Tasks 1–3 run in `~/code/quarto-play/` using the shared `context/` inputs.
The essay uses `context/wine.csv` for every numerical claim and cites its
provenance. It does not require the later Jupyter notebook.

```bash
quarto render intro.qmd --to revealjs
quarto render essay.qmd --to pdf
quarto convert notebook.qmd --output notebook.ipynb
jupyter nbconvert --to notebook --execute --inplace notebook.ipynb
```

The introduction addresses first-year data science students: title, the
mystery-cultivar question, samples and labels, two chemical features,
overlap and limits, and sources.
Use the dark Reveal.js theme and inspect all six slides on desktop and laptop.

The essay asks what wine chemistry can tell us about the three cultivars.
Use A4, 11-point text, and 1-inch margins. Page 1 covers the question,
provenance, and unit of analysis; page 2 covers alcohol and color intensity,
group summaries, and overlap; page 3 covers limits and references. Verify the
rendered three-page total rather than inferring it from a word count. Do not
present descriptive differences as measured prediction accuracy.

For Task 3, create the notebook from the worked source and fix paths to `context/`.
Include all 178 samples in a captioned alcohol-versus-color scatterplot and
report each cultivar's sample count, mean, median, and sample standard deviation
for both features. State that each row is one wine sample and explain the labels.
Add readable source links in notebook Markdown.

Task 4 starts in a separate `~/code/quarto-blog/` project and adapts the same
context into a website post. The blog does not replace Tasks 1–3. Before rendering,
restrict the blog's `_quarto.yml` to its intended pages and posts:

```yaml
project:
  type: website
  render:
    - index.qmd
    - about.qmd
    - posts/**/*.qmd
```

Preserve the rest of the generated configuration. Add any new public pages to
this list. Run `quarto render` and test the home-page listing and post navigation.
Check that `_site/context/notes.html` and `_site/context/notebook.html` are absent;
otherwise the copied context becomes extra website pages. See Quarto's
[render targets](https://quarto.org/docs/projects/quarto-projects.html#render-targets)
(checked 2026-10-19). Keep sources,
unchanged context inputs, and build instructions in each workspace. Use a suitable
local Python/Jupyter runtime and PDF engine, with the agent recording the actual
commands. Conversion, execution, and PDF guidance checked 2026-10-19 against
[Quarto conversion](https://quarto.org/docs/cli/convert.html),
[nbconvert execution](https://nbconvert.readthedocs.io/en/latest/usage.html), and
[Quarto PDF output](https://quarto.org/docs/output-formats/pdf-basics.html).

The [sample context bundle](examples/ai-context/) contains an optional synthetic runtime example. The active
[marketing context bundle](examples/marketing-context/) contains the original 64,000-customer
Hillstrom email experiment, a data dictionary and provenance notes, and a bibliography.
The marketing lab runs from this local CSV without downloading data during rendering.
Use the graduate module independently or after the foundations deck.

The marketing workflow states its inputs and outputs on its opening content slide:
`context/hillstrom.csv`, `notes.md`, and `sources.bib` become `report.pdf`,
`report.docx`, `report.ipynb`, and an eight-slide `slides.html`, with editable
`.qmd` sources and build instructions. Create the report from one source and run:

```bash
quarto render report.qmd --to pdf
quarto render report.qmd --to docx
quarto convert report.qmd --output report.ipynb
jupyter nbconvert --to notebook --execute --inplace report.ipynb
quarto render slides.qmd --to revealjs
```

These commands run in the attendee's marketing workspace. Ask the agent to inspect
available tools and prepare Python/Jupyter and a PDF engine as needed. Inspect
PDF page layout, DOCX figures and tables, and notebook cells and saved results.
Use `quarto convert` to preserve runnable cells, then `nbconvert` to execute
and save the notebook results. Restart its kernel and run all cells from the lab
root, then compare all formats. Include readable reference links in its Markdown. Format guidance: [PDF](https://quarto.org/docs/output-formats/pdf-basics.html),
[Word](https://quarto.org/docs/output-formats/ms-word.html), and
[notebook conversion](https://quarto.org/docs/cli/convert.html), checked 2026-10-07.

### Publishing your own blog

After reviewing and committing your blog, create its remote repository and publish:

```bash
gh auth login
gh repo create my-blog --public --source=. --push
quarto publish gh-pages
```

Use these in **your blog's directory**. Check the repository's Pages settings and deployment
status if needed. This workshop repository uses a different publishing mechanism, described below.
The foundations deck also shows how to ask your coding agent to prepare publication, review the destination,
then explicitly authorize the commit, remote creation, push, and publication.

## For instructors and contributors

| Path | Purpose |
|---|---|
| `index.qmd` | Foundations deck |
| `ai-workflows.qmd` | Marketing experiment lab on agent-assisted Quarto authoring |
| `_quarto.yml` | Explicit render list, execution defaults, shared Reveal.js settings |
| `slides.css` | Shared responsive content styling and reduced-motion support |
| `section-progress.html` | Shared colored section/task progress and navigation |
| `examples/wine-context/` | UCI Wine CSV, provenance notes, references, and worked notebook; outside the render list |
| `examples/marketing-context/` | Public Hillstrom promotion experiment and provenance; outside the render list |
| `examples/ai-context/` | Preserved optional synthetic runtime inputs; outside the render list |
| `AGENTS.md` | Repository instructions, review criteria, and delegation conventions |
| `CLAUDE.md` | Imports the shared agent instructions |
| `environment.yml`, `environment-r.yml` | Optional Python and R environment recipes |
| `docs/` | Committed rendered output; GitHub Pages serves `main:/docs` |

### Build and preview

```bash
quarto render
quarto preview
# Or preview a single module:
quarto preview ai-workflows.qmd
```

The teaching decks target desktop computers and modern laptops. Shared configuration
uses fast fade transitions, code copying, and explicit execution settings. Computations run on project builds; errors stop the build.
The bottom bar divides each deck into colored sections, with a white marker for the
active segment and a label showing the current section/task and its slide count.
Click a segment or focus it and press Enter to jump to its start. Segment widths
reflect slide counts, not elapsed time or completed exercises. Level-one section
headings start segments automatically; `data-progress-label` on a slide heading
starts a task segment (used for the eight marketing turns). The bar updates when
navigating backward or opening a slide link directly.
Preview does not open a browser automatically: open the URL printed in the terminal.
Quarto 1.6.40 is the locally validated baseline; use a current supported release for teaching.

The foundations deck executes a Python cell. Ask the agent to prepare a local Python/Jupyter
runtime and record how to use it. If reusing this checkout's existing environment, the explicit
build invocation is:

```bash
QUARTO_PYTHON="$PWD/.conda/bin/python" \
  JUPYTER_PATH="$PWD/.conda/share/jupyter" quarto render
```

This assumes `.conda/` has already been created from `environment.yml`. A virtual environment
with Jupyter and the required packages works too; no particular environment manager is required.

### Editing and verification

- `#` creates a section slide, `##` a content slide, and `### Exercise` an exercise within a slide.
- Keep one main idea per slide. Split dense content before applying `{.smaller}`.
- Use executable `{python}` cells only for code that should run during rendering.
  Use display-only `{.python}` or `python` fences for examples.
- To display executable cell syntax, use `{{python}}` inside a longer outer Markdown fence.
  A longer fence alone does not prevent Quarto from executing the nested cell.
- Recheck progressive `code-line-numbers` ranges after editing examples.
- Add each new deck to `project.render` and link it from the README and a relevant slide.
- Render the whole project, inspect both decks at desktop and laptop presentation sizes,
  check internal links, and run `git diff --check`.

Re-render and include `docs/` alongside source edits. Do not hand-edit generated HTML or switch
this repository to `quarto publish gh-pages`. A failed clean render can remove existing output;
fix the failure and complete a successful full render before delivering changes.

`embed-resources: true` bundles deck resources, but Quarto may still emit shared `site_libs/`
assets. Keep generated dependencies together; external links still require network access.
The `.gitignore` exception for `docs/site_libs/**` prevents the generic `dist/` rule from hiding
Reveal.js assets.
