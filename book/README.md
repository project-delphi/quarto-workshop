# One Source, Every Format: the book edition

The workshop as a book, from one Quarto book project in two editions:

- **EPUB** (the main edition): `_book/epub/one-source-every-format.epub`
- **HTML** (the companion, where the live 3-D scenes and data explorers run): `_book/html/`

Both are published under `docs/book/` and served at
<https://project-delphi.github.io/quarto-workshop/book/>. The workshop deck and its
`docs/` output are built separately (the root `_quarto.yml`) and are unaffected by building
the book. `PLAN.md` holds the design: the table of contents, the inventory of the deck's
interactive elements with each one's EPUB replacement, and the decisions taken.

## Tools

| Tool | Version used | Needed for |
|---|---|---|
| [Quarto](https://quarto.org/docs/get-started/) | 1.10.20 | every build |
| [uv](https://docs.astral.sh/uv/) | 0.11.32 | the book's Python environment (`pyproject.toml`, `uv.lock`) |
| Java | OpenJDK 11 | EPUBCheck |
| [EPUBCheck](https://github.com/w3c/epubcheck/releases) | 5.4.0 | validating the EPUB; `make` downloads the jar to `~/.cache/quarto-book/` |
| Google Chrome | 157 | `make media` and the screenshot scripts (Playwright drives the installed Chrome) |
| [VHS](https://github.com/charmbracelet/vhs) (with ttyd and ffmpeg) | 0.12.1 | re-recording terminal animations |
| ffmpeg, gifsicle | 9.0.2, 1.95 | assembling and shrinking GIFs |
| `sips` (macOS) | | the PDF page images in `media/figures/` (`media/capture/*_outputs.py`) |

Building the book needs only the first four. Playwright and segno come in through
`uv run --with` in the `make` targets, so they are not project dependencies.

## Build

From the repository root:

```bash
make book          # both editions; the EPUB is post-processed and checked with EPUBCheck
make book-html     # the HTML edition only
make book-epub     # the EPUB only, with post-processing and EPUBCheck
make book-fresh    # the same as `make book`, re-executing every chapter
make book-shots    # screenshot the EPUB's chapters at phone and tablet widths, light and night
make book-publish  # copy the HTML edition and the EPUB into docs/book/
make site          # render the deck, then the book, then publish the book into docs/
```

The chapter list lives in one file, `_chapters.yml`. `make` runs `scripts/sync_chapters.py`,
which writes the two profiles' chapter lists (`_quarto-html.yml` with parts,
`_quarto-epub.yml` without, because Quarto drops parts from EPUB). Edit `_chapters.yml`, never
the generated files. Each edition renders into its own folder, because rendering one format
empties the output folder.

`scripts/epub_postprocess.py` then repairs what Quarto 1.10.20 writes: it nests the chapters
under their parts in the table of contents, puts the copyright page before the preface, adds
landmarks, removes the `alt` attribute that Quarto puts on figure wrappers (invalid in XHTML),
and flattens figures shown on a light panel onto the panel's colour. The EPUBCheck report is
saved as `_book/epubcheck.txt`.

### Python and Jupyter

Chapters run Python from `book/.venv` (`uv sync` creates it; `make` runs Quarto through
`uv run`). The Makefile sets `JUPYTER_PATH` to the environment's own kernels, because a
user-level `python3` kernelspec can point elsewhere and fail with a `ModuleNotFoundError`.

### Cached results and when to clear them

Execution uses `freeze: auto`: a chapter re-runs only when its `.qmd` changes, and its results
are kept in `_freeze/`, which is committed so that a rebuild gives the same numbers. Freezing
does not notice changes outside the chapter, so run `make book-fresh` after changing any of:

- `examples/london/data/` or `examples/water/data/`
- `examples/water/scripts/analysis.py` (Part III imports it and calls `analysis.run()`)
- `scripts/water.py`, `scripts/scenes.py`, `scripts/figures.py` or `scripts/roadmaps.py`

## Conventions

- Every number is computed by a cell from the repository's data. Part III imports the water
  project's `analysis.py`, so the book quotes what the project computes.
- Edition-specific content: `when-format="html:js"` for the HTML edition (plain `html` also
  matches EPUB) and `when-format="epub"` for its EPUB stand-in.
- Asides are divs with the classes `why`, `pitfall`, `practice` and `tryit`, turned into
  callouts by `filters/book.lua`; prompts use the deck's `prompt`, `agent` and `you` boxes.
- Images are referenced without an extension. The HTML edition picks the SVG and the EPUB the
  PNG (`default-image-extension`). Diagrams are drawn portrait, 700 px wide, with text of at
  least 19 px so they stay legible on a phone.
- Figures drawn in dark ink on a transparent background carry the class `on-light`, which puts
  them on a light panel in both editions, so they stay visible in night themes.
- Prose has no emoji; the deck's emoji survive only inside quoted prompts.

## Media

All images and animations are made by `media/build.py`, which `make media` runs. It is slow
(a few minutes) and only needed when an animation or diagram changes. The steps, in order:

| Step | Makes |
|---|---|
| `deck` | copies the deck assets the book reuses into `media/deck/`, and the London photos into `media/london/` |
| `cover` | `media/cover.png`, 1600 × 2560, from `media/cover.svg` |
| `roadmaps` | the "Where we are" roadmaps, `media/roadmaps/part-N.svg`, from `_chapters.yml` |
| `diagrams` | a PNG at twice the size beside every SVG in `media/diagrams/` and `media/roadmaps/` |
| `qr` | the QR codes for the EPUB's links to the live scenes, `media/qr/` |
| `tapes` | terminal animations from `media/tapes/*.tape`, recorded with VHS |
| `capture` | 3-D scene and preview animations from `media/capture/*.py` (build the HTML edition first) |
| `posters` | the book versions of the deck's illustrated GIFs |
| `stills` | the first frame of every GIF, `media/stills/*.png` |
| `check` | fails unless every GIF is at most 2 MB and 800 px wide, and has a still |

To redo part of it, name the steps and limit the tapes or capture scripts with `ONLY`:

```bash
make media STEPS="tapes stills check" ONLY=terminal-basics
make book-html && make media STEPS="capture stills check" ONLY=kmeans
make media STEPS="diagrams"
```

Rules every animation follows:

- **The first frame is a finished still.** Readers that do not animate a GIF show its first
  frame, so each GIF opens on its last frame, held for two seconds, before playing.
- **A still for reduced motion.** `filters/anim.lua` puts each GIF in a `<picture>` that shows
  the still to readers whose system asks for reduced motion (HTML edition).
- **Real recordings use a demo account.** The tapes set `HOME=/tmp/home/ana`, so no personal
  path appears. They run local commands only: no network, publishing or assistant commands.
- **Illustrations say so.** The chat, agent-session and Windows animations are scripted
  illustrations (the repository's rules rule out paid assistant sessions for teaching
  material), and their captions say so.

The animations are:

| GIF | Made by | Size |
|---|---|--:|
| `agent-session.gif` | `tapes/agent-session.tape` (scripted illustration) | 103 KB |
| `catch-up.gif` | `tapes/catch-up.tape` | 344 KB |
| `chat-prompt.gif` | the deck's illustration, `posters` step | 265 KB |
| `cluster-cloud-orbit.gif` | `capture/cluster_cloud.py` | 1.98 MB |
| `colombia-relief-orbit.gif` | `capture/colombia_relief.py` | 1.27 MB |
| `kmeans-steps.gif` | `capture/kmeans.py` | 1.92 MB |
| `london-map-orbit.gif` | `capture/london_map.py` | 1.94 MB |
| `quarto-preview-reload.gif` | `capture/preview_reload.py` | 135 KB |
| `render-many-formats.gif` | `tapes/render-many-formats.tape` | 161 KB |
| `terminal-basics.gif` | `tapes/terminal-basics.tape` | 129 KB |
| `uv-environment.gif` | `tapes/uv-environment.tape` | 265 KB |
| `windows-session.gif` | the deck's illustration, `posters` step | 200 KB |

Sizes in decimal units, as built on 2026-11-12.

## Checking a build

1. `make book` ends with EPUBCheck's summary; anything but
   `0 fatals / 0 errors / 0 warnings / 0 infos` is a failure to fix.
2. `make book-shots` saves each EPUB chapter, screen by screen, at phone (390 × 844) and tablet
   (820 × 1180) sizes, in a light and a simulated night theme, to `_book/shots/`, and reports
   anything that sticks out sideways. Look at the changed chapters.
3. `scripts/shoot_html.py` does the same for HTML pages at desktop (1440 × 1000) and laptop
   (1366 × 768) sizes, light and dark, and reports images that failed to load.
4. In the HTML edition, check that each changed live scene draws and that its view buttons work.

## Publishing

GitHub Pages serves `main:/docs`; the book is `docs/book/`, copied there by `make book-publish`
and committed with its sources. A full render of the deck empties `docs/`, so the deck's
`post-render` script, `scripts/keep-book.ts`, restores the committed `docs/book/` afterwards.
To rebuild everything, run `make site`, which renders the deck first and then publishes the
book over the restored copy. Never use `quarto publish` for this repository.

## How the editions behave in readers

The EPUB is EPUB 3, valid under EPUBCheck 5.4.0. It was checked by rendering its chapters with
its own stylesheet in Chrome at phone and tablet sizes, light and night (`make book-shots`). It
has not been opened on an e-reader or in a reading app, so every reader column below is
untested; the Kindle column quotes Amazon's publishing guidelines, not a test.

| Feature | HTML edition | EPUB, as checked in Chrome | Kindle (Amazon's guidelines) | Apple Books, Kobo, Google Play Books, Thorium |
|---|---|---|---|---|
| Animated GIFs | play; the still is shown when reduced motion is on | play | "do not support … multi-frame GIFs"[^kdp-img]: the first frame, a finished still, should show | untested |
| Live 3-D scenes and data explorers | run (WebGL) | replaced by an animation, a link and a QR code | the same as the EPUB | the same as the EPUB |
| Night and sepia themes | dark theme via the switch | text takes the reader's colours; figures sit on light panels | the guidelines do not support "images with transparent areas"[^kdp-img]: panel figures are flattened to opaque PNGs | untested |
| Diagrams | SVG | PNG at twice the size | PNG, as the guidelines recommend over SVG[^kdp-img] | untested |
| Mathematics | MathJax | MathML (four chapters) | not documented in the pages read[^kdp-tags] | untested |
| Code | wraps, with copy buttons | wraps; no copy buttons | untested | untested |
| Table of contents | sidebar, with parts | nested under the three parts | untested | untested |

[^kdp-img]: Kindle Direct Publishing, *Image Guidelines – Reflowable*,
    <https://kdp.amazon.com/en_US/help/topic/G75V4YX5X8GRGXWV>, read 2026-11-12:
    "Kindle devices and reading applications do not support TIFF, multi-frame GIFs, or images
    with transparent areas"; "We recommend removing SVG tags and using the image tag in HTML for images."
[^kdp-tags]: Kindle Direct Publishing, *HTML and CSS Tags Supported in Kindle Format 8*,
    <https://kdp.amazon.com/en_US/help/topic/GG5R7N649LECKP7U>, read 2026-11-12: no `math`
    element is listed.

Known limitations:

- **Terminal animations on a phone.** They are 800 px wide with 18 px text, so on a phone
  screen the text is about half that size. The commands they show are also printed in the text
  beside each one.
- **Kindle.** Amazon converts EPUB for Kindle; the book has not been through that conversion.
- **Apple Books, Kobo and the asset guides.** Kobo's and Apple's own guidelines could not be
  read on 2026-11-12 (Kobo's help site refused automated access; Apple's guide needs
  JavaScript), so this table cites neither.
