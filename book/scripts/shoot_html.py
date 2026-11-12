"""Screenshot HTML-edition pages at desktop and laptop sizes (book/PLAN.md §6.4, AGENTS.md).

    uv run --with playwright python scripts/shoot_html.py chapters/02-assistant.html [...]

Saves full-page PNGs, light and dark, to _book/shots/ and reports horizontal overflow and
images that failed to load.
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[1]
SITE = BOOK / "_book" / "html"
SIZES = {"desktop": (1440, 1000), "laptop": (1366, 768)}


def main(pages: list[str]) -> None:
    out = BOOK / "_book" / "shots"
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader",
                                                            "--enable-unsafe-swiftshader"])
        for size, (w, h) in SIZES.items():
            for scheme in ("light", "dark"):
                page = browser.new_page(viewport={"width": w, "height": h}, color_scheme=scheme)
                for rel in pages:
                    page.goto((SITE / rel).as_uri())
                    if scheme == "dark":  # Quarto's toggle follows the stored choice, not the OS
                        page.evaluate("window.quartoToggleColorScheme && "
                                      "document.body.classList.contains('quarto-light') && "
                                      "window.quartoToggleColorScheme()")
                    page.wait_for_timeout(800)
                    broken = page.evaluate("[...document.images].filter(i => i.complete && "
                                           "i.naturalWidth === 0).map(i => i.src)")
                    overflow = page.evaluate(
                        "document.documentElement.scrollWidth > window.innerWidth + 1")
                    name = rel.replace("/", "_").replace(".html", "")
                    shot = out / f"html-{name}-{size}-{scheme}.png"
                    page.screenshot(path=str(shot), full_page=True)
                    print(shot.name, "OVERFLOW" if overflow else "", *broken)
                page.close()
        browser.close()


if __name__ == "__main__":
    main(sys.argv[1:])
