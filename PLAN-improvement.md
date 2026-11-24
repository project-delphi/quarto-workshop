# PLAN-improvement: a more engaging *Prompt, Check, Publish*, one page per block

Status: **approved** 2026-11-24, from `main` at `651db10`. This file is the plan; its status log
(§14) records what is done, package by package.

## 0. Context

The book is complete and valid (EPUBCheck clean, both editions published, on Apple Books), but
two things hold it back as a book read alone on a phone or tablet.

**1. Page fit was never measured.** "Tables, figures and boxes stay on one page" exists only as
`break-inside: avoid` in `book/styles/epub.css`; `make book-shots` scrolls and never paginates.
A scratch audit made for this plan
(`/private/tmp/claude-501/-Users-ravikalia-Code-github-com-quarto-workshop/b9c108b6-2b5d-448a-8623-9752a38d7c8d/scratchpad/pag/paginate.py`,
with `gaps.py` and `walls.py` beside it; package A copies them into the repository first, since
the scratchpad can be cleared) lays
each chapter out in CSS columns in Chrome, as Apple Books and Readium paginate:

| Edition, profile | Pages | Blocks | Split over 2+ pages | Taller than a page | > ¾ page | Pages > ⅓ blank |
|---|--:|--:|--:|--:|--:|--:|
| EN phone 390×844, 16 px | 751 | 615 | **24** | 17 | 52 | **101** (45 ≥ ½) |
| EN phone, 18 px | 923 | 615 | **53** | 37 | 92 | — |
| EN phone, 20 px | 1,119 | 615 | 99 | 88 | 168 | — |
| EN tablet 820×1180, 18 px | 451 | 615 | 15 | 5 | 20 | 30 |
| ES phone, 16 px | 823 | — | **37** | 26 | 83 | — |
| ES phone, 20 px | 1,229 | — | 122 | 106 | 207 | — |

Phone splits are tables (13) and agent boxes (11); at larger text also openers, key ideas, think
boxes, quotes and transcripts. Blank pages come from blocks pushed whole to the next page (the
gap attribution and a few end-of-chapter cases are to be re-checked against page images, §3.1).
Text grows about ×1.27 from 16 to 18 px and Spanish adds about ×1.1, so English needs headroom.
Runs of 3+ phone pages with no figure, table, box, quote or code: 12 (glossary, Appendix K, both
exercise chapters, preface, Ch 4, 17, 20, afterword, Appendices E and G).

