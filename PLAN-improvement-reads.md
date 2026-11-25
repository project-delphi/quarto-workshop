# PLAN-improvement-reads: the "before" cold reads of the published book (651db10)

Two cold readers (Fable 5.2) read the published text as plain text, chapter by chapter, without
the plan or any brief. Quotes are passages' opening words. Chapter numbers are those the reader
sees (Ch 1 = 01-quarto … Ch 23 = 14-publish-many).

## Reader A: newcomer (NGO analyst, spreadsheets only, no terminal, reads on a phone)

Verdict: Parts I and II would keep her; she would stall at the Part III page ("if you came by the
route from zero, take the fast path first" sends her back to a chapter she was told to skip),
skim Parts III–IV, and come back for Tunja in Part V. The book's best tricks ("find the wrong
number", "predict before you rebuild") appear too rarely after Chapter 9.

Most engaging: Ch 5 (planted wrong number), Ch 9 (the site on my phone, then predict the
rebuild), Ch 7 (the typed "ten"), Ch 21 (Tunja in a wrong-sounding cluster), Ch 18 (missing data
as a story). Least: Ch 15 (version pins, "not tested"), Ch 13 (trap lists, citation plumbing),
Ch 12 (hex colours, Word XML), Ch 10 (assumes Ch 3; unexplained evaluation terms), Ch 2 (good
core buried under vendor comparisons, prices and policy).

Stop points by chapter:
- Preface: para 2 restates para 1 abstractly; licence detail before she knows what an agent is;
  "Part I covers what you need first" is one enormous paragraph. Her row ("New to the
  terminal") is last in Table 1; the first row (recurring reports) sends her to Ch 3, which she
  cannot do. Best: "Your first afternoon".
- Ch 1: .qmd, YAML, code cells and fences in two paragraphs; Jupyter, knitr, Pandoc, Typst,
  LaTeX in three bullets; the freeze-cache subtlety too early. Best: "You correct one number in
  the data. What do you retype in the report?" / "Nothing."
- Ch 2: SVG, effort levels and 13.09 cents arrive before she knows what an agent is; "What
  'covers' means differs between them" is the author's audit trail; the a16z/Epoch cost
  paragraph; per-agent AGENTS.md lookup rules; she skipped §2.10. The OpenCode warning appears
  twice. Best: "the model decides, the harness does, you direct and check".
- Ch 3: rightly tells her to leave. Typo: "Chapters 4 and 5 (Chapter 4 and Chapter 5)".
- Ch 4: five dense paragraphs (connection, VPN, proxy, API key) before step 1; the plan list
  ("Pro, Max, Ultra, Team, Enterprise or Console") made her think it costs money she lacks; the
  free route is buried in caveats ("might be decent… none was tested"); §4.8's codespace "was
  not tested", yet it is the route for a locked work laptop. Best: "Two places to type"; "The
  pointer starts on 'No, exit', so pressing Enter straight away quits."
- Ch 5: the name-with-a-space detour breaks the hunt; git identity/nano/Vim; the fresh-clone
  check felt like one too many. Best: "Tate Modern's. The page says 4,154,266; its row says
  4514266"; "In the terminal, silence is success."
- Ch 6: ten Markdown-mark figures before the first prompt ("endless scrolling" on a phone); GFM
  dialects; the lockfile-and-Fortran "Why". Best: §6.9.1, the agent quietly changing Tottenham
  Court Road to Holborn. 8,000 words, three terminal tabs: tiring.
- Ch 7: "Quarto 1.4 introduced this inline syntax"; kernel internals. Best: "The word 'ten' is
  typed, so it never updates". The tightest hands-on chapter.
- Ch 8: per-vendor sub-agent paragraph; the long sub-agent prompt is "a frightening block; I
  would paste it without understanding it"; raw Typst. Best: "would that reader read it, and act
  on it?"; "A 3-D chart has to earn its third dimension."
- Ch 9: six-hosts table; "observed with 1.6.40 and not re-tested with 1.10.20"; "Three traps".
  Best: "open the address on your phone"; "A cited copy is still a copy." Bug: the closing
  paragraph says the water analysis comes next.
- Part II exercises: the intro is a wall; the "Stuck for two minutes?" box five times.
- Ch 10: opens on a chapter she skipped; bootstrap, checksum, leak, Brier score unexplained;
  "Three traps met in the test run". Best: "the called top 10% of the list holds 47.9% of the
  contacts aged 60+".
- Ch 11: "Traps met while building and testing the deck"; the deck_pdf prompt; seven PowerPoint
  layout names. Best: "Read only the titles of the finished deck, and you have its argument".
- Ch 12: Table 12.2 repeats Table 11.3's colours; "Three traps"; Word-XML check. Best: "A person
  checks the page they are looking at. A script checks every page, every time."
- Ch 13: nine rows of syntax in Table 13.1; trap paragraphs. Best: "cite what you have read";
  the "pbge" page number ("the only laugh in Part III").
- Ch 14: Table 14.1 (-P, -M, papermill) before one example; "Where the files went is the trap".
  Best: "45 files, each named by its value and each checked for it." She wanted it on her kind
  of data.
- Ch 15: action version pins; merge vs squash; "What was not tested" lowers trust. Best: "A check
  that has never failed has not been tested."
- Ch 16: vendor-terms table; proxy variables. Best: "Build on a stand-in… Render the real thing
  yourself." She needed this before Ch 4.
- Part V page: excellent ("6.8 million of the 12.6 million people in rural zones…").
- Ch 17: "five times the weighted mean"; acronym flood (IRCA, INS, DANE, DIVIPOLA, ICFES, MEN,
  DNP, MDM, SGP) in §17.5; Tables 17.2–17.3 on a phone. Best: "An empty IRCA is unknown, never
  safe and never zero."
- Ch 18: "Before any model, look at the data" is a slogan. Best: "the zones whose scores are
  worse are also the ones least often scored"; meeting Tunja. "Reads like detective work."
- Ch 19: the z-score formula and "Euclidean distance" paragraph; Table 19.2. Best: unscaled, "the
  clusters would be climate zones". (Her plain-text copy garbled the MathML; check the EPUB.)
- Ch 20: the inertia formula right after "need not be daunting"; adjusted Rand index; Rousseeuw.
  Say at the top that the normal route copies the finished script. Best: "That four is a useful
  summary, not a discovery."
- Ch 21: Table 21.2; "From 2017 the series looks…". Best: Tunja's high-risk rural zone landing in
  "no-risk water": "A label describes a kind; to say anything about one member, go back to its
  rows."
- Ch 22: the second paragraph lost her; range/chance/unit caveats; Table 22.3 all "yes". Best:
  the wrong and honest sentences side by side. "Nobody tells me what I can tell the council."
- Ch 23: §23.4.1 freeze; the dashboard prompt; "Three traps". Best: `assert k == 4`, "a loud
  failure is better than a quiet falsehood".
- Part V exercises: no hook; numbered III.x in Part V.
- Afterword: "An internal metrics brief… Anyone who sends the same figures every month" is "the
  book I bought, and it is on the last pages."

Her top changes: (1) a bridge page at Part III for newcomers (what Acme is, ROC AUC in one line,
copy checkpoint 14) or say newcomers may jump to Part V; (2) move the metrics-brief promise to
the preface and her row first; (3) cut Ch 2 by a third; (4) slim Ch 4 §4.1 and lead with the free
route plainly; (5) introduce Markdown marks where the guide first uses them; (6) thin the "traps
met in the test run" boxes and the "(checked …)" stamps; (7) use the Ch 5 device in every chapter
(a wrong slide title in Ch 11, a fake reference in Ch 13, a wrong month in Ch 14); (8) one plain
sentence before each long prompt saying what it will do, or split it; (9) plain names for Part
V's acronyms, formulas in asides, what she can honestly tell the council in §22.1; (10)
housekeeping: Ch 9's ending, III.x numbering, checkpoint numbers that look random, the
duplicated cross-reference in Ch 3, the full "Stuck for two minutes?" paragraph repeated about 25
times (shorten after first use).

## Reader B: professional (data scientist at a 20-person AI start-up; writes the investor update; tablet)

Verdict: the professional chapters (3, 10–16) are "the best content and the worst shown":
Chapters 3, 11, 12, 13, 14, 15 and 16 have no figure; Ch 10 has one; Ch 6 alone has 15. He never
sees the Acme report, model card, deck, site, white paper or investor update.

Most engaging: Ch 10 (the 10.4 "top 10%" trap), Ch 3, Ch 5, Ch 13 (references; "check_refs.py
is something I would steal tomorrow"), Ch 15 (the red build); then the afterword's projects.
Least: Ch 6, Ch 4, Ch 19, Ch 20, Ch 9; dishonourable mention Ch 2 §2.1–2.4.

Stop points by chapter:
- Preface: the open-source licence essay before his path; two navigation systems ("Find your
  path", then "Three ways through"); checkpoint mechanics. The path table arrives ~1,000 words
  in. Best: "the founder who sends investors a figure from the wrong month."
- Ch 1: "That faith is the problem…" repeats the preface sermon; Table 1.1's wiki/Markdown rows.
  Best: "Reproducible does not mean correct. A wrong analysis reproduces perfectly."; §1.5 earns
  trust.
- Ch 2: §2.1–2.4 beginner material for him; the untested free-models paragraph; the OpenCode
  sentence verbatim in §2.2, §2.4 and Ch 4; 25 "checked 20xx" stamps. Best: Table 2.3 and "Size
  the work by how it will be checked, not by how much typing it saves." Defect: ends "Chapter 4
  gets it there in six checked steps", wrong for fast-path readers.
- Ch 3: the duplicated cross-reference; Table 3.4 captioned "The three checks of Table 5.2", a
  table in a chapter he skipped; §3.8 "On your own repository" too thin: "the section I bought
  the book for". Best: "A guard you have never seen fail is a guard you have not tested." He
  never sees the report.
- Ch 5: "the best hook in the book… The fast path has no equivalent 'find the planted error'
  moment."
- Ch 6: "More is new here than in any other chapter"; repeated full git status dumps; §6.11
  catch-up mechanics.
- Ch 7: line-by-line pandas; the "Line 3 / Line 5 / Line 7" annotations.
- Ch 8: the third paragraph is a lecture; vendor survey; §8.5 three.js then admits Figure 7.2 is
  "the better chart". Best: the In practice box on when not to use sub-agents.
- Ch 9: Git vocabulary; host tables; the §9.4 mega-prompt. Best: "A cited copy is still a copy".
- Ch 10: "It is the first chapter of this part…" repeats the part page; "Three traps met in the
  test run" ("test run" appears seven times); Table 10.4 repeats Table 3.3. Best: §10.4's "top
  10%" caption and the guard "The caption says top 10%, which a caption cannot compute." The
  age-band slice is a real finding. No picture of the card.
- Ch 11: "You will rarely write a Reveal.js option…" stated for the third time; the traps wall;
  Tables 11.3 and 12.2 are the same contrast table. A chapter about slides shows no slide.
- Ch 12: Table 12.2 duplicate; ".gitignore ignored every *.docx" trap; §12.6 repeats Ch 9. Best:
  Table 12.1 (_brand.yml does not reach Word or PowerPoint). No screenshot of the site.
- Ch 13: six traps in one paragraph; "pbge" and partial names read as trivia; the Zotero aside.
  Best: "One paper whose DOI resolved could not be opened at all; it is not cited."
- Ch 14: opens a section with a bare table; §14.5 educator case "a different reader inside my
  chapter"; "Where the files went is the trap" dense. Best: "A guard that repeats the comparison
  that chose the word can never fail, and protects nothing." "The chapter I bought the book for;
  the shortest in Part III; never shows the update."
- Ch 15: CI vocabulary table; squash-vs-merge; "What was not tested" deflates the title. Best:
  "An agent told to make a failing step pass has two routes… only one is right."
- Ch 16: vendor table cells; proxies; §16.6's start-up paragraph for the third time (preface,
  §1.5, here). Best: "'Do not paste it' is not enough. An agent can read a file you never
  mentioned."
- Ch 17–23 (skimmed): Ch 18 opens "Before any model, look at the data"; Ch 20 "If the
  mathematics sounds daunting"; Ch 21 opening good ("Cluster 4 is a number"); Ch 22 caveat upon
  caveat for a ρ of 0.10, best the fair-versus-unfair title pair; Ch 23 opens restating readers
  and formats, "Stuck for two minutes?" four times.
- Afterword: "What you can now do" repeats the preface; the investor-update prompts repeat
  §14.2. Best: "Runway here is cash divided by burn…"; "the most job-shaped pages in the book,
  and they sit after 100,000 words."

His top changes: (1) show the outputs in Parts III–IV (Ch 3 report, Ch 10 model card, Ch 11
three slides with titles, Ch 12 home page, Ch 13 PDF title block, Ch 14 the update, Ch 15 the
red check naming the sentence); (2) give Ch 14 the weight of its promise (parameters cell, one
guarded up/down sentence in source and output; move the educator case out; fold in the
afterword's runway/net-burn/overwritten-file warnings); (3) give the fast path its own planted
error so Ch 3 opens "one figure in this report is wrong"; (4) fix the hand-offs (Ch 2's last line
by route; Table 3.4 not leaning on Table 5.2; the duplicated cross-reference); (5) cut the
preface by half with the path table on the first screen; (6) a "daily agent users: read 2.7–2.9"
signpost in Ch 2, one OpenCode warning, test or cut the free-model paragraph; (7) collapse the
"traps met in the test run" paragraphs (10.2, 11.3, 12.2, 12.3, 13.3, 13.5) into short
symptom/cause/fix tables, stamps to notes; (8) de-duplicate (start-up paragraph ×3, contrast
table ×2, "you will rarely write a theme by hand" ×3, the GitHub Pages plan sentence ×3, "Stuck
for two minutes?" ×4 in Ch 23); (9) expand §3.8 into a worked page (results trapped in notebooks,
an existing conda or Poetry environment, a monorepo) and signpost the afterword's projects from
the end of Ch 3; (10) close or footnote Ch 15's "What was not tested"; rename III.x.
