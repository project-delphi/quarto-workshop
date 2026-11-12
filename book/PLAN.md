# Book plan: *One Source, Every Format*

Status: **approved** (2026-11-12), with the decisions in §10; built, with the changes in §11.

This plan turns the 6-hour workshop deck (`index.qmd` with `slides/_london.qmd` and
`slides/_water.qmd`), its long-form pages and its Markdown guides into one Quarto book
project under `book/`. The project builds an EPUB 3 (the main edition) and an HTML book
(the companion where everything interactive runs) from the same chapter sources.

## 1. What I read, and what a quick spike showed

Read in full or in depth: `README.md`, `INSTRUCTOR.md`, `CHEATSHEET.md`,
`TROUBLESHOOTING.md`, `AGENTS.md`, `_quarto.yml`, `index.qmd`, `slides/_london.qmd`, the
prose and notes of `slides/_water.qmd` (its long compute cells skimmed), `windows-setup.qmd`
(outline and opening), the outline and opening of `ai-workflows.qmd`, the checkpoint
READMEs (02 and 07 in full, all folders listed), `examples/london/` and `examples/water/`
(READMEs and `_quarto.yml`), `assets/deck-3d/` (README, `main.js`, the Reveal hooks in
`stage.js`), `section-progress.html`, `ps-player.html`, `assets/short-player.js`,
`translate-safe.html`, `slide-spacing.html` and the box styles in `theme.scss`.

Before planning I built a throwaway five-file book in the scratchpad with Quarto 1.10.20
(the version installed here) to check how book features come out in EPUB. These results
drive several decisions below:

| # | Finding (Quarto 1.10.20, EPUB) | Consequence for the plan |
|---|---|---|
| S1 | `part:` entries in `book.chapters` are **dropped from the EPUB**: neither the part title nor a part page's content appears, and the EPUB TOC is flat | Part pages become ordinary unnumbered chapters in the EPUB build, and a post-render step nests chapters under their part in `nav.xhtml` and `toc.ncx` (§6.3) |
| S2 | A profile file's `book.chapters` is **concatenated with** the base list, not substituted for it | The base `_quarto.yml` holds no chapter list. One canonical list (`_chapters.yml`) generates `_quarto-html.yml` (with `part:` grouping) and `_quarto-epub.yml` (flat, part pages included). `make book` regenerates both and fails if they drift |
| S3 | `when-format="html"` **also matches EPUB** | HTML-only content uses `when-format="html:js"` (checked: it excludes EPUB); EPUB-only uses `when-format="epub"` |
| S4 | Rendering one format of a book **empties `_book/`** (the HTML from an earlier render disappeared) | Each profile has its own output directory: `_book/html/` and `_book/epub/` |
| S5 | Callouts survive in EPUB as classed `div`s with a bold title and inline CSS; the icon element is empty | The four aside types are Quarto callouts with fixed titles and classes, styled in `epub.css` (§5.3) |
| S6 | `code-annotation` in EPUB becomes a definition list ("Line 1", "Line 2") below the code, with no markers in the code itself | Usable; styled in `epub.css`. Use it for short excerpts; for longer code, numbered notes in prose (§5.4) |
| S7 | `@sec-` and `@fig-` cross-references resolve across chapter files ("Chapter 1", "Figure 1.1") | Use them freely |
| S8 | Pandoc writes a title page and `landmarks` (title page, TOC) but no copyright or body-matter landmark | The post-render step adds them (§6.3) |
| S9 | The figure wrapper is `<div ... alt="...">`; `alt` is not allowed on `div` in XHTML | Expect an epubcheck error; the post-render step removes the attribute (the `img` keeps its alt text) |
| S10 | EPUB's default image extension is `png` | Extensionless image paths let HTML use SVG and EPUB use PNG from one source (§5.5) |

Also relevant from the repo:

- The three.js bundle (`assets/deck-3d.min.js`) starts only when `window.Reveal` exists and
  drives views from Reveal fragments. Outside the deck it needs a small Reveal-like host
  (`book/assets/deck-host.js`, §4). The bundle itself stays unchanged.
- `tunja-explorer.js` has no Reveal dependency and should run on a plain page.
- `.gitignore` ignores `build/`, `parts/`, `lib/`, `dist/` and `downloads/`, so `book/`
  must not use those folder names (hence `part-1.qmd`, not `parts/`).
- The repository has **no licence file**, so the book's rights statement needs a decision
  (open question 1).
- `assets/pelicans/README.md` and the slide notes say no licence is stated on the pelican
  images (open question 5).
- Tools: `ffmpeg`, `gifsicle`, `node`, `uv`, Java 11 and Playwright's Chromium 1243 cache are
  present. `epubcheck`, `vhs`, `asciinema`/`agg`, Calibre and a Python Playwright package are
  not (open question 6).

## 2. Audience, objectives and completion criteria

AGENTS.md asks for these before a new module is written.

- **Audience:** researchers, analysts and students who are new to Quarto and to coding
  assistants, many with little terminal experience. The same readers as the workshop, now
  reading alone.
- **Prerequisites:** a computer they can install software on, a GitHub account, and access
  to one coding assistant (paid plan or API key). No programming is assumed; the Python is
  explained but written by the assistant.
