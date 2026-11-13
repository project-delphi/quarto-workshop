"""media/figures/london-*: pictures of the finished London project's outputs (Chapters 6, 7).

Renders a temporary copy of examples/london (the example itself is not touched) with its own
uv environment, then saves the first page of the flyer, the square advert and the white paper
(macOS Quick Look draws a PDF's first page, _pdf.py; the advert, a full-bleed photo, as a JPEG) and screenshots the dashboard and the guide
in Chrome. Run from book/media/capture: uv run --with playwright python london_outputs.py
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

from _pdf import first_page_png

BOOK = Path(__file__).resolve().parents[2]
EXAMPLE = BOOK.parent / "examples" / "london"
OUT = BOOK / "media" / "figures"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="london-")) / "london"
    shutil.copytree(EXAMPLE, work, ignore=shutil.ignore_patterns(".venv", "_site", ".quarto", "*_files"))
    subprocess.run(["uv", "run", "quarto", "render"], cwd=work, check=True)
    site = work / "_site"
    for pdf, name, size in [("london-flyer.pdf", "london-flyer.png", 1400),
                            ("london-social.pdf", "london-social.jpg", 1200),
                            ("london-whitepaper.pdf", "london-whitepaper-p1.png", 1400)]:
        first_page_png(site / pdf, OUT / name, size)
        print("figure", (OUT / name).relative_to(BOOK))
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        page = b.new_page(viewport={"width": 1400, "height": 860}, device_scale_factor=1)
        page.goto((site / "london-dashboard.html").as_uri())
        page.wait_for_timeout(6000)  # Plotly draws after load
        page.screenshot(path=str(OUT / "london-dashboard.png"))
        print("figure", (OUT / "london-dashboard.png").relative_to(BOOK))
        page.goto((site / "london.html").as_uri())
        page.wait_for_timeout(1500)
        page.screenshot(path=str(OUT / "london-guide.png"))
        print("figure", (OUT / "london-guide.png").relative_to(BOOK))
        b.close()
    shutil.rmtree(work.parent, ignore_errors=True)


if __name__ == "__main__":
    main()
