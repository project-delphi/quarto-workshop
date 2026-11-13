# Book edition of the workshop (book/README.md). The decks still build with `quarto render`.
SHELL := /bin/bash
.SHELLFLAGS := -eo pipefail -c

BOOK := book
EPUB := $(BOOK)/_book/epub/prompt-check-publish.epub
EPUBCHECK_VERSION := 5.4.0
EPUBCHECK_DIR ?= $(HOME)/.cache/quarto-book
EPUBCHECK_JAR := $(EPUBCHECK_DIR)/epubcheck-$(EPUBCHECK_VERSION)/epubcheck.jar
# A user-level python3 kernelspec can shadow the book's environment; point Jupyter at it.
QUARTO_BOOK := cd $(BOOK) && JUPYTER_PATH="$$PWD/.venv/share/jupyter" uv run quarto

.PHONY: book book-sync book-html book-epub book-fresh epubcheck media book-shots book-publish deck site

## book: render the HTML and EPUB editions, post-process the EPUB, run epubcheck, check the
## EPUB's links into the website edition, and check the live scenes' data against the deck's
book: book-html book-epub
	cd $(BOOK) && uv run python scripts/check_live_links.py $(EPUB:$(BOOK)/%=%)
	cd $(BOOK) && uv run python scripts/check_scenes.py

## book-sync: chapter lists for both editions, and fresh copies of the deck's assets
## (its three.js bundle, Tunja explorer and reused images; book/media/build.py step "deck")
book-sync:
	cd $(BOOK) && uv run python scripts/sync_chapters.py
	cd $(BOOK) && uv run python media/build.py deck

book-html: book-sync
	$(QUARTO_BOOK) render --profile html --to html
	@if grep -rl '<ol class="example"' $(BOOK)/_book/html; then echo "book-html: a line starting '@label.' became an example list in the file(s) above; rewrap it" >&2; exit 1; fi

book-epub: book-sync
	$(QUARTO_BOOK) render --profile epub --to epub
	cd $(BOOK) && uv run python scripts/epub_postprocess.py _book/epub/prompt-check-publish.epub
	$(MAKE) epubcheck

## book-fresh: re-execute every chapter (after changing examples/*/data or analysis.py)
book-fresh:
	rm -rf $(BOOK)/_freeze
	$(MAKE) book

## epubcheck: validate the EPUB; the report is saved beside it
epubcheck: $(EPUBCHECK_JAR)
	java -jar $(EPUBCHECK_JAR) --failonwarnings $(EPUB) 2>&1 | tee $(BOOK)/_book/epubcheck.txt

$(EPUBCHECK_JAR):
	mkdir -p $(EPUBCHECK_DIR)
	curl --http1.1 -fSL -o $(EPUBCHECK_DIR)/epubcheck-$(EPUBCHECK_VERSION).zip \
	  https://github.com/w3c/epubcheck/releases/download/v$(EPUBCHECK_VERSION)/epubcheck-$(EPUBCHECK_VERSION).zip
	cd $(EPUBCHECK_DIR) && unzip -q -o epubcheck-$(EPUBCHECK_VERSION).zip

## media: re-record GIFs and stills, rasterise diagrams, cover and QR codes (only when asked).
## STEPS picks steps of book/media/build.py; ONLY="name" limits the tapes and capture steps.
STEPS ?=
media:
	cd $(BOOK) && ONLY="$(ONLY)" uv run --with playwright --with segno python media/build.py $(STEPS)

## book-shots: screenshot EPUB chapters at phone and tablet widths, light and night
book-shots:
	cd $(BOOK) && uv run --with playwright python scripts/shoot_epub.py $(EPUB:$(BOOK)/%=%)

## book-publish: copy the HTML edition and the EPUB into docs/book/ for GitHub Pages
## (build both first: it stops before touching docs/book/ if either is missing). Quarto copies
## every frozen figure folder into the HTML edition; the EPUB's (figure-epub/) are left out.
book-publish:
	@test -f $(BOOK)/_book/html/index.html -a -f $(EPUB) \
	  || { echo "book-publish: build both editions first (make book)" >&2; exit 1; }
	rsync -a --delete --delete-excluded --exclude $(notdir $(EPUB)) --exclude 'figure-epub/' \
	  $(BOOK)/_book/html/ docs/book/
	cp $(EPUB) docs/book/

## deck: render the workshop decks into docs/, keeping docs/book/ exactly as it was (a full
## render empties docs/). A copy waits in .book-keep/; if the render fails, the next run keeps it.
deck:
	if [ -d docs/book ]; then rm -rf .book-keep && cp -R docs/book .book-keep; fi
	QUARTO_PYTHON="$$PWD/.conda/bin/python" JUPYTER_PATH="$$PWD/.conda/share/jupyter" quarto render
	if [ -d .book-keep ]; then rsync -a --delete .book-keep/ docs/book/ && rm -rf .book-keep; fi

## site: everything GitHub Pages serves from docs/: the decks, then the book (in this order)
site:
	$(MAKE) deck
	$(MAKE) book
	$(MAKE) book-publish
