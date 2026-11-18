# Spanish edition: plan

Status: done on branch `spanish-edition` (decisions D1–D6 taken as recommended; D5: the
Spanish text writes around the author's gender). The sections below are the plan as approved.

## 1. What gets translated, in order

The English book is `book/` (a Quarto book, chapter list in `book/_chapters.yml`). It publishes
to `/quarto-workshop/book/` (`docs/book/`); its landing page is `ebook/index.qmd`, at
`/quarto-workshop/ebook/`. 31 source files, about 72,500 words, plus the landing page
(about 1,800 words in `ebook/index.qmd`, and the strings in `ebook/_source.py` and
`ebook/_parts.py`).

| # | File | Words | Cells / inline | Notes |
|--:|---|--:|---|---|
| 1 | `index.qmd` (preface) | 2,023 | 1 / 5 | |
| 2 | `copyright.qmd` | 288 | | |
| 3 | `dedication.qmd` | 13 | | |
| 4 | `about-author.qmd` | 63 | | |
| 5 | `part-1.qmd` | 269 | | roadmap figure |
| 6 | `chapters/01-quarto.qmd` | 2,972 | 1 / 4 | |
| 7 | `chapters/02-assistant.qmd` | 4,913 | 1 / 5 | |
| 8 | `chapters/03-setup.qmd` | 3,704 | | |
| 9 | `part-2.qmd` | 311 | | roadmap figure |
| 10 | `chapters/04-markdown.qmd` | 6,680 | 3 / 6 | nine Markdown GIFs |
| 11 | `chapters/05-compute.qmd` | 3,116 | 3 / 13 | |
| 12 | `chapters/06-audiences.qmd` | 3,247 | 2 / 8 | QR card |
| 13 | `chapters/07-publish.qmd` | 3,503 | 2 / 5 | |
| 14 | `chapters/exercises-london.qmd` | 1,628 | 1 / 1 | |
| 15 | `part-3.qmd` | 474 | 1 / 5 | roadmap figure |
| 16 | `chapters/08-water-question.qmd` | 3,488 | 3 / 17 | |
| 17 | `chapters/09-explore.qmd` | 2,672 | 5 / 36 | |
| 18 | `chapters/10-prepare.qmd` | 2,939 | 3 / 49 | |
| 19 | `chapters/11-cluster.qmd` | 4,285 | 8 / 67 | |
| 20 | `chapters/12-interpret.qmd` | 4,990 | 10 / 50 | cluster names, most guards |
| 21 | `chapters/13-causation.qmd` | 3,785 | 6 / 39 | |
| 22 | `chapters/14-publish-many.qmd` | 3,555 | 2 / 1 | |
| 23 | `chapters/exercises-water.qmd` | 2,097 | 1 / 7 | |
| 24 | `afterword.qmd` | 829 | | |
| 25–34 | `appendices/a-windows.qmd` … `j-glossary.qmd` | 10,664 | 2 / 20 | F gets a note on this edition; J is re-sorted |

"14 chapters" in the brief are chapters 1–14; the two exercise chapters and the three part
pages are translated too.

## 2. Build setup (recommended): a sibling project, `book-es/`

```
book/                 English, untouched apart from shared scripts made language-aware
book-es/
  _quarto.yml         translated copy of book/_quarto.yml: lang: es, title, description,
                      site-url …/book/es/, a new EPUB identifier, output-file prompt-check-publish-es
  _quarto-html.yml    written by book/scripts/sync_chapters.py from book/_chapters.yml
  _quarto-epub.yml    (one chapter list for both languages)
  index.qmd, part-*.qmd, chapters/, appendices/   same relative paths as book/
  media/diagrams/, media/roadmaps/, media/cover.*, media/qr/   Spanish versions
  media/{gifs,stills,figures,london,deck,examples}, scripts, filters, styles, assets
                      -> symlinks into book/ (shared, not copied)
  _freeze/            its own cache, committed like book/_freeze/
```

Why a sibling and not a profile inside `book/`:

- **Code stays byte-for-byte identical.** Cells run from the project folder and read
  `../examples/...`; `book-es/` sits at the same depth as `book/`, so every path resolves the
  same. A folder inside `book/` (`book/es/`) would need every path changed.
- **Pairs line up one-to-one**: `book/chapters/09-explore.qmd` ↔ `book-es/chapters/09-explore.qmd`.
- **English output cannot change by accident.** A profile in `book/` shares its project, search
  index and `_freeze/`, and a Quarto book's `index.qmd` must sit at the project root.

Build targets: `make book-es` (HTML + EPUB, post-processing, EPUBCheck `--failonwarnings`,
link check), `make book-es-publish` → `docs/book/es/`. `make book-publish` gets an rsync
protect rule for `es/` (today its `--delete --delete-excluded` would wipe `docs/book/es/`).
`scripts/keep-book.ts` already restores all of `docs/book/`, so `es/` survives a deck render.
Symlinks with Quarto's resource copying are the main risk: I will prototype the skeleton
(one chapter) first and fall back to `../book/...` paths in the config if they misbehave.

### URLs

Existing English URLs do not change. Proposed Spanish URLs mirror the English layout:

| | English (unchanged) | Spanish (proposed) |
|---|---|---|
| Web edition | `/quarto-workshop/book/` | `/quarto-workshop/book/es/` |
| EPUB | release asset `prompt-check-publish.epub` | release asset `prompt-check-publish-es.epub` (and a copy in `docs/book/es/`) |
| Landing page | `/quarto-workshop/ebook/` | `/quarto-workshop/ebook/es/` (`ebook/es/index.qmd`, added to the root `project.render`) |

The brief says the book goes to `/ebook/es/` and the landing page to `/es/`. In this repository
`/ebook/` is the landing page and `/book/` the book, and `/quarto-workshop/es/` would sit
beside the workshop deck, so the table above is my recommendation (see decision D1).

## 3. Shared code made language-aware (English output unchanged)

Labels that are not in the chapter files, each given an `es` table chosen by the document's
`lang` (read from the `QUARTO_EXECUTE_INFO` file Quarto passes to the kernel, the way
`figures.target()` already reads the format; Lua filters read `lang` from the metadata):

- `filters/book.lua`: box, aside, opener, think and "You're done when" labels.
- `scripts/prose.py`: number words (*nueve*), `spans()` joining with *y*.
- `scripts/epub_postprocess.py`: matches Spanish headings and captions ("Capítulo 3",
  "Apéndice A", "Parte I", "Figura 1.1", "Apéndices", landmark titles).
- `scripts/roadmaps.py`: a Spanish `META`, writing `book-es/media/roadmaps/`.
- `scripts/water.py`: Spanish cluster names alongside the English ones (the guards keep
  testing the English names, so they guard the same facts).
- `scripts/check_live_links.py`: the Spanish EPUB's links into `/book/es/`.
- `ebook/_source.py`: read from a book folder and language passed in.

The English edition is checked for unchanged output by building it on `main` and on the branch
and diffing `_book/html/` and the unzipped EPUB (timestamps aside).

## 4. The comparison script (`translation/compare.py`)

For each EN/ES pair: same number of executable cells and display fences; same cell options
except `fig-cap`, `fig-alt`, `tbl-cap`, `fig-subcap`; same set of `{#…}` IDs, `@…`
references, URLs and shortcodes; same heading levels and IDs, in order; inline code identical.
Executable code identical byte-for-byte except reviewed string literals (decision D3), which it
lists. A second pass greps the rendered Spanish HTML and EPUB text, code removed, for English
sentences (stop-word density per sentence) and reports them.

## 5. Decisions for you (my recommendation first)

**D1. URLs.** `/book/es/` for the Spanish book and `/ebook/es/` for its landing page, as in §2,
rather than `/ebook/es/` and `/es/`.

**D2. Title.** Translate it: *Pide, revisa, publica*, subtitle *Publicación reproducible de datos
con Quarto y agentes de programación con IA*, with a Spanish cover from `media/cover.svg`.
The alternative keeps *Prompt, Check, Publish* as a brand with a Spanish subtitle.

**D3. Code that writes words.** "Code byte-for-byte identical" conflicts with the cells that put
English on the page: chart axis labels and legends, table headers, word lists such as
`WORDS = {"water_coverage": "piped-water coverage", …}` in Chapter 12, `cname()`'s "cluster",
`" and "` joins. Left alone, Spanish sentences would read "…en nine municipios" and the charts
would be in English. Recommendation: translate only string literals that reach the page;
everything else in a cell stays identical; `compare.py` enforces that and lists every changed
literal in `translation/code-strings.md` for your review. Comments in code stay English, as
you asked.

**D4. Prompts in the agent boxes** (50 `default` fences). Recommendation: translate them,
keeping every literal (file, column, option, quoted heading) exactly as in English. The book's
own Appendix F tells readers they can prompt in Spanish with literals in backticks, and a
Spanish reader should not have to type English. They have only been tested in English; the
`Catch me up: follow …/README.md` lines stay in English because the checkpoint READMEs are
English.

**D5. "About the author" and gender.** Spanish needs a gender for *el autor* / *la autora*
(about-author page, copyright page, landing page). Which should I use? Otherwise I will write
around it ("Ravi Kalia escribe…", "Sobre Ravi Kalia").

**D6. Numbers.** Inline values are computed by code, so they keep English formatting
(1,122 and 0.45), which matches Mexican and Central American usage and the RAE's acceptance of
the decimal point, but not Colombian usage (1.122 and 0,45). Recommendation: leave them.

## 6. What stays in English (to be listed in the PR)

- The 21 GIFs and the screenshots of the projects (London guide, water report, …): their
  captions and alt text are translated; alt text quotes the English on screen and translates it.
- The live 3-D scenes and explorers, which run the deck's own bundle and data (English labels).
- Checkpoint READMEs, the workshop deck and the example projects, which the book links to.

The ten diagrams (`media/diagrams/*.svg`, 202 text elements), the three roadmaps, the cover and
the QR code (pointing to `/book/es/`) are made in Spanish.

## 7. Working method

One file at a time in the order of §1; after each, a pass against `glossary.md` and
`compare.py`, a render of that chapter, and one commit
(`feat(book-es): translate chapter 9`). Glossary changes found along the way are committed with
the chapter that needed them. I translate sequentially myself; sub-agents could translate
files in parallel against the glossary, at the cost of more uneven voice. Lines must not start
with `@label.` after rewrapping (it becomes an example list; `make` checks for it).

## 8. Not yet translated (the 2026-11 revision)

The revision for professional and start-up readers (`REVISION-PLAN.md`) was written in English
first, at the author's request, without translating it. Two mechanisms keep the Spanish edition
building and checked meanwhile:

- **New files** (chapters, part pages, appendices) are listed in `book/_chapters.yml` under
  `english_only`. `book/scripts/chapter_list.py` leaves them out of the Spanish edition's
  profiles, roadmaps and landing page, and `scripts/lang_switch.py` points their EN | ES switch
  at the Spanish home page.
- **Changed files** are listed in `translation/pending.yml` with the commit their Spanish twin
  matches; `compare.py` compares the twin with the English text of that commit.

To translate one: translate the file (or the changed sections, `git diff <commit> -- book/<file>`),
remove its line from `pending.yml` or its entry from `english_only`, and run `make book-es`.
The list of what waits is kept in `REVISION-PLAN.md`, "For the Spanish edition".

### 8.1 The Spanish to-do for the revision (WP14, 2026-11-18)

What the Spanish edition needs before it matches the English one, in the order to do it. Each
step ends with `make book-es` (EPUBCheck, `compare.py`, `english_scan.py`) and removes its
files from `english_only` or `pending.yml`.

1. **The changed files first** (`pending.yml`, 32 lines): the preface (audiences, reading paths,
   the three examples, how the book is organised, free and open source), Chapters 1 to 4, the
   first report, the London and water chapters whose references changed, Appendices A, E, G, I
   and J, the copyright page, the afterword (two new projects) and the three existing part
   pages. Most are references and short sections: `git diff <commit> -- book/<file>` shows
   each one's change.
2. **The glossary's new terms** (into `translation/glossary.md` first, then Appendix J):
   API key, `apt`, artifact, brand file, calibration, citeproc, codespace, continuous
   integration (CI), contrast ratio, cron, cross-reference, CSL, `curl`, description, dev
   container, fragment, Homebrew, model card, notebook, package manager, papermill, parameter,
   print view, protected branch, proxy, reference document, ROC AUC, runner, slice, social card,
   speaker notes, spending limit, status check, template partial, theme, VPN, workflow, zero data
   retention. Decide which stay in English as GitHub's or Quarto's interface words (*workflow*,
   *runner*, *status check*, *pull request*), as section 6 does for code.
3. **Appendix K and `facts.yml`.** The facts' `text` and `label` are English sentences.
   Add `text_es` and `label_es` beside each (`scripts/facts.py` reads the document's `lang`),
   rather than a second file, so a re-checked fact changes once. The Spanish landing page
   already reads `facts.yml` in English (`ebook/_source.py`); switch it to the Spanish texts.
4. **New chapters, in reading order**, each with its part page: The Fast Path; Part III, The
   Craft of Outputs (One Set of Results, slides, sites, white papers, parameters); Part IV,
   Working in a Team (pull requests and CI, at work and in a start-up). Their roadmap entries
   go in `META_ES` (`scripts/roadmaps.py`); the Spanish water part becomes *Parte V* when Parts
   III and IV arrive, not before.
5. **Prompts.** Translate each printed prompt, keeping file names, column names, options and
   commands as code (section 6). A translated prompt is a new prompt: dry-run it from the same
   checkpoint before it is printed, as the English ones were, and record any change of result.
6. **What stays in English:** the Acme example (`examples/eval/`, checkpoints 14 to 20,
   `starters/eval-repo/`) and `examples/feedback/`, like the other projects' code; their
   READMEs and page text are a separate decision for the author (a Spanish Acme site would need
   its own `_brand.yml` strings and checks).

The shared scripts already take their words from `lang` (section 3); the new ones added by the
revision do not, and need the same treatment before their chapters are translated:
`scripts/evaluation.py` needs nothing (numbers only), and `scripts/partpage.py` already reads
Spanish descriptions (from `META_ES`). `filters/glossary.lua` is off in Spanish (it returns
early for `lang: es`): turning it on needs the Spanish Appendix J's terms and IDs. And the new
chapters' setup cells build some sentences in English (for example `team.qmd` joins its list of
pinned actions with "and"); give them the edition's words through `scripts/prose.py`, as the
water chapters do.