**2. Engagement is uneven.** Strong chapters exist (Ch 5's planted wrong number, Ch 4's "ends with
a number: 42", Ch 7's sight that changed hands), but: the "correct one fact, count the documents"
hook is used five times; six craft and team chapters (Ch 11–16) have no figure and no Pause and
think; Ch 2 and Ch 4 carry 16 and 13 "(checked …)" parentheticals; walls of 300–530 words;
payoffs are described, not shown (the Acme report, the deck's titles, the site, the council's last
slide); the Tunja and council threads of Part V never land (`book/PLAN.md` §15 lists this as
"worth doing next").

**Decisions (2026-11-24):** devices plus targeted rewrites, book length within ±5%; stories are
true (traced to the project's record) or **labelled illustrative scenes with no invented numbers
or results**; page breaks verified with the Chrome pagination simulation only (readers stay
"untested" in `book/README.md`); models mixed by role (§8); English first, then Spanish. No pause
for the author after the pilot: the lead and the cold readers judge it and work carries on. Each
package goes up as a stacked PR, gets one `/code-review` round, valid findings are fixed, and it
is merged bottom-up; `make book-release` and store uploads stay the author's.

## 1. Targets (definition of done)

A **unit** is the smallest piece the stylesheet keeps whole: a table, figure, image, block quote,
code or transcript block, aside, story box, live-link card, card of a card list, list item of an
opener or key ideas, half of a Pause and think (question; answer), part of an agent box (prompt;
agent; you). Measured by `make book-pages` (§3.1):

| Measure | Now (EN) | Target EN | Target ES |
|---|--:|--:|--:|
| Units split, gating profiles: phone 16 px, phone 19 px (Spanish proxy), tablet 18 px | 24 / – / 15 (blocks) | **0** | 0 at phone 16, 18 px and tablet |
| Unit height at phone 16 px | up to 1.6 pages | text ≤ 0.45, prompt ≤ 0.6, figure ≤ 0.65 (tablet ≤ 0.8) | — |
| Phone 20 px (report only) | 99 splits | each remaining one listed | listed |
| Pages > ⅓ blank / ≥ ½ blank, phone 16 px | 101 / 45 (re-measure) | ≤ 50 / ≤ 15 | ≤ 60 / ≤ 18 |
| Runs of ≥ 3 phone pages with no visual unit | 12 | 0 outside glossary and App. K | 0 |
| Screenshot text at phone width | many ~4 px | ≥ 9 CSS px (tool-checked) | same images |
| Chapter words | 86.3k | ±5% overall | follows EN |
| EPUB size | 16 MB | ≤ 20 MB | ≤ 20 MB |

Exceptions (the glossary; reference tables declared breakable) are listed with a reason in
`book/pagefit.yml`.

**Engagement:** blind pairwise cold reads (§7): for each numbered chapter a reader sees the
`651db10` text and the new text in random order and chooses on five axes (opening pull,
momentum, payoff seen, clarity, "I could do this"). Target: the new text wins opening pull,
momentum and payoff in at least 90% of chapters and loses no axis in any chapter after at most
two fix rounds. Structural floor for every numbered chapter: a cold open of ≤ 120 words before
any definition; at least one figure; at least one Pause and think; in hands-on chapters a
picture of the finished result in or just after the opener.

**Unchanged integrity rules** (AGENTS.md): numbers computed or cited; illustrations labelled and
number-free; EPUBCheck 0/0/0/0; live-link, scene, checkpoint and prompt-value checks;
translation checks; landing-page `quote()` guards; GIF rules; alt text on every new figure.

## 2. Engagement devices (book-wide)

**D1 Cold opens.** The first paragraph after each chapter title (`p.hook`; the post-processor's
regex needs a paragraph straight after the `h1`, `epub_postprocess.py` ~277) becomes a scene,
puzzle or real incident, ≤ 120 words, with no italic glossary terms (`filters/glossary.lua` links
the first italic term of a page, which would land in the hook). Keep the strong openings (Ch 4,
5, 7, 9, 10, 11, 23, afterword); retire the repeated "correct one fact" hook outside the preface.

**D2 Story boxes**, a new `::: story` aside after the hook, never before it, ≤ 80 words, in two
kinds. Each must be a failure the reader can meet in that chapter, not production trivia.
- *From the build log* — true, with a source comment (`<!-- source: REVISION-PLAN.md §10 -->`)
  the evidence reviewer checks. Candidates: "top 10%" left in our own checkpoint's labels, found
  by a dry run (Ch 10, `results.qmd` 273); the blank first slide from notes before the first
  heading (Ch 11, `slides.qmd` 145) and the headless print that came out blank (205); a navy logo
  on a navy bar (Ch 12, `sites.qmd` 216); "page 1 of 1" printing "pbge" (Ch 13,
  `white-papers.qmd` 203); `duration` leaking the target (Ch 3/10); zsh passing inline `#`
  comments as arguments (Ch 4, `book/PLAN.md` §15.4); a chapter's argument contradicted by its
  own numbers and "missing at random" corrected (Ch 18, 22, `book/PLAN.md` §12.2); Word dropping
  `fig-alt` (Ch 11/12, REVISION-PLAN "Not verified").
- *An illustration* — a composite scene, titled as one, with no numbers or results except ones
  computed from the repository: last month's figure in this month's investor update (Ch 14); a
  customer's name in an error message sent to an agent (Ch 16); a council member's question about
  Tunja (Ch 17).

**D3 Payoff pictures.** Hands-on chapters show the finished output early, captured at phone width
or cropped (and stacked, never side by side) so that its text is at least 9 CSS px. A new
`book/media/capture/eval_outputs.py` (pattern of `water_outputs.py`) makes the Part III–IV
pictures: the Acme report, the deck's title slide, the site home page, the model card, white-paper
page 1, two months of the investor update (stacked crops), a red and a green check. Recaptures for
screenshots unreadable at 340 px (`london-guide`, dashboards, `water-post`, white-paper pages:
title and abstract only). The council's last slide (Ch 23) from `examples/water`. New images keep
the EPUB within 20 MB.

**D4 Predict, then reveal.** At least one `::: think` per chapter; new ones where the reviews
found natural questions (slides L136, sites L206, white-papers L109, parameters L159, team L156,
at-work "may this file meet this agent?", fast path "a guard you have never seen fail"). The
question and answer halves may fall on different pages, so the page turn becomes the reveal. Ch 1
gains a no-install Try it: three error messages; name the render step each came from.

**D5 Spot the error, once per part** (as Ch 5's planted number): Part II exercises (a table a cell
renders with one value altered deterministically from the real one), Parts III–IV (a model-card
claim that disagrees with `results.json`), Part V (a council sentence that claims a cause).
Answers in Appendix E, computed: the D authors write the answer cells, the lead integrates them.

**D6 Through-lines.**
- *Part V:* opens on the council's question (Ch 17); a small computed **Tunja ledger** card (a
  definition list: raw value, kept?, transformed, cluster, what may be said) closes Ch 17–23; Ch 20
  gets Tunja back; Ch 23 ends on the council's last slide and Tunja after the rebuild.
- *Parts III–IV:* the Acme founder's decision the deck must carry; tease the age-ranking finding
  (`results.qmd` 147–154) in Ch 10's opening.

**D7 Rhythm and voice.** Break the walls listed in §5 into steps, tables or figures; move the
"(checked …)" parentheticals of Ch 2 and Ch 4 to Appendix K behind one dated line per section,
and reword `copyright.qmd` 13 ("checked on the dates given in the text") and its landing-page
guards (EN and ES) in the same branch; move production notes (how the animations were made) to
Appendix H; merge the preface's three route sections; second person, active voice.

**D8 Small fixes the reviews found:** exercises-water's "Exercise III.x" → V.x (auto IDs change;
the Spanish twin hard-codes them, so give explicit IDs); Ch 8's title against "all three in one
step" (check and align); lead-ins that point to the wrong next chapter (Ch 2 summary → fast path;
Ch 9 end → exercises and Part III); Ch 4 repeating Ch 1's `hello.qmd` listing.

