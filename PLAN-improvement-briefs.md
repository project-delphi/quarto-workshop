# PLAN-improvement-briefs: the spine and the three pilot briefs (package B1)

Written 2026-11-24 by the developmental editor, from `improve/a-pagefit-tooling` at `52d9215`.
It expands `PLAN-improvement.md` §2, §5 and §6. Line numbers are those of the `.qmd` files at
that commit. Word counts are `wc -w` on the `.qmd` (code cells included); a chapter may land
within ±5% of its target. Inputs: the reader-view text of `651db10`, the page audit
(`book/_book/pages/en.md`), the two "before" cold reads (`before-reads.md`), and the story
sources named below, each read at the line cited. Section 5 lists what I could not verify.

## 0. Lead decisions (2026-11-24)

Accepted as written unless listed here. The two cold reads are in `PLAN-improvement-reads.md`.

1. **T7, the blank PDF.** The Chapter 11 author tests it: in a scratch copy of
   `checkpoints/16-eval-slides/`, print the deck six times with
   `--run-all-compositor-stages-before-draw` and six times without, count the blank PDFs,
   and rewrite `slides.qmd` 204–207 to what was observed, with the date and Chrome's
   version. The story quotes no rate. `REVISION-PLAN.md` is a historical record and stays.
2. **The council stays generic** (rule 5): accepted.
3. **The deck's eight titles are not rendered inside a book cell** (a `quarto render` nested
   in a book render is fragile). The `deck` step of the new `media/capture/eval_outputs.py`
   renders the deck, captures the title slide and writes the titles as rendered to
   `media/figures/eval-deck-titles.json`. The chapter reads that file, prints the numbered
   list, and guards it: as many titles as `n_slides`, and the headline title equal to the
   sentence the chapter computes (L91–92). A stale capture then stops the render. No change
   to `scripts/evaluation.py`.
4. **The fast path's planted error** is the cell-derived "README claim" (§2.2); the starter
   does not change.
5. **Chapter 11's deck prompt** is trimmed as proposed. The author records the change; the
   lead dry-runs it (Sonnet, then Haiku) before the pilot merges.
6. **`fig-drift`**: shorten the caption to one sentence first; redraw the SVG only if
   `make book-pages` still fails it (a redraw also changes the Spanish diagram).
7. **Shared capture scripts:** the Chapter 11 author creates `eval_outputs.py` with the
   `deck` step only; the Chapter 18 author adds an `explore` step to `water_outputs.py`.
   Each commits the pictures (and JSON) the step makes and says the capture's text size in
   pixels, for `pagefit.yml`'s `screenshots`.
8. **"Stuck for two minutes?"** (rule 6): done by the lead in `filters/book.lua`: the first
   catch-up box of a chapter explains in full, later ones in one line.

## 1. Rules of the spine

1. **One hook each, no repeats.** "Change one number: how many documents are now wrong?" is
   the preface's alone. Chapters 1, 7, 8 and 9 stop posing it; Chapter 9 keeps "predict the
   rebuild" as an exercise (it is the chapter's task), not as its opening.
2. **The Chapter 5 device, often.** Both cold readers named "find the planted error" and
   "predict before you rebuild" as the book's best moments and asked for more. So besides
   the three D5 puzzles, every hands-on chapter from 10 on has one predict-or-spot moment,
   normally as its Pause and think. A planted value is always derived by a cell from the
   real one, with a `text_holds` that the two differ, and its answer is computed too.
3. **Show the output.** Parts III–IV are "the best content and the worst shown". Each of
   Chapters 3 and 10–15 gets a `::: payoff` picture straight after the opener.
4. **Collapse the audit trail.** "Traps met in the test run" paragraphs become one true
   story (where one is vivid) plus a symptom / cause / fix table or cards within budget.
   "(checked …)" stamps leave the prose: Chapters 2 and 4 to Appendix K (D7); elsewhere they
   stay only in Further reading. "Not re-tested" and "What was not tested" passages move to
   one short note per chapter, or to Appendix H.
5. **The council is never a real council.** Tunja is a real municipality, and an
   illustration may not show a real organisation acting. The reader's audience stays "a
   municipal council" (as `08-water-question.qmd` 114–115 has it), never "Tunja's council";
   Tunja is the case *the analyst* follows. Acme Signals is fictional and already labelled.
