"""Screenshot EPUB chapters as an e-reader would show them (book/PLAN.md §6.4).

Unzips the EPUB, opens chapter XHTML files with the book's epub.css in Chrome (through
Playwright) at phone and tablet widths, once in the reader's default light theme and once
in a simulated night theme (the reader overrides page and text colours, as Apple Books and
Kobo night modes do), and saves full-page PNGs to _book/shots/.

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
# Reader night themes override page colours; images and the book's tints stay as they are.
NIGHT = "html, body { background: #111 !important; color: #ddd !important; }"
PAGE = "body { margin: 1.2em 1.1em !important; max-width: 40em; }"


def main(epub: str, names: list[str]) -> None:
    out = Path(epub).parent.parent / "shots"
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        zipfile.ZipFile(epub).extractall(tmp)
        text = Path(tmp, "EPUB", "text")
        files = sorted(text.glob("ch*.xhtml"))
        if names:
            files = [f for f in files if f.stem in names]
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome")
            for size, (w, h) in SIZES.items():
                for theme in ("light", "night"):
                    page = browser.new_page(viewport={"width": w, "height": h},
                                            device_scale_factor=2,
                                            color_scheme="dark" if theme == "night" else "light")
                    for f in files:
                        page.goto(f.as_uri())
                        page.add_style_tag(content=PAGE + (NIGHT if theme == "night" else ""))
                        overflow = page.evaluate(
                            "document.documentElement.scrollWidth > window.innerWidth + 1")
                        shot = out / f"{f.stem}-{size}-{theme}.png"
                        page.screenshot(path=str(shot), full_page=True)
                        flag = "  HORIZONTAL OVERFLOW" if overflow else ""
                        print(f"{shot.name}{flag}")
                    page.close()
            browser.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
