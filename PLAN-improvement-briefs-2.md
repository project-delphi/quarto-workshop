# PLAN-improvement-briefs-2: the remaining briefs (package B2)

Written 2026-11-24 by the developmental editor, on `improve/c-pilot`. It follows
`PLAN-improvement-briefs.md` (B1): read that file's §0 (the lead's decisions), §1 (the six
rules of the spine), §2 (the spine table and the planted errors), §3 (the threads) and §4
(which story goes where) first. This file has one section per package: D1, D2, D3, D4, E.
Chapters 1, 11 and 18 are the pilots and are not briefed here. Each author reads their own
package and the notes below. The voice guide (one page, from the accepted pilot) is not in
this file: it waits for the pilot chapters.

Line numbers are those of the `.qmd` files on `improve/c-pilot` (the same as `651db10` for
every file briefed here). Word counts are `wc -w` on the `.qmd`. Page-fit figures are from
`book/_book/pages/en.md` as it stands (figure budget 0.7 page, images capped at 55vh); sizes
"after" are estimates until `make book-pages` is run.

## Lead decisions (2026-11-24)

They override the notes and briefs below where they differ.

1. **The rival** (note 1) is defined once, by the lead, in `book/scripts/evaluation.py`
   (`ev.rival()`: the release with the next-highest `roc_auc`), at the sync point before
   D1–D4. Chapter cells and Appendix E's answer cells call it; no chapter defines its own.
2. **Captures** (note 3): one media package, M, runs at that sync point and owns every new
   capture step: `eval_outputs.py` (`report`, `card`, `site`, `paper`, `update`, `checks`,
   beside the pilot's `deck`), `water_outputs.py` (the council's last slide), the phone-width
   recaptures in `london_outputs.py`, `toy_examples.py` (the toy pair split at the `---`
   rule) and `hello_outputs.py`. It records each picture's text size in `pagefit.yml`. The
   D authors use the pictures; if a crop is wrong, they say so in their report.
3. **The copyright sentence** (note 4) is the lead's, in D1's branch, with its Spanish twin and
   both landing-page guards; section E's draft is the starting point.
