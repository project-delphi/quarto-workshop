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

.PHONY: book book-sync book-html book-epub book-fresh epubcheck media book-shots book-publish deck site \
	ebook-media ebook-check book-release book-es book-es-sync book-es-html book-es-epub book-es-fresh \
	book-es-publish epubcheck-es book-store

## book: render the HTML and EPUB editions, post-process the EPUB, run epubcheck, check the
## EPUB's links into the website edition, and check the live scenes' data against the deck's
book: book-html book-epub
	cd $(BOOK) && uv run python scripts/check_live_links.py $(EPUB:$(BOOK)/%=%)
	cd $(BOOK) && uv run python scripts/check_scenes.py

## book-sync: chapter lists for both editions, and fresh copies of the deck's assets
## (its three.js bundle, Tunja explorer and reused images; book/media/build.py step "deck")
book-sync:
	cd $(BOOK) && uv run python scripts/sync_chapters.py
	cd $(BOOK) && uv run python scripts/thaw.py
	cd $(BOOK) && uv run python media/build.py deck

book-html: book-sync
	$(QUARTO_BOOK) render --profile html --to html
	@if grep -rl '<ol class="example"' $(BOOK)/_book/html; then echo "book-html: a line starting '@label.' became an example list in the file(s) above; rewrap it" >&2; exit 1; fi
	@if grep -rlE '<strong>\?@(sec|tbl|fig|eq)-' $(BOOK)/_book/html --include='*.html'; then echo "book-html: a cross-reference in the file(s) above names a section, table or figure that does not exist" >&2; exit 1; fi
	cd $(BOOK) && uv run python scripts/lang_switch.py

book-epub: book-sync
	$(QUARTO_BOOK) render --profile epub --to epub
	cd $(BOOK) && uv run python scripts/epub_postprocess.py _book/epub/prompt-check-publish.epub
	$(MAKE) epubcheck

## book-fresh: re-execute every chapter (after changing examples/*/data or analysis.py)
book-fresh:
	rm -rf $(BOOK)/_freeze
	$(MAKE) book

## epubcheck: validate the EPUB; the report is saved beside it. `set -o pipefail` is in the recipe
## because macOS's make 3.81 ignores .SHELLFLAGS, so tee would otherwise hide a failure.
epubcheck: $(EPUBCHECK_JAR)
	set -o pipefail; java -jar $(EPUBCHECK_JAR) --failonwarnings $(EPUB) 2>&1 | tee $(BOOK)/_book/epubcheck.txt

$(EPUBCHECK_JAR):
	mkdir -p $(EPUBCHECK_DIR)
	curl --http1.1 -fSL -o $(EPUBCHECK_DIR)/epubcheck-$(EPUBCHECK_VERSION).zip \
	  https://github.com/w3c/epubcheck/releases/download/v$(EPUBCHECK_VERSION)/epubcheck-$(EPUBCHECK_VERSION).zip
	cd $(EPUBCHECK_DIR) && unzip -q -o epubcheck-$(EPUBCHECK_VERSION).zip

## media: re-record GIFs and stills, rasterise diagrams, cover and the QR code (only when asked).
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
## The Spanish edition in docs/book/es/ is protected (make book-es-publish writes it).
book-publish:
	@test -f $(BOOK)/_book/html/index.html -a -f $(EPUB) \
	  || { echo "book-publish: build both editions first (make book)" >&2; exit 1; }
	rsync -a --delete --delete-excluded --exclude $(notdir $(EPUB)) --exclude 'figure-epub/' \
	  --filter 'P /es/' $(BOOK)/_book/html/ docs/book/
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
	$(MAKE) book-es
	$(MAKE) book-es-publish

## ebook-media: remake the landing page's media and <head> (ebook/media/, ebook/_head.html).
## STEPS picks steps of scripts/ebook_media.py: fonts cover og icons clips inside head.
## EDITION=es makes the Spanish page's own media (cover og inside head qr) in ebook/es/media/.
ebook-media:
	uv run --no-project --python 3.12 --with fonttools --with brotli --with pillow --with pyyaml \
	  --with playwright --with segno python scripts/ebook_media.py $(if $(filter es,$(EDITION)),--es) $(STEPS)

## ebook-check: check the rendered landing page (render it first with `make deck`): screenshots,
## the first screen on a phone, links, contents numbers, share card and JSON-LD, into _ebook-check/
ebook-check:
	uv run --no-project --python 3.12 --with playwright --with pillow python scripts/ebook_check.py $(if $(filter es,$(EDITION)),--es)

## ---- The Spanish edition (book-es/, translation/PLAN.md) --------------------------------------
## It shares book/'s environment, scripts, filters and styles, and its chapter list.
BOOK_ES := book-es
EPUB_ES := $(BOOK_ES)/_book/epub/prompt-check-publish-es.epub
QUARTO_BOOK_ES := cd $(BOOK_ES) && JUPYTER_PATH="$$PWD/../$(BOOK)/.venv/share/jupyter" uv run --project ../$(BOOK) quarto

