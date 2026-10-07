# Quarto Workshop

Build technical documents, Reveal.js slides, sites, and blogs by asking a coding agent in plain English.
Learn the Quarto commands and source syntax alongside the requests. The same prompts work with Claude Code or Codex.

- **[Quarto foundations](https://project-delphi.github.io/quarto-workshop/)** — a continuing coding agent conversation that builds a CRISPR-Cas9 research notebook and blog with executable code, research notes, and primary references, then prepares publication.
- **[AI workflows](https://project-delphi.github.io/quarto-workshop/ai-workflows.html)** — a real marketing experiment covering email promotions, incremental sales, a report in PDF, DOCX, and IPYNB, eight slides, and verified revisions.

## For attendees

Install [Quarto](https://quarto.org/docs/get-started/), Git, an editor, and one coding agent.
The [foundations source](index.qmd) shows installation of both agents, verified against
[Claude Code documentation](https://code.claude.com/docs/en/setup) and
[Codex documentation](https://developers.openai.com/codex/cli/).
Use a GitHub account and [GitHub CLI](https://cli.github.com/) when you reach publishing.
Shell examples assume macOS, Linux, or WSL on Windows.

Environment setup used to be a workshop bottleneck. Now the coding agent handles dependencies
and verifies the build; attendees focus on the source material and the resulting publication.
The existing environment recipes remain available for reproducibility.

### Learning through a conversation

Each major activity pairs **Ask your coding agent**, **Commands** (or a source pattern), and a
**Check**. Enter the prompt in a coding agent session opened in the exercise folder. The coding agent can
edit files and run tools there, subject to its permissions. Commands show what performs
the work and provide a manual route; do not rerun a scaffold command the agent already ran.

For example, ask: “Create hello.qmd, a short HTML page introducing Quarto. Render it,
fix build errors, and tell me which file to open.” Then inspect both files and follow up:
“Add a reading list with a link to the Quarto guide. Render it again.”

The foundations session takes 165 minutes including exercises and discussion. The
60-minute marketing lab uses eight conversation turns, from inspecting evidence to
reviewing the complete deliverable. Website and blog adaptations are optional extensions.
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

The [CRISPR-Cas9 context bundle](examples/crispr-context/) supplies synthetic target-site
read counts, interpretation notes, two primary references, and a complete executable
`notebook.qmd`. Copy it into a separate workspace before rendering or adapting it
into a blog post. The counts illustrate indel-fraction reporting and are not experimental
results from the cited papers.

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
| `examples/crispr-context/` | Synthetic CRISPR-Cas9 counts, notes, references, and worked notebook; outside the render list |
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