4. **`pagefit.yml` exceptions for tested prompts** (Chapter 4's setup check, Chapter 23's
   three prompts, Appendix G's credits table) are accepted only for "over budget": if one of
   them splits at a gating profile, it is trimmed and dry-run like any other.
5. **New facts** (Chapter 16's short vendor grid): the lead adds them to `facts.yml` with
   `_es` twins after opening each source; a cell with no source is left out of the grid
   ("not stated") rather than filled.
6. **Structure** (Chapters 6, 14, 15, 16, 20–21, 23; exercises V.x; the appendices as cards):
   accepted as briefed. Appendix H's new "What was not tested" section belongs to package E.
7. **A wrong error message, found by the Chapter 1 pilot and checked by the lead.** The book says
   `{height=60px}` makes Typst fail with "cannot parse length '60px'". Quarto 1.10.20, the only
   version the book and its checks target, renders it without error (run 2026-11-24). D2 drops
   the claim from Chapter 6's pitfall (`04-markdown.qmd` 681–683); E replaces Appendix D's row
   (L40) with the Typst message Chapter 1's Try it uses, "error: file not found", for a missing
   image. The workshop's `TROUBLESHOOTING.md` entry is removed. Older Quarto versions are not
   tested or described.

## Notes that cross packages

1. **One definition of the rival.** Three plants use "the right name with another release's
   number": Chapter 3 (ROC AUC, because recall is not introduced there), Chapter 11 and
   Chapter 15 (`recall_top10`). `rival` is the release with the next-highest `roc_auc` in
   `ev.metrics()`. One helper should define it, called by the chapter cells and by Appendix
   E's answer cells; the lead decides where it lives.
2. **D5-a reads `visits.csv`.** B1 §2.1 named `attractions.csv` and a `visits_2024` column;
   that file has no 2024 column. The plant swaps the third-ranked sight's 2025 value for
   its 2024 value from `examples/london/data/visits.csv`.
3. **Captures.** `media/capture/eval_outputs.py` is D3's after the pilot. D1 needs its
   `report` step for Chapter 3's payoff, so that step is written at the sync point before
   D1 starts, or D1's picture waits for D3. `london_outputs.py` and `toy_examples.py` are
   D2's, `water_outputs.py` D4's; D1 adds a separate `hello_outputs.py`.
4. **Stamps and the copyright page.** Moving the "(checked …)" stamps of Chapters 2 and 4
   to Appendix K, and those of other chapters to Further reading, makes
   `book/copyright.qmd` 12–13 ("were checked on the dates given in the text") untrue. The
   lead rewords it, its Spanish twin and both landing-page guards in the same branch as D1;
   section E drafts the sentence.
5. **Cards and cross-references.** A table that becomes `::: cards` loses its `@tbl-…`
   target. Each brief names the references to change; all new IDs, splits and cards go in
   `translation/pending.yml`.
6. **Changed prompts** are listed in each brief with the new text. Authors do not run them;
   the lead dry-runs each (Sonnet, then Haiku) and records the run.
7. **Stories were checked against their sources after drafting.** Where a draft said more
   than the record (the navy logo, "pbge", the time zone, "top 10%"), it was cut back to
   what the cited lines say. Authors must not add colour to a story from the build log.
8. **Length.** This file runs well over the 14,000 words asked for, because prompts, story
   boxes and cold opens are drafted in full. Each author reads only their own section.

---

# D1: front matter and Part I (`improve/d1-front-part1`)

Files: `index.qmd`, `part-1.qmd`, `chapters/02-assistant.qmd`, `fast-path.qmd`, `03-setup.qmd`,
`first-report.qmd`. All six were read line by line.

**Shared decisions the D1 author needs before starting**

- **Stamps.** Every "(checked …)" in the prose of Chapters 2 and 4 goes. A fact that comes
  from `facts.yml` keeps its `fact()` call and loses its `checked()` call; each section that
  quotes one ends with a single line: "Checked `{python} …`; @sec-facts has each source." The
  author hands the lead a list (fact key, URL, date) of every stamp that has no `facts.yml`
  entry yet (listed per chapter below). **For the lead:** `copyright.qmd` 12–13 ("were
  checked on the dates given in the text") becomes false; it, its Spanish twin and the two
  landing-page guards change in the same branch (package E's brief drafts the sentence).
- **Captures.** `eval_outputs.py` belongs to the Chapter 11 pilot and then D3. D1 needs one
  picture from it (the Acme report). Ask the lead to have the `report` step added at the
  sync point before D1 starts; D1 does not edit that script.
- **Cards lose table numbers.** Where a table becomes cards, replace `@tbl-…` references
  with a link to the section.

## Preface, `index.qmd`

**Budget:** 3,788 → 3,350. **Aim:** the reader's own path on the second screen, not after
1,000 words; one navigation system, not two; no essay before the reader knows what an agent
is.

**Cold open:** keep L21–26 (the question). Cut L27–43 (paragraphs 2 and 3) except one
sentence, moved to the end of "Prompt, Check, Publish": Git records every version and a host
such as GitHub Pages puts the result on the web; the agent types for all three.

**New order:** hook; Prompt, Check, Publish with Figure 1 (unchanged text: three guarded
sentences live here); Find your path (cards); Who this book is for; The three running
examples; How the book is organised; What a hands-on step looks like; When you get stuck;
Free and open source; Two editions; Versions and dates.

**Find your path (L132–154, L215–225, L267–290 merged).**
- `tbl-reading-paths` (1.52 pages, split over 3; 2.12 at 19 px) becomes
  `::: {.cards #reading-paths}`, one card per role: the role as the term, then "Read: …" and
  "You finish with: …". Order: New to the terminal; A student; An educator; An analyst who
  produces recurring reports; A researcher or graduate student; A data scientist or ML
  engineer; A software engineer; A technical founder. The analyst's card begins "If a
  terminal and Git are routine: … If not: @sec-setup and @sec-first-report first", so that
  reader A is not sent to a chapter she cannot do, and it names the afterword's metrics
  brief first.
- "Your first afternoon" becomes two sentences under the cards. Keep verbatim: "takes you
  from there to a report in three formats in under an hour".
- "Three ways through" goes. Its core-path list (L272–285) stays as a short list under the
  cards, headed "The core path"; "By role" is now the cards; "Workshop-paced" is one
  sentence pointing to @sec-workshop.
- Update L134 and L269 (`@tbl-reading-paths`) to "the cards below".

**Who this book is for (L61–103).** Keep L63–73 (the `audiences()` pattern "I wrote this
book for … : anyone" and the four example readers; reader B's best line is "the founder who
sends investors a figure from the wrong month"). Cut L75–83 (reproducibility; publishing is
half the job) to two sentences. Cut the start-up paragraph (L85–91) to one sentence ending
"(@sec-wrong-tool; the full case is @sec-at-work)": its home is §16.6. Keep L93–103 as they
are ("No programming is assumed"; the needs list).

**How the book is organised (L180–213).** The one enormous paragraph (L182–200) becomes a
five-item list, one line per part. Keep the phrases "the route from zero sets up your
computer", "fast path (@sec-fast-path)" and "adds Quarto to an existing repository". Move
the Claude Code cost sentence to Chapter 4 (its home). Add to Part V's line: "following one
municipality, Tunja, from raw rows to a council's last slide". Keep "By the end of the book"
(L202–213).

**Free and open source (L105–130).** Three paragraphs to one of about 110 words: what is
open (one list), why it matters for rebuilding, and that the agent is the one proprietary,
swappable part. The per-product licences (L122–127) go to Appendix K. Facts for the lead:
`licences.quarto` (https://quarto.org/license.html), `licences.pandoc`
(https://pandoc.org/), `licences.typst` (https://github.com/typst/typst), `licences.codex`
(https://github.com/openai/codex), `licences.claude_code` (its licence page), each dated.

**When you get stuck (L292–321).** About 330 → 200 words: keep the four diagnosis questions
and Figure 2; cut L318–321 to one sentence (the README names a workshop slide; in the book,
carry on from the box).

**What a hands-on step looks like (L227–265).** Keep the five sample asides and the sentence
"the exact prompt to give your agent, what it will probably run, and the few things only you
can do". Add one sentence naming the three new components (a story from the build log, an
illustration, "what you will build"), without samples.

**Page fit.** The cards fix the table and its splits. Walls at pages 4–7 and 11–13 go with
the cuts to "Who this book is for" and with the merge. No other unit of the preface fails.

**Landing page: keep verbatim, or tell the lead to re-quote** (`ebook/_source.py` 80–103):
"one small piece of work with its files and columns named"; "fast path (@sec-fast-path)";
"adds Quarto to an existing repository"; "takes you from there to a report in three formats
in under an hour"; "the route from zero sets up your computer"; "read what changed, look at
the result, compare it with the data"; "An agent can be fluent, fast and wrong, so this step
is never skipped, and it is always yours"; "every output from the checked source the same
way every time"; "No programming is assumed"; the needs list (L100–102); "the exact prompt
to give your agent …"; "a web page, a Word brief for partners, a printed flyer, a dashboard
for managers and a published website"; "publish the analysis as a report, slides, a blog
post and a website, all from one analysis script". `make ebook-media STEPS=head` after any
change to the title or description (the lead's).

**Do not change:** the setup cell; Figure 1 and Figure 2; the three running examples'
computed figures; "Versions and dates" (it already says facts are kept in Appendix K).

## Part I, `part-1.qmd`

**Budget:** 360 → 150. Replace L3–30 with (paste):

> Part I has two routes, and you need only one. Both begin with two chapters of reading:
> @sec-quarto, on why one source that rebuilds every output can be trusted, and
> @sec-assistant, on how to ask an agent for work and check what comes back.

Then two cards. **A terminal and Git are routine:** @sec-fast-path adds Quarto to an
existing repository and ends, in under an hour, with a report in three formats reviewed as a
pull request. **Starting from zero:** @sec-setup takes your computer to a web page and a PDF
that both say 42; @sec-first-report puts a real report in your hands, with one wrong number
to find, before any agent edits it. Allow about two hours. Keep the roadmap cell. No offender.

## Chapter 2, `02-assistant.qmd`

**Budget:** 5,736 → 5,300; aim for its lower edge (reader A: "cut by a third"; reader B:
§2.1–2.4 is beginner material). **Aim:** the pelicans as a guess and a reveal; the
chapter's audit trail out of the reader's way.

**Cold open (replaces L39–46; paste):**

> Since 2024 the developer Simon Willison has put one request to most new AI models:
> "Generate an SVG of a pelican riding a bicycle." An SVG is a drawing written as text, so a
> model writes one the way it writes code. Below are `{python} len(pelican_cost)` answers,
> from four models. Every one is recognisably a pelican on a bicycle, and they did not cost
> the same. Before you look at the prices, guess: how many times dearer was the dearest
> than the cheapest that was good enough?

(About 80 words; no "effort", no cents, which reader A met before she knew what an agent
was.) **Move the grid** (both edition blocks, L193–209, with `#fig-pelicans`) to straight
after this paragraph. Then the reveal, from L44–46: the dearest cost … cents, about … times
the cheapest good enough, at … cents. Then L48–53 unchanged. §2.2's subsection (L187–225)
keeps its discussion and refers back to the figure; L176–177 (the Fable price) becomes a
clause there.

**Signpost** (new, after the opener): "If you already use an agent every day, read
@sec-three-skills to @sec-boxes and skim the rest."

**Pause and think:** four exist; keep all. The hook's guess is the chapter's predict moment.

**Walls and density**
- L124–134, "What 'covers' means": cut to two sentences (every prompt is written to work in
  all four; the install command, account and rules file of each were checked against its
  documentation). The detail goes to Appendix H.
- **OpenCode warning** (L129–132, L282–285, and Chapter 4 L263–268): home is Chapter 4.
  Here, cut L129–132; L282–285 becomes one sentence, "OpenCode asks neither question by
  default; @sec-step-assistant shows how to make it ask." Keep the six words in
  `fig-agent-loop`'s caption, which would otherwise be untrue.
- **Free models** (L152–158): home is Chapter 4's low-cost route. Here, one sentence with a
  pointer. Reader B: an untested claim told twice.
- L160–164 and the practice box (L166–174): keep; drop the box's "(checked …)".
- L179–185 (a16z, Epoch): one sentence, "the price of a fixed level of capability has been
  falling fast, though perhaps not at the frontier", with the sources in Further reading.
- L218–225: keep "Keep the evidence in proportion"; move the 128,000-token aside to a
  clause.
- L252–254 (OpenCode's command names): to Appendix C, by the lead.
- L309–315 (how each agent finds `AGENTS.md`): one sentence, "All four agents read it;
  Claude Code through a one-line `CLAUDE.md` that imports it (@sec-facts)." Fact for the
  lead: `agents.rules_lookup`, sources https://code.claude.com/docs/en/memory,
  https://learn.chatgpt.com/docs/agent-configuration/agents-md,
  https://antigravity.google/docs/rules, https://opencode.ai/docs/rules/.
- L383–384 ("you will rarely write a theme's stylesheet … by hand"): cut to "With an agent
  doing the typing, you need three skills"; the Part III page is the sentence's home.
- **Lead-in (L536–537), D8:** "If a terminal and Git are routine, @sec-fast-path is next. If
  not, @sec-setup gets your computer ready in six checked steps."

**Stamps to move** (line: what): 69, 130–131, 146–147, 154–155, 167 (all `checked()` calls:
delete); 122 (caption: Gemini CLI replaced; new fact `agents.gemini_cli_replaced`,
https://geminicli.com/docs/get-started/installation); 182–183; 203 and 208 (captions); 222;
250 (caption); 253–254; 272; 309 and 314; 488 (ICMJE: keep the date in Further reading).

**Page fit**

| Unit | Now | Fix |
|---|---|---|
| `tbl-slash` (L244–250) | 0.67; split at 19 px; pushes page 13 (47% blank) | two columns, Command; Use it when, with what the command does folded into the second ("`/clear`: a new conversation with empty context, when one task ends and an unrelated one starts"). The Claude Code and Codex differences shrink to "wording differs by agent: type `/` to list yours". Caption: one sentence |
| `tbl-assistants` (L115–122) | 0.48; caption 299 characters | three columns: Agent (with its maker), You type, Default models. Caption: "The agents this book covers." |
| `fig-agent-loop` (L94) | 0.70 (at budget); pushes page 4 (72% blank) | caption to its first sentence; place the figure after the paragraph at L96–101, so the page before it fills |
| Try it (L66–76) | 0.43; page 2, 43% blank | within budget; the moved grid changes this page, re-measure |
| `fig-agent-session` (L481) | pushes page 26 (36% blank) | move above the paragraph at L477–479 |

**Landing page.** `S.chapter("02-assistant")` reads the title; `assistant_cost()` and
`book_fact()` read `facts.yml` keys, which stay. `gif_figure()` may read the captions of
`chat-prompt.gif` and `agent-session.gif`: leave both captions and alt texts as they are.
**Glossary:** none new. **Prompts changed:** none.
**Do not change:** the setup cell and its `QUOTED_CENTS` guard; "the model decides, the
harness does, you direct and check"; `tbl-step-or-task` and "Size the work by how it will be
checked" (reader B's best); §2.9's three boxes; §2.10's three ICMJE points; section IDs.

## Chapter 3, `fast-path.qmd`

**Budget:** 3,125 → 3,250. **Aim:** give the fast path its own "find the wrong number", show
the report, and stop leaning on chapters this reader skipped.

**Cold open (replaces L25–33; paste), then a cell:**

> Somewhere in a repository you work on, a sentence states a result: in a README, on a
> slide, in a message to a client. Below is such a sentence about this chapter's repository,
> and under it what the repository's own script computed. They disagree. Nobody lied; a
> sentence like this is typed once, after one run, and the results move on. By the end of
> this chapter the repository has a report in HTML, Word and PDF that cannot do that: every
> number in it is read from the results, and a guard stops the build when a sentence stops
> being true.

(94 words.) **The plant (lead decision 4).** A cell prints, as a block quote, "`best` ranks
best, with a ROC AUC of …" using the *rival's* `roc_auc`, and under it each release's
`roc_auc` from `ev.metrics()`, as `grep roc_auc outputs/metrics.csv` would show them. `rival`
is the release with the next-highest `roc_auc`. Guards: the two values differ at three
decimals; the sentence is labelled in the text as written for this exercise, not found in
the starter. This chapter plants ROC AUC, not `recall_top10` (which Chapters 11 and 15 use),
because recall is not introduced here; one shared helper should define `rival` for all three
(package E). **The reveal** is a new think box in §3.5 after L249–251.

- Question: "Go back to the sentence that opened the chapter, and put it beside the
  report's. Which number was wrong, and whose is it?"
- Answer (computed): "The ROC AUC. `{python} …` is `{python} rival`'s; `{python} best`'s is
  `{python} …`. The name was right and the number was a copy from another row. The report
  cannot make that slip: its number is inline code, and its name is guarded."

The route note (L30–33) moves into §3.1, which already says it; fix the doubled reference
there ("Chapters 4 and 5 (@sec-setup and @sec-first-report)" → "the other route,
@sec-setup and @sec-first-report"). Keep L35–39, adding to its first sentence that the two
founders must decide which release a call centre will use.

**Payoff.** `::: payoff` after the opener: `media/figures/eval-report.png`, the finished
report's title, guarded sentence and the top of its metrics table, from `report.html` of
`checkpoints/14-eval-start/` at a 390 px viewport, device scale 2, cropped (body text about
14 px on a phone). Made by the `report` step the lead arranges. Caption: "The report this
chapter builds, at a phone's width. Rendered from `checkpoints/14-eval-start/report.qmd`."

**Story box** (in §3.6, replacing the last sentence of L296–299):

```markdown
::: story
<!-- source: book/chapters/fast-path.qmd lines 186–189 and 296–299 at 651db10; dry run of
2026-11-18 noted at lines 20–22 -->
In the test run of this chapter, the step that restores the notebook was skipped. Rendering
with `--execute` had written several hundred lines of outputs into `notebooks/explore.ipynb`,
and `git add -A` took them: a notebook full of outputs went into the commit that was meant to
add a report. Nothing failed. `git status`, read before the commit, was the one place it
showed.
:::
```

The think answer at L186–189 then drops "in the test run, several hundred changed lines".

**Walls and density**
- §3.8 (L357–371) is "the section I bought the book for" and too thin. Add about 120 words,
  from what the chapter already establishes and no more: begin with results trapped in
  notebooks (the first job is the script that writes them to files); say that the three
  packages join whatever manages the environment; end with a pointer to the afterword's
  projects by ID. Do not add untested instructions for conda, Poetry or monorepos.
- L254–257 (Word and alt text): keep as the pitfall, two sentences.
- Stamps: only in Further reading already.

**Page fit**

| Unit | Now | Fix |
|---|---|---|
| `tbl-fast-vocab` (L228–237) | 0.68 | two columns, The prompt says; You check. Quarto's name for each feature moves into the first cell in brackets ("hide code (`echo: false`)"); the cross-references move to one sentence after the table |
| `tbl-fast-starter` (L102–112) | 0.65; pushes page 4 (46% blank) | shorten each "Holds" cell to one clause, about 330 characters in all; `pyproject.toml`, `uv.lock` become a sentence after the table |
| `tbl-fast-review` (L328–334) | 0.50 | caption "Three checks for a pull request."; shorten the "Here" cells; before the table, name the checks in one sentence (scope, correctness, rebuild), so that the table no longer leans on Table 5.2 |
| Prompt in §3.3 (L139) | 0.53; page 6, 37% blank | within budget; leave |

**Prompts changed:** none. **Landing page:** the preface quotes "fast path
(@sec-fast-path)"; keep the ID. **Glossary:** none new (`ROC AUC`, `guard` exist).
**Do not change:** the four prompts; the setup cell's guards; the `ClaimError` block; "A
guard you have never seen fail is a guard you have not tested"; the command blocks; the
catch-up; `tbl-fast-tools`.

## Chapter 4, `03-setup.qmd`

**Budget:** 4,654 → 4,300. **Aim:** the six steps on the first screen after the opener; the
free route said plainly; one home for the cost and OpenCode material.

**Cold open:** keep L11–16; keep L18–21.

**Payoff.** `::: payoff` after the opener: `media/figures/hello-42.png`, two stacked crops:
`hello.html` at a 390 px viewport and the top of `hello.pdf`, each showing "The answer is
42." A new `book/media/capture/hello_outputs.py` (pattern of `toy_examples.py`, which D2
edits, so do not touch it) renders the chapter's `hello.qmd` in a temporary folder. Caption:
"What Step 6 ends with: a web page and a PDF, built on your computer." The 42 is the file's
own output; no cell needs to compute it.

**Before you start (L45–107): the wall.**
1. Move the six-step table (L96–107) to the top of the section.
2. Set the rest as `::: cards`, each ≤ 70 words:
   - **A good connection** (L45–53; keep the glosses of VPN and proxy).
   - **Two accounts** (L55–63): a free GitHub account and one agent's; the list of plans
     goes ("@sec-facts lists what each agent accepts"); sign-up can take hours.
   - **It can cost nothing** (L65–75), leading with the free route: the two `fact()` calls
     first, then "none was tested on this book's prompts, so check each result as the book
     teaches", then the capped pay-per-use route, where the gloss of API key now lives.
   - **No install rights?** (L77–79).
3. "A plan for when a step fails" (L81–94) stays a numbered list, about 150 → 110 words.

**Story box** (Step 1, after L130):

```markdown
::: story
<!-- source: book/PLAN.md lines 602–603 (§15, item 4: "no alternatives as inline # comments
in copyable commands (zsh passes them as arguments)") -->
An early draft of this book put a note after a `#` on the same line as a command to copy. In
a script, that is a comment. Pasted into zsh, the Mac's default shell, it was not: the shell
handed the `#` and the words after it to the command as arguments. So every command here
stands alone on its line, and a choice between systems is made in the sentence above it.
:::
```

**Duplicates**
- The `hello.qmd` listing (L504–533) repeats §1.2 (D8). Replace with: "Its file is the one
  @sec-what-quarto showed. The test run is a check that the tools work together, not a
  lesson: you need not understand the file to pass it." About −130 words.
- OpenCode: L263–268 is the warning's one home; keep. L355–356 stays as one clause.
- The preface's Claude Code cost sentence lands in the "Two accounts" card.

**Density**
- L270–273 and L278: one clause of provenance for the three screens ("as captured from
  Claude Code 2.1.319 in November 2026; wording changes between versions").
- L577–579 (the codespace was not tested on GitHub): this is reader A's route for a locked
  laptop. Keep one honest sentence ("built from this file and checked on a local computer,
  not on GitHub's own"), and send the detail to Appendix H's "not tested" section.
- Lead-in (L597–604): three sentences.

**Stamps to move:** L59–60, 66–68, 73–74, 87–88, 573–574 (`checked()` calls: delete, one
dated line for §4.1 and one for §4.8); L213–214 and 234 (install commands: new facts
`agents.install_claude_code`, `…codex`, `…antigravity`, `…opencode`, with the URLs in
Further reading); L250–252; L268; L411–412.

**Page fit**

| Unit | Now | Fix |
|---|---|---|
| `tbl-setup-map` (L98–107) | 0.58 | two columns: the step with its name and reference; "It worked when" |
| `tbl-terminal` (L163–174) | 0.49 | shorten the "Does" cells ("prints the folder you are in"); keep all eight rows, which `fig-terminal-basics` records in order |
| Trust-folder transcript (L297–314) | 0.46 | excerpt: replace the three explanatory lines (L304–305) with "…" and say so |
| Setup-check prompt (L446) | 0.62, budget 0.6 | do not trim a tested, single-copy setup prompt for 0.02 page: ask the lead for a `pagefit.yml` exception |
| Pages 3–5, a wall | — | the cards and the moved table |
| `fig-terminal-basics` (L179) | pushes page 9 (42% blank) | place it straight after the table, before L176 |

**Pause and think:** two exist; keep. **Prompts changed:** none. **Landing page:**
`S.chapter("03-setup")` reads the title; `assistant_accounts()` reads `facts.yml`; the
preface refers to §4.1 and §4.8: keep `#sec-before-setup`, `#sec-codespace`,
`#sec-two-places` and the step IDs. **Glossary:** none new.
**Do not change:** "This chapter ends with a number: 42"; "Two places to type" and its think
box; "The pointer starts on 'No, exit'"; the three prompts; the why box at L407–413.

## Chapter 5, `first-report.qmd`

**Budget:** 5,383 → 5,350. **Aim:** leave the best chapter alone, clear the hunt of one
detour, and fit its transcripts on a page.

**Cold open:** keep L138–141 and L143–148.

**The detour.** "A name with a space" (L222–253) interrupts the hunt between rendering and
checking (reader A). Hand its text to the lead for Appendix B's Paths section
(`#sec-keys-paths`), and leave one sentence in §5.1: "The folders in this book have no
spaces in their names; @sec-keys-paths shows what a space does." About −190 words.

**Density.** L482–488 (identity, nano, Vim): keep, two sentences shorter. L518: drop
"(checked on macOS 26, 2026-11-12)". Keep the fresh-clone check: it is the third of the
three checks.

**Page fit**

| Unit | Now | Fix |
|---|---|---|
| `cat report.qmd` transcript (L364–369) | 0.90; split at 19 px | two computed transcripts with a sentence between them: the settings and the cell; then the sentences. `show_file()` takes a line range; a `text_holds` on the file's line count stops the render if the starter changes. The starter is not rewrapped |
| Diff of the fix (L787–807) | 0.87; split at 19 px | two transcripts, one per change (the cell's two new lines; the sentence), each with its `@@` line and one line of context; drop the `diff --git` and `index` lines and say "trimmed" |
| Diff of the data (L547–556) | 0.51 | drop the `index` line; one line of context each side |
| `tbl-three-checks` (L774–780) | 0.47; pushes page 26 (47% blank) | shorten the third column ("the page's Tate Modern figure against its row") |

**Story, payoff:** none; the chapter is the puzzle, and its block quote of the page
(L296–305) is computed. **Pause and think:** six exist; keep. **Prompts changed:** none.
**Landing page:** nothing quoted. **Glossary:** none new.
**Do not change:** the setup cell and every guard on the planted figure; the starter;
"silence is success"; the three mistakes and their real messages; `#sec-three-checks` and
`#tbl-three-checks` (Chapter 3 and the exercises refer to them); the agent prompt (L744).

## Not verified (D1)

- Sizes after the fixes are estimates from the §3.3 rules; nothing was built.
- Whether `gif_figure()` is called for Chapter 2's two GIFs on the landing page; the brief
  keeps their captions to be safe.
- The licence and install-command URLs are the ones the chapters already cite; I did not
  open them.
- Whether a `::: cards` div may carry an ID that `[text](#reading-paths)` links to in the
  EPUB.

---

# D2: Part II (`improve/d2-part2`)

Files: `part-2.qmd`, `chapters/04-markdown.qmd` (Ch 6), `05-compute.qmd` (Ch 7),
`06-audiences.qmd` (Ch 8), `07-publish.qmd` (Ch 9), `exercises-london.qmd`. Line numbers at
`improve/c-pilot`. All five were read line by line. Shared for the whole package:

- **Stamps.** Every "(… checked 20xx-xx-xx)" leaves the prose; Further reading keeps its dates.
  Lines: Ch 6 237–238, 241, 244, 254–255, 627, 788, 797–798; Ch 7 218–219; Ch 8 89–90, 131,
  146, 273–274; Ch 9 92–93, 255. Where a version matters to the instruction ("needs Quarto
  1.10 or newer") keep the version, drop the date.
- **Landing page.** `ebook/index.qmd` 52 reads `fig-ldn-top10`'s caption and alt text
  (`cell_figure`), 158 and 260 read the titles and addresses of `04-markdown`, `05-compute`
  and `06-audiences`, and `scripts/ebook_media.py` 269–270 photographs `#sec-yaml .agent-box`
  (the first agent box in §7.2) and the *last* `.tryit:has(.catchup)` of `04-markdown`. So:
  no chapter title or file name changes; `#sec-yaml` keeps a prompt, agent and you box as its
  first box; Chapter 6's last Try it keeps its catch-up inside it; `fig-ldn-top10` keeps its
  label, and a change to its caption or alt text changes the landing page (tell the lead, who
  reruns `make ebook-media STEPS=inside`). No quoted sentence (`S.quote`) is in Part II.
- **Prompts that change** (all listed in `PLAN-improvement.md` §3.4; the lead dry-runs each):
  Ch 8's audiences prompt; Ch 9's publish prompt. No other Part II prompt changes.
- **Section IDs stay.** Other chapters and Appendix E point at nearly every one.

## Part II page, `part-2.qmd`

**Budget:** 223 → 220. **Keep** the opening (L3–7): it is a scene already. One change: the
last line before the roadmap ("The exercises at the end of the part test whether you can do
it without the prompts") gains the hook of the exercises: "…and hide one stale number for
you to find." No page-fit entry names this page.

## Chapter 6, `04-markdown.qmd`

**Budget:** 8,070 → 7,700. **Aim:** the newcomer called it "endless scrolling" (ten
animations before the first prompt, three terminal tabs, 8,000 words); reader B ranked it
least engaging. Get to the first prompt sooner, and make its best moment (§6.9.1, the agent
quietly changing Tottenham Court Road to Holborn) the thing the chapter promises.

### Cold open

Keep L34–37 and `fig-london-guide` as the first thing seen. Replace L41–51 (two paragraphs,
the second defensive: "More is new here than in any other chapter") with (paste):

> It starts as an empty folder and one plain-text file. The agent writes most of that file,
> and you check it: Markdown is the layer you read, compare between versions and fix by
> hand when a sentence is wrong. Near the end of this chapter the agent will change
> something you did not ask it to change, and its report will not mention it. By then you
> will have the two commands that show it.

(61 words, no italics; the chapter's first paragraph, L34–37, stays as the hook and is 56
words.) Then one sentence of orientation: "Work in order: read a section, paste its prompt,
look at the result, read the diff, commit." The catch-up sentence (L49–51) goes; §6.11 says
it.

### Payoff picture

`fig-london-guide` (L39) is the payoff and stays first, but its text is unreadable at
340 px. Recapture in `media/capture/london_outputs.py` at a 390 px viewport, device scale 2,
cropped to the title block, the welcome sentence and the start of "Five sights" (so body
text is about 14 px on a phone); the "Other Formats" links, which sit in the margin only at
desktop width, go in a second small crop or into the caption's words. Set it in
`::: payoff`. Alt text rewritten to the crop. Say the capture's text size in the report.

### Structure: marks where the guide first uses them

Reader A's change 5. §6.1 (L70–266, about 1,900 words, nine animations and two tables
before any prompt) is restructured, not cut:

- §6.1 keeps: what Markdown is (L72–76), "Two things make Markdown safe" (L85–93), the
  headings, paragraphs and emphasis animations (L95–115), and §6.1.5 render and preview
  (L251–266). L78–83 (how the animations were made) moves to Appendix H: give the lead the
  paragraph; here one clause remains ("the right-hand page is Quarto's own render").
- The lists animation moves to §6.6 (L510), the link and picture animations to §6.7 (L596),
  the quote animation to §6.7, the rule animation to the toy file. Each replaces the
  sentence that currently re-explains the mark there (L377–379, L534, L612–615 shrink).
  `fig-md-image-link` stays with the picture. Figure IDs do not change.
- "All the marks together" (L158–221: two tables, `toy.md`, `fig-toy-md`, the think box)
  moves to *after* the Try it of §6.9, under its own heading with the same ID, as the
  chapter's reference page: "every mark you have now used".
- "GitHub's Markdown and Quarto's" (L232–249) shrinks to the three differences as a list
  with a one-sentence lead; the two quoted definitions and their stamps go.

### Pause and think

Keep the four. Two changes:

- The "spot the change" think (L743–762) is the chapter's planted error and its answer is
  0.70 page. Split it: the question keeps the `git status` transcript above it; the answer
  is cut to ≤ 80 words: "Look before you undo. `git diff data/sights.csv` shows one value
  changed: the British Museum's station. The agent replaced the station the museum's own
  page names with one from its memory, against the rule that keeps `data/` unchanged.
  `git restore data/sights.csv` puts that one file back and leaves the checklist alone.
  Commit `london.md`, and tell the agent which rule it broke." The two-line diff becomes a
  `transcript` block *after* the box, followed by one sentence in the text: "This scene is an
  illustration, not a recorded session…" (L759–761). The guard at L720–726 stays.
- New predict box before the lists prompt's diff (L540): "Before you run `git diff`: how many
  files will it list, and will any line start with `-`?" Answer: one file; no line is
  removed, because the prompt only added; a `-` line would be a change you did not ask for.

### Story box

None: I found no recorded incident for this chapter's steps, and §6.9.1 is itself labelled an
illustration. Do not add one.

### Walls and density

- L482–490, the four rules in one paragraph (plan: "rules paragraph → table"): a two-column
  table, Rule | Why, four rows, ≤ 350 characters (e.g. "Every number from a cited file |
  an agent asked for a number it lacks may supply a plausible one"). The listing at L494–502
  stays.
- L782–798 (uv, lockfile, the platform-tag "Why"): cut the "Why" box at L793–799 (reader A:
  "the lockfile-and-Fortran Why") to one sentence in the text, drop the other languages'
  lockfiles (L789–791) and footnote `uv-speed` (L817–820).
- L354–359 (trust question, `--add-dir`): keep the first two sentences; `--add-dir` to one
  clause.
- L680–690: the pitfall's two traps become a two-row symptom / cause / fix table; the `403
  Forbidden` paragraph joins it as a third row.
- §6.11 (L860–912): reader B stopped at "catch-up mechanics". Keep the agent line and the
  `git status` transcript; cut L871–875 to two sentences and the "Why" at L879–882 to a
  clause. About −120 words.
- Repeated `git status` dumps: keep L389–397 (first) and L731–740 (the planted one) and
  L888–904; none added.

### Page fit

| Unit | Now | Fix |
|---|---|---|
| `cb1`, `toy.md` printed whole (L196–215) | 0.97 page; splits at 19 px | per §3.4: show the file as two source-and-result pairs, split at its `---` rule (line 23 of `media/examples/toy.md`). `show_file()` gains a line range; each half is followed by its own picture. The file is not edited |
| `fig-toy-md` (L221) | 0.73, budget 0.7; 920 × 1923, capped | `toy_examples.py` writes two pictures, `toy-md-1.png` and `toy-md-2.png` (new names: Spanish reads `media/figures` through a symlink), each of the matching half of `toy.html`; second figure gets a new ID `fig-toy-md-2`. One-sentence captions; the photo credit stays on the half that shows the photo |
| think answer, "spot the change" (L747–761) | 0.70, budget 0.45; splits at 19 px | the split above |
| `tbl-md-blocks` (L180–191) | 0.59 | drop the two rows that the animations already show in full (link, picture) or split by theme: "links and pictures" (3 rows) and "blocks and escapes" (5 rows). Prefer the split; new ID `tbl-md-escapes` |
| `tbl-md-text` (L163–174) | 0.54; pushes page 10 (41% blank) | shorten the right-hand cells to the result alone ("a heading", "a new paragraph"); the section pointers move to one sentence under the table |
| diff transcript (L545–570) | 0.58 | print the hunk without the three unchanged context lines and the `index` line, or show the first eight added lines and "…"; say so in the sentence above |
| `git status` transcript, §6.11 (L888–904) | 0.46 | drop the two "(use …)" hint lines for untracked files, with "…" |
| Try it, §6.10 (L844–857) | 0.52 | first sentence to "Run the environment prompt, read its diff and commit it."; move "Keep the preview running…" to the text. **Keep the catch-up inside this Try it** (landing-page capture) |
| pages 4, 9 (35–39% blank), page 40 (44%) | figures pushed whole | eased by moving the animations to their sections; no other action |

### Other points

- **Duplicates:** the preview-and-render collision is explained here (L447–452), in §7.5
  and at length in §7.7. Home: §7.7. Here keep the pitfall, two sentences.
- **Glossary:** none new.
- **Do not change:** all eight prompts; `fig-preview-reload`, `fig-uv-environment`; the
  `.gitignore` listing and its explanation (L316–333); the first `git status` (L381–403);
  the practice box (L586–594); the "Why" on alt text (L619–624); the think boxes at L671 and
  L830; the last sentence of the Summary lead-in (L929–931).

## Chapter 7, `05-compute.qmd`

**Budget:** 3,422 → 3,400. **Aim:** reader A called it "the tightest hands-on chapter";
change little.

### Cold open

**Keep** L34–38 (computed, guarded by the `assert` at L29). In L40–43, cut "That is the
workflow's central promise, and the rest of the book builds on it."

### Payoff picture

None new: `fig-toy-qmd` and `fig-ldn-top10` already show the result within the first third.
Do not touch `fig-ldn-top10`'s caption or alt text (landing page).

### Pause and think

Keep four of the five. **Cut** the matplotlib-or-Plotly box (L377–383): L285–287 says the
same in the text. The Tower prediction (L352–367) is the chapter's predict device and stays;
its answer is over budget (below). No new box.

### Story box

None; nothing recorded for this chapter. (The Apple Books story is Chapter 23's.)

### Walls and density

- L200–208 ("The cell does four things"): reader B stopped at line-by-line pandas. Keep the
  list, cut each item to one line; delete L217–219 (Quarto 1.4 and knitr; reader A stopped
  there).
- L425–438: keep the kernel paragraph (it explains the collision, whose home this is); cut
  the `IPKernelApp` sentence (L438) to a clause pointing at @sec-step-test.
- L412–415: one sentence on opening the EPUB; drop "This book's EPUB edition is built the
  same way…".

### Page fit

| Unit | Now | Fix |
|---|---|---|
| `cb1`, `toy.qmd` printed whole (L69–87) | 0.68, budget 0.45 | two computed halves, as for `toy.md`: front matter, prose and the shown fence; then the cell and the sentence. The five-item list (L91–102) divides to match (items 1–3 after the first half, 4–5 after the second) |
| think answer, Tower (L358–366) | 0.51 | end the answer at "The typed word 'ten' does not change either." Move "To check a prediction like this one…" (L363–366) to a sentence after the box |
| `cb4`, the agent's cell and sentences (L186–198) | 0.48; pushes page 8 (38% blank) | show the cell and the two sentences as two fences, the sentences introduced by "and below it:" |
| Try it, §7.7 (L448–462) | 0.52 | "If you have not yet, run the formats prompts with the preview stopped, then restart it."; done text to one clause per file |
| page 18, 35% blank (`fig-render-many`) | pushed whole | follows from the cut at L412–415; otherwise leave |

### Other points

- **D8:** the plan's "Ch 4 repeating Ch 1's `hello.qmd` listing" is reader Chapter 4
  (`03-setup.qmd`, package D1). This chapter only refers to it (L66) and is right.
- **Do not change:** `#sec-yaml`'s box (L133–145) and its annotated YAML; `tbl-qmd-code`; the
  `ch5-one-row` cell; all prompts; the think boxes at L122, L221, L440; the "Why" at L369.

## Chapter 8, `06-audiences.qmd`

**Budget:** 3,367 → 3,350. **Aim:** open on the three readers, not on the retired hook;
make the long prompt something a newcomer understands before pasting it.

### Cold open (replaces L39–53; paste)

> A manager opens the dashboard between two meetings and gives it a few seconds. A partner
> forwards the brief to a colleague without rereading it. Someone walking past the tourist
> office takes a flyer, glances at it and puts it in a pocket. Three readers, three glances,
> and each must come away with the same facts. A correct document that its reader does not
> use has failed, so this chapter chooses each format for how it will be met, and gives
> every output one test: would that reader read it, and act on it?

(88 words.) Second paragraph, ≤ 70 words, from L43–48: the chapter writes the three in one
step, and because none needs another to exist they are the first job worth splitting across
several agents; the flyer copies its facts, a choice §9.5 returns to. **D8, title:** the
title stays ("Five Audiences" matches `tbl-audiences`); add one sentence so "three in one
step" no longer contradicts it: "Three of the five audiences in @tbl-audiences are served
here, a fourth optionally, and the fifth, visitors, in @sec-publish."

### Illustration (I1), after L156–160

```markdown
::: {.story .illustration}
Two helpers are each told to build a page in the same folder. Both finish, and both render
at once. Each render writes its working files under the same names; one of them fails with a
message about a file it never mentions in its report, and the lead, reading two cheerful
summaries, sees only that an output is missing. Nothing was wrong with either page. The
folder was shared and the rendering was not coordinated.
:::
```

(No recorded incident exists; the mechanism is the chapter's own, L156–159.)

### Payoff picture

`::: payoff` after the opener: the three outputs as stacked crops in one picture,
`media/figures/london-audiences.png`, made by a new step in `london_outputs.py`: the
dashboard's value-box row (captured at a 390 px viewport), the brief's first heading and
paragraph (first page of the docx's PDF export, or the HTML of the same source if no
converter is available: say which), and the flyer's top third. Each crop's body text
≥ 9 CSS px at 340 px wide. `fig-london-dashboard` and `fig-london-flyer` stay in their
sections; the dashboard screenshot there is recaptured at phone width (plan D3 list).

### Pause and think

Keep the two (L170, L214). Add a predict box before "Then check the two rules yourself"
(L207): "Three sub-agents have reported success. Before you open anything: what should
`git status` list, exactly?" Answer: the four source files the prompt named and nothing
else; no rendered file (`.gitignore`), nothing in `data/`, `images/` or `london.qmd`. A
fifth entry is a sub-agent that strayed, whatever the lead's summary says. L207–212 then
shortens to the commit instruction.

### The audiences prompt (L181–189): changes; lead dry-runs

942 characters, 1.07 pages, split over three. Per §3.4: a lead prompt plus the items as a
list outside the fence, pasted as a second message. Draft for the dry run:

1. **Prompt** (≈ 330 characters): "Run three sub-agents in parallel, one per item of my next
   message (none? do the items in turn). Each reads london.qmd, data/ and images/, hides
   code, follows AGENTS.md and only writes its own files: no rendering. Then render the
   three .qmd files yourself, one at a time, and check each. Wait for the items."
2. **The three items**, each its own short fence (so each has a copy button and is a unit of
   ≤ 400 characters), with the wording of L184–186 unchanged, under "then paste these
   three, in one message".

Before the box, one plain sentence (reader A: "a frightening block; I would paste it
without understanding it"): "The prompt does three things: it says how the work is split,
gives each helper one file to write, and keeps the rendering for the lead." If the dry run
shows two messages confuse a smaller model, fall back to one fence per item with the lead
sentence repeated; record which was run.

### Walls and density

- L144–154, the per-vendor paragraph (both readers stopped): a four-row table, Agent | How
  it runs sub-agents, ≤ 350 characters, no stamps; the OpenCode caution ("check every file
  exists before the lead renders") is the fourth row's text, not a new warning.
- L115–121: keep; it carries the data's two caveats.
- L222–228, pitfall: three symptom / fix pairs as a three-row table.
- L272–275: "This was tested with Quarto 1.10.20…" loses its date.
- §8.5 (L283–343): reader B noted it "admits Figure 7.2 is the better chart". Keep the
  pitfall, which is the point; cut L331–336 to two sentences.

### Page fit

| Unit | Now | Fix |
|---|---|---|
| audiences prompt (L181–189) | 1.07 page, split over 3 (1.50 at 19 px) | the split above |
| `fig-london-flyer` | 986 × 1400, capped by max-height (not failing) | leave; its text is a flyer's, large |

### Other points

- **Duplicates:** the collision rule's home is §7.7; here one clause. The sub-agents
  vendor survey has no other home; it stays as the table.
- **Glossary:** none new (`sub-agent`, `lead`, `value box`, `div` are defined here; check
  the first two are in Appendix J and report if not).
- **Do not change:** `tbl-audiences`; the dashboard outline (L92–104); the practice box
  (L162–168), reader B's best; the scene and live-link blocks of §8.5 (L289–309;
  `check_scenes.py`, `check_live_links.py`, the QR code); the advert and three.js prompts;
  the Summary.

## Chapter 9, `07-publish.qmd`

**Budget:** 3,720 → 3,600. **Aim:** the newcomer's two best moments are "open the address
on your phone" and "A cited copy is still a copy". Show the first; clear the host trivia
and the "not re-tested" aside out of the way of the second.

### Cold open

**Keep** L59–64, trimmed to (paste):

> The guide is finished, and nobody but you can see it: every output sits in a folder on
> your computer. This chapter puts it on the web, where anyone can open it on a phone. Then
> it asks a question with no prompt attached: one input changes; which outputs change with
> it, and how do you know? You will predict first, then rebuild, then check.

(62 words.) The GitHub and GitHub Pages clause moves to §9.2.

### Story box (T4), in §9.4 in place of L255–258

```markdown
::: story
<!-- source: book/chapters/07-publish.qmd lines 255–257 at 651db10; AGENTS.md, "Workshop
slide conventions" (Quarto 1.6.40's --no-prompt cannot create the gh-pages branch) -->
In a dry run, the first publish was handed to the agent with `--no-prompt`. It stopped:
"the remote origin does not have a branch named gh-pages". The branch is made by the first
publish, and that flag would not make it. That was Quarto 1.6.40; whatever your version
does, the first publish is the one to type yourself. After it, updates can be the agent's.
:::
```

L250–258 then keeps: stop the preview; the one question and Enter; what the publish does;
"Once the branch exists, the agent can update the site with … `--no-prompt`." "Not
re-tested with 1.10.20" is inside the story as "whatever your version does".

### Payoff picture

`::: payoff` after the opener: the published guide on a phone,
`media/figures/london-live-phone.png`, captured by `london_outputs.py` from a local render
of `examples/london` served at a 390 px viewport, device scale 2 (not from the live
address: captures use no network), cropped to the navbar, title and first lines. Caption:
"The guide as a visitor's phone shows it. Rendered from `examples/london`." Body text about
14 px on a phone.

### The publish prompt (L229–233): changes; lead dry-runs

660 characters, 0.76 page. Per §3.4, two prompts, each ending in a check:

1. "Check that .gitignore covers _site/, .quarto/, .venv/, *_files/, *.quarto_ipynb,
   london*.html, *.docx, *.pdf, *.pptx and *.epub. Replace README.md with a short one
   linking to https://<your-github-username>.github.io/london-guide/ and listing the files
   in the site's Downloads menu. Commit it with any work not yet committed. Show me the
   README and `git status`."
2. "Create a public GitHub repository named `london-guide` with gh and push `main` to it.
   Set the repository's website to https://<your-github-username>.github.io/london-guide/
   with `gh repo edit --homepage`. Show me the repository's URL and the website URL you
   set."

The "If this folder is not yet a Git repository, run `git init -b main`" clause goes: the
folder has had a history since §6.2 (say so to the lead; the catch-up route also has one).
The agent and you boxes divide to match.

### Pause and think

Keep the two (L112, L136). The Try it at L304–314 is the predict device; leave it.

### Walls and density

- **§9.5's opening (L295–299)** points at the hook Chapter 1 no longer poses. Rewrite:
  "@sec-drift listed what goes wrong when a correction has to be carried by hand into every
  file that quotes it. Here is the correction for real, in a project where no visitor count
  was ever copied." L355–357 loses "that answers the question @sec-quarto began with".
- **§9.2 (L144–167):** reader A stopped at the hosts tables, reader B too. Keep the two-way
  split (L129–134) and its think box; merge the two tables into one of three rows (GitHub
  Pages, Netlify, "a host that builds: Vercel, GitLab Pages, Render"), and cut L164–167 to
  the one sentence this project needs ("Quarto's Netlify build runs no Python, so render and
  upload"). Quarto Pub goes. The plan sentence about free plans stays here, its one home.
- **L260–262** (timings from the dry run): keep "a 404 in the first minute usually means the
  site is still being deployed"; drop the measured seconds or move them into the story's
  source comment.
- **L405–412, "Three traps":** a three-row symptom / cause / fix table.
- **L84–110:** reader B stopped at Git vocabulary. Cut L84–90 to two sentences; keep the
  figure and L99–104.
- **D8, the lead-in (L428–432)** says the water analysis comes next. Replace: "That completes
  one guide for many audiences. The exercises that follow leave the prompts out, and hide one
  stale number for you to find. After them, Part III takes one set of results to the
  documents a company is asked for: a model card, a deck, a site and a white paper." (If
  §2.3's bridge sends newcomers to Part V, the part page says so; not here.)

### Page fit

| Unit | Now | Fix |
|---|---|---|
| publish prompt (L229–233) | 0.76, budget 0.6; splits at 19 px; pushes page 10 (47% blank) | two prompts, above |
| `fig-whitepaper` (L403) | 0.73, budget 0.7; 989 × 1400, capped | crop to the title, abstract and first heading (plan: "white-paper crop"), new file `london-whitepaper-top.png`; alt text to match |
| `tbl-london-deps` (L328–341) | 0.63, budget 0.45; splits at 19 px | drop the "Writes" column (the sentence at L343–344 gives the count; list the formats in a sentence), leaving Page and four narrow mark columns; if still over, show only the pages that read `attractions.csv` and `sights.csv` |
| Try it, §9.5 (L304–314) | 0.53 | steps 2 and 4 to five words each ("Rebuild: stop the preview, `uv run quarto render`."); done text to "you can name what changed, what did not, and the line of code that links each changed output to the input." |

### Other points

- **Duplicates:** "A cited copy is still a copy" appears at L363 and in the exercises'
  answer 10 in other words: keep both. The `freeze` "Why" (L365–371) repeats §7.7 and
  §23.4: cut to two sentences.
- **Facts:** none new. `tbl-hosts-free` stays in Appendix K.
- **Glossary:** none new.
- **Do not change:** the setup cell and its asserts (L3–57); `fig-git-cycle`,
  `fig-publish-flow`; the website prompt and YAML (L171–207); the three paragraphs at
  L346–363 apart from the clause above; the practice box (L270–276); the white-paper prompt.

## Exercises for Part II, `exercises-london.qmd`

**Budget:** 1,931 → 2,000. **Aim:** a hook, a planted error (D5-a), and no wall (the audit:
pages 7–11 without a visual unit).

### Cold open (replaces L16–26; paste)

> One number in the table below is a year out of date. It is in the right column, in the
> right units, beside the right name, and nothing about the page says so. Finding it needs
> only what Part II taught: put each number beside the row it came from. Do that first; then
> the five exercises below rebuild the guide in order, and the ones after them leave the
> prompts out.

(67 words.) Then the table, then L16–26 reduced to a three-item list: "did the chapters: use
the five as a checklist"; "read without doing: do them in order"; "each done-when asks for
the three checks (@sec-three-checks) where they fit". The definitions of scope, correctness
and rebuild go (Chapter 5 owns them).

### D5-a, the planted value

A cell reads `../examples/london/data/visits.csv` (the five sights by `year`; `attractions.csv`
has no 2024 column) and prints Attraction | Visits in 2025 for the five sights, sorted by
their 2025 visits, after replacing the 2025 value of the sight ranked third with its own
2024 value from the same file. Guards (`text_holds`): the two values differ, and the altered
table's order is unchanged. Caption:
"Visits in 2025 to five ALVA member attractions. One cell is wrong." The reader checks
against `~/london-guide/data/visits.csv`. **For Appendix E** (the lead integrates):
hand over an answer cell that prints the sight, the printed value, the real value, their
difference and the sentence "it is that sight's 2024 count".

### Walls (pages 7–11)

- "Write your own prompts" (L124–153): the five tasks become `::: cards`, term = the task's
  name, definition = task and "done when", each ≤ 80 words (task 4 and task 1 need
  trimming).
- "Review questions" and "Answers" (L155–218): keep as numbered lists, but put each answer
  under its question as a `::: think` pair for questions 2, 5, 7 and 10 (the four that ask
  for a prediction), which gives the run four visual units; the other six stay in the
  Answers list. Answer 2 (L187–191) is cut to ≤ 80 words.
- L90, "There is no checkpoint 03…": keep (reader A: checkpoint numbers "look random").
- The five catch-up boxes: the filter now shortens all but the first (§0.8); nothing to do.

### Other points

- IDs: Part II's exercise headings have no explicit IDs and the Spanish twin may hard-code
  the generated ones (the plan found this for Part V). Do not rename a heading; if a
  heading must change, give it an explicit ID equal to the old generated one.
- **Do not change:** the done texts of II.1–II.5 (Appendix E mirrors them); the catch-up
  lines; the paragraph at L216–218.

## Not verified (D2)

- Nothing was built or measured: every "≤ 350 characters", page fraction after a fix and
  capture text size is an estimate for `make book-pages` to confirm.
- D5-a: `attractions.csv` has no 2024 column (checked), so the plant reads `visits.csv`; I did
  not check that the third-ranked sight's 2024 and 2025 values differ without changing the order.
- Whether `london_outputs.py` can render the Word brief to a picture without a converter;
  the brief gives a fallback.
- The split audiences and publish prompts are drafts; none was run. Dropping the
  `git init` clause from the publish prompt assumes every route into §9.4, the catch-up
  included, already has a repository.
- That moving the animations out of §6.1 leaves `ebook_media.py`'s captures and
  `gif_figure` lookups working: `gif_figure` searches every chapter for the GIF by name, so
  it should, but I did not run `make ebook-check`.
- Whether Appendix J already lists `sub-agent` and `lead`.
- I did not re-read Chapter 7 L1–19 (the setup cell's imports) or L470–end (Summary's last
  items and Further reading).

---

# D3: Parts III and IV (`improve/d3-craft-team`)

Files: `part-craft.qmd`, `results.qmd` (Ch 10), `sites.qmd` (12), `white-papers.qmd` (13),
`parameters.qmd` (14), `part-team.qmd`, `team.qmd` (15), `at-work.qmd` (16), and the new steps
of `book/media/capture/eval_outputs.py`. Line numbers are at `52d9215`. Every prompt changed
below is recorded in the author's report and dry-run by the lead (Sonnet, then Haiku).

## What the Chapter 11 pilot hands to D3

- **The contrast table lives in Chapter 11** (`tbl-slides-contrast`). Chapter 12's
  `tbl-sites-palette` goes (below).
- **`eval_outputs.py` exists with a `deck` step.** D3 adds steps, each rendering a temporary
  copy of a checkpoint with its own `uv` environment and writing pictures to
  `media/figures/`: `report` (checkpoint 15, for D1's Chapter 3 if D1 asks), `card` (15),
  `site` (17), `whitepaper` (18), `update` (19), `red` (20). **No render inside a book
  cell** (§0.3): where a chapter prints rendered text, the step writes JSON beside the
  picture and the chapter reads and guards it, so a stale capture stops the render.
- **Captures:** HTML at a 390 px viewport, device scale 2 (body text about 14 px on a phone);
  PDF pages with `_pdf.first_page_png`, cropped to the title block so text is ≥ 9 px at
  340 px wide. Crops are stacked, never side by side. Report each capture's text size for
  `pagefit.yml`. Alt text carries no result unless `alt_text_holds` guards it.
- **Rule for every chapter here:** "in the test run" appears once, in a story or a table
  caption ("met while testing, 2026-11-18"), not in each sentence. Dates of checks stay in
  Further reading and the setup cell's comment.

---

## Part III page, `part-craft.qmd`

**Budget:** 411 → 300 words. **Aim:** a stake instead of a recap, then the fork reader A
stalled at (L36–38 sends her back to a chapter she was told to skip).

**Opening (replaces L3–13; paste):**

> A two-person company has a model, three releases of it, and a decision to make: which one
> its client's call centre should use. Five kinds of reader will check the answer. A
> reviewer wants to know whom the model treats differently. The room wants one slide that
> says what is being decided. An investor wants one address, a client's analyst wants a
> paper with references that exist, and next month somebody will want all of it again, with
> new numbers. This part makes each of those documents from one set of results.

(91 words.) Then one sentence for the method: vocabulary, a tested prompt, verification
(@sec-three-skills). **Keep here**, and only here, "You will rarely write a theme or a
template by hand…" (L11–13); Chapters 10 and 11 drop their copies.

**The bridge (replaces L36–38):**

```markdown
::: {.cards title="Where you are coming from"}
By the fast path
: Carry on: @sec-results continues your `acme-eval` repository.

From zero
: Two honest routes. Copy `checkpoints/14-eval-start/` with its catch-up line and read on:
  the terminal of @sec-setup and @sec-first-report is enough. Or go straight to the water
  analysis (@sec-water-question), which needs only your setup, and come back later.
:::
```

Then three one-line definitions: Acme Signals (fictional; real public data), a model that
ranks a call list, and "recall in the top tenth: of the people who would subscribe, the
share found by calling the first tenth of the list". Chapter summaries (L15–34): one
sentence each, ≤ 25 words. No page-fit entry. **Do not change:** the roadmap cell.

---

## Chapter 10, `results.qmd`

**Budget:** 2,731 → 2,800. **Aim:** open on the finding, show the card, turn two trap
walls into tables. Reader A met "bootstrap, checksum, leak, Brier score unexplained";
reader B wants the card shown and "test run" (seven times) thinned.

**Cold open (replaces L34–45; paste):**

> The fast path ended with one report and one winner. This chapter asks a second question
> of the same results: whom does the winning release call? The answer is in a file the
> report never opened, and it is not one its makers would have guessed from the headline.
> The list the call centre would work from is not a fair sample of the bank's customers,
> and one group is called far more often than another. A report can leave that out. A
> model card cannot, and writing one is this chapter's larger task: handed to the agent
> whole, with a plan first and its checks after.

(100 words; no numbers; the computed finding stays at L147–154.) Second paragraph, ≤ 45
words, from L37–39: one script computes every result once, and every document reads them.
Cut L43–45 (repeats the part page).

**Payoff (after the opener):** `::: payoff`, `media/figures/eval-card-top.png`: the model
card's HTML at phone width, cropped from its title to the end of "Intended use". Step
`card`. Caption: "The top of the finished model card, rendered from
`checkpoints/15-eval-results/model-card.qmd`."

**Story (in §10.4, before the Try it at L251; the incident is the reason for the exercise):**

```markdown
::: story
<!-- source: REVISION-PLAN.md line 475 (WP5: "the dry run found 'top 10%' typed in our own
checkpoint's labels and captions, now computed or guarded"); results.qmd lines 272–277 -->
This project failed its own exercise. A dry run of this chapter's change found "top 10%"
still typed in our own checkpoint: in a table caption and two row labels, beside the new
figures. The numbers had moved and the words had not. The labels are computed now, and
each caption that names the share has a guard.
:::
```

**Think 1 (rewrite of L266–281; answer was 0.78 page):** question unchanged. Answer, ≤ 80
words: "The number of calls (to `{python} f"{calls_double:,}"`) and every top-of-list
metric change: recall, precision, lift, each band's share called. ROC AUC, the Brier score
and the calibration do not: they measure the whole ranking, not where it is cut. The trap
is the share named in words: a typed 'top 10%' stays. In the finished project both
documents stop on a caption's guard, and two unit tests that pin the rule fail, on
purpose." The agent's own stopped card (L279–280) is cut.

**Think 2 (new, after `tbl-results-check-kinds`):** "The data have a column, `duration`,
the length of each call in seconds. It predicts a subscription better than anything else
in the table. Should a release use it?" Answer: "No. A call's length is known only after
the call, and the model's job is to choose whom to call. A model trained on it would score
superbly in the evaluation and be useless in service: a leak. No render would notice; a
test does (`tests/`, 'no leakage'), which is why the repository has one." Source for the
fact: `results.qmd` 88; `REVISION-PLAN.md` 560–561.

**Walls and density**

- L88: the Tests cell names four catches in 190 characters; keep two here (the checksum, the
  leak) and define both in a sentence after the table: a checksum is a fingerprint of a
  file; a leak, above. "95% bootstrap interval" (L76): add "(a range from re-drawing the
  test set many times)". Brier score (L271): "the mean squared error of the probabilities".
- L125–145: keep the four checks as a list; cut "in the test run" from three of them (keep
  the garbled DOI record, L138–140, as the example).
- **Pitfall L167–176** (0.54 page) → a two-column table, "Met while testing the card":
  `df.style` needs `jinja2` | write the table another way. PDF citations in another style,
  second "Bibliography" page | `citeproc: true` under `typst:`. An old `model-card.html`
  after a failed render | read the render's last lines.
- L203–205: cut the quoted sentence; "search each output for ??" is the check.

**Page fit**

| Unit | Now | Fix |
|---|---|---|
| Model-card prompt (L117) | 0.81 (1.20 at 19 px, split) | trimmed below, about 520 characters; the nine section names leave the fence, since the paper named in it lists them, and go in a sentence after the box so the reader can check the plan against them |
| Think answer (L269–280) | 0.78 | above |
| Try it (L251–264) | 0.65 | steps to one line each ("Predict: `TOP_SHARE` in `src/acme_eval/metrics.py` is `…`; double it and write down what will change, what will not, and what will stop."); done text ≤ 20 words |
| `tbl-results-check-kinds` | 0.62 | as above; third column ≤ 60 characters a row |
| Pitfall (L167) | 0.54 | the table above |
| `tbl-results-outputs` | 0.50 | row 1: "the best release, the test-set size, the base rate, seeds and versions", the three computed values moving to the sentence before |
| `tbl-results-refs` | 0.46 | reader B: it repeats `tbl-fast-vocab`. Keep two rows (numbered sections; a section referred to) and point to @tbl-fast-vocab for tables and figures; the citation row is in the trap table |
| Page 10, 54% blank | sections prompt 0.56 | put the "check is in the prompt" sentence before the box |

**Trimmed prompt (L117):**

```default
Plan first, and wait for my go-ahead: add model-card.qmd (html, docx and typst) for the best release, with the sections of Mitchell et al. (2019), "Model Cards for Model Reporting". Read only outputs/ and data/README.md; slices by age band and by job come from outputs/segments.csv, calibration from outputs/calibration.csv. Cite the paper and the dataset from a new references.bib, opening each DOI first. Guard every sentence whose wording depends on the results with `claim`. Render all three formats, then list anything you could not verify.
```

**Other:** landing page: nothing quoted. Glossary: propose `leak` (data leakage) and
`Brier score` to the lead. **Do not change:** the setup guards (L28–29); L147–154 and
`tbl-results-ages` (reader A's and B's best passage); the sections prompt (L194);
`fig-results-calibration`; "A guard whose condition can never be false… protects nothing";
the closing two sentences (L298–299).

---

## Chapter 12, `sites.qmd`

**Budget:** 2,481 → 2,600. **Cold open:** keep L53–58 (79 words); trim L60–63 to ≤ 40 words.

**Payoff (after the opener):** `media/figures/eval-site-home.png`: the site's home page at
phone width, from the navbar to the listing's first entry. Step `site`. Caption: "The
finished site's home page at a phone's width, rendered from `checkpoints/17-eval-site/`."

**Story (replaces the pitfall's second half, L215–217), with before and after:**

```markdown
::: story
<!-- source: book/chapters/sites.qmd lines 215–217 at 651db10 ("a navbar in the brand's
primary colour hid a logo in the same navy; `background: light` in the navbar fixed it") -->
In the test run of this chapter, the navbar took the brand's primary colour, a navy. The
logo was the same navy, so the bar hid it. `background: light` in the navbar fixed it. A
build log reports what was written, not what can be seen: look at the site, not only its
log.
:::
```

Under it, two stacked crops of the navbar (`eval-site-navbar-before.png`, `-after.png`),
made by the `site` step rendering once with the navbar's `background` removed. If the
checkpoint's `_quarto.yml` does not reproduce the hidden logo that way, show the after
crop only and say so in the report; do not stage a before picture by other means.

**Think (after the checks prompt, L225–229):** "`check_site.py` passes on every page. Name
one thing it has proved on all of them, and one thing only your eyes can check." Answer:
"Proved: every image has alt text, every page a title, a description and a language, no
heading level is skipped, and the brand's text colours pass 4.5:1. Not proved: that the
alt text is true, that the logo can be seen on its bar, that the page reads well on a
phone. A script checks every page for what can be stated as a rule; you check one page
for everything else."

**Walls and density**

- **L118–128, `tbl-sites-palette`: cut** (duplicate of Table 11.3). One sentence instead:
  "The brand's text colours are the theme's of @tbl-slides-contrast, now read from
  `_brand.yml`, and the same test checks them." The `text_holds` at L44–45 stays.
- **Pitfall L135–143** → table "Met while testing the brand": Sass "Undefined variable" |
  `brand` must be last in `theme:`. Typst "unknown font family" | no generic `sans-serif`
  in the brand's fonts. Charts ignore the brand | a helper gives matplotlib the brand's ink
  and paper.
- **L156–168** (Word XML; reader A stopped): to 60 words. Keep "check the file, not the
  script" and "check a Word file in Word, and in whatever your readers open it with". The
  `.gitignore` exception joins the table above; Quick Look and Times go.
- **L231–242** (130 words): the two findings (logo without alt text; no description tag on
  the deck's page) stay as two sentences; the five reasons become a five-item list of one
  line each.
- **L250–256:** point to @sec-hosting for where a site may go; keep "who may see it" and
  `site-url`. The Pages-plan sentence has its home in Chapter 9.

**Page fit**

| Unit | Now | Fix |
|---|---|---|
| `tbl-sites-vocab` (L175–186) | 0.91 (1.34 at 19 px, split) | two tables of two columns (Ask for; Quarto calls it). **Pages and navigation** (`#tbl-sites-vocab`): exactly these pages, a menu with the logo, a line on every page, an About page. **Finding and sharing** (new `#tbl-sites-find`): a listing home page, search, social cards, the other formats. The Check column becomes the done text and the think box |
| Site prompt (L190) | 0.67 | split at "index.qmd:". Turn 1 ends "…and a description on every page. Render the site and list the pages and any warnings." Turn 2: "Write index.qmd: a first sentence stating the headline result as inline code with a guard, then a table listing of the three documents. Write about.qmd: an about page with the trestles template. Render the site and tell me what the home page's first sentence says." |
| `tbl-sites-brand` (L91–100) | 0.66 | two columns: Format; How it gets the brand ("yes/no" folded in: "from `_brand.yml`: colours, fonts, logo"; "not reached: a reference document"). Four rows: web pages and dashboards; Reveal.js; Typst PDFs; Word and PowerPoint |
| Brand prompt (L110) | 0.62 | cut "(a simple wordmark, marked in a comment as a fictional company's)" to "(a wordmark; say in a comment the company is fictional)" and "tell me where the brand's colours appear in each output" stays |
| Page 5, 36% blank | pitfall 0.45 | the table above |

**Other:** glossary: `brand file`, `listing` exist; propose `social card`. Landing page:
nothing. **Do not change:** `tbl-sites-brand`'s content (reader B's best table); the
templates prompt (L152) and the checks prompt (L227); "A person checks the page they are
looking at. A script checks every page, every time."; the catch-up and done text.

---

## Chapter 13, `white-papers.qmd`

**Budget:** 2,276 → 2,400. **Cold open:** keep L42–47 (83 words). L49–53 to ≤ 45 words; drop
the pointer to the optional London and water papers.

**Payoff (after the opener):** `media/figures/eval-whitepaper-p1.png`: page 1 of the PDF,
cropped to the house title block and the abstract. Step `whitepaper`; `first_page_png` at
1400 px wide, then crop. Body text in a PDF page shown 340 px wide is too small; the crop
must be no wider than the text column and is checked for ≥ 9 px. If it fails, crop to the
title block alone.

**Story (in §13.5, replacing L201–203):**

```markdown
::: story
<!-- source: book/chapters/white-papers.qmd lines 201–203 at 651db10 ("a pattern written
"page 1 of 1" printed "pbge" on the second page") -->
The house template's page-number pattern was written `"page 1 of 1"`. On the second page
it printed "pbge". In a Typst pattern, letters are counters too: the "a" in "page" was read
as a request to count in letters, and the second page is "b". Keep words outside the
pattern, and look at a page that is not the first.
:::
```

**Think (after L109–113):** "`check_refs.py` reports that every DOI resolves, with the
right year, first author and title. Is the reference list checked?" Answer: "Half of it.
The works exist and are described correctly. Whether each says what the paper claims it
says, no script knows: someone has to have read it. While this paper was built, one DOI
resolved to a paper that could not be opened at all. It is not cited, and the measure it
introduced is defined in the text instead."

**Spot the error, kept honest.** Reader A asked for "a fake reference". Do not print an
invented reference as if it were real. Instead, in §13.4 after L179–181, a cell prints one
real entry of `references.bib` twice, the second with its year reduced by one (guard: they
differ), captioned "one of these is the entry as published": the reader says what
`check_refs.py` would report. Answer in one line beneath, computed.

**Walls and density**

- **Pitfall L154–166** (0.72 page) → table "Met while testing the references", four rows:
  a second "Bibliography" heading in the PDF | `citeproc: true`. "bank marketing" in lower
  case | brace proper names in the `.bib`. The dataset's DOI not found in Crossref | it is a
  DataCite DOI. An opening quote in "ICML '05" | leave abbreviated venue names out of the
  `.bib`. The unopenable paper moves to the think answer; `typst-smart` is cut.
- **L146–152:** cut the Zotero sentences to one ("a reference manager such as Zotero exports
  the same `.bib` format"); reader B stopped there.
- **L197–207** (150 words, five facts): story for "pbge"; the rest as a three-item list
  (the company's name needs its own `company:` field; a single-page render with `keep-typ`
  leaves files to delete; only Quarto's own partial names are accepted). The journal
  template keeps its closing sentence.
- L95: "checked on 2026-11-18" out of the prose.

**Page fit**

| Unit | Now | Fix |
|---|---|---|
| `tbl-wp-vocab` (L77–89) | 1.00 (1.38 at 19 px, split) | 9 → 6 rows, two columns (Part; Quarto calls it): sections, an equation, a table or figure, citations, a citation style (with "`citeproc: true` for the PDF" in the same cell), a house look. The reference-manager and journal rows go to the text, where both already are; the checks go to the list at L109–113 |
| Paper prompt (L101) | 0.76 (1.13, split); page 5 is 78% blank | two turns, below; and a 30-word paragraph between the heading "The paper" and the box, saying what the prompt will do (reader A's request for every long prompt) |
| `tbl-wp-refs` (L135–144) | 0.72 | three columns: Key, Year, Cited by; the DOIs are in the project's `references.bib` and in Further reading. If still over, cards |
| Pitfall (L154) | 0.72 | the table above |
| Page 7, 46% blank | references prompt 0.59 | within budget; move L117–119 to end on the box |

**Trimmed prompt (L101), turn 1:**

```default
Create whitepaper.qmd, a short technical white paper for clients and investors, from outputs/ only: numbered sections (Introduction, Data, Method, Results, Limitations, Conclusion), the abstract in the body, not the YAML, ROC AUC defined as a numbered equation, a results table and the ROC figure, each referred to with @eq-, @tbl- and @fig-, `fig-format: svg` for the PDF, and a guard on every sentence whose wording depends on the results. Formats html, typst and docx (the existing reference document). Render it and check that no cross-reference shows "??".
```

Turn 2: `Add whitepaper.qmd to the site's render list and to the home page's listing, with a description. Render the site and list its pages.`

**Other:** glossary: `CSL`, `template partial` exist; propose `DOI`. Landing page:
nothing. **Do not change:** the references prompt (L123), the checker prompt (L175) and the
template prompt (L193); "cite what you have read"; "Test it once on a deliberately broken
copy" (L180–181); the computed counts at L91–93.

---

## Chapter 14, `parameters.qmd`

**Budget:** 1,854 → 2,150. **Aim:** reader B: "the chapter I bought the book for; the
shortest in Part III; never shows the update." Give the update the weight; shrink the rest.

**Cold open (replaces L42–52; paste):**

> Much of what an organisation publishes is the same document with different numbers: the
> monthly update for investors, one report per customer, region or team. Built by hand,
> each copy starts as last month's file, and each is a chance to leave one of last month's
> figures in it. Built from one source with a parameter, a value given when the document
> is rendered, each copy is the same tested document run on a different value, and a
> script can make every one of them and check it.

(84 words; "parameter" in roman here, italic at its definition in §14.1.) Then ≤ 40 words:
the chapter makes Acme's monthly update and a report per customer segment; the update's
business figures are synthetic and say so on every number.

**Illustration (after the cold open):**

```markdown
::: {.story .illustration}
A founder writes this month's update the usual way: open last month's, save it under a new
name, change the figures. Revenue, changed. Customers, changed. The sentence in the third
paragraph that says the month was the best so far is not a figure, so it is not changed.
It goes to every investor. Nobody lied, and nothing in the file was able to object.
:::
```

**Payoff (after the opener):** two stacked crops, `eval-update-a.png` above
`eval-update-b.png`: the headline block of the update's HTML for two consecutive months,
at phone width. Step `update`, rendering with `-P month:` for the last two months of
`data/synthetic_business.csv`. The crops must show the "synthetic" labels.

**Predict (think, in §14.2 after L118–122):** the `update` step also writes
`eval-update-sentences.json`: the update's sentences for each of the two months. The
chapter reads it, guards that both months are in `months` and that at least one sentence
is identical and one differs, and asks: "Between these two months, which sentences should
differ: the figures, the change from the month before, the release that was live? Which
must not?" Answer: the count of differing sentences, in words, and the one whose wording
(not only its number) changed, printed from the JSON; "the 'synthetic' label and the
method note must be identical: if they differ, a parameter leaked into text it should not
reach."

**New, ≤ 150 words, in §14.2 (reader B's change 2):** show the mechanism once, from the
checkpoint's `update.qmd`, printed by a cell (never retyped): the parameters cell (the
chapter's `parameters()` already finds it), and the lines that choose "up" or "down" with
their guard, each ≤ 10 lines. Then the sentence they produce for one month, from the JSON.

**The educator's case (L171–188): stays, shortened and marked optional.** Moving it to the
afterword would cross into D4's file, orphan `@sec-params-feedback` (used by `at-work.qmd`
64 and Appendix E 98–100) and take a tested prompt out of its checkpoint's chapter. So:
heading "For teachers: a sheet per section (optional)", same ID; the prompt unchanged;
prose cut from 130 to about 70 words (keep the personal-data rule and "render the real one
yourself"). It moves below the catch-up and Try it, so the chapter's main line ends on the
update. The lead may still prefer the move; say so in the report.

**Walls and density**

- **§14.1 opens on a bare table (L77–85).** Put L87–94 first, as two short paragraphs with
  the one command, then the table.
- **L96–104** (120 words, two rules): two cards, "Validate the value" and "Let code choose
  the words", ≤ 45 words each. Keep "A guard that repeats the comparison that chose the
  word can never fail, and protects nothing" as the sentence after them.
- **Pitfall L124–131** → two sentences: "The update is not in the site's `render` list, and
  should not be: it is not a public page. So Quarto renders it beside its source, not in
  `_site/`, and the batch script moves each file into `reports/`."
- **Pitfall L163–169** → table "Met while testing the batch": the PDF check for "18-29"
  failed | the PDF returns a soft hyphen; normalise dashes before comparing.
  Self-contained HTML is far larger than the PDF | send the PDF.

**Page fit**

| Unit | Now | Fix |
|---|---|---|
| Update prompt (L110) | 0.70 (1.00 at 19 px, split); page 4 is 38% blank | two turns. Turn 1: "Add papermill with `uv add papermill`, then create update.qmd, a monthly investor update parameterised by `month` (a cell tagged `parameters` whose default is "latest", meaning the last month in data/synthetic_business.csv): that month's business figures, each labelled synthetic, and the release live that month with its real model metrics from outputs/. Stop with a clear message if the month is not in the data. Formats html, docx and typst; render it for 2026-06 with `-P month:2026-06` and tell me where the files went." Turn 2: "In update.qmd, add the change from the month before, its wording chosen by code from the printed numbers and guarded; the first month says there is no earlier one. Render 2026-06 and the first month in the data, and show me both sentences." |
| `tbl-params-vocab` (L77–85) | 0.57 | two columns (Ask for; Quarto calls it), four rows; papermill leaves the table for the sentence that already explains it |

**Other:** glossary: `parameter`, `papermill` exist. Landing page: nothing. **Do not
change:** the setup cell's readers and guard (L19–36); the segment and batch prompts (L140,
L153) and the feedback prompt (L180); the computed count of files (L157–161), reader A's
best line; `FEW` and `MIN_STUDENTS` as settings, not typed numbers.

---

## Part IV page, `part-team.qmd`

**Budget:** 188 → 170. **Opening (replaces L3–6; paste):**

> The report builds on your machine. A colleague clones the repository and it does not: a
> package you installed by hand, a file you never committed. Then the client's data
> arrive, and they may not be shown to the agent that built everything so far. Neither is
> a failure of the method. They are the two things one person's computer hides: whether
> the work rebuilds anywhere, and what may leave the building. This part takes the Acme
> project to both.

(77 words.) Keep the two chapter summaries, ≤ 30 words each, and L17–18. This removes the
first of two "Work is rarely like that". **Do not change:** the roadmap cell.

---

## Chapter 15, `team.qmd`

**Budget:** 2,415 → 2,550. **Cold open:** keep L42–48 with two trims: start "The fast path
reviewed…" (a bare cross-reference cannot open the hook; put `(@sec-fast-pr)` at the
sentence's end) and set "Continuous integration" in roman, italic at §15.1. Result ≈ 105
words. Second paragraph L50–53: keep.

**Payoff (after the opener): the red check, as text.** No screenshot of GitHub: those runs
were not made (L232–237), and a picture of one would be staged. The `red` step copies
checkpoint 20, breaks the condition of the home page's guard, runs `uv run quarto render`
and writes the last lines of the failed render to `eval-red-build.json`. The chapter
prints them in a transcript block (≤ 10 lines), guarded to contain "ClaimError" and the
sentence. Label it "What a red build says"; caption that it is the render step's output,
run locally.

**D5-b, spot the error (new Try it in §15.2, after L110–114):** a cell takes the two
releases with the highest and second-highest `recall_top10` from `ev.metrics()` (`best`,
`rival`), prints the pull request's one changed line, "`best` reaches [the rival's recall]
of subscribers by calling a tenth of the list", and beside it a two-row table of both
releases' `recall_top10` from the file. `text_holds`: the two recalls differ as printed
(`ev.percent`), and "a tenth" holds (`S["top_share"]`, as `slides.qmd` 19–20). Text: "A
pull request changes one sentence of the model card. Its description says 'wording only'.
Review it against `outputs/metrics.csv`." Done when: "you can say which figure is wrong,
whose it is, and which of the three checks found it." Hand the lead the answer cell for
Appendix E: both values, the difference, and "correctness: one number traced to its
source".

**Think (at L156, before the red-build prompt):** "You are about to break a guard on
purpose. Before you push: which step of `check.yml` will go red, and what will the log
name: a file, a line, or a sentence?" Answer: "The render step, the third of
`{python} WORD[len(runs)]`: the results still compute and the tests still pass, because
neither reads prose. The log names the sentence, since a `claim` quotes it. If the tests
went red instead, the change broke more than a sentence."

**Story (replaces the first half of the pitfall, L224–227):**

```markdown
::: story
<!-- source: book/chapters/team.qmd lines 225–227 at 651db10 ("a first comment said 06:00
UTC was 07:00 in London in winter; it is 06:00, and 07:00 in summer. The agent caught it") -->
The schedule's first comment said that 06:00 UTC is 07:00 in London in winter. It is 06:00;
it is 07:00 in summer. The agent caught its own slip. A reviewer skimming a comment in a
YAML file might not have. Check any time arithmetic an agent writes.
:::
```

**Walls and density**

- **L124–130:** keep "ask for the versions to be looked up"; the `uv` incident becomes one
  clause ("a prompt that said only 'uv' got that day's newest").
- **L142–148** (merge against squash; both readers stopped): to two sentences. "Merge the
  first pull request with a merge commit, as above, so the second shows only the workflow."
- **L196–197:** "in the test run, a version of the prompt…" → "say so in the prompt:
  unprompted, an agent may give it to the whole workflow."
- **"What was not tested" (L232–237): remove the section.** One sentence at the end of
  §15.4, in a `practice` box: "For this edition the check workflow was run on a local
  runner (act), green and then red; the runs that need GitHub (publishing, the schedule,
  branch protection) were checked against GitHub's documentation, not run." The full
  account goes to the author's report for Appendix H (the lead's file). Reader B: the
  heading "deflates the title"; the honesty stays, the heading goes.
- "(checked …)" at L150–152, L181–182, L200–201, L218, L228: keep the fact, drop the
  inline date; `@sec-facts` carries it.

**Page fit**

| Unit | Now | Fix |
|---|---|---|
| `tbl-team-vocab` (L77–87) | 0.85 (1.11 at 19 px, split) | two columns (Ask for; GitHub Actions calls it), seven rows of ≤ 55 characters: drop the Check column (the Try it's done text checks) and the trigger list ("`on:` a trigger, such as `pull_request`") |
| Team-rules prompt (L101) | 0.76 (1.10, split); page 4 is 59% blank | two turns (§3.4). Turn 1, rules: the text up to "…report what you could not verify.", then "Do this on a new branch `team-rules` and commit it." Turn 2, template: "Create .github/pull_request_template.md: the three checks (scope, correctness, rebuild) as a checklist, saying what to look at for each in this project, and a line asking which agent made the change and what it did not verify. Commit it on `team-rules`." |
| Page 11, 42% blank | heading with the schedule prompt | open §15.6 with one sentence before the box: what the workflow will do |

**Other:** glossary: all seven terms of the table exist except `trigger`; propose it. Facts:
none new. Landing page: nothing. **Do not change:** the setup cell's guards (L31–34); the
check, red, publish and monthly prompts (L120, L161, L189, L210); "A check that has never
failed has not been tested."; "An agent told to make a failing step pass has two routes…
and only one is right."; the cron explanation's computed values.

---

## Chapter 16, `at-work.qmd`

**Budget:** 1,367 → 1,650. **Aim:** a scene, a diagram, one short grid for the 1.61-page
table, and the book's start-up case told once, here.

**Cold open (replaces L15–20; paste):**

> A render fails. You do what you have done all through this book: copy the error and hand
> it to the agent. The agent reads it, reads the file it points to, and fixes the cell.
> Only afterwards do you look at what the error said. It quoted the row that broke the
> code, and the row was a customer's: a name, an account, a balance. They have left your
> computer, and no command brings them back. Until now every file in this book was public.
> At work, most are not.

(84 words.) Then ≤ 40 words from L17–19: none of this changes the method; it changes what
an agent may see, which agent, and how its traffic leaves the building.

**Illustration (in §16.2, before the four habits):**

```markdown
::: {.story .illustration}
Nobody pasted the file. The analyst asked for a chart of monthly totals and named only the
summary table. To write a test, the agent listed the folder, found the full export beside
it and opened the first rows to learn the columns. Every step was reasonable, and each was
shown before it ran. The rows were in the conversation before anyone thought to say no.
:::
```

**Figure (new; chapter has none): `media/diagrams/may-this-file.svg`**, portrait, 700 px,
text ≥ 19 px, h/w ≤ 1.25, class `on-light`: three questions in order. Is the file public,
or yours to share? Is this agent, on this plan, approved for it? If not: build on a
synthetic stand-in, and render the real file yourself. Words only, no vendor names. Then
`make media STEPS="diagrams"`; tell the lead, who runs `media_es.py`. Place at the head of
§16.2.

**Think (after the figure):** "A colleague says: 'I never paste confidential data into the
agent, so we are fine.' Using the diagram, what has that rule missed?" Answer: "Pasting is
one route of three. An agent also reads files it finds, and the output of commands it
runs, an error message included. The diagram asks about the file and the plan, not about
your intentions: a confidential file in the agent's folder is one `ls` from the
conversation. Keep it out until the agent's work is done."

**Try it (end of §16.2, no installation):** "Take one file you work with. Answer the
diagram's three questions for it, and write the header row of its synthetic stand-in."
Done when: "you can name the plan you are on, and your stand-in has the real file's
columns and none of its rows."

**The vendor table (L37–47): 1.61 pages, split over three, 2.23 at 19 px.** Replace with a
grid of three columns, cell text ≤ 350 characters, and one sentence pointing to Appendix K
for the vendors' wording:

| Plan | Trains on it? | Kept |
|---|---|---|
| Claude, personal plans | if your setting allows | 5 years, or 30 days |
| Claude, company plans and API | not unless you opt in | 30 days |
| OpenAI API | not unless you opt in | up to 30 days |
| ChatGPT business plans | not by default | (see Appendix K) |
| Antigravity | yes; you can opt out | (see Appendix K) |

Every cell above paraphrases an existing long entry and is **not to be typed into the
chapter**: each comes from a new short `facts.yml` entry, printed with `fact()`. Codex
(the policy follows how you sign in) and OpenCode (a connected provider's terms apply)
become two sentences under the grid, from the existing entries.

**Facts the lead must add** (each with `_es`, `url`, `checked`; open the page first):

| New key | Short text to confirm | Source to open |
|---|---|---|
| `data.short.anthropic_consumer_trains`, `_kept` | trains if the privacy setting allows; five years with it, thirty days without | https://code.claude.com/docs/en/data-usage |
| `data.short.anthropic_commercial_trains`, `_kept` | not unless the customer opts in; thirty days by default | same, and https://code.claude.com/docs/en/zero-data-retention |
| `data.short.openai_api_trains`, `_kept` | not unless you opt in; abuse logs up to thirty days | https://developers.openai.com/api/docs/guides/your-data |
| `data.short.openai_business_trains`, `_kept` | not by default; **retention is not in the existing entry: find it or print "set by the workspace"** | https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security |
| `data.short.antigravity_trains`, `_kept` | used to improve products, reviewable by staff, opt-out in settings; **retention not in the existing entry** | https://antigravity.google/terms |

A column "Opt-out?" (plan §3.4) is folded into "Trains on it?" to keep three columns.

**Walls and density**

- **L93–107** (proxies; both readers stopped): keep `tbl-at-work-proxy` (within budget);
  cut L104–107 to "If a download still fails, ask IT to allow the hosts the tools reach,
  rather than turning certificate checks off." Dates out of the prose and caption.
- **§16.6 (L119–132) is the one home of the start-up case.** Rewrite its first paragraph
  as the close of the Acme thread, ≤ 110 words: what the two-person company now has (a
  report, a card, a deck, a site, a paper, an update that renders itself, a build that
  goes red on a false sentence), what it did not build this way (the pitch deck, the
  marketing site), with @sec-wrong-tool for the list. Keep L127–132 whole (reader B's
  kind of paragraph). No outcome, meeting or investor's reply is invented.
- The second "Work is rarely like that" (L15) goes with the old opening.

**Page fit**

| Unit | Now | Fix |
|---|---|---|
| `tbl-at-work-data` | 1.61, split over 3 (2.23, over 4, at 19 px); page 2 is 46% blank | the grid above, same ID; caption ≤ 2 lines, the date from `checked()` |

**Other:** glossary: propose `managed settings`, `stand-in (synthetic)`; `proxy` exists.
Landing page: nothing quoted from this file. **Do not change:** the four habits (L60–69);
the pitfall at L71–76 ("'Do not paste it' is not enough…", reader B's best line); "I need
Quarto 1.10 and uv" (L88–89); `data.claude_local` at L51; section IDs (`#sec-at-work-flow`
is cited from Chapter 2, `#sec-at-work-startup` from the Chapter 1 pilot).

---

## Not verified (D3)

- I read all eight files line by line, except the setup cells of `white-papers.qmd` (L1–19)
  and `team.qmd` (L1–19), and Further reading lists past their first entries.
- Nothing was built, captured or measured. Whether each reshaped table meets 0.45 page,
  each split prompt 0.6, and each crop 9 px is for `make book-pages` and the author.
- T8: that removing the navbar's `background` reproduces the hidden logo is an inference
  from `sites.qmd` 213–217; the story itself says only what those lines record.
- The trimmed model-card prompt drops the nine section names; whether an agent still
  produces all nine from the citation alone is exactly what the dry run must show.
- The five short vendor facts paraphrase the existing long entries; two retention cells
  have no source in `facts.yml` yet. I opened none of the vendors' pages.
- Whether checkpoint 19's `update.qmd` has a separable "change from the month before"
  passage of ≤ 10 lines to print, and whether checkpoint 20's home page fails as described
  when its guard is broken locally.
- `ev.metrics()` rows for `recall_top10` exist for every release (I read `evaluation.py`,
  not the CSV); "rival" as the second-highest recall is my definition, not the deck's.

---

# D4: Part V and the afterword (`improve/d4-part5`)

Files: `book/part-3.qmd`, `chapters/08-water-question.qmd` (Ch 17), `10-prepare.qmd` (19),
`11-cluster.qmd` (20), `12-interpret.qmd` (21), `13-causation.qmd` (22),
`14-publish-many.qmd` (23), `exercises-water.qmd`, `afterword.qmd`. Chapter 18 is the pilot;
these briefs assume its cold open (Tunja's 2017 infant mortality) and ledger 2. Line numbers
are at `improve/c-pilot`; page-fit figures are from the current `book/_book/pages/en.md`
(figure budget 0.7; images capped at 55vh).

**Rules for every D4 chapter.**

- The council is "a municipal council", never Tunja's. Tunja is the analyst's case.
- The ledger is `::: {.cards .ledger title="Tunja so far"}`, placed before the Summary, cards
  of ≤ 25 words, every value inline code. Each ledger's words that depend on data get a
  `text_holds`.
- Water prompts are not reworded (`scripts/check_prompt_values.py` reads them). The only
  prompt questions are the three 0.64-page prompts of Chapter 23 (lead decision 1 below).
- "(checked …)" stamps leave the prose and captions; Further reading keeps its dates.
- Keep every section ID. The landing page links `14-publish-many.html#sec-water-report`,
  `#sec-water-website`, `#sec-water-dashboard` (`ebook/_source.py` 177–183) and
  `chapter("11-cluster")` (`ebook/index.qmd` 159), and reads the Part V page's title
  (`index.qmd` 57). No sentence of these files is quoted by the landing page.
- Glossary: no new terms; `confounder`, `ecological fallacy`, `selection on the outcome`,
  `difference-in-differences`, `bootstrap`, `zone-year`, `municipality-year` exist.

## Part V page, `part-3.qmd` (366 → 380 words)

Keep paragraph 1 (L16–21): both cold readers praised it. In paragraph 2, after "a municipal
council, which needs slides" (L27–28), add: "When the slides end, someone on that council
will ask whether it is the water. This part is about what you can honestly answer." L31–32
becomes "finds where the data are empty or misleading, through one municipality, Tunja"
(Chapter 17 now names it). The roadmap picture is capped (1400 × 2120, shown 311 px wide);
the lead has ruled out a redraw, so nothing to do. Do not change the setup cell or the list.

## Chapter 17, `08-water-question.qmd` (3,576 → 3,500)

**Aim:** open on the reader's audience, not on two typed figures; name Tunja; thin the
acronyms and the Saber 11 arithmetic that stopped reader A.

**Cold open (replaces L74–78; paste).**

> When your slides end, someone on the council will ask the question the whole room is
> thinking: so is it the water? They will mean their own town and their own children, and
> they will want a yes or a no. You will have a table of scores, groups that an algorithm
> found, and three outcomes compared between them. Whether any of that can answer the
> question, and what you may honestly say instead, is settled long before the last slide: by
> what the score measures, by what one row of the table is, and by the rules you give the
> agent before it writes a line. This chapter settles those three.

(110 words, no numbers.) L74–78 becomes paragraph 2, unchanged in its figures (they are
cited, `@tbl-irca-bands`), then L80–84 with "*Part II's*" kept plain.

**Illustration (I4), in §17.1 in place of L115–116's "both will be tempted…" sentence.**

```markdown
::: {.story .illustration}
A council meeting, in any town. The analyst shows a chart in which places with riskier water
record more infant deaths. A member asks whether fixing the water would save those children.
The analyst says the chart cannot tell. "Then why show it?" The rest of this part is the
answer: what the chart can say, and how to say it.
:::
```

**Tunja, named.** After L205 add two sentences: this part follows one municipality through
every step, Tunja, the capital of Boyacá department, code `15001`; Chapter 18 looks at its
rows. New in the setup cell: `tj = raw[raw["divipola"] == "15001"]`,
`text_holds(tj["municipio"].eq("TUNJA").all() and tj["department_capital"].eq(1).all(), "Tunja")`.

**Ledger 1.**

```markdown
::: {.cards .ledger title="Tunja so far"}
On the table
: code `15001`: `{python} len(tj)` rows, `{python} WORD[tj["zone"].nunique()]` zones over
  `{python} WORD[tj["year"].nunique()]` years.

Checked
: nothing yet. Its values are as published.

What may be said
: nothing: no value has been read against the README's caveats.
:::
```

**Pause and think:** keep both (L207–214, L276–283).

**Walls and density.**

- §17.3 (L161–175) moves after §17.5, as a subsection of the outcomes, and loses the
  scoring arithmetic (L166–169): keep "scored from 0 to 500, set so that years can be
  compared"; the ICFES citation stays in Further reading. Keep L171–175 (what an average
  covers).
- §17.4 list (L185–192): plain name first, acronym second ("the national health institute,
  INS"), one line each.
- L232–237 (IPM, MDM, SGP): fold each definition into its table row's "measures" text and
  cut the paragraph.
- L239–242 and L264–269 say the same thing twice: keep L264–269.

**Page fit.**

| Unit | Now | Fix |
|---|---|---|
| `tbl-water-features` (L244–255) | 1.07 pages, split over 3 | `var_table()` prints two columns (Variable and what it measures; Level and years), no code names, sources in one sentence after the tables. Two tables: water and government (5 rows, keeps `#tbl-water-features`), people and place (4 rows, new `#tbl-water-features-place`). The guard at L57–59 stays |
| `tbl-water-outcomes` (L257–262) | 0.49 | the same two columns; caption one sentence |
| `tbl-irca-bands` (L129–137) | 0.50 | caption to "The IRCA risk bands (Resolución 2115, art. 15) and where the 2023 national figures fall (*INCA 2023*, Tabla 4)."; full citation already in Further reading |
| Pitfall (L151–159) | 0.51; page 4 35% blank | ≤ 80 words: the "30 of 30 … only 5" check becomes a sentence of prose before the box |
| Try it (L392–406) | 0.66 | the tab, `git status`, `git add` and commit steps become a `::: {.you}` box before it; done text ≤ 35 words; L404–405 becomes prose after the box |

**Do not change:** the three prompts (L341, L359, L378); `FEATURE_ROWS`/`OUTCOME_ROWS`
guards; "An empty IRCA is unknown, never safe and never zero" (L212–213); `fig-compute-once`;
the why box on `idf`.

## Chapter 19, `10-prepare.qmd` (2,940 → 2,850)

**Cold open (replaces L81–86; paste).** All values exist: `A.LAST_YEAR`, `share_raw`,
`diff` (L69–75), guarded at L76–78.

> Tunja stands high in the Andes; Cartagena lies on the Caribbean coast. Put their head
> towns side by side in the water table for `{python} A.LAST_YEAR` and ask how far apart they
> are. In the table's own units, the answer is nearly all altitude:
> `{python} f"{share_raw['altitude_m']:.0%}"` of the distance between the two rows is metres
> of height, and a `{python} f"{diff['water_coverage']:.0f}"`-point gap in piped water hardly
> registers. A clustering algorithm sees nothing but such distances. So before it runs,
> someone decides which rows it sees, which numbers, on what scale, and what stands in for a
> number that is missing. Those decisions are preparation, and each has a price.

"Preparation" is no longer italic here; italicise it at L104's first use if wanted. L240–247
then refers back ("the two rows that opened the chapter") and loses its first sentence.

**The wall, L106–131 → one Tunja row before and after.** Each of the four steps shrinks to
two sentences (what, and why). After them, a computed table, new `#tbl-tunja-steps`, three
columns (Step; Tunja urban; Tunja rural) for `A.LAST_YEAR`, four rows: as published (zone
coverage empty; the municipal total); transform (takes the total, flagged; unchanged);
impute (nothing to fill; the rural median of its year, flagged); standardise (each row's
`z_water_coverage`). New variables: the two raw rows from
`raw[(raw.divipola == "15001") & (raw.year == A.LAST_YEAR)]` (`water_coverage`,
`water_coverage_total`) and the two rows of `tjp` (L32) for that year (`water_coverage`,
flags, `z_water_coverage`); guard that the raw zone values are missing and the flags are 1.
The capital-share evidence (L118–122) moves to one sentence under the table. The z-score
formula (L133) stays, with L135–138 as its legend.

**Ledger 3.**

```markdown
::: {.cards .ledger title="Tunja so far"}
Kept
: all `{python} n_window` zone-years, `{python} A.FIRST_YEAR`–`{python} A.LAST_YEAR`.

Filled, and flagged
: `{python} tj_from_total` urban rows took the municipal total for coverage;
  `{python} tj_imputed` rural rows, their year's rural median.

Not flagged
: the 0 reported for `{python} tj_zero[0]`, kept as published.

What may be said
: the same facts, on the scale every place shares. Its rural coverage is now a guess.
:::
```

(`n_window`, `tj_from_total`, `tj_imputed`, `tj_zero`: L34–37, guarded at L38.)

**Pause and think:** keep both (L189–198, L265–273).

**Page fit.**

| Unit | Now | Fix |
|---|---|---|
| `tbl-two-rows` (L249–263) | 0.56; page 8 42% blank | caption to one sentence ("Tunja's and Cartagena's urban zones in the last year: their difference on each feature and its share of their squared distance, raw and in z-scores."); the "Difference" column loses its units (they are in @tbl-water-features); if still over, keep the five largest rows and say so |
| Why box (L140–148) | 0.51 | ≤ 80 words: drop "Two reasons" framing and the last sentence, which moves to the text |
| Practice (L275–284) | 0.48 | ≤ 80 words: the definition of r moves to the sentence before the box |

**Do not change:** both prompts (L292, L312; checked values); the annotated code (L323–340);
`tbl-prepare-counts`; `fig-wat-scale` and its guard; "the clusters would be climate zones"
(L233), reader A's best line.

## Chapter 20, `11-cluster.qmd` (4,285 → 4,250)

**Cold open:** keep L114–120, with "*kinds*" plain. Replace paragraph 2 (L122–124, "If the
mathematics sounds daunting…") with: "You will not write this algorithm. The normal route
copies the finished script (@sec-routes), and your work is to check what it chose: how many
kinds, by what rule, and how close the call was."

**Formula placement.** L152–162: keep the sentence defining inertia in words; move the
formula and its legend (L155–159) into a `::: why` box after `fig-kmeans-panels`. L266–270:
keep the plain agreement figure; the adjusted Rand index gets one clause.

**Predict (new Pause and think, before §20.4, L391).** The reveal is `tj_text` (L58–63), so
cut it from L428, which keeps only Tunja's altitude.

Question: "Tunja's rural water scored in the high-risk band for years, and its urban water
never did (@sec-tunja). k-means has now placed all `{python} len(tj_cl)` of its prepared
zone-years. Before you read on: do its two zones fall in the same cluster?"

Answer: "`{python} tj_text[0].upper() + tj_text[1:]`. k-means places a row by all
`{python} WORD[n_feat]` features at once, and several of them belong to the municipality,
not the zone, so both of Tunja's rows carry the same values for them
(@sec-water-features). @sec-tunja-kind works out which features decided it."

The second sentence explains a shared cluster: add
`text_holds(tj_in["urban"] == tj_in["rural"], "Tunja's zones sharing a cluster")`.

**Ledger 4.**

```markdown
::: {.cards .ledger title="Tunja so far"}
Grouped
: `{python} tj_text`.

How firm
: k = `{python} k` by a written rule and a narrow margin; the kinds overlap.

What may be said
: which kind each zone-year was grouped with. Not why, and not yet what the kind is.
:::
```

**Page fit.**

| Unit | Now | Fix |
|---|---|---|
| `tbl-k-selection` (L278–288) | 0.55 | three columns (k; one more cluster cuts; verdict): the silhouette is in `fig-k-selection` and the text. Shorter verdicts ("excluded", "silhouette too low", "one more still cuts enough", "chosen", "passes, larger"), with the guard at L87–88 updated. Caption one sentence |
| Pitfall (L304–312) | 0.48; page 8 51% blank | ≤ 80 words: end at "do not force a number of clusters to make a nicer story"; the last sentence is already key idea 2 |
| Try it (L519–532) | 0.52; page 17 44% blank | done text ≤ 30 words ("you can say what k is and why, and `clusters.html` shows the elbow, the silhouette and the PCA picture") |

No wall is listed for this chapter now. **Do not change:** the three scene blocks and their
live-link cards (`check_scenes.py`, `check_live_links.py`; `#sec-kmeans-steps`,
`#fig-cloud-3d`, `#sec-relief`); the GIFs' captions and alt texts; the four prompts
(L452, L469, L490, L507); the think boxes at L314 and L477 ("a useful summary, not a
discovery"); the guards at L43–46.

## Chapter 21, `12-interpret.qmd` (4,991 → 4,800)

**Cold open:** keep L226–231 (reader B: "opening good").

**The think at L339–347** asked the reader to predict what Chapter 20 now reveals. Reword
the question: "@sec-relief showed Tunja's rural zone-years in the same cluster as its head
town, though its rural water scored far worse. Before reading on: which features could have
carried it there?" Keep the answer, trimmed to ≤ 80 words, starting "The ones it shares with
its head town."

**Walls.**

- L502–516 (two reasons the highest mortality is not where the water is worst): a two-item
  list, small numbers and what is missing, ≤ 55 words each; "From 2017 the series looks
  like…" shortens to "the series holds no zeros, so a blank may be a recorded zero".
- L358–367: with the table reduced (below), two sentences go.

**Ledger 5.**

```markdown
::: {.cards .ledger title="Tunja so far"}
Its kind
: cluster `{python} tj_c`, "`{python} names[tj_c]`", for all `{python} len(tjc)` zone-years.

Its rural water
: never in the no-risk band; medium in `{python} NUM[tj_medium]` of
  `{python} NUM[len(tjr)]` years.

What may be said
: the kind's name describes the kind. For Tunja, quote Tunja's rows.
:::
```

(`tj_c`, `tjc`, `tjr`, `tj_medium`: L163–174, already guarded.)

**Page fit.**

| Unit | Now | Fix |
|---|---|---|
| `tbl-tunja-place` (L369–389) | 0.74 | three rows only: squared distance over its own features, over the shared ones, over all nine; columns Centre `tj_c`, Centre `rural_c`. The per-feature z-scores go; the text (L361–367) already argues from the sums. Caption one sentence |
| `tbl-names` (L317–325) | 0.50 | three columns: "1 · kind", zone-years, median IRCA; municipalities move to a sentence. Caption one sentence, keeping "utility-supplied" |
| `fig-wat-outcomes` (L401–432) | 0.73; 894 × 1602; page 9 68% blank | `grid(len(ocols), square=True)`, the legend in the fourth cell (`*spare`, `axis("off")` where there is none in HTML). Caption: "Median outcome by cluster and year, each in its comparable years. Descriptive only: not causal effects of water safety." Years move to the text (L398–399 has them). The alt text is shared by both editions: say "Three small line charts, one per outcome" with no layout; keep the guards at L137–147 |
| `fig-compare`, EPUB cell (L592–607) | 0.71; 894 × 1444 | `grid(3, square=True)`; the fourth cell holds the note "box: middle half; whiskers: middle 90%". Alt text: "Three box-plot panels in a two-by-two grid…", descriptions unchanged; keep `text_holds` at L597 |
| Try it (L678–691) | 0.49 | done text ≤ 30 words |

**Do not change:** `name_rule()`'s description (L308–315) and both build prompts (L639, L645:
their thresholds are checked); `fig-wat-heatmap` and `fig-wat-outcome-heatmap`; "A label
describes a kind; to say anything about one member, go back to its rows" (L391–392); the
think at L493–500.

## Chapter 22, `13-causation.qmd` (3,785 → 3,750)

**Cold open:** keep L139–142. Paragraph 2 (L144–148) lost reader A; replace with: "The
chapter makes one more comparison, inside each kind of place, and then spends most of its
length on a single sentence: the one you may put in front of a council. The sentence a reader
quotes is the one you publish."

**Story (T12), after the first reason, L275–279.**

```markdown
::: story
<!-- source: book/PLAN.md lines 533–534 (§12, item 2: "Chapter 13's range-restriction
argument, which its own numbers contradicted"; this file was Chapter 13 then). The second
half restates lines 275–279, guarded at lines 71–72. -->
An early draft of this chapter explained the small values by range alone: the clusters were
formed partly on IRCA, so it varies less inside them, and a narrow range weakens a
correlation. A review set that beside the chapter's own table. The largest value sat where
IRCA varies little, and the one nearest zero where it varies most. The argument was tidy,
and the numbers printed beside it contradicted it.
:::
```

**L275–296 (range, chance, unit):** a numbered list, three items of ≤ 50 words, each ending
in what it forbids ("so the four cannot be ranked"). The bootstrap's mechanics (L281–283)
become a `::: why` box of ≤ 70 words.

**L315–341 (the paths):** an ordered list whose items start with the diagram's own node
names, in the diagram's reading order: 1 poverty and rurality; 2 health-service access;
3 reporting quality and blank rates; 4 zone against municipality. The Tunja paragraph
(L325–330) follows item 4 unchanged. Numbering the arrows in
`media/diagrams/confounders.svg` to match is the lead's call (it also changes the Spanish
diagram); the list works without it.

**"What you may tell the council".** The wrong and honest sentences leave the think box
(L298–306) for body text, under a new `### What you may tell the council {#sec-tell-council}`
at the top of §22.3 (L373). Two block quotes, labelled Wrong and Honest, the inline code
unchanged (`kind[c_flat]`, `IM_YEARS`); then one sentence: "The honest version is longer, and
it is the only one of the two the data support." Reader A: "Nobody tells me what I can tell
the council." L296 ("It would be easy to read this as 'water does not matter'…") points
forward to it.

**Pause and think (replaces the one at L345–354; one box, not two).**

Question: "@tbl-problems lists blank rates left out, and small places' extreme rates. Find
each in @fig-confounders. Can it create a false link between water and infant deaths, hide
a real one, or both?"

Answer: "Blank rates sit on the reporting path, between real and recorded deaths. Which
places go blank may depend on the outcome itself, so they can push either way. Small
places' rates are on no arrow: they are noise, with no direction, so they can only blur a
real link, never create one. Several paths act at once and their sizes are unknown, which is
why a correlation cannot settle the question."

**Ledger 6.**

```markdown
::: {.cards .ledger title="Tunja so far"}
In this check
: `{python} NUM[len(tj_mean)]` municipality-years in cluster `{python} tj_c`, each with the
  mean IRCA of its two zones.

A value neither zone had
: in `{python} tj_yr`, `{python} f"{tj_mean[tj_yr]:.2f}"`: urban
  `{python} f"{tj_u[tj_yr]:.1f}"`, rural `{python} f"{tj_r[tj_yr]:.1f}"`.

What you may tell the council
: higher utility-supplied IRCA did not go with markedly higher recorded infant mortality
  within its kind. That does not show water has no effect.
:::
```

(L126–136.) The last card's "did not go with markedly higher" needs
`text_holds(abs(rho.loc[tj_c, "spearman_rho"]) < 0.2, …)`; L42 already holds it for every
cluster.

**Page fit.**

| Unit | Now | Fix |
|---|---|---|
| `fig-wat-within` (L224–250) | 0.71 | caption to "Median infant mortality by utility-supplied IRCA band within each cluster, 2017–2019 and 2021–2023 pooled. Descriptive only." The 20-row threshold moves to the text. The guard at L40 names the caption's years: keep them |
| `tbl-problems` (L358–366) | 0.57 | three columns: Problem; Here; Can it… ("create or hide" four times, "only hide" for noise), answering reader A's "all yes". Caption one sentence |

The plan's "split box (0.50)" is not in the current report.

**Do not change:** the four prompts (L400, L416, L424); `tbl-rho` and `tbl-within-spread`;
the pitfall with the fair and unfair titles (L387–392); the guards at L42–43, L71–72,
L97–100.

## Chapter 23, `14-publish-many.qmd` (3,577 → 3,700)

**Cold open:** keep L39–44.

**Payoff: the council's last slide**, in `::: payoff` after the opener. A new `council` step
in `book/media/capture/water_outputs.py` (which now shoots `#/3` at 1400 × 860): open
`slides.html#/5` ("What this does and does not show", `examples/water/slides.qmd` 104–111)
at a phone viewport, 390 × 844, device scale 3, and crop to the slide. Reveal.js scales the
slide to the width, so measure the bullets' rendered size and report it for `pagefit.yml`;
it must be ≥ 9 px. Save `media/figures/water-slides-last.png`, `#fig-water-last-slide`.
Caption: "The council deck's last slide. Rendered from `examples/water/slides.qmd`." Alt
text: the title and the bold line in words, no ρ values. No render in a book cell. L115–116
then refers to this figure; `fig-water-slides` stays.

**Story (T13), in §23.3, replacing L140–144** (that list of the book's EPUB problems is in
Appendix H already).

```markdown
::: story
<!-- source: book/styles/epub.css lines 98–103 (Apple Books does not draw positioned content
on the second page of a box that splits, "so a prompt there showed its label and an empty
panel") -->
In this book's own e-book, Apple Books drew one kind of box wrongly. Where a prompt box fell
across two pages, the second page showed its label and an empty panel: the text was in the
file, and the reader did not draw it. Two style rules fixed it. Nothing but turning the
pages in that reader would have found it, so open `report.epub` in the reader your readers
use.
:::
```

**Traps → tables (rule 4).**

- Pitfall L347–355: a two-column table (You see; Do), three rows: a grey rectangle for every
  municipality → reverse the rings (`load_geojson()` does); a page of
  `{python} f"{geo_mb:.1f}"` MB per year → frames update only `z`; a chart drawn twice →
  assign `fig = fig.add_vline(…)` and end the cell with `fig`. Fixes the 0.48 unit and the
  blank on page 22.
- Pitfall L369–377: ≤ 70 words; the four citations and their date go (the list is in
  Further reading, L425 ff., and `references.bib`).
- L247–248 (the timed test run): cut; Chapter 9 keeps its own. L255: stamp out.

**Ledger 7** must not give away the Try it at L283–294, whose model answer is in Appendix E
by design.

```markdown
::: {.cards .ledger title="Tunja so far"}
In every publication
: one kind, "`{python} names[tj_c]`", for `{python} len(tj_cl)` zone-years, labelled
  utility-supplied.

After `MAX_MISSING` = 1
: your prediction first; the computed answer is in @sec-answer-water.

What may be said
: what the council's last slide says: a description, and what it does not show.
:::
```

New in the setup cell: `from scripts import water as w`,
`tj_cl = w.res()["clusters"]` filtered to `15001`, `tj_c`, `names = w.names()`, with a
guard that Tunja has one cluster. The lead adds the resolved last card to Appendix E's
answer (lead decision 2).

**Page fit.**

| Unit | Now | Fix |
|---|---|---|
| Prompt, §23.5 (L237) | 0.64, budget 0.6; page 12 43% blank | lead decision 1 |
| Two dashboard prompts (L333, L341) | 0.64 each; page 18 56% blank | lead decision 1 |
| `tbl-water-deps` (L300–314) | 0.59 | three columns: Page; Reads `outputs/`; Writes. The `data/` column becomes the sentence at L316–317, which already says it; the guard at L33–35 stays |
| Try it, §23.6 (L283–294) | 0.53 | each step ≤ 15 words; "Undo" becomes a sentence after the box |
| Try it, §23.5 (L264–277) | 0.49 | done text: "the live address opens in a browser, with the report, the slides and the post" |
| `fig-water-report` | 0.66 (in budget), page 3 46% blank | move it after L87–89; recapture cropped to the title block and summary so its text is ≥ 9 px |
| `fig-water-whitepaper` | 0.68, capped; page 23 52% blank | crop to title and abstract (plan D3); new capture in the same script |
| `fig-water-post`, `fig-water-dashboard` | text far below 9 px at 340 px | recapture at a 390 px and a 700 px viewport, device scale 2 |

Report every capture's text size. **Do not change:** the YAML listings (L156–175); the think
boxes (L210, L257); "a loud failure is better than a quiet falsehood" (L192–193); the
catch-up boxes; the licence paragraph's content (L250–254).

## Exercises for the water analysis (2,101 → 2,200)

- **Numbering.** "Exercise III.n" → "Exercise V.n" in the eight headings and at L33 and
  L248. The Spanish twin already carries explicit IDs taken from the old English auto IDs
  (`{#exercise-iii.1-rules-environment-and-a-first-look .unnumbered}` and so on,
  `book-es/chapters/exercises-water.qmd` 37–165). Give the English headings those same IDs,
  so no ID changes in either edition; only the visible text does. Nothing else in `book/`,
  `book-es/`, `translation/` or `ebook/` refers to them.
- **Opening and D5-c.** Replace L26–29 with the puzzle, then two sentences on the three
  kinds of exercise. A cell prints three numbered sentences from `w.res()`: (1) the kind
  with the highest median utility-supplied IRCA, by name; (2) where recorded infant
  mortality was highest, with its years; (3) the plant: a true comparison of Saber 11
  between two named kinds, ending "because its water is less safe". Guards: the comparison
  in (3) holds in `outputs`, so only the verb is wrong; the planted index is a constant.
  "One of these three claims a cause. Which, and how would you rewrite it?"
- **Capstone, new Exercise V.9, no prompt:** "Write the council's last slide." Done when: at
  most five bullets; every number inline code from `outputs/`; the IRCA labelled
  utility-supplied; the rows and years compared are named; one sentence says what the
  comparison does not show; then compare with @fig-water-last-slide. ID
  `#exercise-v.9-the-councils-last-slide` (Spanish gets the same).
- **The wall (pages 12–14).** Each review question becomes a `::: think` with its answer
  (≤ 80 words; answers 2, 4, 7 and 9 need trimming), and the separate Answers section goes.
  Its ID, `#answers-to-the-review-questions`, has no inbound reference. Question 7 keeps its
  two draft titles.
- **Do not change:** the done texts and catch-up lines; the transfer tasks; the guards at
  L18–23.

## Afterword (3,998 → 3,800)

**Cold open:** keep L3–7.

- **Opening box (L9–20), 0.59, page 1 51% blank:** it "fits on a card", so make it three:
  `::: {.cards title="Prompt, Check, Publish"}` with Prompt, Check and Publish, ≤ 40 words
  each.
- **"What you can now do" (L34–58)** repeats the preface (reader B): three items per list,
  about −100 words. The metrics brief's promise also belongs in the preface (D1's brief).
- **The wall, L383–400 (design document).** A two-column table (You see; Do), three rows:
  "file not found" → paths are relative to `rfc/`, or import the package; rendered files in
  `rfc/` → `.gitignore`; alt text cannot be computed in a Python cell option → describe the
  chart without numbers. "Checks only you can do" keeps four sentences: the machine's name,
  run it twice and report direction and ratio, commit `results.json`, ask a reviewer about
  Alternatives.
- **L322–329 (investor update):** a three-item list: runway's definition; every render
  overwrites the last; the first month has no month before it.
- **One predict box** in the metrics brief, before L162. Question: "You remove the newest
  export and render again. Which sentence of the brief must change its words, not only its
  numbers, and what makes sure it does?" Answer: "The one saying whether the total rose or
  fell, and the month it names. Code chooses the word from the two totals at every render; a
  typed 'rose' would have survived the change and been wrong."
- **Prompts: no change.** The plan's "three long boxes → two turns each" measured whole
  boxes. With parts measured, no afterword prompt fails at any gating profile; the one
  remaining mark is page 16 (57% blank, pushed by the 0.59-page investor prompt, in budget).
  Move the confidentiality sentence (L301–302) below the prompt to fill it.
- **Do not change:** every `#sec-project-…` and `#sec-fresh-clone` ID (the preface's reading
  paths link to them); the fresh-clone test; the closing paragraph (L437–439); "Where next".

## Decisions for the lead

1. **Chapter 23's three 0.64-page prompts.** The §23.5 prompt cannot be dry-run without a
   GitHub push; the two dashboard prompts are optional, long and tested. I recommend a
   `pagefit.yml` exception for all three over rewording. Otherwise trim about 40 characters
   each and dry-run.
2. **Ledger 7's last card.** Chapter 23 withholds Tunja after the rebuild so the exercise
   keeps its answer. Appendix E (`e-checkpoints.qmd`, the lead's) should close the answer
   with the resolved card from its own variables (`tj_rural0`, `tj_c`, L32–33): the rural
   zone-years go, the urban ones stay in their cluster.
3. **Numbering the arrows of `confounders.svg`** to match Chapter 22's list (and the
   Spanish diagram), or leaving the list to carry the order.
4. **New table IDs** (`#tbl-water-features-place`, `#tbl-tunja-steps`), a new figure, a new
   section (`#sec-tell-council`), an exercise and the removal of the Answers section all
   change structure the Spanish edition must mirror: `pending.yml` for every D4 file.
5. **Appendix E needs from the D4 author** for D5-c: the cell, the planted index, and the
   honest rewrite of sentence 3.

## Not verified (D4)

- No build or measurement: every "fits" above is the §3.3 rule of thumb, not
  `make book-pages`.
- Lines 1–18 and several helper bodies of `12-interpret.qmd`'s setup cells, and the plotting
  code of all figure cells, were skimmed, not read line by line; prose, tables, prompts and
  guards were.
- The full text of prompts (cut at about 200 characters in my reads), so I propose no
  rewording of any.
- That `#/5` is the last slide of the rendered council deck (six slides by the source's
  headings), and the text size a 390 px capture gives.
- Whether `grid(…, square=True)` is drawn well with `fig-wat-outcomes`' shared legend; the
  cell's body was not read in full.
- T13's wording rests on a stylesheet comment only; "two style rules" is my reading of
  `epub.css` 102–103.
- Whether Saber 11 differs between two kinds in the direction D5-c's third sentence needs;
  the author picks the pair the data support and guards it.

---

# E: the appendices (`improve/e-appendices`)

One layout fixer, after D1–D4, then the lead. Files: `book/appendices/a-windows.qmd`,
`b-terminal.qmd`, `c-cheatsheet.qmd`, `d-troubleshooting.qmd`, `g-sources.qmd`,
`h-how-built.qmd`, `i-workshop.qmd`, `k-facts.qmd`; `e-checkpoints.qmd` is the lead's.
No wording is rewritten for engagement here: the appendices are looked up, not read. The
job is that no unit splits and none exceeds 0.45 page at phone 16 px, with every fix and
message kept. Line numbers are at `improve/c-pilot`.

## E.1 The rule for choosing a fix

- **A table whose second column is a sentence becomes `::: cards`**: a definition list,
  the term the thing looked up (a key, a message, a path), the definition what the table's
  other cells said, ≤ 80 words a card. The list may break between cards, so its length no
  longer matters. Cards have no caption: the caption's sentence becomes the line before
  the list, and its sources ("checked …") the line after.
- **A table of short cells splits by theme** into tables of ≤ 3 columns and about 350
  characters, each with its own `#tbl-…`.
- **No `.breakable`.** `epub.css` has no such class at this commit, and every table below
  fits one of the two fixes above, so none needs an exception in `pagefit.yml`.
- An ID that the text refers to must survive. A `cards` div cannot be a `@tbl-` target, so
  where a table with references becomes cards, put the ID on the section heading and
  change each reference to it (listed per table below).

## E.2 Unit by unit

### Appendix B (`b-terminal.qmd`)

| Unit | Now (phone 16 / 19) | Fix |
|---|---|---|
| `tbl-keys-symbols` (L26–43) | 1.42, 3 pages / 2.08 | cards, 14 of them. Term: the symbol and its name ("`` ` `` backtick (grave accent)"); definition: where you meet it. No reference uses the ID; drop it and the `tbl-colwidths` |
| `tbl-keys-basic` (L11–19) | 0.82 / 1.11 | cards, five. Term: the keys; definition: "what to know". The Apple source goes in a line after the list |
| `tbl-terminal-keys` (L61–71) | 0.84 / 1.18 | cards, seven. `03-setup.qmd` 185 refers to `@tbl-terminal-keys`: change it to `@sec-keys-terminal` (the heading, L55) |
| `tbl-keys-paths` (L107–114) | 0.49 | shorten two cells: "`~/first-report` is that folder inside it, from anywhere"; "relative: in the `data` folder of the folder you are in". Stays a table |
| Pitfall (L45–53) | 0.48 | two pitfalls: curly quotes and long dashes (L46–49); dead keys (L49–52) |
| Page 1 (46% blank), 3 (81%), 7 (71%) | pushed tables | gone once the three tables are cards |

`tbl-terminal-line` (L80–87) passes; leave it.

### Appendix C (`c-cheatsheet.qmd`)

| Unit | Now | Fix |
|---|---|---|
| `cb1`, front matter (L9–30) | 0.51 | two blocks. First: `title`, `author`, `date`, `lang` and `format:` with `html` (and its `format-links`), `docx` and `typst`. Second, introduced by "More formats go in the same list": `pptx`, `revealjs` with `output-file`, `epub` |
| `cb3`, dashboard (L55–77) | 0.58 | two blocks at the second `## Row`: the front matter, page and value-box row; then the chart row. Both stay `markdown` fences with `{{python}}` |
| `cb4`, website (L85–103) | 0.46 | cut the nested Downloads menu (L98–100) to one line of prose after the block: "a `menu:` under a navbar item makes a drop-down (@sec-london-website)" |
| `tbl-cheat-git` (L125–135) | 0.67 | split at L130/L131. **Look** (`#tbl-cheat-git`): `git init -b main`, `git status`, `git diff`, `git log --oneline`. **Record and undo** (new `#tbl-cheat-git-undo`): `git add .`, `git commit -m`, `git restore`. Trim "Does" cells to one clause |
| `tbl-cheat-commands` (L107–118) | 0.62; page 4 54% blank | split by tool. **uv** (new `#tbl-cheat-uv`): `uv init --bare`, `uv add`. **Quarto** (`#tbl-cheat-commands`): preview, render one file, render the project, publish, publish `--no-prompt`, `check jupyter` |

No chapter refers to either table by ID.

### Appendix D (`d-troubleshooting.qmd`)

Every table here is "message, then what to do": all five become cards, one list per
existing section, in the same order. Term: the message or symptom, as now (code in
backticks). Definition: cause, then fix. A sample, from L40:

```markdown
Typst PDF fails: `cannot parse length '60px'`
: Typst does not accept CSS pixels in image sizes: write `{height=60}` or `{width="30%"}`.
```

| Unit | Now (16 / 19) | Note |
|---|---|---|
| `tbl-trouble-render` (L35–46) | 1.55, 2 pages / 2.24 | eight cards; the YAML card (L38) is the longest: keep it under 80 words by pointing to "Reading an error" for the caret |
| `tbl-trouble-setup` (L10–21) | 1.06 / 1.31; page 1 47% blank | eight cards. L27 refers to `@tbl-trouble-setup`: give the heading at L8 the ID `#sec-trouble-setup` and refer to that |
| `tbl-trouble-publish` (L68–75) | 0.61 | four cards |
| `tbl-trouble-python` (L50–57) | 0.56 | four cards |
| `tbl-trouble-terminal` (L25–31) | 0.54 | three cards |

Chapter 1's new Try it (pilot) quotes messages from this appendix: keep each message's
text exactly. D-authors' "symptom / cause / fix" rows that do not fit their chapters land
here as new cards, under the section they belong to.

### Appendix E (`e-checkpoints.qmd`, lead)

| Unit | Now (16 / 19) | Fix |
|---|---|---|
| `tbl-checkpoints-eval` (L90–103) | 1.61, 3 pages / 2.28; page 6 89% blank | cards, ten. Term: the path; definitions: "Catch-up box: @sec-…" and what it holds |
| `tbl-checkpoints-water` (L75–88) | 1.06 / 1.46 | cards, ten, same fields |
| `tbl-checkpoints` (L66–73) | 0.66 / 1.01; page 2 61% blank | cards, four, same fields, so the three lists read alike |

Each caption's second sentence (water: "sources only: their catch-up copies the data";
evaluation: "their catch-up runs `scripts/evaluate.py` before rendering") becomes the line
before its list, under a small unnumbered heading (London; Water; Evaluation). No file
refers to the three IDs. `tbl-answer-water` (L147–154) passes.

### Appendix H (`h-how-built.qmd`)

| Unit | Now (16 / 19) | Fix |
|---|---|---|
| `tbl-epub-fixes` (L23–35) | 1.10, 3 pages / 1.44; page 2 72% blank | cards, nine. Term: the problem; definition: the fix. No reference uses the ID |
| `tbl-reading` (L56–63) | 0.58 | cards, four (term: the feature). No reference uses the ID (`index.qmd` 134 and 269 name `@tbl-reading-paths`, a different table) |

### Appendix I (`i-workshop.qmd`)

The two agenda tables are written by hand, with `[-@sec-…]` references; no cell prints
them.

| Unit | Now (16 / 19) | Fix |
|---|---|---|
| `tbl-agenda` (L20–34) | 1.12, 3 pages / 1.56; page 2 81% blank | split at the break. **Before the break** (`#tbl-agenda`): the "before" row to 1:05. **After the break** (new `#tbl-agenda-late`): 1:20 to the meal. Still over 350 characters each, so also fold the third column into the second ("London: `.md` to `.qmd`, formats (02) · [-@sec-compute]") and shorten the "before" row to "Setup and reading ([-@sec-assistant], [-@sec-setup], [-@sec-markdown]); optionally [-@sec-first-report]". Two columns: Time; Block, checkpoint and chapter |
| `tbl-agenda-water` (L36–48) | 0.80 / 1.09 | the same two-column form; split at the 4:20 break only if it still fails (new `#tbl-agenda-water-late`). The caption's second sentence (the 9:30 start) moves to the paragraph at L50 |

References to update: `i-workshop.qmd` 17 and `index.qmd` 290 name `@tbl-agenda` and
`@tbl-agenda-water`; add the new table or tables to both sentences (the D1 author is
rewriting that part of the preface: tell them).

### Appendix K (`k-facts.qmd`)

The cell at L34–47 already prints each fact as a paragraph because "a table of four
columns does not fit a phone"; do the same for prices.

| Unit | Now (16 / 19) | Fix |
|---|---|---|
| `tbl-prices` (L51–62) | 0.98, 2 pages / 1.39; page 6 78% blank | the cell prints `::: cards`, one card per model. Term: `r['model']`; definitions: the vendor's quoted `for` line, then "Input / output: … / … dollars per million tokens". The caption (`prices['caption']`, checked date) becomes a sentence before the list. `02-assistant.qmd` 168 refers to `@tbl-prices`: put `{#sec-prices}` on the heading at L49 and change the reference. `02-assistant.qmd` 29–31 reads the same rows and is unaffected |

`tbl-hosts-free` passes. The appendix is exempt from the wall measure.

### Appendices A and G (noted in the audit; same fixer)

- `a-windows.qmd` `tbl-windows-stuck` (L213–224; 0.81 / 1.05; page 12 48% blank) and
  `tbl-windows-stuck-ubuntu` (L226–235; 0.59): cards, eight and six, term "You see",
  definition "Do this". `d-troubleshooting.qmd` 5 links to `#sec-windows-stuck`, the
  heading, which stays. Page 11 (57% blank, pushed by `tbl-wsl-commands`): once the stuck
  tables are cards the section reflows; re-measure before touching that table.
- `g-sources.qmd` `tbl-photo-credits` (L27–36; 0.46, budget 0.45): it is 0.01 over and its six
  rows cannot shrink: list it in `pagefit.yml` with that reason. Its wall (pages 4–6, L38–75: three
  pages of source lists) needs a visual unit: set the water sources (L38–61) as cards, one
  per provider (term: the provider and dataset; definition: licence, URL, what the book
  takes from it). Do not change a credit, a licence or a URL.

## E.3 What must stay for the landing page

- `i-workshop.qmd` L3: the phrase "six-hour, hands-on workshop" (`ebook/_source.py`,
  `HOURS`), and its Spanish twin.
- Appendix A's title starts "Windows"; the last appendix is titled "Facts That Change".
- `facts.yml` keys `agents.claude_code_cost` and the four `agents.*_accounts` items, each
  with `text`, `checked` and `_es` twins (`book_fact()`, `assistant_cost()`,
  `assistant_accounts()`).
- `copyright.qmd`: "Checked with Quarto 1.10.20" (`checked_with()`).

## E.4 Stamps arriving from Chapters 2 and 4 (D7)

Form in the chapters: one line at the end of each section that states changing facts,
"Checked `{python} checked("…")`; sources in @sec-facts." Nothing else dated in the prose.
Form in Appendix K: unchanged; each fact is already a paragraph ending "Checked
YYYY-MM-DD, source."

For every stamp removed, the D1 author hands the lead: a proposed `facts.yml` key
(`section.item`), a `label`, the `text` exactly as the chapter worded the fact, the source
URL (and `also` URLs), and the date from the removed stamp. The lead adds the `_es` twins
and re-opens each URL. Stamps on documentation that is not a changing fact (a commands
reference, a manual) do not go to Appendix K: they stay in the chapter's Further reading,
where they already are.

**Lead: `copyright.qmd` L12–13 becomes false.** "…were checked on the dates given in the
text and will change" is quoted by `ebook/index.qmd` 102 and, as "se consultaron en las
fechas que da el texto y van a cambiar", by `ebook/es/index.qmd` 101 (`book-es/copyright.qmd`
15). Replace, in the same branch as D1, both books and both guards:

> Prices, versions, screens and plans described in this book were checked on the dates
> given in Appendix K and in each chapter's further reading, and will change.

New guard phrase: "were checked on the dates given in Appendix K". Write the appendix as
`@sec-facts` in the source only if the guard is then matched on the words before it.

## E.5 Production notes arriving in Appendix H

- **From Chapter 6** (how the Markdown animations were made: each step's right-hand pane
  is a real render, the sizes): a new bullet under "Media" (after L49), ≤ 60 words.
- **From Chapter 15** ("What was not tested") and the "not re-tested" notes (Chapter 9's
  Quarto 1.6.40 publish; Chapter 4's codespace on GitHub itself; prompts run in Claude
  Code only): a new section after "Reading the EPUB", `## What was not tested
  {.unnumbered #sec-not-tested}`, as cards. Term: the thing; definition: what was checked
  instead, and how a reader can test it. Each chapter keeps one sentence and a reference
  to this section. The D2 and D3 authors hand over the text; nothing is added that the
  chapters did not already say.

## E.6 Answers to the planted errors (lead integrates; D authors supply cells)

Pattern to follow: `appE-setup` (L3–45) computes the water answer from the project, guards
it with one `text_holds`, and the prose at L142–181 prints values inline. Each new answer
is a labelled cell plus ≤ 60 words, under `## Answer: … {.unnumbered #sec-answer-…}`,
placed in book order: fast path, London exercise, Chapter 11, Chapter 15, then (after
`sec-answer-water`) the water exercise. The chapter's planted cell and the answer cell
must compute the plant the same way: the D author writes one small function and gives the
lead both the chapter cell and the answer cell that call it, so the two cannot drift.

| Puzzle (owner) | Inputs | Computation | Guard | Printed answer |
|---|---|---|---|---|
| Fast path "README claim" (D1) | `ev.summary()`, `ev.metrics()` | `best`; `rival` = the release with the next-highest `roc_auc`; the claim prints `rival`'s `recall_top10` under `best` | the two recalls differ at the printed precision | which figure is wrong, whose it is, and `best`'s real value, each inline |
| D5-a, Part II exercises (D2) | `examples/london/data/attractions.csv` | among the five sights, the third by `visits_2025`; its printed value is its `visits_2024` | the two values differ, and the swap leaves the five's order unchanged | the sight, the printed and the true value, the difference, and "found by reading the row in `data/attractions.csv`" |
| Chapter 11 planted title (pilot author) | `ev.metrics()`, `eval-deck-titles.json` | the headline title with `rival`'s recall | as the fast path's; and the true headline equals the captured title | which title, and why a guard on a typed number could not have stopped it |
| D5-b, Chapter 15 (D3) | `ev.summary()`, `ev.metrics()` | the model card's headline sentence with `rival`'s `recall_top10` | recalls differ as printed | the sentence corrected, and the file to check it against (`outputs/metrics.csv`) |
| D5-c, Part V exercises (D4) | `w.res()` outputs | three sentences; a fixed index picks the one given a causal verb | the index is in range and the planted sentence contains the causal phrase, the others none of a listed set ("because", "causes", "leads to", "due to") | which sentence, the phrase, and the honest rewrite with verbs of association |

The fast path and Chapters 11 and 15 all plant the rival's recall; that is deliberate
repetition of one check, but the three answers should say so in a clause ("the same slip
as in @sec-answer-fast") rather than explain it three times. The appendix's title already
says "and Answers"; its opening section gains one sentence listing the answers.

## E.7 Spanish and checks

Every split, every table turned into cards and every new ID changes structure that
`translation/compare.py` holds equal between editions, so the lead lists each changed
appendix in `translation/pending.yml` at its pre-change commit until package G. Changed
references (`03-setup.qmd` 185, `02-assistant.qmd` 168, `d-troubleshooting.qmd` 27,
`index.qmd` 290, `i-workshop.qmd` 17) have Spanish twins at the
same lines' sense. Before returning: `make book-epub`, `make book-pages ONLY="ch037 ch038
ch039 ch040 ch041 ch043 ch044 ch045 ch047"`, and `make book-html` (it fails on an
unresolved cross-reference).

## Not verified (E)

- Nothing was built or measured: card heights, and whether the two-column agenda tables
  meet 0.45 page, are estimates from §3.3's rule of thumb.
- Whether Quarto resolves `@sec-…` to an unnumbered appendix heading with useful text in
  the EPUB (the references proposed for `sec-keys-terminal`, `sec-trouble-setup`,
  `sec-prices`); the book already links some such headings by file and anchor instead
  (`b-terminal.qmd#sec-keys-errors`), which is the fallback.
- I did not read `book-es/` beyond the copyright sentence, nor `a-windows.qmd` and
  `g-sources.qmd` beyond their tables and headings.
- Whether a `::: cards` list printed from a cell with `output: asis` (Appendix K) is
  processed by `filters/book.lua` like one typed in the source.
- That `rival` is best defined by `roc_auc` rank; the pilot brief defines it only as "the
  second-best release". The three chapters must agree on one definition.

---

# What could not be verified (whole file)

Each section ends with its own list; the points that matter most:

- **Nothing was built, captured, measured or run.** Every size "after" a fix, every capture's
  text size and every split or trimmed prompt is a proposal until `make book-pages`, the
  capture scripts and the lead's dry runs say otherwise.
- **How the briefs were written.** D1 was written by the editor from a line-by-line read. D2,
  D3, D4 and E were written by four forks of the editor, each reading its own files line by
  line, and then checked by the editor at their cold opens, story boxes and decisions, not
  re-read against every source line. The forks report these gaps: Chapter 7's setup imports
  and its text after L470; prompt texts in Part V beyond about 200 characters; figure cells'
  plotting code in Part V; Appendices A and G beyond their tables.
- **Stories.** Four drafts were cut back to their records by the editor (note 7). T12 says
  an early draft explained the small correlations "by range alone"; the record says only
  that the range-restriction argument was contradicted by the chapter's own numbers.
- **No vendor, licence or documentation page was opened.** Every URL given for a new
  `facts.yml` entry is one the book already cites or the obvious official page; the lead's
  evidence review must open each.
- **Landing page.** Constraints come from reading `ebook/_source.py`, `ebook/index.qmd` and
  `scripts/ebook_media.py`; `make ebook-check` was not run.
- **Spanish.** `book-es/` was read only for the copyright sentence and the exercise IDs.
