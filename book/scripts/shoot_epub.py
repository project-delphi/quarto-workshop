"""Screenshot EPUB chapters as an e-reader would show them (book/PLAN.md §6.4).

Unzips the EPUB, opens chapter XHTML files with the book's epub.css in Chrome (through
Playwright) at phone and tablet widths, once in the reader's default light theme and once
in a simulated night theme (the reader overrides page and text colours, as Apple Books and
Kobo night modes do). Each page is saved screen by screen (full-page shots of long chapters
exceed Chrome's texture limit) to _book/shots/, and any element that scrolls or sticks out
sideways, such as an unwrapped code block, is reported.

    uv run --with playwright python scripts/shoot_epub.py _book/epub/book.epub [ch004 ch009 ...]

With no chapter names it shoots every chapter.
"""
from __future__ import annotations

import sys
import tempfile
import zipfile
from pathlib import Path

from playwright.sync_api import sync_playwright

SIZES = {"phone": (390, 844), "tablet": (820, 1180)}
NIGHT = "html, body { background: #111 !important; color: #ddd !important; }"
PAGE = "body { margin: 1.2em 1.1em !important; max-width: 40em; }"
SIDEWAYS = """[...document.querySelectorAll('pre, code, table, figure, img, div')]
  .filter(e => (e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflowX !== 'visible')
               || e.getBoundingClientRect().right > window.innerWidth + 2)
  .map(e => e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ')[0] : '')
            + ': ' + (e.textContent || e.getAttribute('src') || '').trim().slice(0, 50))"""


def main(epub: str, names: list[str]) -> None:
    out = Path(epub).parent.parent / "shots"
    out.mkdir(parents=True, exist_ok=True)
    problems = 0
    with tempfile.TemporaryDirectory() as tmp:
        zipfile.ZipFile(epub).extractall(tmp)
        files = sorted(Path(tmp, "EPUB", "text").glob("ch*.xhtml"))
        if names:
            files = [f for f in files if f.stem in names]
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome")
            for size, (w, h) in SIZES.items():
                for theme in ("light", "night"):
                    page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2,
                                            color_scheme="dark" if theme == "night" else "light")
                    for f in files:
                        page.goto(f.as_uri())
                        page.add_style_tag(content=PAGE + (NIGHT if theme == "night" else ""))
                        page.wait_for_timeout(200)
                        if theme == "light":
                            for item in page.evaluate(SIDEWAYS):
                                problems += 1
                                print(f"{f.stem} {size}: sideways {item}")
                        total = page.evaluate("document.documentElement.scrollHeight")
                        for i, y in enumerate(range(0, total, h)):
                            page.evaluate(f"window.scrollTo(0, {y})")
                            page.screenshot(path=str(out / f"{f.stem}-{size}-{theme}-{i:02d}.png"))
                    page.close()
            browser.close()
    print(f"shots in {out}; {problems} sideways element(s)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