## 3. Page fit

### 3.1 The measuring tool: `book/scripts/paginate_epub.py`, `make book-pages`

Productionise the scratch prototype. It unzips the EPUB, opens each chapter with `epub.css` in
installed Chrome through Playwright (as `shoot_epub.py`), measures each unit's natural height,
then lays the chapter out in columns (`html { height; column-width; column-fill: auto }`) and
records the pages each unit's fragments fall on (`getClientRects()` per column fragment).
- Profiles: phone 390×844 at 16, 19 px and tablet 820×1180 at 18 px gate; phone 18 and 20 px report.
- Per page: blank share, attributed to the unit that was pushed, following `break-after: avoid`
  from a heading to the unit it travels with. Before the targets are trusted, the lead checks the
  baseline's half-blank pages against page images (some fall on the page before a chapter's last,
  with no block nearby).
- Per image: rendered scale; with each screenshot's text size at capture (listed in
  `pagefit.yml`), the text size on a phone; a capped image counts as a warning, not a pass.
- Per chapter: pages, words, runs of pages with no visual unit.
- Outputs: `_book/pages/<edition>.json`, a Markdown report sorted by severity naming the chapter
  file and the unit (`#tbl-…`/`#fig-…` id, or section id and first words), and a PNG of each
  offending page for the render reviewer.
- `make book-pages [EDITION=es] [ONLY="ch012 ch019"] [EPUB=…]`, non-zero on a unit split or over
  budget at a gating profile unless listed in `book/pagefit.yml`. Run on the store EPUB too.
- Self-test: a fixture chapter with a too-tall table and a split box must fail (mutation test).
- CI (`.github/workflows/build.yml`, beside the Chrome-only landing-page step): **report only**,
  because the runners lack Charter and Avenir Next; the gate is local.

### 3.2 Shared CSS, filter and helper changes (lead only; they reach Spanish through symlinks)

All land in package A, which is checked on both editions at once; later shared changes are
additive only while Spanish lags (§4).
- `epub.css`:
  - Break points by design: `.think` may break between `.think-question` and `.think-answer`
    (each kept whole); `.opener` before `.opener-meta`, and its list between items; `.keyideas`
    between items, label kept with the first; card lists between cards.
  - Agent boxes: measure both variants in A (whole box kept vs parts kept, as now) and keep the
    one with no unit splits and fewer blank pages; keep the Apple Books fix (`position: static`,
    `overflow: visible`, `epub.css` 94–100) either way.
  - `blockquote { break-inside: avoid }`.
  - Images: `max-height` in `vh` with `object-fit: contain` and `!important` where inline widths
    would otherwise win; replace `img.scaled`'s `max-height: 40em`, which grows with the font.
  - `.story`, `.payoff`, `.cards`, `.ledger` styles; `.breakable` written against the element
    Quarto actually puts the class on (checked in A), with those tables listed in `pagefit.yml`.
