# Book edition of the workshop (book/README.md). The decks still build with `quarto render`.
SHELL := /bin/bash
.SHELLFLAGS := -eo pipefail -c

BOOK := book
EPUB := $(BOOK)/_book/epub/one-source-every-format.epub
EPUBCHECK_VERSION := 5.4.0
EPUBCHECK_DIR ?= $(HOME)/.cache/quarto-book
EPUBCHECK_JAR := $(EPUBCHECK_DIR)/epubcheck-$(EPUBCHECK_VERSION)/epubcheck.jar
# A user-level python3 kernelspec can shadow the book's environment; point Jupyter at it.
QUARTO_BOOK := cd $(BOOK) && JUPYTER_PATH="$$PWD/.venv/share/jupyter" uv run quarto

.PHONY: book book-sync book-html book-epub book-fresh epubcheck media book-shots book-publish deck site

## book: render the HTML and EPUB editions, post-process the EPUB, run epubcheck, and check
## the EPUB's links into the website edition
book: book-html book-epub
	cd $(BOOK) && uv run python scripts/check_live_links.py $(EPUB:$(BOOK)/%=%)

book-sync:
	cd $(BOOK) && uv run python scripts/sync_chapters.py

book-html: book-sync
	$(QUARTO_BOOK) render --profile html --to html

book-epub: book-sync
	$(QUARTO_BOOK) render --profile epub --to epub
	cd $(BOOK) && uv run python scripts/epub_postprocess.py _book/epub/one-source-every-format.epub
	$(MAKE) epubcheck

## book-fresh: re-execute every chapter (after changing examples/*/data or analysis.py)
book-fresh:
	rm -rf $(BOOK)/_freeze
	$(MAKE) book

## epubcheck: validate the EPUB; the report is saved beside it
epubcheck: $(EPUBCHECK_JAR)
	java -jar $(EPUBCHECK_JAR) $(EPUB) 2>&1 | tee $(BOOK)/_book/epubcheck.txt

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
book-publish:
	rsync -a --delete $(BOOK)/_book/html/ docs/book/
	cp $(EPUB) docs/book/

## deck: render the workshop decks into docs/ (the post-render script keeps docs/book/)
deck:
	QUARTO_PYTHON="$$PWD/.conda/bin/python" JUPYTER_PATH="$$PWD/.conda/share/jupyter" quarto render

## site: everything GitHub Pages serves from docs/: the decks, then the book (in this order)
site:
	$(MAKE) deck
	$(MAKE) book
	$(MAKE) book-publish
