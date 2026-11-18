# Revision plan: *Prompt, Check, Publish* for professional and start-up readers

Status: **Phase 2 under way.** The plan was approved on 2026-11-18 with every recommendation
(§8 records the answers). Written 2026-11-18 from `main` at `bde9102`; the status log (§9) says
what is done.

## 0. Baseline

Read: `AGENTS.md`, `CLAUDE.md`, `_quarto.yml`, `book/_quarto*.yml`, `book/_chapters.yml`,
`Makefile`, `book/README.md`, `book/PLAN.md` (headings and decisions), the preface, every
chapter of Parts I and II, Chapter 15 (`14-publish-many`), the afterword, the appendices
(glossary, Windows, workshop, checkpoints, cheatsheet and how-built in full or by section),
`ebook/index.qmd`, `ebook/_source.py`, `book/scripts/sync_chapters.py`,
`translation/compare.py`. Part III's analysis chapters (`08`–`13`, both exercise chapters) and
the workshop deck, checkpoints and `examples/` were surveyed by two read-only sub-agents
whose reports, with line references, back the Part III and workshop statements below.

Builds run, all passing:

| Command | Result |
|---|---|
| `make book` | EPUBCheck 0 fatals / 0 errors / 0 warnings / 0 infos; 7 live links, 0 broken; 5 scenes, 0 different (54 s, frozen) |
| `make book-es` | EPUBCheck clean; 36 files compared, 0 mismatches; glossary lint clean; 0 English sentences left (52 s) |
| deck render (`quarto render` with `.conda`, in a scratch worktree) | exit 0; the rendered `docs/` is byte-identical to the committed one |
| `make ebook-check` (same worktree) | all checks passed; first load on a phone 163 KB. One standing note: the latest release's EPUB (`book-2026-11-16`) is older than the committed one, so a `make book-release` is due once `main` moves (author only) |

There is no CI in the repository (no `.github/`, no other CI configuration).

## 1. Audience, revised

The author's two messages during Phase 1 changed the brief. Start-ups are a major focus, and
the audiences are ranked by fit. The book is written for these readers.

**Primary**, in order of fit:

1. **Analysts who produce recurring reports**: corporate, BI, public-sector and NGO
   analysts. Their pain is copying numbers into Word and PowerPoint, which is exactly what
   the book's core idea removes. This is the largest group.
2. **Academic researchers and graduate students.** This is Quarto's home ground, and the
   book already speaks to them (Part III, the AI-disclosure section).
3. **Data scientists and ML, AI and research engineers.** They write experiment and
   evaluation reports and need the same results as a write-up, a deck and a page. They need
   the checking discipline and the multi-format output, not terminal basics.
4. **Technical founders and data or AI start-ups.** Their outputs carry numbers that
   change:
   - monthly investor updates and board metrics;
   - benchmark and evaluation white papers;
   - per-customer reports;
   - a product or documentation micro-site without a designer.

   The checking habit keeps a wrong number away from investors. The book must also say
   where Quarto fits them badly: pitch decks driven by design, marketing sites, and
   documents co-founders comment on in Google Docs or Notion.

**Secondary:**
- educators and students (course sites, lecture decks, coursework);
- complete novices, whose path must keep working unaided;
- software engineers, a weaker fit: they gain mainly from supervising agents and from
  data-bearing reports.

**Also served by role-specific notes rather than chapters:**
- consultants and freelancers, through per-client parameterised reports;
- data journalists and think-tank researchers;
- government statisticians and regulated industries, through auditability and the
  locked-down-machine section;
- developer advocates and technical writers, through benchmarks with live numbers.

The Spanish edition already reaches Spanish-speaking Latin America. **R users stay
excluded**; see question Q12.

## 2. Review findings, checked against the source

C = confirmed, P = partly true, W = wrong.

### Output craft

| Finding | Verdict | Evidence |
|---|---|---|
| **Slides**: only a six-slide Reveal.js and PowerPoint deck near the end; no themes, notes, fragments, layouts, PDF export, presenting or design guidance | **P** | There are two decks, not one: the guide's optional `pptx`/`revealjs` formats (`05-compute.qmd:385-417`) and the six-slide council deck (`14-publish-many.qmd:97-124`). There is a little design guidance: "one thing per slide", and the conclusion on the last slide (`14-publish-many.qmd:113-116`). Themes, speaker notes, fragments, columns, PDF export and presenting are absent, and the deck uses all of them without teaching them (`_quarto.yml:28-55`, `slides/_london.qmd:158`). |
| **Websites**: navbar, listing home page and pre-render hooks only; nothing on theming, styling, about pages, search or branding | **C** | Navbar at `07-publish.qmd:169-222`; listing and `pre-render` at `14-publish-many.qmd:152-197`. The examples set `theme: cosmo` with no lesson. Search, about pages and branding appear nowhere. The chapter also compares hosts (`07-publish.qmd:120-167`). |
| **White paper**: optional and light; no figure/table cross-references, citation styles, reference managers, or journal/house templates | **P** | Both white papers are optional (`07-publish.qmd:377-415`, `14-publish-many.qmd:359-385`). They do have a `references.bib`, Typst's `ieee` style, numbered sections, numbered equations with `@eq-kmeans`, and a reference-checking rule (open each DOI). Figure cross-references are taught in Chapter 6 (`05-compute.qmd:255-256`), but table and section cross-references are not. CSL styles, reference managers and templates are absent. |
| **Brand and templates**: no shared brand across formats; no corporate Word or PowerPoint reference templates | **C** | No `_brand.yml` and no `reference-doc` anywhere in the repository, book or deck. |
| **Parameterised reports**: none | **C** | No `params` anywhere. The afterword's metrics brief reads the newest export (`afterword.qmd:115-121`), which is a precursor. |
| **GitHub Actions**: described briefly, not taught | **C** | One practice box (`07-publish.qmd:270-276`) and a glossary entry for "CI job". The deck has one sentence in its notes. |
| **Accessibility**: alt text only | **C** (as teaching) | Readers are taught alt text and captions (`05-compute.qmd:242-263`). The book and landing page themselves go further, with light panels for night themes, reduced-motion stills, hatching that encodes without colour and WCAG AA on the landing page, but none of this is taught. |