- `filters/book.lua`: `story` (two titles, en/es labels), `cards` (definition-list cards), `payoff`
  figure class, `ledger`.
- `book.scss`: the same components for the HTML edition, light and dark.
- `scripts/figures.py`: an opt-in `grid(3, square=True)` (2×2 with the legend or a note in the
  fourth panel) for D4 to adopt cell by cell, changing each cell's unpacking, caption and alt text
  with it; the existing `grid(3)` is unchanged, since `09-explore.qmd` 230 unpacks three axes and
  Spanish runs the same cells. Saved PNG shapes are checked by `book-pages`, not by `figsize()`.
- `scripts/roadmaps.py`: the Part V roadmap (h/w 1.51) in two columns; then `media_es.py`.
- `Makefile`: `book-pages`, and `book-es-fresh`.
- `book/README.md` Conventions: the budgets of §3.3 replace "kept to about one phone screen".

### 3.3 Budgets for authors

The gate is the tool's (§1). Rules of thumb at phone 16 px, from the baseline's own blocks (a
boxed prose unit is about 0.11 page plus 0.41 page per 100 words):

| Unit | Rule of thumb | If over |
|---|---|---|
| Aside, story, card | ≤ 80 words | cut, or move detail to the text |
| Pause and think | question ≤ 60 words, answer ≤ 80 | shorten the answer |
| Opener | ≤ 4 objectives of ≤ 20 words; meta lines short | — |
| Key ideas | items ≤ 25 words | fewer, shorter items |
| Table | ≤ ~350 characters of cell text, ≤ 3 columns, caption ≤ 2 lines | split by theme; detail to prose or Appendix K; or cards |
| Figure | EPUB image h/w ≤ 1.25; caption ≤ ~180 characters | `grid(3, square=True)`; notes from caption to text |
| Prompt | ≤ ~500 characters (≈ 0.6 page) | two turns, or a short prompt with the items as a list outside the fence |
| Agent, you parts | ≤ 4 short items each | — |
| Code, transcript | ≤ ~18 lines after wrapping at ~39 characters | excerpt plus the file's path, or two computed transcripts |
| Block quote | ≤ 60 words | quote less |
| Screenshot | text ≥ 9 CSS px on a phone | recapture at phone width, or crop |

### 3.4 Known offenders (the audit confirms the list in package A)

- **Tables:** preface reading paths (1.5 pages) → cards; Ch 11 deck vocabulary (1.3) → "on
  screen" and "look and export"; Ch 16 vendor terms (1.6) → a short grid (trains on it? kept how
  long? opt-out?) from new short `facts.yml` entries the lead drafts with sources and dates
  (`_es` twins), the full text staying in Appendix K; Ch 17 the nine features (1.1) →
  `var_table` without code names in the first column; Ch 13 white-paper vocabulary (1.0) → 6
  rows; Ch 12 site vocabulary (0.9); Ch 2 slash commands → 2 columns; Appendices B.2 (1.4), D.1,
  D.3 (1.6), E.2, E.3 (1.6), H.1, I.1, K.1 → cards or splits.
- **Agent boxes:** Ch 8's 942-character audiences prompt (1.26 pages) → a lead prompt plus the
  three items as a list; Ch 9 publish prompt (660) → two; Ch 15 team prompt (708) → rules and
  template; Ch 10 (715) and Ch 13 (682) trimmed; the boxes split in Ch 4, 7, 10, 11, 12, 22;
  the afterword's three long boxes (1.26–1.28) → two turns each.
- **Figures:** Ch 21 `fig-wat-outcomes` (h/w 1.79) and `fig-compare` (1.62), Ch 18 `fig-tunja`
  (1.58, 372-character caption) → `grid(3, square=True)` or a set EPUB size, one-sentence
  captions; Ch 6 `toy.md` (39 lines) with `toy-md.png` (h/w 2.09) → two source-and-result pairs
  split at the `---` rule (new image names, since Spanish reads `media/figures` through a
  symlink); the Part V roadmap.
