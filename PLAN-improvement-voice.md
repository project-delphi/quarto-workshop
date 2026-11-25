# PLAN-improvement-voice: how the revised book sounds

One page for every chapter author and translator, drawn from the accepted pilots (Chapters 1,
11 and 18 on `improve/c-pilot`) and the blind cold reads that preferred them. Examples are
quoted from those chapters. `book/PLAN.md` §5.1 and `book/README.md` still apply.

## Open on a person, a case or a puzzle

The first paragraph is at most 120 words of plain prose: no italics, no definition, nothing
about the chapter. Begin inside the situation.

> An analyst runs a script and copies a number into a Word document. … Four copies now exist,
> and the script knows about none of them. (Ch 1)

If you pose a puzzle, pay it off later, by name: Chapter 18 opens "Was it progress? Decide
now", and its think box begins "The chapter opened on Tunja's infant mortality". One hook per
chapter; never reuse another chapter's.

## Stories: true, or labelled

A story from the build log says only what its source records, and carries the source in a
comment. An illustration is labelled, and has no numbers or results. Either way it is a
failure the reader can meet in this chapter, and its lesson is an action.

The first sentence must stand on its own. A newcomer stalled on a draft that assumed she knew
what a part's map was; the accepted version explains in passing: "The descriptions of its
part maps, which screen readers read aloud, … named chapters by typed numbers." End on what
to do: "Count the slides in what comes back." (Ch 11)

## Show the result before the method

A hands-on chapter shows what the reader will build straight after the opening, legible on a
phone. Chapter 11 shows the title slide, then: "Read only its titles, and you have its
argument", and prints the eight titles from the finished deck. Give a small win early too:
Chapter 1's Try it needs nothing installed.

## A Pause and think is a puzzle, not a recap

Ask something the reader can get wrong, and that the page so far lets them get right. Where
you can, plant the error and let a cell derive it:

> Two of them read "…" and "…". Which habits can a list of titles alone prove, and is either
> title wrong? (Ch 11)

The answer says why, in at most 80 words, and names what would have caught it.

## Cut words, never the gloss

Both readers wanted shorter chapters; the newcomer then missed the plain explanations that
went with the cuts. Define a term in the clause that uses it, every time it is first needed
in a chapter:

> … its *seed*, the number that starts the random sequence … (Ch 1)
> … `{python} rival`'s recall, the share of subscribers its top tenth reaches … (Ch 11)
> … its median (the middle value, with half the rows below it) … (Ch 18)

## Be exact

The professional reader caught every loose phrase. So:

- **Exact terms.** "An unfixed random seed", not "a random seed". WCAG's minimum is "4.5 to 1
  between normal text and its background, 3 to 1 for large text", not "4.5 to 1". If you
  cannot state a term's meaning correctly in a clause ("missing at random"), look it up.
- **Keep the rule when you cut the paragraph.** The freeze paragraph went; its rule stayed:
  "A frozen page runs again when its source changes, not when its data do."
- **Observed behaviour is dated and versioned**, in a source comment or Further reading, not
  in a parenthesis: "Messages as Quarto 1.10.20 printed them, 2026-11-24".
- **No typed numbers.** Inline code, with a `text_holds` or `alt_text_holds` wherever words
  depend on data ("falls smoothly", "the first title is wrong").

## What to cut

- Commentary on the chapter ("This section explains…", "More is new here than…").
- A hook the book has already used.
- Audit-trail paragraphs ("Traps met in the test run…"): one story if one is vivid, then a
  small table of symptom, cause and fix.
- Hedges and repeats ("it is worth noting", a point made in the part page and again here).
- Walls: three reasons become a list; four properties become cards; a table has at most
  three columns.

## Sentences

Second person, active verbs, present tense. Short sentences that carry one fact each: "A typed
number is never an error to the program that prints it. Both are computed from the chapter
list now, and cannot fall behind it." (Ch 1) British spelling. No
emoji, no exclamation marks, no hype.

## Do not

- Do not add colour to a true story: no outcome, rate or motive the record lacks.
- Do not open a box, a story or a section on a pronoun or a term from elsewhere.
- Do not trim a tested prompt, or a sentence a guard or the landing page quotes, without
  saying so in your report.

## For the Spanish translators

- **Keep the cold open's shape:** the same person or case first, the same short closing
  beat, the question still a question the reader must answer ("Decide now").
- **Keep every gloss.** Translate the defining clause in full, in the same sentence as its
  term. Terms follow `translation/glossary.md`; where it has no entry, ask, do not coin.
- **Keep the precision:** "unfixed", "normal text", "utility-supplied" and their like are
  the point of the sentence.
- **You may condense wording** to stay within a unit's page budget, since Spanish runs about
  a tenth longer and cannot split a unit. Condense connectives and repetition. Never cut a
  gloss, a story's source comment, or a phrase a `text_holds` or `alt_text_holds` checks, and
  never change code, IDs or a quoted literal.