6. **Cut each duplicate to one home.** Start-up fit: full in §16.6, a short bullet in §1.5
   (reader B: "earns trust"), one sentence in the preface. Contrast table: Chapter 11 only;
   Chapter 12 refers to it. "You will rarely write a theme by hand": the Part III page only.
   The OpenCode warning: once, in Chapter 4. The GitHub Pages plan sentence: Chapter 9 only.
   The full "Stuck for two minutes?" paragraph: once per chapter, then the bare box (a
   filter change: the lead's).

## 2. The spine

Hook types: S scene, P puzzle, T true incident, I illustration. "Keep" means the first
paragraph stays, trimmed to ≤ 120 words with italics removed.

| Unit (file) | Hook | Story box (source in §4) | Payoff picture | Think / predict to add | Thread | Words |
|---|---|---|---|---|---|---|
| Preface (`index`) | P, keep: "how many documents are now wrong?" Cut paras 2–3 | — | Figure 1 (the loop) on the first screen | keep the one | names Tunja, Acme, London in a line each | 3,788 → 3,350 |
| Part I (`part-1`) | the fork, in three sentences | — | roadmap shows both routes | — | — | 360 → 150 |
| 1 (`01-quarto`) **pilot** | S: four copies of one number | T1 the book's own typed chapter numbers | — (reading; two diagrams) | Try it: three errors, name the step | — | 3,226 → 3,100 |
| 2 (`02-assistant`) | P: the pelican question, one plain sentence; grid (`fig-pelicans`, L194) moved to straight after para 1; cost figures follow the grid | — | the grid | keep 4; add a signpost "daily agent users: read §2.7–2.9" | — | 5,736 → 5,300 |
| 3 (`fast-path`) | P: "One sentence in this repository's README no longer matches its results" (planted, §3.3 below) | T2 a notebook full of outputs in the commit | the Acme report, top of page 1 | keep "a guard you have never seen fail" | Acme introduced: two people, one model, a bank's call list | 3,125 → 3,250 |
| 4 (`03-setup`) | keep "42" | T3 zsh and the inline `#` | the two outputs that say 42 | keep 2 | — | 4,654 → 4,300 |
| 5 (`first-report`) | keep | — (the chapter is the puzzle) | — | keep 6 | — | 5,383 → 5,350 |
| Part II (`part-2`) | keep | — | — | — | — | 223 → 220 |
| 6 (`04-markdown`) | keep (finished guide first); cut "More is new here…" | — | `london-guide` recaptured at phone width | keep 4 | — | 8,070 → 7,700 |
| 7 (`05-compute`) | keep (the sight that changed hands) | — | — | keep 4 of 5 (drop the repeated matplotlib/Plotly one) | — | 3,422 → 3,400 |
| 8 (`06-audiences`) | S: three readers, three glances (from L50–53) | I1 two helpers, one folder | the three outputs, stacked crops | keep 2 | — | 3,367 → 3,350 |
| 9 (`07-publish`) | keep ("nobody but you can see it") | T4 the first publish that `--no-prompt` stopped | the live guide on a phone | keep 2 | — | 3,720 → 3,600 |
| Part II exercises | P: "one cell of this table is last year's" | — | — | **D5-a** | — | 1,931 → 2,000 |
| Part III (`part-craft`) | the stake: a decision three kinds of reader will check. Then a bridge (§3.4) | — | — | — | Acme's decision stated | 411 → 300 |
| 10 (`results`) | P: the model card will say something its makers did not expect: whom the list reaches (age finding, L147–154, teased without the numbers) | T5 "top 10%" left behind | the model card, top of page 1 | think answer L267–280 cut to ≤ 80 words; the leak (`duration`) as a second think | the finding the decision must carry | 2,731 → 2,800 |
| 11 (`slides`) **pilot** | keep "remember perhaps three of them" | T6 the blank extra slide; T7 the blank PDF | the title slide; the eight titles printed | think: which habits can the title list prove? with one planted title | the last slide is the decision | 2,603 → 2,750 |
| 12 (`sites`) | keep | T8 the navy logo on the navy bar (before/after crops) | the home page at phone width | think (L206): what can a script check that an eye cannot, and the reverse? | where an investor finds it | 2,481 → 2,600 |
| 13 (`white-papers`) | keep | T9 "pbge" | page 1: title block and abstract only | think (L109): a DOI resolves; is the reference checked? | the document that leaves the building | 2,276 → 2,400 |
| 14 (`parameters`) | S, keep, trimmed | I2 last month's figure in this month's update | two months of the update, stacked crops | predict: which sentences differ between the two months? (computed diff) | the monthly update to investors | 1,854 → 2,100 |
| Part IV (`part-team`) | S: the change is right on your machine and red on everyone else's | — | — | — | — | 188 → 170 |
| 15 (`team`) | keep | T10 06:00 UTC is not 07:00 in London in winter | the red check naming the sentence (log excerpt, computed from `team.qmd` 172–173) | **D5-b**; think (L156) | the build that stops a false claim | 2,415 → 2,550 |
| 16 (`at-work`) | S: you paste an error into the agent; a customer's name is in it | I3 the same scene, carried to its end | diagram: "may this file meet this agent?" | think on that diagram; a Try it | closes Acme: what a start-up builds this way | 1,367 → 1,600 |
| Part V (`part-3`) | keep the data hook; add the council's question in one sentence | — | roadmap | — | council question | 366 → 380 |
| 17 (`08-water-question`) | S: the question a council member will ask when the slides end (no numbers); the INCA figures move to para 2 | I4 "so is it the water?" | — | keep 2 | Tunja named; **ledger 1** | 3,576 → 3,500 |
| 18 (`09-explore`) **pilot** | P: Tunja's infant mortality falls in 2017. Progress? | T11 "missing at random" | `explore.html`, missing values by zone | the reveal (L257–263), reworded | **ledger 2** | 2,674 → 2,750 |
| 19 (`10-prepare`) | P: Tunja and Cartagena, far apart on the map; how far apart in the table? (uses the existing two-place distance example) | — | — | keep 2 | **ledger 3**; one Tunja row before and after replaces the wall at L106–131 | 2,940 → 2,850 |
| 20 (`11-cluster`) | keep; say at the top that the normal route copies the finished script | — | — | predict: which cluster(s) will Tunja's two zones fall in? (answer: `tj_text`, L47–58) | **ledger 4** | 4,285 → 4,250 |
| 21 (`12-interpret`) | keep ("Cluster 4 is a number") | — | — | keep 3 | **ledger 5** | 4,991 → 4,800 |
| 22 (`13-causation`) | keep | T12 the argument its own numbers contradicted | — | the wrong and the honest sentence leave the think box (L298–306) for the text; new think: which arrow of the diagram does each caveat belong to? | **ledger 6**: "what you may tell the council" | 3,785 → 3,750 |
| 23 (`14-publish-many`) | keep | T13 the prompt panel a reader drew empty (§23.3) | the council's last slide | keep 2 | **ledger 7**: Tunja after the rebuild; council's last slide | 3,577 → 3,700 |
| Part V exercises | P: "one of these three sentences claims a cause" | — | — | **D5-c**; capstone "write the council's last slide"; V.x numbering with explicit IDs | — | 2,101 → 2,200 |
| Afterword | keep | — | — | one predict box | 3,998 → 3,800 |

Chapters total 86,290 → about 85,900 (−0.5%); front matter, part pages and afterword
9,334 → about 8,470.

### 2.1 The three D5 puzzles (exactly what is planted)

- **D5-a, Part II exercises.** A cell reads `examples/london/data/attractions.csv` and prints
  the five sights' `visits_2025` as a table, after replacing the 2025 value of the sight
  ranked third in 2025 with its own `visits_2024` (a stale figure, the failure Part II is
  about). Guards: the two values differ, and the swap does not change the ranking (so the
  error cannot be seen without the data). The reader finds it with the file in their own
  `~/london-guide/data/`. Appendix E prints the row, both values and the difference.
- **D5-b, Chapter 15 (Parts III–IV).** In §15.2 a pull request "edits the model card". The
  cell prints the card's headline sentence with the *second-best* release's
  `recall_top10` under the best release's name (`ev.value(rival, "recall_top10")`, `rival`
  taken from `ev.metrics()`), beside the real metrics table. Guard: the two recalls differ
  at the printed precision. The plan calls the file `results.json`; the project's files are
  `outputs/summary.json` and `outputs/metrics.csv` (`results.qmd` 75), so say those.