- **Code:** Ch 5's `cat report.qmd` (26 lines, up to 76 characters, with inline code) → two
  computed transcripts (lines 1–16, 17–26); the starter is not rewrapped. Ch 6 fence L657 (a
  174-character table row) and Ch 4 L348 (aligned notes that wrap).

## 4. Order of work, branches and file ownership

| # | Branch | Who (§8) | Contents | Done when |
|---|---|---|---|---|
| 0 | `improve/0-plan` | lead | `PLAN-improvement.md` | merged |
| A | `improve/a-pagefit-tooling` | lead | §3.1 tool, `pagefit.yml`, §3.2 shared changes, short vendor facts, README budgets, CI step; baseline report in §14 | tool self-test fails as it should; `make book` and `make book-es` green; baseline for every profile, checked against page images |
| B1 | (no branch) | developmental editor | `PLAN-improvement-briefs.md`: the whole-book spine (hooks, threads, which stories go where, word budget per chapter) and the three pilot briefs | lead accepts |
| — | — | cold readers | "before" reads of the `651db10` text, kept for §7 | reports saved |
| C | `improve/c-pilot` | 3 module authors | Ch 1 (`01-quarto`), Ch 11 (`slides`), Ch 18 (`09-explore`) to the full standard | **lead gate:** pilot wins its pairwise reads, page targets met; then the voice guide |
| B2 | (no branch) | developmental editor | voice guide (from the pilot), the remaining briefs | lead accepts |
| D1 | `improve/d1-front-part1` | author | preface, part-1, Ch 2–5 | §12 checks; the lead's `make deck` and `make ebook-check` pass in the main checkout |
| D2 | `improve/d2-part2` | author | part-2, Ch 6–9, exercises-london | §12 checks |
| D3 | `improve/d3-craft-team` | author | part-craft, Ch 10, 12–16, part-team, `eval_outputs.py` | §12 checks |
| D4 | `improve/d4-part5` | author | part-3, Ch 17, 19–23, exercises-water, afterword, the ledger, the council slide | §12 checks |
| E | `improve/e-appendices` | layout fixer, then lead | Appendices B, C, D, H, I, K layout; E's puzzle answers integrated by the lead | after D1–D4; §12 checks |
| F | `improve/f-review-fixes` | reviewers, then lead | §7 reviews of the whole book; fixes (two rounds at most); full page sweep | §1 English targets |
| G | `translation/improve-es` | translators, Spanish layout fixer | §10 | §1 Spanish targets; translation checks clean |
| H | `improve/h-publish` | lead | §11 | §12 final checks |

**Worktrees and ownership.**
- D1–D4 run in parallel, each in its own git worktree with its own `book/.venv` (`uv sync`) and
  `book/_book`, writing only its own `.qmd` files and the media or capture files named for it,
  and committing only its own `book/_freeze/<page>/`, never `_freeze/inputs.json` or the
  generated profile files. New worktrees get new names; the four left in `.claude/worktrees`
  from earlier sessions are not touched.
- **Shared files are the lead's alone:** `epub.css`, `book.scss`, `filters/*`,
  `epub_postprocess.py`, `figures.py`, `prose.py`, `roadmaps.py`, `thaw.py`, `facts.yml`,
  `j-glossary.qmd`, `appendices/e-checkpoints.qmd`, `_chapters.yml`, `media/build.py`,
  `translation/pending.yml`, `ebook/*`, `copyright.qmd`, `Makefile`, README, AGENTS. Authors put
  what they need in their report (glossary terms, facts with sources, answer cells, quoted
  sentences they changed). Shared changes land in A or at named sync points between waves, where
  the lead regenerates `_freeze` (a `facts.yml` change re-runs every page that quotes it), so no
  author's tree changes under them.
- The lead adds each changed file to `translation/pending.yml` at merge, at its pre-change
  commit (translation/PLAN.md §8), so `make book-es` stays green until G.
- Checks that need `.conda` (`make deck`) or the landing page run in the main checkout, by the
  lead, after each package returns. Nothing renders into `docs/` until H.
- At most four writing agents at once; read-only reviewers may run alongside.

## 5. Chapter worklist (from the reviews; the briefs expand it)