### Novice friction

| Finding | Verdict | Evidence |
|---|---|---|
| Windows needs WSL, from an appendix, before setup starts | **C** | `03-setup.qmd:10-13`; Appendix A. The deck's notes say "no native Windows route is supported", and readers without admin rights are paired with a neighbour. |
| A paid agent account is required; there is no low-cost route | **P** | The deck asks for "a paid agent plan or API key" (`index.qmd:371`) and the preface warns of cost (`index.qmd:114-116`). But Antigravity needs only a Google account (`03-setup.qmd:50`), and free web chats appear twice (`02-assistant.qmd:55-65, 343-357`). The book never states plainly that a free or low-cost route exists, or what it costs in capability. |
| Setup uses terms it never defines | **P** | WSL, YAML, Pandoc, Typst, `sudo`, PATH, token and API are defined at or before first use. Homebrew (`03-setup.qmd:350`), apt (`:101`), proxy (`:43`), API key (`:48`) and VPN are not. curl gets only "for downloading" (`:83`), and none of these is in the glossary. Separately, the glossary is never linked from the text: defined terms are not linked at first use. |
| The setup test render uses YAML, code cells and inline code before they are taught | **P** | The test run does use them (`03-setup.qmd:446-463`). But Chapter 1 shows and annotates the exact file first (`01-quarto.qmd:93-119`), and Chapter 3 calls it a black-box check on purpose. The friction is real but already mitigated. |

### Structure and audience

| Finding | Verdict | Evidence |
|---|---|---|
| The preface has no role-based reading paths | **C** | It offers self-paced, core-path and workshop-paced routes (`index.qmd:185-207`). Role-shaped projects appear only at the end, in the afterword (metrics brief, research supplement, coursework). |
| Both running projects are data analyses: none without a dataset, none from engineering or ML | **C** | Part III uses k-means, but as a descriptive analysis. There is no supervised model, train/test split or evaluation report anywhere (deck survey). `examples/ai-context/` is a synthetic benchmark stub that no deck uses. |
| Privacy guidance is brief: nothing on vendor retention, enterprise plans or confidential data | **P** | There are three passages: `02-assistant.qmd:354-357, 421-424` and `afterword.qmd:88-96`, the last a sound practice box on confidential data. Vendor retention, training opt-outs, enterprise and zero-retention plans, and approved-tool lists are absent. |
| Dated facts such as model prices sit in the text and will age in the EPUB | **C** | They are spread across several chapters: prices (`02-assistant.qmd:143-165`), pelican costs, agent versions and screens (`03-setup.qmd:229-290`), account requirements (`03-setup.qmd:46-51`, preface `:114-116`) and hosts' free plans (`07-publish.qmd:144-167`). Each carries a date, but they live in the prose. The landing page also reads two of these sentences with regular expressions (`ebook/_source.py:366-388`). |
| Chapter file names are offset from chapter numbers | **C** | `04-markdown` is Chapter 5, and so on, up to `14-publish-many`, which is Chapter 15. The cause is that `first-report.qmd` was inserted as Chapter 4. Published URLs, the landing page (`ebook/_source.py:170-193`, `ebook/index.qmd:162-172, 254-258`), the EPUB's live links and the Spanish edition all use the file names. |

No finding was wrong outright. Six are confirmed as stated, and seven are partly true; the
evidence column says which part holds.

### Found while reading (not in the review)

1. **The book has no CI, yet "CI does the same" is in the definition of done.** The deck
   builds with a local `.conda` environment and the book with `uv`, so CI needs both
   recipes. Is `environment.yml` current? Unverified.
2. **The Spanish edition shares `book/_chapters.yml`.** Any new English chapter breaks
   `make book-es` until there is a way to mark chapters English-only. `compare.py` fails on
   any structural change to a shared English file (headings, IDs, cross-references).
   `AGENTS.md` asks that Spanish twins change in the same branch, which conflicts with this
   task's "do not translate yet". Proposed resolution: WP0.
3. **The landing page quotes the preface by regular expression.** It quotes the audience
   list ("I wrote this book for … : anyone"), "No programming is assumed", the list of
   needs, and the cost and account sentences (`ebook/index.qmd:69-96`,
   `ebook/_source.py:325-388`). Rewriting the preface and moving dated facts both mean
   changing the landing page in the same commit; the render stops otherwise, which is the
   intended guard.
4. **Part III has some typed values that nothing guards** (sub-agent survey). They are
   mostly inside prompts: "2016–2023" and "more than 2 features" (`10-prepare.qmd:292,312`),
   `random_state=42, n_init=20` (`11-cluster.qmd:490`), and the naming rule's 40% and
   0.5 SD (`12-interpret.qmd:308-336`). Prompts are literal text, so a typed value there is
   defensible. A cheap guard (`text_holds`) against `analysis.py`'s settings would keep them
   honest. This is optional work package WP16.
5. **The Hillstrom data used by the `ai-workflows.qmd` lab have no stated licence**
   (`examples/marketing-context/notes.md`). This is outside the book, but it matters if the
   lab is reused.

## 3. The shape of the revised book

### 3.1 Principles

- **Two routes through Part I.**
  - **Route A, the fast path**, for readers who already use a terminal and Git, is a new
    chapter. It starts from an *existing repository*, not an empty folder, and reaches a
    multi-format output and a pull request; target under an hour, to be timed in the
    dry run.
  - **Route B, from zero**, keeps today's setup and first-report chapters, unchanged in
    substance and marked as the novice route, so a novice still completes Part I unaided.
  - Recommendation: keep both routes in Part I rather than moving the basics to an
    appendix. Moving them would push the appendix letters along, break the landing page's
    appendix checks and the published URLs, and bury the tested novice path.
- **The London guide stays the "foundations in depth" part.** Fast-path readers can skip it
  or use it as reference; the preface's paths say which sections each role needs.