- **D5-c, Part V exercises.** Three sentences about the kinds, numbers computed from
  `outputs/`; one swaps its verb of association for a causal one ("because of their
  water"). The plant is the wording; a cell picks which sentence from a fixed index and
  Appendix E names it with the honest rewrite from `13-causation.qmd` 302–305.

### 2.2 The fast path's planted error (reader B's request; a lead decision)

Preferred: no change to `starters/eval-repo/` (a tested artefact with checkpoints behind
it). The chapter's first cell prints a two-line "README claim" naming the best release with
the rival's `recall_top10`, beside the first rows of `outputs/metrics.csv`; the cold open
says one of them is wrong and §3.5 has the reader find it once the report computes the
figure. If the lead prefers a real planted sentence in the starter's README, the starter,
checkpoints 14–20, `examples/eval` and the file-for-file check all change together, and
every Chapter 3 prompt is dry-run again; I do not recommend it inside this plan.

### 2.3 The bridge at Part III (reader A stalls here)

`part-craft.qmd` gains, after its stake paragraph, a short fork set as two cards:
"Came by the fast path: carry on." "Came from zero: either copy `checkpoints/14-eval-start/`
with the catch-up line and read on (the terminal you learned in Chapters 4–5 is enough), or
go straight to Part V (@sec-water-question), which needs only Chapter 4's setup"
(`08-water-question.qmd` opener: "The London guide is not needed"). One line each defines
what the part assumes: Acme Signals (fictional), a model that ranks a call list, "recall in
the top tenth". The preface's reading-path cards put "New to the terminal" first.

## 3. The threads

**Tunja ledger (Part V).** One `::: {.cards .ledger title="Tunja so far"}` before each
Summary in Chapters 17–23, three or four cards of ≤ 25 words, every value inline code from
that chapter's existing variables. The last card is always "What may be said".

| Ch | The reader learns about Tunja | "What may be said" |
|---|---|---|
| 17 | it exists in the table: code `15001`, capital of Boyacá, two zones, its count of rows | nothing yet: no value has been checked |
| 18 | an IRCA in every year for both zones; rural high-risk to `tj_rural_high_to`; coverage reported as 0 in `tj_zero`; infant mortality changes method in 2017 | what was measured, zone by zone; nothing across 2017 |
| 19 | which of its rows survive selection; its filled coverage, flagged; one year's z-scores | the same facts, now on the scale every place shares |
| 20 | `tj_text` (`11-cluster.qmd` 47–58): the cluster or clusters of its zone-years | which kind each zone-year was grouped with, not why |
| 21 | its kind's name, and that the name fits the kind better than this member (review question 6) | a label describes a kind; for Tunja, go back to its rows |
| 22 | the mean IRCA of its two zones, "a value neither zone had" (L325–330) | an association within a kind; not what its infants drank |
| 23 | what `MAX_MISSING` 2 → 1 does to its two zones (Appendix E's computed answer) | the same sentences, rebuilt; the ledger is unchanged where the data are |

**The council (Part V).** Chapter 17 opens on the question a council member will ask (I4).
Chapter 20 says what a council can and cannot read from a cluster number. Chapter 22
answers reader A's "nobody tells me what I can tell the council": the wrong and the honest
sentence become body text under a heading of that name, and the ledger card repeats the
honest one. Chapter 23 shows the deck's last slide, "What this does and does not show"
(`examples/water/slides.qmd` 104–111), captured so its bold line is ≥ 9 CSS px on a phone
(crop to the bullets; `water_outputs.py` currently shoots `#/3`), in place of or beside
`fig-water-slides`. The exercises' capstone is "write the council's last slide".

**Acme's decision (Parts III–IV).** The deck's own title is the thread: "Which release should
the call centre use?" and its last slide, "We decide: offer [best], after a legal review of
its use of age" (`checkpoints/16-eval-slides/slides.qmd` 2, 341). Chapter 3: the report
exists. Chapter 10: the card finds that the list reaches age bands unequally (computed,
`results.qmd` 147–154); that is why the decision has a condition. Chapter 11: the deck
carries the decision and its condition. Chapter 12: one address for the investor and the
client's risk team. Chapter 13: the paper that is read without Acme in the room. Chapter
14: the update that reports it monthly. Chapter 15: the build that goes red when the
sentence stops being true. Chapter 16: what a two-person company should and should not
build this way. No chapter invents a meeting, an investor's reply or an outcome.

## 4. Stories: each to exactly one chapter

True ("From the build log"), each read at its source:

| # | Incident | Source | Chapter |
|---|---|---|---|
| T1 | The book's roadmap descriptions and agenda held typed chapter numbers that were already out of date | `REVISION-PLAN.md` 474 (WP3 row); renumbering at `book/PLAN.md` 605 | 1 |
| T2 | A notebook full of saved outputs went into a commit because a restore was skipped; `git status` showed it | `fast-path.qmd` 186–189, 296–299 | 3 |
| T3 | zsh passes an inline `#` comment in a copied command as arguments | `book/PLAN.md` 602–603 | 4 |
| T4 | `--no-prompt` stopped a first publish: "the remote origin does not have a branch named gh-pages" (Quarto 1.6.40) | `07-publish.qmd` 255–257; AGENTS.md | 9 |
| T5 | A dry run found "top 10%" typed in our own checkpoint's labels and captions | `REVISION-PLAN.md` 475; `results.qmd` 267–275 | 10 |
| T6 | Notes before the first `##` became an extra, blank slide | `slides.qmd` 145–147 | 11 |
| T7 | Headless Chrome printed the deck as one blank page | `slides.qmd` 204–210; `REVISION-PLAN.md` 546–548 | 11 |
| T8 | A navbar in the brand's navy hid a logo in the same navy | `sites.qmd` 214–216 | 12 |
| T9 | `"page 1 of 1"` printed "pbge" on page 2 | `white-papers.qmd` 201–203 | 13 |
| T10 | An agent's comment said 06:00 UTC was 07:00 in London in winter | `team.qmd` 225–226 | 15 |
| T11 | An early draft called the rural gaps "missing at random" | `book/PLAN.md` 531–532 | 18 |
| T12 | A range-restriction argument that the chapter's own numbers contradicted | `book/PLAN.md` 533–534 | 22 |
| T13 | Apple Books drew a prompt box's label and an empty panel | `book/styles/epub.css` 98–101 | 23 (§23.3, the e-book) |

Not used as story boxes, and why: `duration` leaking the target is a fact about the data
(`REVISION-PLAN.md` 560–561; `results.qmd` 88), not an incident, so it becomes Chapter 10's
second think; Word dropping `fig-alt` (`REVISION-PLAN.md` 518) is already prose at
`fast-path.qmd` 254 and `slides.qmd` 236 and stays prose; the soft hyphen in "18-29"
(`parameters.qmd` 164) and the unpinned `uv` (`team.qmd` 128) go into their chapters'
symptom / cause / fix tables. I found no recorded sub-agent failure, so Chapter 8 gets an
illustration.

Illustrations (labelled, no numbers, no real organisation acting): I1 two helpers
rendering in one folder (mechanism at `06-audiences.qmd` 157–159); I2 last month's figure
in this month's update; I3 a customer's name in an error message; I4 a council member's
question.

## 5. Not verified

- I read the three pilot chapters, the preface and every opening in full, and the rest by
  section, searching for the passages cited; I did not read every line of Chapters 2, 4–7
  and 19–21. B2 briefs need a full read of each.
- T7: the two records disagree. `REVISION-PLAN.md` 546–548 says the print *with*
  `--run-all-compositor-stages-before-draw` "was flaky (1 blank in 6)"; `slides.qmd` 204–207
  says blanks came "in most runs without the flag … and in none with it". The story below
  quotes neither rate. The lead should settle which is right before L204–207 is kept.
- T1: the record says the typed numbers were "already out of date"; that a renumbering
  caused it is my reading of `book/PLAN.md` 605, dated the day before. How they were found
  is not recorded, so the draft does not say.
- Whether Appendix D records a real Pandoc-stage error message (Chapter 1's Try it); whether
  a render inside a book cell (Chapter 11's titles) is acceptable build time; text sizes in
  the proposed captures; whether the new two-column tables meet 0.45 page. None was built
  or measured: I ran no build.
- `ebook/index.qmd` uses of the pilot chapters beyond what `_source.py` shows (titles,
  links, `cell_figure`, `gif_figure`): I found none for Chapters 1, 11 and 18.

---

# Pilot brief: Chapter 1, `book/chapters/01-quarto.qmd`

**Budget:** 3,226 → 3,100 words. **Aim:** a scene, then the book's own failure, then the
same content with fewer tools named per paragraph (reader A stopped at "Jupyter, knitr,
Pandoc, Typst, LaTeX in three bullets" and at the cache; reader B at the repeated sermon).

## Cold open (replaces L31–50; paste)

> An analyst runs a script and copies a number into a Word document. She pastes the chart
> into a slide, retypes the number in an email and exports a PDF for the website. Four
> copies now exist, and the script knows about none of them. Next month the data are
> revised. The script runs again in a moment; the copies have to be found, one by one, and
> nobody can say whether the one in the email was ever fixed. Nothing here was careless.
> Each copy was a small act of faith that the number was right and would stay right, and
> most reports are still built this way: by hand, on faith.

(101 words; no italics; "four" counts the copies named in the paragraph.)

## Story box (straight after the cold open)

```markdown
::: story
<!-- source: REVISION-PLAN.md line 474 (WP3: roadmap alt text and Appendix I's agenda "had
typed chapter numbers already out of date"); book/PLAN.md line 605 (chapters renumbered) -->
This book did it too. The descriptions of its roadmap diagrams and the agenda in an appendix
named chapters by typed numbers. Chapters were added, the numbering moved, and the typed
numbers stayed where they were, in a book about not typing numbers. No render failed and no
message said so. They are computed from the chapter list now, and cannot fall behind it.
:::
```

Then one bridge paragraph (≤ 60 words) carrying L47–50's point: the alternative is **one
source that rebuilds every output**, the Publish step of the loop; the more a program does,
the fewer places an error can slip in. Cut L39–45 (trust, decisions, built on): the preface
says it and key idea 4 keeps it. Do not italicise "Publish" here; the glossary filter links
the first italic term of the page, which should be `command-line program` at L93.

## Retire the repeated hook

L73–75 ("Suppose … ALVA … corrects one figure … has to reach N files by hand") becomes a
statement, not the question: "Kept by hand, those `{python} in_words(n_outputs)` files are
`{python} in_words(n_outputs)` copies of the same counts, and three things go wrong with
copies:". Keep the computed counts (L68–71), the three failures and `fig-drift`. Trim
L253–256 to two sentences. **Keep** the think box at L258–263: it is a retrieval question,
not a hook, and reader A's favourite line in the chapter.

## Try it (new, no installation; after the think box at L149–156)

"Three renders stopped. For each message, name the step it came from." Use three *real*
messages, copied from Appendix D, never invented: a Python exception from its Python and
Jupyter table (step 1, execute); `cannot parse length '60px'` (`d-troubleshooting.qmd` 37;
step 3, typeset); and `ERROR: YAMLException` (L36), the trick: no step ran, because Quarto
could not read the settings. Done when: "you have named a step, or none, for each, and can
say whether to look at the code or at the document." Answers in one line under the box,
≤ 60 words. If Appendix D holds a real Pandoc-stage message, use it for step 2 instead of
asking for one; do not make one up.

## Walls and density

- **L132–141 (three steps).** Cut the LaTeX parenthesis (L140–141) and "This book uses
  Python only" (the preface says so); keep one named tool per step. Move `fig-pipeline` to
  *after* the list, so the page it was pushed from fills (audit: page 6, 52% blank).
- **L222–256 (four properties, conditions).** Set the four properties as `::: cards`
  (One source; Numbers are computed; One command; Versioned), each ≤ 45 words. "Versioned"
  keeps Track Changes, repository and commit (Chapter 9 refers back to them); the lockfile
  and environment sentence (L242–244) becomes prose after the cards. The conditions
  (L246–251) become a three-item list: live data, a random seed, a cache.
- **L273–278 (freeze).** Cut to the list's third item: "a cache can serve an old result;
  @sec-publish-many shows how to use one safely." Drop "This book itself uses one" (it is in
  Appendix H). Key idea 5 (L323–324) shortens to match.
- **L168–169.** Drop the inline "(… checked 2026-11-12)"; Further reading carries it.
- **§1.5, L299–303.** The start-up bullet: two sentences, ending "(@sec-at-work-startup has
  the full case)" with whatever ID §16.6 carries. It stays here; the preface's copy goes (D1).

## Page fit (every offender in the audit)

| Unit | Now | Fix |
|---|---|---|
| `fig-drift` (L89) | 0.74 page, budget 0.65; PNG 1400 × 1980, h/w 1.41 | redraw `media/diagrams/drift.svg` to h/w ≤ 1.25 (tighter rows; text still ≥ 19 px), `make media STEPS="diagrams"`; tell the lead, who runs `media_es.py`. Caption stays (one line would be better: cut its second sentence to "By hand, copies go stale; from one source, one render updates them all.") |
| `tbl-formats` (L171–179) | 0.54, budget 0.45; pushes page 9 (54% blank) | two columns, two rows: Documents; Presentations ("used in this book" and "others"), then one sentence: "Quarto also writes Markdown dialects, wiki formats, Jupyter notebooks and more." Keep `#tbl-formats` |
| `fig-pipeline` (L130) | 0.64 (within budget), pushes page 6 (52% blank) | moved after the list, above |
| Key ideas (L314–328) | items of 30–36 words | ≤ 25 words each; item 4 loses "earns trust, justifies decisions and can be built on" only if the bridge paragraph keeps it |

## Other points

- **Payoff picture:** none new; the chapter is reading, and its two diagrams meet the floor.
- **Landing page:** no quoted sentence is in this chapter. Keep the title and every section
  ID: the preface, Chapters 2, 7 and 9 refer to §1.2–§1.5.
- **Glossary:** no new terms.
- **Do not change:** the setup cell (L3–29); the `hello.qmd` listing (L104–117; Chapter 4
  drops its copy, D8); `tbl-split` and the paragraph after it; the think boxes at L149 and
  L208; both pitfalls (L216, L265: "Reproducible does not mean correct" is reader B's best
  line); the practice box (L305–310); the lead-in to Chapter 2 (L330–333).

---

# Pilot brief: Chapter 11, `book/chapters/slides.qmd`

**Budget:** 2,603 → 2,750 words. **Aim:** a chapter about slides that shows a slide, prints
the deck's argument, and replaces its wall of traps with two stories and a small table.

## Cold open (replaces L40–51; paste)

> The report and the model card are for people who read. The decision about which release
> Acme's call centre will use is made somewhere else: in a meeting, in front of a screen,
> by people who will look at each slide for a few seconds and remember perhaps three of
> them. One of those three had better be the slide that says what is being decided, and on
> what condition. A deck for that room is a different document: not a report cut into
> pieces, but a short argument, one claim at a time, ending in the decision.

(96 words.) Second paragraph, ≤ 50 words, from L48–51: what the chapter builds (a web deck
that presents itself, a PDF to send afterwards, a PowerPoint file in the house template,
one source). Cut L46–48 ("You will rarely write a Reveal.js option…"): third time of
saying; the Part III page keeps it.

## Payoff (straight after the opener)

1. **Picture.** `::: payoff` holding `../media/figures/eval-deck-title.png`: the finished
   deck's title slide, "Which release should the call centre use?". Capture with a new
   `book/media/capture/eval_outputs.py` on the pattern of `water_outputs.py`: copy
   `checkpoints/16-eval-slides/` to a temporary folder, `uv run --frozen python
   scripts/evaluate.py`, `uv run --frozen quarto render slides.qmd --to revealjs`, open
   `slides.html` in Chrome at 1280 × 720, device scale 2. The picture is shown about 340 px
   wide (scale 0.27), so measure the subtitle's rendered size; if it is under 34 px at
   capture (9 px on a phone), crop to the title-and-subtitle band rather than shrink.
   Record the capture's text size in the author's report for `pagefit.yml`. Write only the
   `deck` step; package D3 extends the file. Caption, one sentence: "The finished deck's
   title slide, rendered from `checkpoints/16-eval-slides/slides.qmd`." Alt text: the title,
   the subtitle, the colours; no results.
2. **The eight titles, printed.** Under the picture: "Read only its titles, and you have its
   argument:" and a numbered list a cell prints. The titles hold inline code
   (`slides.qmd` of the checkpoint, L85–341), so the source alone cannot give them. Add
   `ev.deck_titles(checkpoint)` to `book/scripts/evaluation.py` (not on the lead-only list;
   confirm with the lead): it renders a temporary copy as above, cached like `ev.run()`,
   and returns the YAML title and the seven `<h2>` texts. Guards: `len(titles) == n_slides`;
   the headline equals the sentence already computed at L91–92. Fallback if the lead rules
   out a render in a cell: print titles 1, 2 and 8 only, which need just `best`, `recall`
   and `share`. With the list printed, L88–93 shrinks to two sentences.

## Story boxes

In §11.3, in place of the pitfall's second sentence pair (L145–147):

```markdown
::: story
<!-- source: book/chapters/slides.qmd lines 145–147 at 651db10 ("Notes written before the
first ## heading became an extra, blank slide"); dry run noted at lines 35–37 -->
While this deck was being built, the notes for its title slide were written before the first
`##` heading, the natural place for them. They became a slide of their own: an extra, blank
one. That is why the prompt asks for notes "on each of the seven", and why the finished deck
attaches the title's notes with a short filter. Count the slides in what comes back: there
should be `{python} WORD[n_slides]`.
:::
```

In §11.5, before the paragraph at L204:

```markdown
::: story
<!-- source: book/chapters/slides.qmd lines 204–210 at 651db10; REVISION-PLAN.md lines
546–548. The two give different rates: quote neither (PLAN-improvement-briefs.md §5). -->
Printed from the command line, Chrome sometimes printed the deck before it had laid itself
out, and wrote a PDF of a single blank page. Nothing failed: there was a file, with the
right name, and nothing in it. A person would have seen that only by opening it, perhaps
after sending it. The script's check, one page per slide, caught every blank print.
:::
```

L204–210 then shrinks to: what the flag does, and that the check also catches a slide too
tall for its page. Keep or correct "in none with it" as the lead rules (§5).

## The traps wall (L141–154) becomes three units

1. Story T6 above.
2. A two-column table, "Why the prompt says", ≤ 350 characters: `a plain YAML title` |
   inline code in `title` runs before any cell (`NameError`); with no title, the first
   heading is promoted, uncomputed. `no fig- labels` | a `fig-` label adds "Figure 1:" to
   the caption. `notes on each of the seven` | see the story.
3. A short pitfall, ≤ 60 words: look at every slide at the deck's size (one run's figures
   overflowed with `fig-dpi`; another's filled half the slide). The `np.int64(6)` title
   moves into the think answer below.

## Pause and think (before "Read the titles first", L136), with a planted title

Question (≤ 60 words): "The agent says the deck rendered and lists its titles. Here are two
of them as it might have listed them:" then two titles printed by a cell: the real
comparison title, and the headline with the second-best release's `recall_top10` under the
best release's name (guard: the two recalls differ as printed). "Which habits can this list
alone prove, and is either title wrong?"

Answer (≤ 80 words): "From the list: that titles state claims, and that the deck ends on a
decision. Notes need the slides; computed numbers and guards need the source. The headline
is wrong: that figure is `{python} rival`'s. No guard would stop it if the number were
typed, which is why a title's numbers are inline code. A title can also be computed and
still read badly: one run printed `np.int64(6)`. Read every rendered title."

## Page fit (every offender in the audit)

| Unit | Now | Fix |
|---|---|---|
| `tbl-slides-vocab` (L101–114) | 1.31 pages, split over 3 (1.75 at 19 px) | two tables of two columns (Ask for; Quarto calls it), about 240 characters each. **On the screen** (`#tbl-slides-vocab`): speaker notes, fragments, two columns, smaller text, speaker view. **Look and export** (new `#tbl-slides-export`): theme, footer and slide numbers, a stable link, PDF by print view, a house PowerPoint template. The third column's PowerPoint differences join "Know what PowerPoint loses" (L235–238), which already lists most. "(Quarto 1.10.20)" stays in the first caption |
| Pitfall (L141–154) | 0.75 page; splits at 19 px | the three units above |
| `tbl-slides-habits` (L78–86) | 0.69, budget 0.45 | two columns, Habit; You check. "What it means" is one clause after the habit's name or goes to the sentence before the table. Keep the ID and the computed title in row 2 |
| Prompt (L124) | 0.64, budget 0.6; pushes page 7 (40% blank) | trim about 45 characters without changing an instruction: "one claim per slide, each slide's title stating its claim" → "one claim each, every title stating its claim". §3.4 lists Chapter 11's boxes, so this is allowed, and the prompt is then dry-run again from checkpoint 15 (§9: Sonnet, then Haiku), with the comment at L35–37 updated. If the lead would rather not touch a tested prompt for 0.04 page, list it in `pagefit.yml` instead |
| Page 4, 62% blank | pushed by the vocabulary table | fixed by the split |

## Other points

- **Duplicate:** `tbl-slides-contrast` (L176–182) stays here; tell the Chapter 12 author
  (D3) that Table 12.2 goes and `sites.qmd` refers to this one.
- **L229–231,** the seven layout names: a one-line list in the text is fine; both readers
  stopped there, so cut the sentence around it to the instruction ("your template works if
  its layouts carry these names").
- **Stamps:** none in the prose; Further reading keeps its dates.
- **Landing page:** nothing quoted. Keep the title and section IDs.
- **Glossary:** propose `speaker view` to the lead (defined at L138–139; `speaker notes`,
  `fragment`, `print view`, `reference document`, `theme`, `contrast ratio` exist).
- **Spanish:** a new table ID and new boxes; the lead adds the file to `pending.yml`.
- **Do not change:** the setup cell's guards (L20, L31, L34); the theme, PDF and PowerPoint
  prompts (L166, L200, L221); the contrast cell; the WCAG paragraph (L158–162); the
  catch-up, Try it and done text (L240–254); "remember perhaps three of them"; "Read the
  titles first" (L136), reader A's best line here.

---

# Pilot brief: Chapter 18, `book/chapters/09-explore.qmd`

**Budget:** 2,674 → 2,750 words. **Aim:** open on the puzzle the chapter already owns, let
the page turn at `fig-tunja` be the reveal, and end on the ledger. Reader A: "reads like
detective work" once past a slogan opening; make the opening the first clue.

## Cold open (replaces L62–71; paste)

> In 2016, Tunja, the capital of Colombia's Boyacá department, recorded
> `{python} f"{tj_im[2016]:.1f}"` infant deaths for every 1,000 live births. In 2017 the
> figure was `{python} f"{tj_im[2017]:.1f}"`. Nothing in the table marks the year: the
> column keeps its name and its units, and no row is missing. Drawn as a line, it is the
> kind of fall a council would applaud and an analyst would be glad to report. Was it
> progress? Decide now; the answer comes later in this chapter, and it is not in the data.

(About 85 words as rendered; both numbers come from `tj_im`, L57; the guard at L58 already
requires the fall. Match the decimal places the explorer shows.) Second paragraph, ≤ 70
words, from L62–67: before any model, look, because a sparse column, a zone nobody measured
and a series that changes method raise no error; a clustering will group rows made
comparable only by filling their gaps. Chapter 17 now names Tunja (ledger 1), so L69–71
goes.

## Payoff (straight after the opener)

`::: payoff` with `../media/figures/water-explore.png`: the page the reader builds. Add an
`explore` step to `book/media/capture/water_outputs.py` (tell the lead; D4 also edits this
file): copy `checkpoints/05-water-explore/` and `examples/water/data/` to a temporary
folder, `uv run quarto render explore.qmd`, open `explore.html` at a 390 px viewport,
device scale 2, and crop to the title and the missing-values-by-zone table. Body text is
then about 14 px on a phone. Caption: "The first page of the water project, `explore.html`,
at a phone's width. Rendered from `checkpoints/05-water-explore/explore.qmd`." Alt text
without numbers (say `irca` is far sparser in rural rows), or guard it with
`alt_text_holds`.

## Story box (after L140–144, where the term is defined)

```markdown
::: story
<!-- source: book/PLAN.md lines 531–532 (§12, item 2: 'Chapter 9's "missing at random"
(the gaps depend on zone, and perhaps on risk: missing not at random)'; this file was
Chapter 9 then) -->
An early draft of this chapter called the rural gaps "missing at random". A review caught
it. The gaps depend on zone, and perhaps on the risk itself, which is the opposite claim.
The phrase sounded right and rendered without complaint, and it would have licensed filling
the gaps with typical values. A technical term is a claim about the data: check it against
the rows, as you would a number.
:::
```

## Pause and think: the reveal (rewrites L257–263)

Question: "The chapter opened on Tunja's infant mortality, which falls in 2017. You have
now seen the whole series (@fig-tunja). What else changes that year, and is the fall
progress?"

Answer (≤ 80 words): "Not on this evidence. Before 2017 the line is smooth; from 2017 it
jumps from year to year. The series changes method there, from what look like modelled
estimates to observed rates (the data's README, caveat 8), so the fall may be the change
itself, and the table cannot tell. Compare such a series only within one method, as the
analysis does: `{python} infant_years`."

"Smooth" and "jumps" now appear in prose both editions show, so move `im_smooth` and
`im_jumpy` (L221–222) into the setup cell and add `text_holds(im_smooth and im_jumpy, …)`.
Keep the think box at L146–154 as it is.

## Ledger 2 (new, before the Summary; after L331)

```markdown
::: {.cards .ledger title="Tunja so far"}
Rows
: `{python} len(tjr)`: two zones, `{python} WORD[n_years]` years, an IRCA in every one.

Water
: rural in the high-risk band until `{python} tj_rural_high_to`; urban never above
  `{python} f"{tj_urban_max:.1f}"`.

Not as given
: coverage reported as 0 in `{python} spans(tj_zero)`; infant mortality across 2017.

What may be said
: what was measured, zone by zone and year by year. Nothing yet about kinds, or causes.
:::
```

"an IRCA in every one" depends on `tj_full` (L36): add it to a `text_holds`.

## Walls, cuts and moves

- L265–270 repeats three rows of the table below it: cut the paragraph to one sentence
  ("Five things are worth finding (@tbl-tunja-caveats); hollow points mark a coverage
  reported as 0, which beside its neighbours probably means not reported"), about −70 words.
- L186–196: three reasons in one paragraph; set them as a three-item list (no cut).
- L180–184 (the median against INCA's 36.5): keep; the figure is cited (`@tbl-irca-bands`).
- The slogan "Before any model, look at the data" survives only inside paragraph 2.
- Lead-in (L346–347) is right; no D8 fix here.

## Page fit (every offender in the audit)

| Unit | Now | Fix |
|---|---|---|
| `fig-tunja`, EPUB cell (L216–249) | 0.87 page, budget 0.65; 894 × 1414 (h/w 1.58), capped by max-height; caption 372 characters | `rows, cols = grid(3, square=True)`; `a1, a2, a3, *spare = axes.flat` and `for a in spare: a.axis("off")` (in HTML there is no spare). In the EPUB the legend and the two notes ("hollow: reported as 0", "new method from 2017") go in the fourth cell; panel titles shorten ("IRCA", "Aqueduct coverage (%)", "Infant mortality"); x ticks 2010, 2016, 2022. Caption, one sentence: "Tunja, 2010–2023: IRCA by zone, the municipality's aqueduct coverage and its infant mortality (deaths under one year per 1,000 live births), from `water_municipal.csv`." The hollow points, the break at 2017 and 2020's other source move to the text and the think answer. Alt text: "Three small charts in a two-by-two grid, with the legend in the fourth cell. Top left: … Top right: … Bottom left: …", the three descriptions unchanged, so the `alt_text_holds` conditions (L223–224) stay as they are |
| `tbl-tunja-caveats` (L272–280) | 0.55, budget 0.45 | two columns, "In Tunja's rows" and "The analysis", the caveat's name folded into the first ("coverage: the municipal total only"); cross-references stay. If `make book-pages` still fails it, set it as `::: cards`, five cards, and keep the ID on the div |
| Try it (L315–328) | 0.46, budget 0.45 | shorten the done text to "`explore.html` shows rows and columns, missing values by zone, and IRCA by band, zone and year." The catch-up stays inside the Try it (`ebook_media.py` 270 selects `.tryit:has(.catchup)`, though on another chapter) |

No blank-page or wall entry names this chapter.

## Other points

- **Landing page:** nothing quoted. Keep `#sec-tunja` and `#fig-tunja`: the live-link card
  (L251–254) and `check_live_links.py` use them.
- **Glossary:** no new terms (`median`, `missing not at random` exist).
- **Spanish:** the EPUB cell's caption and alt text have Spanish twins; the lead adds the
  file to `pending.yml`.
- **Do not change:** `fig-wat-bands` and `fig-wat-years` with their guards; the paragraph
  at L140–144 ("the zones whose scores are worse are also the ones least often scored" is
  reader A's best line); the HTML explorer block (L204–213; `check_scenes.py`); the prompt
  at L292 (`check_prompt_values.py`, tested); the pitfall at L307–313; the practice box at
  L282–286; "divipola as text" (L304–305).