| Ch (file) | Opening | Engagement | Page fit |
|---|---|---|---|
| Preface (`index`) | keep the hook question; cut paras 2–3 | merge three route sections; "who it is for" and licences ~830 → ~300 words; keep every phrase the landing page quotes or re-quote it | reading paths → cards |
| Part I (`part-1`) | — | 343 → ~120 words; roadmap shows the fork | — |
| 1 (`01-quarto`) **pilot** | a real copy-and-paste failure in place of abstract paras 2–3 | Try it: name the render step from three errors | key ideas items |
| 2 (`02-assistant`) | the pelican grid right after the first paragraph | 16 dated parentheticals → Appendix K; hedges cut | slash table → 2 columns; Table 2.1 caption 299 → ≤ 180 characters |
| 3 (`fast-path`) | a scene with an existing repository, not a feature list | payoff: the Acme report; think box on the guard; `duration` story | three ~450-character prompts |
| 4 (`03-setup`) | keep "42" | six-step map first; 530-word wall → checklist; 13 dated parentheticals → Appendix K; duplicated low-cost text cut; zsh story | "you do" box (0.83); aligned-notes fence |
| 5 (`first-report`) | keep | — | `cat report.qmd` → two computed transcripts |
| Part II (`part-2`) | keep | — | — |
| 6 (`04-markdown`) | keep the finished guide first; cut the defensive paragraph | animation notes → Appendix H; rules paragraph → table | toy pair split; table-row fence; guide screenshot recaptured |
| 7 (`05-compute`) | keep | remove the repeated matplotlib/Plotly think box | split box (0.50) |
| 8 (`06-audiences`) | the three readers (L50–53) | vendor paragraph → 4-row table; a sub-agent-gone-wrong story; title check | 942-character prompt → lead prompt + list |
| 9 (`07-publish`) | keep | payoff: the live site on a phone; host trivia cut; lead-in fixed | publish prompt → two; white-paper crop |
| Part II exercises | — | spot the altered value | wall (6 pages) |
| Part III (`part-craft`) | recap → stake | repeated frame cut | — |
| 10 (`results`) | tease the age-ranking finding | "top 10%" story; think answer ~80 words | prompt 715; "you do" box (1.08) |
| 11 (`slides`) **pilot** | keep "remember perhaps three" | the deck's eight titles printed (the cell already reads them); title-slide picture; blank-slide story; think box | vocabulary table split |
| 12 (`sites`) | keep | site picture; navy-logo story with before and after; think box | box (0.93) |
| 13 (`white-papers`) | keep | "pbge" story; page-1 picture; think box | vocabulary 9 → 6 rows; prompt 682 |
| 14 (`parameters`) | illustration: last month's figure | two months, stacked crops; think box | — |
| 15 (`team`) | keep | red-build log excerpt and picture; think box | prompt → rules + template |
| Part IV (`part-team`) | a concrete stake | — | — |
| 16 (`at-work`) | illustration: a customer's name in an error message | "may this file meet this agent?" diagram (then `media_es.py`); think, Try it | vendor table → short grid |
| Part V (`part-3`) | keep the data hook; name the council's question | — | roadmap redrawn |
| 17 (`08-water-question`) | the council's question about Tunja | Saber 11 later; sources → compact table; first ledger | features table; diagram labels |
| 18 (`09-explore`) **pilot** | the 2017 infant-mortality puzzle (L257–263) | ledger; "missing at random" story | `fig-tunja` |
| 19 (`10-prepare`) | tease Tunja vs Cartagena | 390-word wall → one Tunja row before/after; ledger | caption 299 → ≤ 180 |
| 20 (`11-cluster`) | keep | Tunja back; ledger | wall (3 pages) |
| 21 (`12-interpret`) | keep | small-numbers wall trimmed; ledger | `fig-wat-outcomes`, `fig-compare` |
| 22 (`13-causation`) | keep | the wrong and the honest sentence as the climax in the text; paragraphs numbered to the diagram's arrows; ledger | key ideas; split box (0.50) |
| 23 (`14-publish-many`) | keep | the council's last slide; Tunja after the rebuild; legible crops | — |
| Part V exercises | — | V.x numbering, explicit IDs; capstone "write the council's last slide"; spot the causal claim | wall (4 pages) |
| Afterword | keep | 257-word caveat wall trimmed | three long boxes → two turns each |

## 6. The briefs (B1, B2)