- **Objectives:** a reader can (1) explain how Quarto turns one source into many formats,
  (2) direct a coding assistant safely: scope, rules, prompts and checks, (3) build and
  publish the London guide and the water-safety site, and (4) predict and verify which
  outputs a changed input updates.
- **Exercises:** every hands-on chapter ends at a checkpoint; each part ends with an
  exercise set that maps to `checkpoints/` and a rebuild task with no supplied prompt.
- **Observable completion:** the same as the workshop's: two published sites and two
  explained rebuilds. The book adds one more check: the reader can say which edition (EPUB or
  HTML) shows each interactive figure, and why.

## 3. Table of contents and where everything goes

Chapter numbers run continuously across parts. Each chapter has an opening paragraph (what
and why), the body, a **Summary**, and **Further reading** with verified links. Slide IDs
refer to the deck (`index.qmd`, `#/slide-id`).

Length estimate: about 50,000–60,000 words, roughly 150–190 screens at an e-reader's default
size. This is an estimate, not a target. Chapters will be as long as their content warrants.

### Front matter (unnumbered)

| File | Content | Sources |
|---|---|---|
| cover | Typographic cover, 1600 × 2560 PNG from `media/cover.svg` | new |
| title page | Pandoc's EPUB title page from metadata (EPUB); Quarto's title block (HTML) | `_quarto.yml` metadata |
| `copyright.qmd` | Rights, edition and date, versions validated (Quarto 1.10.20 with Typst 0.15), an AI usage statement written the way the book teaches it, a summary of data licences, and the HTML edition URL | `#ai-use-deck`, `examples/*/data/README.md` |
| `index.qmd` · **Preface: How to Use This Book** | Who it is for; the two running examples; how the hands-on boxes and asides work; **two paths**: self-paced (chapter order) and workshop-paced (the 6-hour agenda mapped to chapters, breaks included); falling behind (checkpoints, the two-minute rule, a catch-up flow diagram); the HTML edition vs the EPUB; versions and verification dates | `#agenda`, `#objective`, `#expected-outcomes`, README "How the slides work", INSTRUCTOR §1 and §3, `#london-story`, `#catch-up-drill` |

### Part I · Foundations

Part page: a short introduction and a "Where we are" roadmap figure.