## book-es: render the Spanish HTML and EPUB editions, post-process and check the EPUB, check its
## links into the Spanish website edition, compare every file with its English original, lint
## the glossary and scan the output for English left untranslated
book-es: book-es-html book-es-epub
	cd $(BOOK) && uv run python scripts/check_live_links.py ../$(EPUB_ES) --edition ../$(BOOK_ES)
	python3 translation/compare.py
	python3 translation/lint.py
	python3 translation/english_scan.py

## book-es-sync: the Spanish chapter lists (from book/_chapters.yml), the deck assets and copies of
## the animations and stills, which Quarto's resource globs cannot reach through a symlink
book-es-sync: book-sync
	cd $(BOOK) && uv run python scripts/sync_chapters.py --book ../$(BOOK_ES)
	rsync -a --delete $(BOOK)/media/gifs/ $(BOOK_ES)/media/gifs/
	rsync -a --delete $(BOOK)/media/stills/ $(BOOK_ES)/media/stills/

book-es-html: book-es-sync
	$(QUARTO_BOOK_ES) render --profile html --to html
	@if grep -rl '<ol class="example"' $(BOOK_ES)/_book/html; then echo "book-es-html: a line starting '@label.' became an example list in the file(s) above; rewrap it" >&2; exit 1; fi
	cd $(BOOK) && uv run python scripts/lang_switch.py

book-es-epub: book-es-sync
	$(QUARTO_BOOK_ES) render --profile epub --to epub
	cd $(BOOK) && uv run python scripts/epub_postprocess.py ../$(EPUB_ES)
	$(MAKE) epubcheck-es

## book-es-fresh: re-execute every Spanish chapter
book-es-fresh:
	rm -rf $(BOOK_ES)/_freeze
	$(MAKE) book-es

epubcheck-es: $(EPUBCHECK_JAR)
	set -o pipefail; java -jar $(EPUBCHECK_JAR) --failonwarnings $(EPUB_ES) 2>&1 | tee $(BOOK_ES)/_book/epubcheck.txt

## book-es-publish: copy the Spanish HTML edition and its EPUB into docs/book/es/
book-es-publish:
	@test -f $(BOOK_ES)/_book/html/index.html -a -f $(EPUB_ES) \
	  || { echo "book-es-publish: build both Spanish editions first (make book-es)" >&2; exit 1; }
	rsync -a --delete --delete-excluded --exclude $(notdir $(EPUB_ES)) --exclude 'figure-epub/' \
	  $(BOOK_ES)/_book/html/ docs/book/es/
	cp $(EPUB_ES) docs/book/es/

## book-store: the store editions for Apple Books and Google Play Books (book/STORES.md), made
## from the published EPUBs in docs/book/: GIFs become their first-frame stills. Each lands in
## book/_book/store/{en,es}/ with its cover and listing.md, and must pass EPUBCheck.
book-store: $(EPUBCHECK_JAR)
	cd $(BOOK) && uv run python scripts/store_edition.py ../docs/book/prompt-check-publish.epub _book/store/en
	cd $(BOOK) && uv run python scripts/store_edition.py ../docs/book/es/prompt-check-publish-es.epub _book/store/es
	java -jar $(EPUBCHECK_JAR) --failonwarnings $(BOOK)/_book/store/en/prompt-check-publish-store.epub
	java -jar $(EPUBCHECK_JAR) --failonwarnings $(BOOK)/_book/store/es/prompt-check-publish-es-store.epub

## book-release: attach the committed EPUB in docs/book/ to a new GitHub release, which the
## landing page's download buttons link to (releases/latest/download/). Run by the author, after
## the book is published and pushed: make book-release TAG=book-2026-11-13
book-release:
	@test -n "$(TAG)" || { echo "book-release: name the release, e.g. TAG=book-2026-11-13" >&2; exit 1; }
	for f in docs/book/prompt-check-publish.epub docs/book/es/prompt-check-publish-es.epub; do \
	  git ls-files --error-unmatch $$f >/dev/null && git diff --quiet HEAD -- $$f \
	  || { echo "book-release: commit $$f first" >&2; exit 1; }; done
	git fetch --quiet origin main && git merge-base --is-ancestor HEAD origin/main \
	  || { echo "book-release: merge this commit into main first" >&2; exit 1; }
	gh release create $(TAG) docs/book/prompt-check-publish.epub \
	  docs/book/es/prompt-check-publish-es.epub --latest \
	  --title "Prompt, Check, Publish ($(TAG))" \
	  --notes "The EPUB edition of Prompt, Check, Publish, and of its Spanish edition, Pide, revisa, publica. Read online: https://project-delphi.github.io/quarto-workshop/book/ (Spanish: https://project-delphi.github.io/quarto-workshop/book/es/)"