- **A new part, *The Craft of Outputs*, is prompt-first.** Its running example is the
  professional worked example (§4), so its chapters double as that example, with one
  checkpoint per chapter. Every topic section follows the same three beats:
  1. **Vocabulary**: what is possible and what it is called. A short table of terms and the
     Quarto option each maps to, checked against Quarto 1.10.20's schema.
  2. **Specification**: a tested prompt, plus the lasting rules it implies, as an
     `AGENTS.md` excerpt.
  3. **Verification**: what good output looks like, and how to confirm it by reading the
     diff, inspecting the render (a screenshot of the real output) and running a guard or
     test.
- **A new part, *Working in a Team*,** covers existing repositories, pull requests for
  agent changes, CI that renders and fails on stale claims, and corporate and start-up
  realities.
- **The water analysis stays the deep case study**, after the craft and team parts, and is
  unchanged apart from renumbering.
- **Dated facts move to one place**: `book/facts.yml`, rendered as a new appendix and read
  by the chapters and the landing page (§3.4).

### 3.2 Table of contents: current and proposed

Chapter numbers are those the reader sees. New files get descriptive names with no numbers,
as `first-report.qmd` already has; existing files keep their names (§3.5).

| # now | Current | # new | Proposed | File | Change |
|--:|---|--:|---|---|---|
| | Preface | | Preface | `index.qmd` | **Rewritten**: who it is for (§1), a role-based reading-paths table, two routes, and the start-up fit and limits |
| **Part I** | Foundations | **Part I** | **Start Here** | `part-1.qmd` | Retitled; roadmap regenerated |
| 1 | Publishing That Rebuilds Itself | 1 | same | `01-quarto.qmd` | **Reframed**: the drift example opens on an analyst's monthly pack and an investor update; the deliverables list covers evaluation reports, model cards, RFCs, briefs, investor updates and white papers; "wrong tool" gains a start-up paragraph |
| 2 | Working With a Coding Agent | 2 | same | `02-assistant.qmd` | Price table and versions move to Appendix K. **New sections**: "Vocabulary, specification, verification" (the book's frame for every later prompt) and "A step or a task?" (when to hand an agent a larger task, and how to check it). Privacy moves to Ch 20 with a pointer |
| — | — | 3 | **The Fast Path** (Route A) | `fast-path.qmd` **new** | Install by one prompt, or the zero-install container. Clone the starter repository (an ML repo with `src/`, `tests/` and a notebook). Render the existing notebook (`quarto render nb.ipynb`, `quarto convert`). Add `report.qmd` in HTML, DOCX and Typst with computed numbers. Branch, commit, open a PR. Checkpoint 14 |
| 3 | Setting Up Your Machine | 4 | same (Route B) | `03-setup.qmd` | Novice fixes (WP4): glossary links at first use, the low-cost agent route, the container route, test-run resolution |
| 4 | A First Report, by Hand | 5 | same (Route B) | `first-report.qmd` | Marked as Route B; unchanged otherwise |
| **Part II** | One Guide, Many Audiences | **Part II** | same: "Foundations in depth" | | Part page says who can skip what |
| 5–8 | Markdown · Compute · Audiences · Publish | 6–9 | same | `04`–`07` | Small edits only: Ch 7 (audiences) gains a pointer to Part III's brand chapter; Ch 8 (publish) replaces the Actions practice box with a pointer to Ch 19; its hosts' free plans move to Appendix K |
| — | Exercises for Part II | — | same | | none |
| — | — | **Part III** | **The Craft of Outputs** (new part) | `part-craft.qmd` **new** | |
| — | — | 10 | **One Set of Results** | `results.qmd` **new** | The worked example's analysis as a compute-once script with tests and guards. The evaluation report and **model card**, with figure, table and section cross-references. Checkpoint 15 |
| — | — | 11 | **Slides That Carry a Decision** | `slides.qmd` **new** | Covers what makes a technical deck good (one claim per slide, the number in the title, the decision on the last slide). Reveal.js: themes, speaker notes, fragments, columns, layouts, `smaller`/`scrollable`, PDF export, presenting (speaker view, timing). PowerPoint: its layouts and limits, and a `reference-doc` template. Stakeholder deck and investor deck. Readable contrast and type. Checkpoint 16 |
| — | — | 12 | **A Site and One Brand** | `sites.qmd` **new** | Covers `_brand.yml` (colours, type, logo) driving the site, slides and Typst PDF (and what it does not reach in DOCX/PPTX); themes and custom SCSS by prompt; about page; search; listings; navbar and footer; social cards. Accessibility checks: contrast, headings, alt text, reduced motion, Lighthouse. The project micro-site. Checkpoint 17 |
| — | — | 13 | **White Papers and References** | `white-papers.qmd` **new**, **core path** | Covers the benchmark white paper, figure/table/equation/section cross-references, BibTeX and CSL styles (APA, IEEE, a journal's), Zotero/Better BibTeX export, verified references (open each DOI), journal and house Typst templates, Word `reference-doc` for house style, and the abstract and author block. Checkpoint 18 |
| — | — | 14 | **Reports That Run Themselves** | `parameters.qmd` **new** | Parameters (`params`, `-P`, `--execute-params`). Professional case: one report per model version and per customer segment. Educator case: one feedback sheet per section from a gradebook (synthetic, labelled). The investor update as a parameterised monthly report. Scheduled data. Checkpoint 19 |
| — | — | **Part IV** | **Working in a Team** (new part) | `part-team.qmd` **new** | |
| — | — | 15 | **Existing Repositories and Pull Requests** | `team.qmd` **new** | Adding Quarto to a repo you did not start: `_quarto.yml` beside code, render lists, what to ignore. Agent work on branches, one PR per prompt, reviewing an agent's diff in a PR, issue → branch → PR. Code-review rules in `AGENTS.md` |
| — | — | 16 | **Builds You Can Trust: CI** | `ci.qmd` **new** | A GitHub Actions workflow that installs Quarto and uv, renders, runs tests and guards, and publishes to Pages. Freeze in CI. Scheduled rebuilds (cron) for recurring reports. A failing claim as a red build. Checkpoint 20 |
| — | — | 17 | **At Work and in a Start-up** | `at-work.qmd` **new**, short | Confidential data and vendor retention: consumer vs business plans, training opt-outs and zero-retention options, all dated in Appendix K. Approved tools. Proxies and locked-down machines. House Word/PowerPoint templates and brand rules. Investor data and private hosting. Where Quarto is the wrong tool in a start-up |
| **Part III** | One Analysis, Many Publications | **Part V** | same | | renumbered only |
| 9–15 | Question · Explore · Prepare · Cluster · Interpret · Causation · Publish Many | 18–24 | same | `08`–`14` | Ch 24 (publish many) points to Chs 11–13 for craft |
| — | Exercises for Part III | — | same | | none |
| | Afterword | | same | `afterword.qmd` | Adds two projects, a **monthly investor update** and a **design doc / RFC with live benchmark numbers** (the worked example without a dataset), and a reading-path recap |
| A–J | Windows … Glossary | A–J | same | | Glossary gains the new chapters' terms; Appendix E lists the new checkpoints; Appendix I notes the book-only parts |
| — | — | **K** | **Facts That Change** | `appendices/k-facts.qmd` **new** | Rendered from `book/facts.yml`: prices, plans, agent versions, account requirements and hosts' free plans, each with its source URL and the date it was checked |

Part III (craft) is written to stand on its own: a reader on the fast path goes Ch 1 → 2 → 3 → 10 → 11/12/13 → 14 and has not
read a page meant for beginners.

### 3.3 Reading paths (preface table)

The table goes in the preface and is checked by a cell: each listed chapter must exist.

| You are | Read | Your first finished output |
|---|---|---|
| Analyst with recurring reports | 1, 2, 3 → 10, 14 (parameters), 12 → 17 | a parameterised brief in HTML and Word, rebuilt from next month's data |
| Researcher or graduate student | 1, 2 (AI policy), 3 or 4–5 → 10, 13 → Part V | a supplement or white paper with verified citations and cross-references |
| Data scientist or ML/AI/research engineer | 1, 2, 3 → 10 → 11, 13 → 15–16 | an evaluation report, model card and deck from one results file, built in CI |
| Founder or early technical team | 1, 2, 3 → 10 → 14 (investor update), 12, 13 → 16 → 17 | a monthly investor update and a benchmark white paper on a branded micro-site |
| Consultant or freelancer | 1, 2, 3 → 10 → 14 → 12, 17 | one report per client from one template |
| Software engineer | 1, 2 (§ step or task), 3 → 15, 16 → 13 | an RFC whose numbers come from the code's own benchmarks, reviewed in a PR |
| Educator | 1, 2 → 4–5 → Part II → 11, 12, 14 (educator case) | a course site, a lecture deck, per-section feedback sheets |
| Student | 1, 2 (AI policy) → 4–5 → Part II → afterword coursework project | a coursework report a marker can rebuild |
| New to the terminal | 1, 2, 4, 5 → Part II → Part V | the London guide on its own website |

### 3.4 One place for facts that change

- `book/facts.yml` holds every volatile fact as `key: {value, source, url, checked}`.
- `book/scripts/facts.py` reads it. Chapters use `fact("claude_code.accounts")` inline,
  with its date, and mostly point to Appendix K for anything that dates fast.
- `appendices/k-facts.qmd` renders the whole file with dates.
- `ebook/_source.py` reads the same file instead of matching preface sentences with
  regular expressions.
- An update is then one YAML edit and `make book`. The EPUB still ages, but it ages in one
  appendix, and its Further-reading links lead to the current pages.
- The pelican grid's costs stay in Chapter 2. They record an experiment (dated and
  guarded), not current prices.

### 3.5 File names and redirects

Quarto 1.10.20's schema lists `aliases` for HTML documents in a website. Whether it works in
a book project has **not been tested** yet. A spike in WP0 renders one alias in the book and
checks that the redirect page is written and that `check_live_links.py`, `lang_switch.py`
and the landing page still pass.

Recommendation:
- Give new chapters descriptive names now.
- Do not rename existing files in this revision: the renumbering above makes every number
  drift anyway, so numbered names would be wrong again.
- Offer one optional late package (WP15): rename `01`–`14` to descriptive names, with an
  alias from each old URL in both editions. Do it only if the spike passes and you approve.

### 3.6 What moves, what is new, what is cut

- **Moves**:
  - prices, account requirements, agent versions and hosts' free plans → Appendix K;
  - privacy and confidential-data guidance → Ch 17, with pointers left behind;
  - Chapter 8's Actions practice box → Ch 16;
  - the afterword's "Keep private data private" box → Ch 17, keeping a one-line pointer.
- **New**:
  - 8 chapters (3, 10–17), 3 part pages and Appendix K;
  - `book/facts.yml`;
  - starter `starters/eval-repo/`;
  - the finished example `examples/eval/`;
  - checkpoints 14–20;
  - `.github/workflows/build.yml`;
  - possibly a `.devcontainer/`.
- **Cut**: nothing. No chapter or checkpoint is deleted. The London and water white papers
  stay optional in their chapters, since the core-path white paper is now Ch 13.

## 4. The professional worked example

Recommendation: one evaluation project in the shape of a small AI start-up, which doubles
as the start-up example the author asked for. A fictional company, named as fictional,
evaluates successive versions of a classification model on real public data. From one set
of computed results it publishes:

- an **evaluation report and model card** (Ch 10);
- a **stakeholder or investor deck** (Ch 11);
- a **project micro-site** with a shared brand (Ch 12);
- a **short benchmark white paper** (Ch 13);
- a **monthly investor update and per-segment reports** from one parameterised template
  (Ch 14).

It is built from a starter repository, not an empty folder, then reviewed in PRs and built
in CI (Chs 15–16). Everything runs locally with scikit-learn (already in the water project's
lock file), fixed seeds and a frozen copy of the data. There are no network calls, model
APIs or paid services at render time.

The project ships **no synthetic numbers presented as real**:
- The model metrics are real, computed from the public data.
- The company is fictional.
- The investor update's business figures (users, revenue) come from a small CSV labelled
  **synthetic** in its file name, its README and every page that shows them. Or, if you
  prefer (Q4), the update reports only the real model metrics.

Dataset options, none added yet (your approval is needed). Licences are as listed on each
source page and **must be re-read before adding**:

| Option | What it is | Fit | Licence (to verify) |
|---|---|---|---|
| **A. UCI Bank Marketing** (Moro, Cortez and Rita, 2014), recommended | 45k phone-campaign contacts, binary outcome, subgroups (age, job) for slice metrics | a realistic product model, per-segment reports, model-card slices; small, tabular, fast | CC BY 4.0 on the UCI repository |
| B. UCI Default of Credit Card Clients (Yeh and Lien, 2009) | 30k clients, binary default | the same shape; fairness slices are sharper and more sensitive | CC BY 4.0 on UCI |
| C. A public text set for a TF-IDF classifier | for example a CC-licensed sentiment or topic corpus | feels more like "AI"; larger files, licences vary more | varies |
| D. Benchmark results only (no model) | published leaderboard tables | the closest to an AI start-up's benchmark white paper, but licences are unclear and the figures are volatile | often unstated |

The **example without a dataset** is the afterword's RFC project. Its numbers come from the
repository's own code: a timing benchmark written to `results.json` with its environment
recorded, and a table of configuration options read from the code itself.

## 5. Effects on the rest of the repository

**Checkpoints.**
- New book-only series: `checkpoints/14-eval-start` (fast path end),
  `15-eval-results`, `16-eval-slides`, `17-eval-site`, `18-eval-whitepaper`,
  `19-eval-params`, `20-eval-ci`.
- Each carries `AGENTS.md`, `pyproject.toml`, `uv.lock` and a catch-up README with no
  rendered output, as `AGENTS.md` requires; data travel with the checkpoint, as London's do.
- Existing checkpoints are unchanged. Appendix E and `.gitignore` already cover the
  patterns.

**Workshop.**
- The six-hour agenda is unchanged and stays viable. The tightest block, Publish Many, has
  10 minutes of slack, so nothing new fits in the day.
- Everything new is book-only, and Appendix I says so.
- Optional: one ⭐ slide at 🏁 Done pointing to the professional parts (Q9).
- A professional-track variant of the day (eval project instead of water) is possible later
  but not in scope.

**Landing page** (`ebook/`).
- Copy is addressed to the primary audiences: role pills from the preface's paths table,
  and "No programming required" becomes the novice note.
- The cost and account notes come from `facts.yml`.
- The contents section picks up the new parts automatically.
- Its checks change: the appendix check ("first Windows, last Glossary") becomes "last
  Facts That Change", and the chapter count text follows.
- Re-run `make ebook-media STEPS=head` (the description changes), `make ebook-check` and
  Lighthouse (mobile); check at 375 × 812 and 1440 × 900.

**EPUB.**
- Every new chapter passes EPUBCheck with `--failonwarnings`, `make book-shots` (phone and
  tablet, light and night), and the live-link check.
- Screenshots of real slides and sites go in as stills.
- Interactive pieces, such as a live deck embed, get the usual `html:js` / `epub` pair.
- Any GIF stays under 2 MB and 800 px, has a still, and is made by `make media`.

**Spanish edition** (no translation now).
- `_chapters.yml` entries gain an `only: en` flag. `sync_chapters.py --book ../book-es`
  leaves them out, and `lang_switch.py` links an English-only page to the Spanish home
  instead of a missing twin.
- `translation/pending.yml` records, for each shared English file changed in this revision,
  the last English commit its Spanish twin matches. `compare.py` compares those files with
  that commit's English text (`git show`) instead of the working copy, so the check stays
  meaningful and the Spanish build stays green.
- `translation/PLAN.md` gets a "to translate" list: new chapters, the changed sections,
  `facts.yml` strings and new glossary terms.
- `AGENTS.md`'s rule "change its Spanish twin in the same branch" needs a recorded
  exception for this revision (Q2).

**CI** (new, `.github/workflows/build.yml`).
- On every pull request: set up Quarto 1.10.20, uv, Java 11, EPUBCheck 5.4.0 and the
  deck's conda environment. Run `make book`, `make book-es`, the deck render to a scratch
  `docs/`, `make ebook-check` and `git diff --check`.
- Optionally, fail if the committed `docs/` differs from the fresh render.
- It builds and checks only: it never publishes, pushes or touches `gh-pages`.
- Running it needs GitHub Actions minutes, which are free for public repositories (to
  verify, recorded in Appendix K).
- Whether `environment.yml` reproduces `.conda/` is unverified; WP0 checks it.

## 6. Work packages (each one PR, in this order)

| WP | Branch | Contents | Done when |
|---|---|---|---|
| 0 | `infra/revision-groundwork` | `only: en` chapters; `pending.yml` in `compare.py`; `lang_switch` fallback; `facts.yml`, `facts.py` and Appendix K skeleton; aliases spike (report only); CI workflow (build and check only); README/AGENTS notes | `make site` and CI green; Spanish unchanged |
| 1 | `book/facts-in-one-place` | Move prices, plans, versions and hosts to `facts.yml`; chapters and landing page read it | No dated price left in chapter prose; landing page check passes |
| 2 | `book/audiences-front-matter` | Preface (paths table, routes, start-up fit), Ch 1 reframing, part pages, landing-page copy, glossary additions | Every path's chapters exist (cell check); landing page at both sizes; Lighthouse |
| 3 | `book/fast-path` | `starters/eval-repo/` (ML repo, notebook, tests), Ch 3, checkpoint 14 | Every prompt dry-run in a copy of the starter; fresh-clone render; EPUB checks |
| 4 | `book/novice-fixes` | Ch 4 (setup): glossary links at first use (a filter, or explicit links), undefined terms defined, low-cost agent route, container route (if Q6 is approved and verified), test-run resolution (Q7) | A novice walk-through of Part I against the rendered book; definitions present |
| 5 | `book/results-and-model-card` | Dataset (Q3), `examples/eval/` analysis with tests and guards, Ch 10, checkpoint 15 | Numbers computed; guards fail when tested by mutation; prompts dry-run |
| 6 | `book/slides` | Ch 11, checkpoint 16 | Decks rendered, screenshots, speaker view and PDF export checked |
| 7 | `book/sites-and-brand` | Ch 12, `_brand.yml` across formats, checkpoint 17 | Brand visible in site, slides and PDF; accessibility checks reported |
| 8 | `book/white-papers` | Ch 13 (core), CSL styles, a house template, `reference-doc`, checkpoint 18 | Every reference opened and dated; cross-references resolve in all formats |
| 9 | `book/parameters` | Ch 14, professional and educator cases, investor update, checkpoint 19 | `-P` renders verified per value; output names distinct |
| 10 | `book/team-and-ci` | Chs 15–16, checkpoint 20 | Workflow run on a real disposable repo (Q8) or with the limitation stated |
| 11 | `book/at-work` | Ch 17 (confidential data, vendors, proxies, templates, start-ups) | Each vendor claim sourced and dated in `facts.yml` |
| 12 | `book/afterword-projects` | Investor-update and RFC projects; "what you can now do" | Prompts dry-run; fresh-clone test |
| 13 | `workshop/pointer-slide` (optional, Q9) | One ⭐ slide; Appendix I note | Deck at 1440 × 1000, 1366 × 768, 1280 × 720 |
| 14 | `translation/to-do` | `translation/PLAN.md` list for the Spanish edition | Spanish build green |
| 15 | `book/descriptive-file-names` (optional, Q5) | Rename `01`–`14` with aliases in both editions; update landing page and link checks | Old URLs redirect; all link checks pass |
| 16 | `book/guard-part-v-prompts` (optional) | `text_holds` for Part V's typed prompt values | Render stops when a setting changes |
| — | (each PR) | `REVISION-PLAN.md` status log updated | |

Every package ends with:
- `make book`, `make book-es`, `make deck`, `make ebook-check` and `git diff --check`;
- `make book-shots` for changed chapters, and HTML pages at 1440 × 1000 and 1366 × 768;
- `make book-publish` and `make book-es-publish` into `docs/` (local only), committed with
  the sources as the repository requires.

There will be one commit per coherent change, in `type(scope): lowercase description`
style. Nothing is pushed to `main` and nothing is merged; you review and merge.

## 7. How prompts and facts will be tested

- **Prompts.**
  - Each printed prompt is run verbatim by a Claude Code session (this one or a sub-agent),
    in a disposable copy of the starter or checkpoint, in the scratch directory.
  - The resulting diff, render and checks are inspected, and the dry run is recorded in the
    chapter source as a comment: date, agent and model, and what was checked.
  - Prompts are tested with Claude Code only. Codex and Antigravity are not run, and the
    book says so, as it already does for screens.
  - Outputs shown in the book are real renders or real command output, never typed.
- **Quarto features.** Every option named is checked against
  `/Applications/quarto/share/schema` (1.10.20) and rendered once.
  - Already confirmed in the schema: `brand`, `reference-doc`, `csl`, `crossref`, speaker
    notes, `multiplex`, `chalkboard`, `logo`, website `search`, `aliases`, and
    `-P`/`--execute-params`.
  - Not yet checked: whether `_brand.yml` reaches DOCX and PPTX, and Reveal.js PDF export
    in 1.10.20. Both are to be rendered before writing.
- **External facts.** Each is opened at its official page and recorded in `facts.yml` or
  Further reading with the date. References are opened before they are cited.

## 8. Decisions (approved 2026-11-18: "go for it on all your mentions")

The author approved the plan and every recommendation. Where a question offered two options
without a recommendation, the first was taken: Q4 labelled synthetic business figures beside
the real model metrics; Q7 the agent still writes `hello.qmd`, with an annotated listing; Q8
the workflow is tested locally with `act` (installed with Homebrew, 0.2.98) and Docker; Q11
work stops for review after WP5; Q12 the preface says plainly that the book is Python-only.
The questions as asked:


- **Q1 — Structure.** Approve the two-route Part I, the new Parts III (Craft) and IV
  (Team), and the water analysis moving to Part V? The alternative is a new final part with
  the water analysis kept as Part III, which means fewer renumbered chapters but puts the
  professional material last.
- **Q2 — Spanish.** Approve `only: en` chapters, `translation/pending.yml` and a recorded
  temporary exception to `AGENTS.md`'s same-branch translation rule?
- **Q3 — Dataset.** Option A (UCI Bank Marketing) or another from §4? A new dataset needs
  your approval, and I will re-read its licence page before adding it.
- **Q4 — Investor update figures.** Use clearly labelled synthetic business metrics beside
  the real model metrics, or real model metrics only?
- **Q5 — File names.** Leave the existing names (recommended), or do WP15 (rename with
  aliases) after the spike?
- **Q6 — Zero-install route.** May I add a `.devcontainer/` for GitHub Codespaces? It is a
  new dependency on a container image and Quarto and uv features, verified before use.
  Codespaces has a free monthly allowance (to verify and date). It would also give Windows
  readers a route without WSL.
- **Q7 — Test render.** Keep the agent-written `hello.qmd` (it tests the agent too) with a
  side-by-side annotated listing in Chapter 4 (setup), or ship `starters/hello/hello.qmd` in
  the clone and have the agent only render it?
- **Q8 — CI testing.** Testing the book's Actions workflow needs a real GitHub repository,
  and this repository's push rules block test-repo pushes from here. Will you create and
  push a disposable test repository when WP10 reaches that step? Alternatively I can test
  with `act` locally, which is a new dependency.
- **Q9 — Workshop.** Add one optional ⭐ slide pointing to the professional parts, or leave
  the deck untouched?
- **Q10 — Low-cost route.** I would document the cheapest verified route for each agent
  (free tiers where they exist, small models, API pay-as-you-go with a spending cap) in
  Appendix K, and drop the deck's "paid plan required" wording only if a free agent route
  is verified. Agreed? Local open-weight models are left out unless you want them.
- **Q11 — Scope and order.** About 8 new chapters is a large revision. Ship in the WP order
  above, with WP0–WP5 as the first milestone (fast path and worked example) and pause for
  review there?
- **Q12 — R users.** The book stays Python-only. Add an R note per chapter (knitr's
  equivalents), or leave R out explicitly in the preface?
- **Q13 — Software engineers.** Per the audience ranking, they get one reading path and
  the RFC project, not a chapter of their own. Agreed?

## 9. Status log

| Date | Package | Done | Deferred, and why |
|---|---|---|---|
| 2026-11-18 | Phase 1 | Read the sources, ran the baseline builds (all green), checked the review's findings, wrote this plan | — |
| 2026-11-18 | WP0 (`revision/wp0-groundwork`) | `english_only` chapters (`book/scripts/chapter_list.py`, used by the profiles, roadmaps and Spanish landing page; roadmaps named after their part page); `translation/pending.yml` and `compare.py` reading pending files' English text at their commit; language-switch fallback to the other edition's home; CI workflow `.github/workflows/build.yml` (build and check only), run locally with `act` 0.2.98; README, `AGENTS.md` and `translation/PLAN.md` notes. English and Spanish HTML byte-identical to the published copies apart from sitemaps | The aliases spike was done in a scratch book instead (see §10); no rename needed now |
| 2026-11-18 | WP1 (`revision/wp1-facts`) | `book/facts.yml`, `scripts/facts.py`, Appendix K *Facts That Change* (English-only), `scripts/thaw.py` (clears frozen pages that quote facts.yml when it changes, run by `make`); Chapter 2's prices and model names, Chapter 4's accounts and chats, the preface's cost note and Chapter 8's hosts' free plans now come from facts.yml; Claude Code's accounts rechecked (now lists Ultra); landing page reads facts.yml in English | — |
| 2026-11-18 | WP4 (`revision/wp4-novice`, done before WP3 because it needs neither the example nor new chapters) | Glossary links at first use (`filters/glossary.lua`, both editions' formats, EPUBCheck clean); Chapter 4 defines VPN, proxy, API key, apt, curl, Homebrew, package manager; a low-cost route (Antigravity's free tier; API spending caps, each verified 2026-11-18); the test run's file shown with where each part is taught; `.devcontainer/` (Quarto 1.10.20, uv 0.11.32, gh; built and tested locally with the Dev Containers CLI 0.90.0 on arm64: tools present, the first report and the test run render) and a codespace section in Chapter 4 and Appendix A; ten glossary entries | A codespace on GitHub itself, and an amd64 build, were not tested |
| 2026-11-18 | WP2a (`revision/wp2-front-matter`) | Chapter 1 opens on professional and start-up reports and says where a start-up should keep other tools; Chapter 2 gains "Vocabulary, specification, verification" and "A step or a task?" | The preface waited for the new chapters (WP2b) |
| 2026-11-18 | WP3 (`revision/wp3-fast-path`) | `starters/eval-repo/` (Acme Signals, fictional; UCI Bank Marketing, CC BY 4.0; tests, a notebook, no Quarto), `checkpoints/14-eval-start/`, `checkpoints/15-eval-results/`, `examples/eval/` (deterministic outputs; 21 tests); Chapter 3, The Fast Path, every prompt dry-run verbatim by a fresh agent in a copy of the starter (8 minutes of agent time; three formats agree; fresh clone agrees); `scripts/evaluation.py` runs the example in its own locked environment; `thaw.py` re-runs pages when the example changes; Part I's two routes; roadmap alt text and Appendix I's agenda now computed (they had typed chapter numbers already out of date) | The pull-request step (`gh repo create`, `git push`, `gh pr create`) was checked against `gh --help` but not run: it needs your GitHub account (see below) |
| 2026-11-18 | WP5 (`revision/wp5-results`) | Part III, The Craft of Outputs, and its first chapter, One Set of Results: compute once and three kinds of check; a model card as a larger task with a plan first; numbered sections and references; a changed setting to predict and rebuild. Prompts dry-run from checkpoint 14; the dry run found "top 10%" typed in our own checkpoint's labels and captions, now computed or guarded. The water analysis is named instead of numbered (it is Part IV). Sources, copyright, glossary and checkpoints appendices updated | — |
| 2026-11-18 | WP2b (`revision/wp2b-preface`) | The preface names its readers, the start-up fit and limits, Python-only; reading paths by role (@tbl-reading-paths); three running examples; the landing page's audience copy, pills and project cards (found by page, after the craft part moved the water analysis); `make book-html` fails on an unresolved cross-reference | A landing-page card for the evaluation project needs its own media (`make ebook-media`); deferred |

| 2026-11-18 | WP6 (#140) | Chapter 11, Slides That Carry a Decision: deck vocabulary, a Reveal.js deck, a theme whose contrast a test checks, PDF from print view with headless Chrome, PowerPoint in a house template with alt text checked; checkpoint 16 | — |
| 2026-11-18 | WP7 (#141) | Chapter 12, A Site and One Brand: `_brand.yml` across html, revealjs and typst, Word and PowerPoint reference documents made from it, a website, `check_site.py`; checkpoint 17 | — |
| 2026-11-18 | WP8 (#142) | Chapter 13, White Papers and References: cross-referenced sections, equations, tables and figures, one CSL style in every format, `check_refs.py` against DOI registries, a Typst house template; checkpoint 18 | — |
| 2026-11-18 | Preface (#143, at the author's request) | "Free and open source, nearly all the way": the open-source toolchain and its licences, the agent as the one proprietary, swappable part | — |
| 2026-11-18 | WP9 (#144) | Chapter 14, Reports That Run Themselves: parameters through papermill, values validated, words chosen from printed numbers, a monthly investor update (business figures synthetic and labelled), segment reports, a checked batch script, and an educator's feedback sheets from a synthetic gradebook (`examples/feedback/`); checkpoint 19 | — |
| 2026-11-18 | WP10 and WP11 (`revision/wp10-team-ci`) | Part IV, Working in a Team: Chapter 15, Pull Requests and Builds You Can Trust (team rules, a pull request template, check, publish and monthly workflows; checkpoint 20), and Chapter 16, At Work and in a Start-up (vendors' data terms, confidential data, approved tools, proxies, templates, start-ups), every vendor and GitHub claim in `facts.yml` with its date. The water analysis becomes Part V. The plan's Chapters 15 and 16 (pull requests; CI) became one chapter: the pull-request part is short once the fast path has taught it, and CI is what makes the review trustworthy | Pushing, pull requests, the Publish and Monthly runs and branch protection need a GitHub repository; the check workflow was run with act, green and then red on a broken guard |

### Milestone (WP0–WP5): stopped here for review, as agreed

Checks on the final state (`revision/wp2b-preface`):

- `make book`: EPUBCheck 0 fatals / 0 errors / 0 warnings / 0 infos; 7 live links, 0 broken;
  5 scenes, 0 different. `make book-shots`: 0 sideways elements; new chapters checked by eye at
  phone width.
- `make book-es`: EPUBCheck clean; 36 files compared, 0 mismatches; glossary lint clean; 0 English
  sentences.
- `make deck`; `make ebook-check` and `make ebook-check EDITION=es`: all checks passed (the
  standing note that the release EPUB is older than the committed one remains; the author
  runs `make book-release`). Lighthouse 12.2.1, mobile, on the landing page: performance 99,
  accessibility 100, best practices 100, SEO 100.
- CI workflow run locally with `act` (arm64): every step passes; the landing-page step is
  skipped there because it needs Chrome.

Branches, each stacked on the one before (merge in this order): `revision/wp0-groundwork`,
`revision/wp1-facts`, `revision/wp4-novice`, `revision/wp2-front-matter`,
`revision/wp3-fast-path`, `revision/wp5-results`, `revision/wp2b-preface`, pushed on 2026-11-18 at the author's request as stacked pull requests #133 to #139, reviewed once with `/code-review` and merged bottom-up.

### Not verified, and why

- **The pull-request step of the fast path** needs a GitHub account and pushes to it; this
  repository's rules hand such pushes to the author. The commands were checked against
  `gh repo create --help` and `gh pr create --help` (gh 2.69.0). To test: run the fast path's
  "Review it as a pull request" box once in a private test repository.
- **Codespaces itself**: the dev container was built and checked locally on arm64; GitHub's
  amd64 codespace, its port forwarding and its token were not.
- **Prompts in Codex and Antigravity**: dry runs used Claude Code (Opus 5.5) only, as the book
  says of its screens.
- **Word alt text**: Quarto 1.10.20 does not carry `fig-alt` into Word pictures' descriptions
  (seen in both dry runs); the chapter says so, but no workaround is automated.

### For the Spanish edition (to translate)

New, English-only (`book/_chapters.yml`, `english_only`): `chapters/fast-path.qmd`,
`part-craft.qmd`, `chapters/results.qmd`, `slides.qmd`, `sites.qmd`, `white-papers.qmd`,
`parameters.qmd`, `part-team.qmd`, `team.qmd`, `at-work.qmd`, `appendices/k-facts.qmd`. Changed, waiting
(`translation/pending.yml`): the preface, Chapters 1–4 and 8 (01–03, 07), the setup and
first-chapter references in 08, 04, 05, 09, 10, 12 and the water exercises, Appendices A, E, G, I
and J, the copyright page, the afterword and the three part pages. `facts.yml` texts are English;
the Spanish landing page still reads its own preface and setup chapter.

### Remaining work packages (after review)

WP12 afterword projects, WP13 the workshop pointer slide, WP14 the Spanish to-do in
`translation/PLAN.md`, and optional WP15 (file renames with aliases, which the spike showed
work as JavaScript redirects) and WP16 (guards for Part V's typed prompt values).

## 10. Verified while working (2026-11-18)

Feature spikes in scratch folders, with Quarto 1.10.20 (Pandoc 3.10.0, Typst 0.15.1):

- `_brand.yml` reaches HTML, Reveal.js, dashboards and Typst; **not** DOCX or PPTX, which still
  need a `reference-doc` (both reference documents work; Word's heading colour also needs the
  theme's `accent1`).
- `-P`/`--execute-params` need **papermill** in the project's environment; `--output` and
  `-M output-file:` name each parameterised output; papermill's injected cell is echoed unless
  `echo: false`.
- Reveal.js has **no built-in PDF export** in 1.10.20: print view (E key) and the browser, or
  headless Chrome with `--run-all-compositor-stages-before-draw` on `?print-pdf`, which was
  flaky (1 blank in 6), so a script must check the page count. Print options must be set in
  YAML (`-M` is ignored).
- APA in HTML, DOCX and Typst alike: `csl: apa.csl` with `citeproc: true` (without it Typst
  formats the bibliography itself, with its own heading and title case).
- `quarto render nb.ipynb` does not execute; `--execute` executes **and writes the outputs
  back into the notebook**. `quarto convert` turns a notebook into a `.qmd`.
- `aliases` work in a book: relative to the chapter's folder, `/` for the project root;
  JavaScript-only redirects; ignored by EPUB.
- Website search is on by default; `about:` templates work; `open-graph` needs `site-url`.

Docs: quarto.org now documents Quarto 1.11.9; the book stays on 1.10.20, as installed, and
every feature it teaches is rendered with 1.10.20. The UCI Bank Marketing dataset is CC BY 4.0
(45,211 rows; DOIs 10.24432/C5K306 and 10.1016/j.dss.2014.03.001), and its `duration` column
leaks the target.