| Ch | Title | Sections | Sources (slides / docs) |
|---|---|---|---|
| 1 | **Publishing That Rebuilds Itself** | 1.1 Why reports drift: copy and paste. 1.2 What Quarto is: Markdown, a code engine (Jupyter or knitr), then Pandoc or Typst; **pipeline diagram**. 1.3 Quarto is not AI: deterministic rendering vs the assistant that writes files. 1.4 Reproducible: one source, computed numbers, one command, versioned; reproducible ≠ correct. 1.5 When Quarto is the wrong tool (trade-offs, stated as judgement and cited where possible) | `#quarto-hub`, `#quarto-not-ai`, `#reproducible`, `#objective`, `#expected-outcomes` |
| 2 | **Working With a Coding Assistant** | 2.1 Model + harness = assistant; **agent loop diagram** (human ↔ harness ↔ model, files and commands, approval gate). 2.2 Choosing an assistant and a model: pick by task; dated price bands in a sidebar; the pelican experiment as evidence and its limits. 2.3 What a conversation costs: tokens, context, `/model`, `/clear`, `/exit`. 2.4 The root folder is the assistant's world: trust, scope, one assistant per folder. 2.5 Rules that persist: `AGENTS.md` (the concept; Chapter 4 uses it). 2.6 Prompting: specific, one step, run and check, read the diff; prompts are engineered; ask when unsure; a web chat can draft a prompt (GIF). 2.7 How to read this book's assistant boxes. 2.8 Using AI in research: say it, own it | `#model-harness`, `#assistant-makers`, `#model-choice`, `#slash-commands`, `#pelican-grid`, `#root-folder`, `#agents-md`, `#how-to-prompt`, `#prompts-engineered`, `#chat-drafts-prompt`, `#three-boxes`, `#ai-policy`, `#ai-use-deck` |
| 3 | **Setting Up Your Machine** | 3.1 Before you start: connection, accounts, where to get help (an AI chat; your group's help channel). 3.2 Step 1: get the computer ready (Mac and Linux here; Windows in Appendix A). 3.3 Step 2: move around the terminal (VHS GIF); two places to type. 3.4 Step 3: install an assistant, with its first screens as text transcripts. 3.5 Step 4: the assistant installs the tools. 3.6 Step 5: the setup check. 3.7 Step 6: the test run, a black box that prints 42. Ends with a checklist exercise | `#setup-map`, `#internet`, `#ask-ai-chat`, `#computer-ready`, `#terminal-basics`, `#two-places`, `#install-assistant`, `#assistant-screens`, `#install-tools`, `#setup-check`, `#test-run`; README pre-work; TROUBLESHOOTING §0 |

### Part II · One Guide, Many Audiences: London

Part page: the tourism-office brief, the folder layout, and the roadmap figure.

| Ch | Title | Sections | Checkpoint | Sources |
|---|---|---|---|---|
| 4 | **Markdown, Rendering and Project Rules** | 4.1 The brief: write once, reuse everywhere. 4.2 Headings, paragraphs and emphasis. 4.3 Render it and keep a live preview (GIF). 4.4 Rules for the guide: `AGENTS.md` in practice. 4.5 Lists; links, images and quotes (alt text and credits); a table from cited data; code fences. 4.6 Environments then and now: uv and lockfiles (GIF). 4.7 When you fall behind: catching up (GIF) | 01 | `#london-story`, `#md-heading` … `#md-code-fence`, `#md-render`, `#london-agents`, `#read-markdown`, `#environments`, `#london-env`, `#catch-up-drill` |
| 5 | **Documents That Compute** | 5.1 YAML front matter. 5.2 Code that runs: cells and inline code (executed: the top attraction sentence). 5.3 Cell options: labels, captions, alt text, cross-references (executed: the ALVA bar chart). 5.4 One source, three formats: HTML, Word, Typst PDF (**diagram** + GIF). 5.5 Three more: PowerPoint, EPUB, Reveal.js (optional); this book is the EPUB case. 5.6 What happens during a render, and why a preview and a render collide | 02 | `#yaml`, `#code-cells`, `#cell-options`, `#formats`, `#formats-more`; TROUBLESHOOTING §2 |
| 6 | **One Guide, Five Audiences** | 6.1 Content once, format per audience: dashboard, Word brief and email, A5 flyer, square ad, website. 6.2 Sub-agents: one lead, many hands (**diagram**: lead, three sub-agents, one file each); costs and when not to. 6.3 One prompt, three audiences (long prompt box). 6.4 The square ad (optional): a raw Typst page size. 6.5 The sights in 3-D: live in HTML, GIF in EPUB; asking for three.js; when a 3-D chart misleads | 04 | `#audiences`, `#sub-agents`, `#audiences-do`, `#london-social`, `#london-map`, `#threejs-prompt` |
| 7 | **Publishing and Proving the Rebuild** | 7.1 Git: every change, safely (**cycle diagram**). 7.2 GitHub Pages and static hosting (redrawn flow diagram; hosts table, dated). 7.3 One folder, one website. 7.4 Publish: the first publish is yours; later updates can be the assistant's. 7.5 Change one input and explain the rebuild (**dependency diagram**; no prompt given). 7.6 A white paper (optional): Typst, citations, cross-references | `examples/london` | `#git-cycle`, `#gh-pages`, `#london-website`, `#london-publish`, `#free-hosts`, `#london-change`, `#london-whitepaper`, `#london-sources`; TROUBLESHOOTING §1; INSTRUCTOR §5 |
| — | **Exercises for Part II** | One exercise per hands-on block, each with its checkpoint, catch-up line, observable "done when" and the rejoin point; the no-prompt rebuild task (answers in Appendix E) | 01, 02, 04, `examples/london` | checkpoint READMEs |

### Part III · One Analysis, Many Publications: Colombian Water

Part page: the question, the unit of analysis (municipality × zone × year) and the roadmap figure.

| Ch | Title | Sections | Checkpoint | Sources |
|---|---|---|---|---|
| 8 | **The Question, the Data and the Rules** | 8.1 Why drinking water: the IRCA risk scale and the INCA 2023 national figures; the utility-supplied ("prestadores") caveat. 8.2 Two measures: IRCA and Saber 11. 8.3 Where the data come from and how they join (DIVIPOLA). 8.4 The question; features vs outcomes, and why clustering on outcomes is circular. 8.5 Compute once, publish many (redrawn **diagram**). 8.6 Rules and environment for the analysis | 05 (start) | `#water-why`, `#water-measures`, `#water-data-origin`, `#water-dataset`, `#water-question`, `#water-features`, `#water-compute-once`, `#water-deliverables`, `#water-agents`, `#water-env`; `examples/water/data/README.md` |
| 9 | **Look Before You Model** | 9.1 What exploring is for. 9.2 Rural: less data, more risk (executed figure). 9.3 One municipality up close: Tunja (live explorer in HTML; static panels in EPUB). 9.4 Building `explore.qmd` | 05 | `#water-explore-what`, `#water-bands`, `#water-tunja`, `#water-explore-do` |
| 10 | **From Table to Features** | 10.1 Select, transform, impute (with flags), standardise within year. 10.2 What we keep (executed table). 10.3 Why scale: one feature's share of the distance (executed). 10.4 Building `prepare()` (prompt boxes; an annotated excerpt of `analysis.py`) | 06 | `#water-prepare-steps`, `#water-prepare-counts`, `#water-scaling`, `#water-prepare-do`, `#water-prepare-do-2` |
| 11 | **Finding Kinds of Places: k-Means** | 11.1 k-means in four steps (GIF; static small multiples computed from the toy points). 11.2 Choosing k: elbow, silhouette, stability; k as a judgement call. 11.3 A picture of the clusters: PCA in 2-D (executed) and 3-D (GIF). 11.4 Where the clusters stand: the relief map (GIF). 11.5 Use the model, or build it: the two routes. 11.6 The clusters page | 07 | `#water-kmeans`, `#water-pca`, `#water-pca-3d`, `#water-relief`, `#water-routes`, `#water-cluster-do`, `#water-cluster-page` |
| 12 | **Interpreting Clusters** | 12.1 What sets each cluster apart (heatmap). 12.2 Name them by a rule. 12.3 Outcomes by cluster, and in SD units. 12.4 Every variable, cluster by cluster (menu in HTML; key panels in EPUB). 12.5 Building the outcome rules, profiles and the page. 12.6 Explorations in 3-D (optional; live in HTML, a still contact sheet in EPUB) | 08 | `#water-heatmap`, `#water-names`, `#water-outcomes`, `#water-outcome-heatmap`, `#water-compare`, `#water-interpret-use`, `#water-outcome-rules`, `#water-interpret-do`, `#water-interpret-page`, `#water-meta-*` |
| 13 | **Correlation Is Not Causation** | 13.1 Worse water, more infant deaths? The within-cluster check (executed). 13.2 What else could explain it: poverty, rurality, health-service access, reporting quality, the ecological level. 13.3 Writing descriptive results honestly | 09 | `#water-within`, `#water-confounders`, `#water-causation-use`, `#water-causation-calc`, `#water-causation-do` |
| 14 | **Publish Many** | 14.1 Report to Word and PDF. 14.2 Slides to Reveal.js and PowerPoint. 14.3 Report to EPUB (optional), with what building this book taught (links to Appendix H). 14.4 Blog and website: `pre-render` and `freeze`, and how to invalidate a cache. 14.5 Publish it. 14.6 Change an input and explain the rebuild (`MAX_MISSING`). 14.7 Dashboard and white paper (optional); further challenges | 10–13, `examples/water` | `#water-report` … `#water-stretch`, `#water-sources`; `examples/water/README.md` |
| — | **Exercises for Part III** | As for Part II | 05–13, `examples/water` | checkpoint READMEs |

### Afterword · What You Built, and Where Next

`#what-you-built`, `#done`, and choosing which output to build first for your own work.

### Appendices

| | Title | Sources |
|---|---|---|
| A | **Windows: Get Ubuntu Ready** (nine steps, "you should see" after each, the stuck table; WSL ↔ Windows) | `windows-setup.qmd`, `#wsl-windows`, `assets/windows-steps/*.svg`, `assets/windows-session.gif` |
| B | **Terminal Keys and Habits** | `#terminal-keys`, `#terminal-basics` |
| C | **Cheatsheet** | `CHEATSHEET.md` |
| D | **Troubleshooting** | `TROUBLESHOOTING.md` |
| E | **Checkpoints at a Glance, and Answers** (every checkpoint: contents, catch-up line, rejoin point; model answers to the two rebuild tasks) | checkpoint READMEs, notes of `#london-change` and `#water-change` |
| F | **Reading in Another Language** (browser translation of the HTML edition; what stays in English and why) | `title-note`, `#how-to-prompt` notes, `translate-safe.html` |
| G | **Data Sources, Licences and Credits** | `#london-sources`, `#water-sources`, both `data/README.md`, `images/ATTRIBUTION.md` |
| H | **How This Book Is Built** (one repository, two editions; profiles; media pipeline; epubcheck) | this plan, `book/README.md` |
| I | **Running This as a Workshop** (timings, the two-minute rule, room logistics, publish pacing) | `INSTRUCTOR.md`, `#agenda` notes |

### Left out

The Discord and WhatsApp slides (`#discord`, `#discord-whatsapp`) become one generic line:
"your group's help channel". Also left out: section clocks and per-slide timing notes (the
preface keeps the agenda table), the title-slide partial, room-only lines ("ask a helper
now"; these go to Appendix I), Reveal-specific spacing logic (`slide-spacing.html`), and the
deck's own AI statement as a slide (it becomes part of the copyright page).

## 4. Interactive and visual elements: inventory and plan

Rule: **all JavaScript interactivity runs in the HTML edition; the EPUB gets the best static
or animated version e-readers support.** Each live element in HTML is wrapped in
`::: {.content-visible when-format="html:js"}`, and its EPUB stand-in in
`::: {.content-visible when-format="epub"}`.

| Element (deck source) | HTML edition | EPUB edition |
|---|---|---|
| **London 3-D map**, three.js relief scene (`#london-map`) | Live scene. Its JSON is computed by a book cell (`scripts/scenes.py`, adapted from the deck cell); the bundle runs through `assets/deck-host.js`; buttons ("tilt", "up close") replace fragments | GIF of a camera orbit with tilt (6–10 s, ≤ 800 px, ≤ 2 MB), caption, still PNG, link and QR code to the live version |
| **k-means toy**, 3-D with step, play and seed buttons (`#water-kmeans`) | Live scene with its own buttons | GIF stepping through assign/update iterations; static four-panel small multiple computed in Python (better on e-ink) |
| **PCA cloud**, 3-D (`#water-pca-3d`) | Live | Orbit GIF + still; the 2-D PCA figure (`#water-pca`) is an ordinary executed figure in both |
| **Colombia relief**, 3-D (`#water-relief`) | Live | Orbit GIF + still + QR |
| **Five optional 3-D outcome scenes** (`#water-meta-terrain`, `-hulls`, `-stack`, `-orbits`, `-voronoi`) | Live, in an optional section of Chapter 12 | One contact sheet of five stills (no GIFs, to save size) + link |
| **Tunja explorer**, menus for table, summary and charts (`#water-tunja`, `tunja-explorer.js`) | Live | Static panels computed in Python: IRCA by year (urban vs rural) and one method-change series; link |
| **Variable explorer**, a menu of box-plot images (`#water-compare`) | Live menu | The three or four panels the text discusses, inline; the rest via link |
| **YouTube Short player** (`short-player.js`, `#water-kmeans`) | A plain link (no embedded player; keeps the page offline-friendly) | Plain link |
| **Section progress bar** (`section-progress.html`) | Replaced by the book sidebar plus a "Where we are" roadmap figure on each part page | The same roadmap figure (PNG) on each part page, plus the nested EPUB TOC (§6.3) |
| **Assistant boxes** (`.prompt`, `.agent`, `.you`; labels added by `translate-safe.html`) | `::: {.agent-box}` with three labelled parts; the prompt keeps a copy button | The same structure; labels are real text from a Lua filter, not CSS or JavaScript; prompts verbatim in wrapped monospace |
| **Catch-up boxes** (`.source .behind`) | A "Catch me up" line in each exercise | Same |
| **Done / check lines** (`.done`, `.check`) | "You're done when …" in each exercise; 💬 checks become "Pause and think" questions with answers in the text or notes | Same |
| **Drawn terminal screens** (raw HTML in `#terminal-basics`, `#assistant-screens`, `#two-places`) | Text transcripts in styled `pre` blocks (searchable and copyable); `terminal-basics` also as a VHS GIF | Same transcripts; the GIF with its still |
| **PowerShell demo player** (`ps-player.html`, `.ps-demo` in `windows-setup.qmd`) | Static transcripts; the existing `windows-session.gif` | Same |
| **Existing GIFs**: `chat-prompt.gif` (an illustration), `windows-session.gif` | Reused | Reused; still PNGs added |
| **Diagrams**: `quarto-hub.svg`, `water-hub.svg`, `gh-pages-flow.svg` (drawn for dark slides; the hub contains the Quarto logo) | Redrawn in one book style (light ink, transparent background), without logos; originals stay for the deck | PNG at 2× from the same SVGs |
| **New diagrams**: render pipeline, agent loop, sub-agents, git cycle, London dependency graph, water compute-once, catch-up flow, four part roadmaps | SVG | PNG at 2× |
| **Windows step drawings** (`assets/windows-steps/*.svg`) | Reused as SVG | PNG at 2× |
| **Pelican grid**, 12 SVGs in a 5-column table (`#pelican-grid`) | The table, credited as on the slide | A single composite figure with the same credits (a 5-column table does not fit a phone) |
| **London photos** (`examples/london/images/*.jpg`, credited, CC0/CC BY/CC BY-SA) | Reused with credits | Recompressed to ≤ 1200 px; credits kept |
| **`threejs-visits.png`** (a dated dry run) | Reused with its caption | Reused |
| **Executed figures** (ALVA bars, IRCA bands, PCA, heatmap, outcomes, within-cluster) | Book plot style, SVG | Book plot style, PNG at 200 dpi |
| **Cards, chips, goal boxes, fragments, clocks, pace pills** | Prose, tables or definition lists; fragments are removed; ⭐ becomes "(optional)" in titles plus a sidebar | Same |
| **Math** (k-means objective, z-scores, Spearman's ρ; white-paper equations) | MathJax | MathML (Quarto's EPUB default) |

**GIFs to record** (open question 4 covers the agent session):

| GIF | Chapter | Method |
|---|---|---|
| `london-map-orbit.gif` | 6 | Playwright (headless Chromium, WebGL via SwiftShader) on the HTML edition's scene; camera driven by scripted drags; frames → ffmpeg `palettegen`/`paletteuse` → `gifsicle -O3` |
| `kmeans-steps.gif` | 11 | Same; the scene's own step buttons |
| `cluster-cloud-orbit.gif` | 11 | Same |
| `colombia-relief-orbit.gif` | 11 | Same |
| `quarto-preview-reload.gif` | 4 | Playwright on a real `quarto preview` of a copy of checkpoint 01, while a script edits `london.md` |
| `render-many-formats.gif` | 5 | VHS tape: `uv run quarto render london.qmd` in a copy of checkpoint 02, then `ls` of the six outputs |
| `terminal-basics.gif` | 3 | VHS tape: the `pwd` … `rmdir` session from `#terminal-basics` |
| `uv-environment.gif` | 4 | VHS tape: `uv init --bare`, `uv add …`, `uv run quarto check jupyter` |
| `catch-up.gif` | 4 | VHS tape: the checkpoint 01 catch-up steps by hand (backup, copy, render, check) |
| `agent-session.gif` | 2 | Open question 4 |

Every GIF is designed so that **its first frame is the best still**, because readers that
do not animate usually show the first frame. Each also gets a separate still PNG and alt
text that describes the motion. Tapes (`media/tapes/*.tape`) and capture scripts
(`media/capture/*.py`) are committed, so each GIF can be re-recorded. No tape runs a
network, publishing or paid-assistant command.

**QR codes and "live version" links:** EPUB stand-ins link to the HTML edition if it is
published (open question 2). Otherwise they link to the deck's already-published slides
(for example `project-delphi.github.io/quarto-workshop/#/london-map`), which show the same
scenes now. QR codes are made with `segno` (pure Python, via `uv run --with segno`).

## 5. Conventions

### 5.1 Writing style

Inspired by Chip Huyen's practitioner books, without imitating her voice or reusing her text:

- Explain **why before how**; name trade-offs, failure modes and when *not* to use a tool.
  No hype, and no claim without a source or a computation.
- **System level first:** each pipeline gets a diagram before its details (Markdown →
  engine → Pandoc/Typst → outputs; human ↔ assistant ↔ files; data → analysis → outputs →
  pages).
- **Dense, short paragraphs.** Terms are defined at first use. Slide bullets become
  explanatory prose, not longer bullet lists. Lists only for steps and genuine enumerations.
- **Two running examples.** Every concept is tied to the London guide or the water analysis.
- **Emoji:** none in the book's prose or headings. Prompts stay verbatim, including the few
  emoji they contain (open question 9).
- **Numbers:** every number is computed by a cell from the repository's data or carries a
  citation (AGENTS.md). Time-sensitive facts (prices, CLI versions, screens, free-plan
  limits) carry a "checked YYYY-MM-DD" date and link to official documentation. The deck's
  checks from the last two weeks are reused with their dates; anything changed is
  re-checked and re-dated. No invented citations.

### 5.2 Assistant boxes

````markdown
::: {.agent-box}
::: {.prompt}
```default
Render london.md with quarto render and tell me which file it wrote.
```
:::
::: {.agent}
`quarto render london.md` → `london.html`
:::
::: {.you}
In a second terminal tab: `cd ~/london-guide && quarto preview london.md`
:::
:::
````

`filters/agent-box.lua` inserts each part's label as real text ("Ask your assistant", "It
will likely run", "You do"), wraps a lone `.prompt` in an `agent-box`, and keeps prompt text
byte-for-byte as in the deck. A check script compares every book prompt with its deck
source (by slide ID), so the two cannot drift silently. Styled in `styles/epub.css` and
`styles/book.scss`, using the deck's violet, amber and green as accents that work on light
and dark pages.

### 5.3 Asides

Quarto callouts with fixed titles and a class per type, so both editions style them:

| Aside | Markup | Use |
|---|---|---|
| Why this works | `::: {.callout-note .why title="Why this works"}` | The mechanism behind a step |
| Common pitfall | `::: {.callout-warning .pitfall title="Common pitfall"}` | Observed failures, from the dry runs and TROUBLESHOOTING |
| In practice | `::: {.callout-tip .practice title="In practice"}` | Judgement calls and habits |
| Try it | `::: {.callout-important .try title="Try it"}` | A short exercise with "You're done when …" and a catch-up line |

Instructor notes become these asides or prose where they help a reader alone, and are
otherwise dropped or moved to Appendix I.

### 5.4 Code

- Executable cells use `{python}` and reuse the deck's computations. The water chapters
  import `examples/water/scripts/analysis.py` (`analysis.run()`, in memory, about 5 s), as
  the deck does; the London chapters read `examples/london/data/`. Raw inputs stay unchanged.
- Book figures use one light plot style (`scripts/figures.py`): dark ink on a transparent
  background, the deck's cluster and band colours, and colour-blind-safe pairs.
- Display-only code uses plain fences. Excerpts of `analysis.py` are shown with
  `code-annotation` when short, or numbered notes otherwise (S6).
- `freeze: auto` for the book. Invalidation is documented, as AGENTS.md requires: Quarto
  does not track the data files a page reads, so `make book-fresh` deletes `book/_freeze/`
  and re-executes everything; run it after any change to `examples/*/data/` or
  `analysis.py`. Open question 8 asks whether to commit `_freeze/`.

### 5.5 Images and dark mode

- Extensionless image paths with `default-image-extension: svg` for HTML and `png` for EPUB
  (S10), so one source line picks the right file.
- `epub.css` never sets page background or text colours, so reader themes (sepia, night)
  stay in control. Transparent figures carry the class `.on-light`, which gives them a soft
  off-white panel with padding. Photos get no panel.
- Some readers ignore CSS on images. If testing shows that, chart PNGs get an off-white
  background built in as a fallback (open question 10).
- Every image has alt text; meaningful figures are numbered and captioned and referenced
  with `@fig-`.

### 5.6 EPUB stylesheet (`styles/epub.css`)

A serif body (the reader's default serif, with Charter/Georgia fallbacks; no embedded body
font unless testing shows a need), a monospace stack for code, `pre` with `white-space:
pre-wrap` and `overflow-wrap: anywhere` (no horizontal scrolling on phones), tables that
shrink their type and wrap, styled callouts and assistant boxes, code-annotation lists, and
`prefers-color-scheme` variants for borders and accents only.

## 6. Project structure and build

### 6.1 Layout

```text
book/
  PLAN.md, README.md
  _quarto.yml            shared: project type book, metadata, execute (freeze: auto), filters, formats
  _chapters.yml          canonical chapter list: parts, chapters, appendices
  _quarto-html.yml       generated: chapters with part: grouping; output-dir _book/html
  _quarto-epub.yml       generated: flat list with part pages; output-dir _book/epub
  pyproject.toml, uv.lock   the book's Python environment (uv), like the examples'
  index.qmd, copyright.qmd, part-1.qmd … part-3.qmd, afterword.qmd
  chapters/01-quarto.qmd … 14-publish-many.qmd
  appendices/a-windows.qmd … i-workshop.qmd
  filters/agent-box.lua
  styles/epub.css, styles/book.scss, styles/book-dark.scss
  assets/deck-host.js    Reveal-like host so assets/deck-3d.min.js runs in the HTML book
  scripts/sync_chapters.py, epub_postprocess.py, scenes.py, figures.py,
          check_prompts.py, check_media.py, shoot_epub.py (screenshots)
  media/cover.svg, cover.png (media/cover/ would match the Python gitignore's cover/ rule)
  media/diagrams/  roadmaps/  gifs/  stills/  qr/  tapes/  capture/
  _freeze/               execution cache (committed or not: open question 8)
  _book/                 render output (gitignored)
```

`assets/deck-3d/` and `assets/deck-3d.min.js` are not changed. The repository's
`_quarto.yml` render list stays as it is, so the deck build and `docs/` are unaffected.

### 6.2 Build commands (root `Makefile`)

| Target | Does |
|---|---|
| `make book` | Sync chapter lists → render HTML (`--profile html`) → render EPUB (`--profile epub`) → post-process EPUB → epubcheck |
| `make book-html`, `make book-epub` | One edition |
| `make book-fresh` | Delete `book/_freeze/`, then `make book` |
| `make media` | Re-record GIFs, stills, diagrams' PNGs, roadmaps, cover and QR codes (only when asked; never part of `make book`) |
| `make epubcheck` | Run epubcheck on the built EPUB(s) |
| `make book-shots` | Screenshot sample chapters at phone and tablet widths, light and night |

Renders run through `uv run` in `book/`, with `JUPYTER_PATH="$PWD/.venv/share/jupyter"` set,
because a user-level `python3` kernelspec on this machine points at another environment and
would otherwise shadow the book's.

### 6.3 EPUB post-processing (`scripts/epub_postprocess.py`, Python standard library only)

1. Nest each part's chapters under the part entry in `nav.xhtml` and `toc.ncx` (S1).
2. Add `bodymatter` and `copyright-page` landmarks (S8); the cover landmark comes from
   `epub-cover-image`.
3. Remove `alt` from figure `div`s and fix whatever else epubcheck reports that the source
   cannot avoid (S9).
4. Re-zip with `mimetype` first and stored, as the OCF spec requires.

Each fix is a small, tested function. If a later Quarto version fixes a problem at source,
its step is removed.

### 6.4 Validation (before calling a chapter done)

- `quarto render` of both editions with no errors; executed output inspected (figures,
  captions, cross-references, math, code wrapping).
- `epubcheck` 5.x: **zero errors and zero warnings**, output saved with the build.
- EPUB screenshots: the unzipped XHTML with `epub.css` rendered in Playwright at phone
  (390 × 844) and tablet (820 × 1180) widths, in light and a simulated night theme; layout
  problems fixed. Calibre's viewer as a second check if installed.
- HTML edition at desktop and laptop sizes (1440 × 1000, 1366 × 768), per AGENTS.md;
  the live scenes, the explorer and the copy buttons checked.
- `check_prompts.py` (book prompts match the deck), `check_media.py` (every GIF ≤ 2 MB and
  ≤ 800 px wide, has a still and alt text; EPUB total < 40 MB, aiming for about 20 MB),
  internal link check, `git diff --check`.
- The deck untouched: `git diff --stat main -- docs/ index.qmd slides/ assets/` is empty
  (unless open question 2 adds `docs/book/`).

### 6.5 Documentation

`book/README.md`: how to build, re-record media, invalidate the cache, and the
**reader-compatibility table** (which readers animate GIFs, render SVG and MathML, and honour
`prefers-color-scheme`). Each row is either tested here (with date and reader version) or
cited from the vendor's documentation (with the check date); anything else is marked
"untested", not guessed. AGENTS.md gets a short **Book** section (build commands and
conventions, so Claude Code and Codex stay aligned), and the root README gets a `book/` row.

## 7. Milestones and commits

Conventional commits on `feat/epub-book`, rendering and fixing after each chapter:

1. `docs(book): add the book plan` (this file).
2. `feat(book): scaffold the book project` (config, chapter sync, filters, styles, cover,
   front matter, empty part pages, Makefile, post-processor). Exit check: an empty book
   passes epubcheck with zero messages.
3. `feat(book): add a media pipeline` (tapes, capture scripts, diagram rasterising, QR),
   with the first GIF as proof.
4. One commit per chapter: Part I (1–3), Part II (4–7 + exercises), Part III (8–14 +
   exercises), the afterword, then appendices A–I.
5. `docs(book): add README, compatibility table and AGENTS.md section`.
6. Validation fixes.
7. Publish the HTML edition and the EPUB download under `docs/book/`, and link the book
   from the deck's title slide.

No push, PR or publish without your go-ahead.

## 8. Risks and known limitations

- **Duplicated scene code.** The book's `scenes.py` adapts the deck's 3-D cells instead of
  sharing them, so the deck's sources and output stay untouched. The cost: two copies to keep
  in step. A shared module is possible later, at the price of editing the deck.
- **Headless WebGL.** Chromium's software renderer may be slow or differ slightly from a GPU.
  Fallback: capture in headed Chromium.
- **Reader variety.** No EPUB fallback mechanism chooses a still over a GIF on readers that do
  not animate; first-frame design covers that (no separate e-ink variant).
- **Fast-changing facts.** Model names and prices, assistant screens and free-plan limits will
  date quickly; they live in clearly dated sidebars so the prose around them does not age.
- **Windows.** As INSTRUCTOR.md notes, the Windows procedure has been checked only against
  documentation and on a Mac. Appendix A says so.
- **Kernelspec shadowing** on this machine (handled by `JUPYTER_PATH` in the Makefile).

## 9. Open questions

Each has a recommended default; "approve with defaults" works.

1. **Title, author and rights.** Proposed: *One Source, Every Format: Reproducible Publishing
   with Quarto and Coding Assistants*, by Ravi Kalia. The repository has no licence, so the
   rights line is yours to choose: "© 2026 Ravi Kalia. All rights reserved", a Creative
   Commons licence for the text (CC BY 4.0 or CC BY-NC-SA 4.0) with code under MIT, or
   something else. Also: publisher name (if any), date, and keywords. *Default: the title
   above; "All rights reserved" until you choose a licence.*
2. **Publish the HTML edition under `docs/book/`?** This does not change Pages settings but
   does change what `main:/docs` serves, and a full deck render can empty `docs/`, so the
   Makefile would render the deck first and the book second. The EPUB could be offered as a
   download there too. *Default: build locally only; ask again when the book is ready.*
3. **The AI workflows lab** (`ai-workflows.qmd`): a Part IV capstone chapter, an appendix,
   or left out? It adds a third dataset, but it has the most on auditing an agent's work.
   *Default: Part IV, one chapter, written last.*
4. **The agent-session GIF.** AGENTS.md rules out paid assistant runs to test a displayed
   command, so options are: (a) a scripted replay of a realistic session in VHS, labelled
   as an illustration like `chat-prompt.gif`; (b) you record one real session with
   asciinema (at your cost), which I then trim and convert; (c) no agent GIF. *Default: (a).*
5. **The pelican images.** No licence is stated on them; a published book is a bigger step
   than a slide. Options: describe the experiment and link to Simon Willison's series without
   reproducing the images; ask him for permission; or keep them as the deck does. Similarly,
   the redrawn hub diagram drops the Quarto logo. *Default: describe and link, no images.*
6. **Installing tools.** `brew install epubcheck vhs` (epubcheck pulls a current OpenJDK; I
   could instead download the official jar and use the Java 11 here, if that release runs on
   it), the Python Playwright
   package through `uv` (it may download a matching Chromium, about 150 MB), `segno` through
   `uv`, and optionally Calibre (`brew install --cask calibre`) for viewer checks. *Default:
   brew for vhs, the epubcheck jar, Playwright and segno through uv, no Calibre.*
7. **A static EPUB variant** for e-ink and Kindle (every GIF swapped for its still, smaller
   file)? *Default: yes, built by `make book-static`.*
8. **Commit `book/_freeze/`?** Committing it lets anyone rebuild the EPUB without Python and
   makes builds reproducible; the cost is a few MB of JSON in history. *Default: commit it.*
9. **Emoji.** None in prose and headings; verbatim prompts keep theirs, which may show as
   boxes on some e-ink fonts. *Default: as stated.*
10. **Light backing for figures.** CSS panel (`.on-light`) first; baked-in off-white chart
    backgrounds only if testing shows a reader strips the CSS. *Default: as stated.*
11. **Workshop logistics in the book.** Discord and WhatsApp details dropped; instructor
    material in Appendix I. *Default: as stated.*

## 10. Decisions (2026-11-12)

1. Title *One Source, Every Format: Reproducible Publishing with Quarto and Coding
   Assistants*, by Ravi Kalia; rights "© 2026 Ravi Kalia. All rights reserved."
2. The HTML edition and the EPUB are published under `docs/book/`, and the deck's title
   slide links to the book. Pages settings stay as they are (`main:/docs`). The Makefile
   renders the deck first and the book second, because a full deck render can empty `docs/`.
3. The AI workflows lab is left out (no Part IV).
4. The agent-session GIF is a scripted VHS replay, labelled as an illustration.
5. The pelican images are reproduced, credited and linked as on the slide.
6. Tools: `vhs` via Homebrew, the official epubcheck jar, Playwright and `segno` through
   `uv`; no Calibre.
7. No static e-ink variant.
8. Defaults stand for the rest: `book/_freeze/` is committed, no emoji in prose, CSS light
   panels for figures, workshop logistics dropped or moved to Appendix I.

## 11. Changes during the build (2026-11-12)

What the finished book does differently from this plan, and why:

1. **The five optional 3-D outcome scenes are linked, not reproduced.** Section 12.6 describes
   them and links (and QR-codes) the workshop slides at `#/water-meta-terrain`, in both editions,
   instead of a contact sheet in the EPUB and live scenes in HTML. Porting five more scene
   computations was a large share of the work for an optional section.
2. **Playwright drives the installed Google Chrome** (`channel="chrome"`), not Playwright's own
   Chromium, which the network could not download in reasonable time. WebGL runs through
   SwiftShader as planned.
3. **Light-panel figures are flattened in the EPUB.** The post-processor composites the
   transparent PNGs shown on a light panel onto the panel's colour, because Amazon's guidelines
   list images with transparent areas as unsupported and a reader that drops CSS backgrounds
   would show dark ink on a night page.
4. **Extra checks:** `make book` also checks every EPUB link and QR code into the website
   edition (`scripts/check_live_links.py`); matplotlib's SVGs are made reproducible so the
   committed `_freeze/` changes only when results do.
5. **No e-reader was tested.** The EPUB was validated with EPUBCheck and checked as rendered in
   Chrome with its own stylesheet; `book/README.md` marks every reader as untested, except where
   it quotes Amazon's guidelines.