One per chapter, by the developmental editor, read by that chapter's author, accepted by the
lead: the cold open (a draft of ≤ 120 words; true or an illustration; its source); story picks
with sources; the payoff picture (what, where, how captured, its text size); the Pause and think
question and answer; walls to break and how; cuts and moves within the chapter's word budget;
the chapter's offenders from the audit and the fix for each (§3.3); landing-page sentences to
keep or re-quote (`ebook/index.qmd` 80–105, `ebook/_source.py` `audiences()` and friends);
new glossary terms (italic at their definition, never in a hook). B1 also sets the spine: which
hook each chapter uses (no repeats), the two threads, and which stories go where. The voice guide
(B2) is one page, drawn from the accepted pilot, read by every author and translator.

## 7. Reviews (package F, and on the pilot)

- **Cold read** (two readers per part: a newcomer, and a working analyst or founder): the chapter
  text with its figures and a few sample pages, not every page image, and not the briefs. Blind
  pairwise against the `651db10` text (order randomised, labelled X and Y), a choice per axis of
  §1, and the three places each reader would stop. Two fix rounds at most.
- **Evidence review:** every story traced to its source; every illustration labelled and free of
  invented numbers; every new number computed (`text_holds`, `alt_text_holds` where words depend
  on data); every new fact in `facts.yml` with URL and date, opened (with a web-fetch agent).
- **Render review:** the tool's offending pages and a sample per chapter (phone 16 px, tablet,
  light and night), `make book-shots` for changed chapters, `scripts/shoot_html.py` at 1440×1000
  and 1366×768 for changed HTML pages; defects by chapter and unit.
- **Triage:** reads the logs of `make book`, `make book-pages`, the translation and landing-page
  checks that the author or lead ran, and reports each failure with the file and line to fix. It
  does not run builds in an author's tree.

## 8. Agents and models

Fable 5.2 ($8/$40 per M tokens) only where whole-book judgement or unanchored reading pays; Opus
5.5 ($4/$20) for writing that must follow this repository's many rules; Sonnet 5.5 ($2/$10) for
bounded fixes, dry runs and reviews; Haiku 5.5 ($0.10/$0.50) for log triage, inventories and a
weak-model dry run. All through the Agent tool; a Workflow only if the author asks.

| Role (AGENTS.md contract) | Agent type, model | Count | Writes | Gets |
|---|---|--:|---|---|
| Lead integrator | this session, Opus 5.5 | 1 | shared files, facts, answers, merges, landing pages, publish | everything |
| Developmental editor | general-purpose, **Fable 5.2** | 1 (B1, B2) | `PLAN-improvement-briefs.md` only | the whole book, the reviews, the audit, §2–3 |
| Module authors (C, then D1–D4) | general-purpose in a worktree, **Opus 5.5** | 3, then 4 | their chapters and named media files | brief, voice guide, §3.3, README Conventions, AGENTS.md |
| Layout fixers (E; F sweep; Spanish pass in G) | general-purpose in a worktree, **Sonnet 5.5** | 1–2 | flagged units only | audit report, §3.3 |
| Cold readers | general-purpose, read-only, **Fable 5.2** | 2 per round | report | text and figures, sample pages; not the briefs |
| Evidence reviewer | general-purpose, read-only, **Sonnet 5.5**, with a web-fetch agent for links | 1 per part | report | diffs, story sources, facts |
| Render reviewer | general-purpose, read-only, **Sonnet 5.5** | 1 per part | report | page images, shots |
| Prompt dry-runner (§9) | general-purpose, **Sonnet 5.5**; a second run on **Haiku 5.5** | 1 per changed prompt | scratch copies only | the prompt as printed, a checkpoint copy |
| Triage and inventories | general-purpose or Explore, **Haiku 5.5** | as needed | report | logs, file lists |
| Translators (G) | general-purpose in a worktree, **Opus 5.5** | 4 (one per part group) | `book-es/` twins of their part | English diff per file, `translation/glossary.md`, voice guide, Spanish budgets |
| Spanish reader | general-purpose, read-only, **Opus 5.5** (not a translator) | 1 | report | rendered Spanish chapters |

Every delegated task gets a bounded file list, the expected output, the checks to run before
returning (`make book-epub`, `make book-pages ONLY=…`), and "say what you did not verify". No
agent publishes, pushes, renders into `docs/`, runs `gh release` or starts a paid agent session
beyond the dry runs of §9.

## 9. Prompts changed by the work

