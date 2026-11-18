"""Print _site/slides.html to _site/slides.pdf with headless Chrome, and check every page.

Run from the project root, after `quarto render` (or `quarto render slides.qmd`):

    uv run python scripts/deck_pdf.py

Quarto has no PDF export for Reveal.js decks; Reveal's own print view (`?print-pdf`)
printed by a browser is the documented route. Headless Chrome sometimes prints before the
deck has laid itself out, giving blank pages, so each try is checked and retried, up to
`TRIES` times:

- The page count must equal the number of slides. The slides are counted in slides.html:
  every `<section>` inside `<div class="slides">` with no `<section>` inside it (a vertical
  stack's parent is not printed; each of its slides is). A slide too tall for its page
  also fails this check, because Reveal prints it on two pages.
- Each page must contain the first words of its slide's title, so a blank page fails.

Chrome is found from the CHROME environment variable, then the macOS default location,
then `google-chrome`, `google-chrome-stable`, `chromium` or `chromium-browser` on PATH.
It runs with a throwaway profile, so an open Chrome window is not disturbed. The print
options (`pdf-separate-fragments`, `show-notes`) are set in slides.qmd's YAML.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

from pypdf import PdfReader

DECK = Path("_site/slides.html")
PDF = Path("_site/slides.pdf")
TRIES = 3
MAC_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LINUX_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]


class Slides(HTMLParser):
    """Collect the title of every printed slide: the leaf <section>s of div.slides."""

    def __init__(self) -> None:
        super().__init__()
        self.inside = False     # past <div class="slides">
        self.sections = []      # open sections: [has a child section, title text]
        self.in_heading = False
        self.titles: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == "div" and "slides" in (dict(attrs).get("class") or "").split():
            self.inside = True
        elif self.inside and tag == "section":
            if self.sections:
                self.sections[-1][0] = True
            self.sections.append([False, ""])
        elif tag in ("h1", "h2") and self.sections and not self.sections[-1][1]:
            self.in_heading = True

    def handle_endtag(self, tag: str) -> None:
        if tag in ("h1", "h2"):
            self.in_heading = False
        elif tag == "section" and self.sections:
            has_child, title = self.sections.pop()
            if not has_child:
                self.titles.append(" ".join(title.split()))

    def handle_data(self, data: str) -> None:
        if self.in_heading:
            self.sections[-1][1] += data


def slide_titles(html: str) -> list[str]:
    """The title of each slide Reveal prints, in order."""
    parser = Slides()
    parser.feed(html)
    return parser.titles


def find_chrome() -> str:
    """The Chrome or Chromium executable to print with."""
    candidates = [os.environ.get("CHROME"), MAC_CHROME] + [shutil.which(n) for n in LINUX_NAMES]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    sys.exit("No Chrome found: set CHROME to the path of Chrome or Chromium.")


def print_pdf(chrome: str) -> str:
    """Print the deck's print view to slides.pdf with a throwaway profile. Returns what went
    wrong in Chrome itself (a hang, an error exit), or "" when it finished."""
    url = f"{DECK.resolve().as_uri()}?print-pdf"
    with tempfile.TemporaryDirectory() as profile:
        try:
            run = subprocess.run(
                [chrome, "--headless", "--disable-gpu", f"--user-data-dir={profile}",
                 "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
                 "--virtual-time-budget=20000", f"--print-to-pdf={PDF}", url],
                check=False, capture_output=True, text=True, timeout=180)
        except subprocess.TimeoutExpired:
            return "Chrome did not finish within 180 s"
    if run.returncode != 0:
        last = (run.stderr.strip().splitlines() or ["no message"])[-1]
        return f"Chrome exited with {run.returncode}: {last}"
    return ""


def squash(text: str) -> str:
    """ASCII letters and digits only, lower case: a PDF's text can lose spaces, and its
    apostrophes and quotes can come back as other characters."""
    return re.sub(r"[^0-9a-z]+", "", text.lower())


def problems(titles: list[str]) -> list[str]:
    """What is wrong with slides.pdf, or nothing."""
    if not PDF.exists():
        return ["Chrome wrote no PDF"]
    try:
        pages = PdfReader(PDF).pages
    except Exception as error:  # a half-written PDF: count it as a failed try, and retry
        return [f"the PDF could not be read ({error})"]
    if len(pages) != len(titles):
        return [f"{len(pages)} pages for {len(titles)} slides"]
    found = []
    for number, (page, title) in enumerate(zip(pages, titles), start=1):
        start = squash(" ".join(title.split()[:4]))
        if start not in squash(page.extract_text() or ""):
            found.append(f"page {number} does not show its title, {title!r}")
    return found


def main() -> int:
    if not DECK.exists():
        sys.exit(f"No {DECK}: run `uv run quarto render slides.qmd` first.")
    titles = slide_titles(DECK.read_text(encoding="utf-8"))
    chrome = find_chrome()
    for attempt in range(1, TRIES + 1):
        PDF.unlink(missing_ok=True)
        chrome_problem = print_pdf(chrome)
        found = ([chrome_problem] if chrome_problem else []) + problems(titles)
        if not found:
            print(f"Wrote {PDF}: {len(titles)} pages, one per slide (try {attempt} of {TRIES})")
            return 0
        print(f"Try {attempt} of {TRIES}: " + "; ".join(found), file=sys.stderr)
    print(f"{PDF} is still wrong after {TRIES} tries; open {DECK}?print-pdf in Chrome "
          "and print it by hand (Save as PDF, no margins, background graphics on).",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