Every prompt that is split or rewritten is run verbatim by a fresh Sonnet 5.5 sub-agent in a
disposable copy of its checkpoint in the scratchpad, as WP3 and WP12 did, then by Haiku 5.5 as a
check that a smaller model (readers may use free ones) still gets there; the run (date, model,
what was checked, where Haiku failed) is recorded as a comment in the chapter. Water prompts keep
passing `scripts/check_prompt_values.py`. Translated prompts are not dry-run, as today. The deck's
prompts are not changed.

## 10. Spanish (package G)

- Translators work from each file's English diff since its `pending.yml` commit, with
  `translation/glossary.md` and the voice guide; new chart text gets `TERMS_ES`, facts `_es`
  twins, changed diagrams `media_es.py`, and the Spanish landing page its re-quotes
  (`ebook/es/index.qmd`).
- Spanish may not split a unit on its own (`compare.py` requires the same IDs and tables), so
  translators get the Spanish page report and may condense wording to fit; a Sonnet layout pass
  then fixes what remains, by wording only.
- Done when `make book-es` (EPUBCheck, `compare.py`, `lint.py`, `english_scan.py`) passes with
  `pending.yml` empty, `make book-pages EDITION=es` meets §1, and the Spanish reader's report is
  resolved.

## 11. Publishing (package H)

`make site` (deck, then both books), `make book-publish` and `make book-es-publish`,
`make ebook-media STEPS=inside` (its selectors `#sec-yaml .agent-box`, `.tryit:has(.catchup)`
must still match), `make ebook-check` for both editions, Lighthouse (mobile) at 375×812 and
1440×900, `make book-store` with EPUBCheck and `make book-pages` on the store EPUBs. Then the
author: `make book-release` (the download buttons serve the latest release) and the store
uploads as updates (`book/STORES.md`), without which readers keep the old book.

## 12. Verification

Per package on its branch, then in full at H:
- `make book`: EPUBCheck 0/0/0/0; live links; scenes; latest checkpoint; prompt values.
  `make book-fresh` (and `book-es-fresh`) after changes to `figures.py`, `roadmaps.py`,
  `scenes.py`, `water.py` or a starter.
- `make book-pages` (EN; ES after G) against §1, with the before/after table in §14.
- `make book-shots` for changed chapters; `scripts/shoot_html.py` for changed HTML pages; the live
  scenes still draw.
- `make book-es` and the translation checks (green throughout, through `pending.yml`).
- In the main checkout: `make deck` (keeps `docs/book/`), `make ebook-check` both editions.
- `git diff --check`; words within ±5%; pairwise cold-read targets; EPUB ≤ 20 MB.

## 13. Risks

- **Shared changes in flight.** A `facts.yml` or filter change re-runs other packages' pages;
  hence the sync points and lead ownership (§4).
- **Spanish drift.** Mitigated by `pending.yml`; class-only changes pass `compare.py`, but shared
  CSS and helpers change Spanish output at once, so A is checked on both.
- **Over-trimming.** The budgets can tempt cuts of real content; the briefs set a word budget per
  chapter and the cold readers check clarity as well as pull.
- **Prompt changes.** Each is dry-run (§9); a prompt that fails on Haiku is simplified or the
  chapter says what a smaller model needs.
- **Fonts.** The simulation uses the macOS fonts the stylesheet names; readers that substitute
  fonts can break differently; readers stay "untested" in `book/README.md`.

## 14. Status log

| Date | Package | Done | Deferred, and why |
|---|---|---|---|
| 2026-11-24 | Plan | Three read-only reviews (Parts I–II; Parts III–V; infrastructure and the Spanish pipeline); pagination baseline in both editions; an independent review of this plan, folded in; decisions on depth, stories, readers, models, pilot and merging | — |

## Critical files

`book/styles/epub.css`, `book/styles/book.scss`, `book/filters/book.lua`,
`book/scripts/epub_postprocess.py`, `book/scripts/figures.py`, `book/scripts/shoot_epub.py`
(pattern for the new `paginate_epub.py`), `book/scripts/thaw.py`, `book/facts.yml`,
`book/media/capture/water_outputs.py` (pattern for `eval_outputs.py`), `book/README.md`,
`Makefile`, `.github/workflows/build.yml`, `ebook/index.qmd`, `ebook/_source.py`,
`book/copyright.qmd`, `translation/compare.py`, `translation/pending.yml`, `translation/PLAN.md`.
