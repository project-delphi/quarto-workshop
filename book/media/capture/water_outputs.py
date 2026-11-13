"""media/figures/water-*.png: pictures of the finished water project's outputs (Chapter 14).

Renders a temporary copy of examples/water (the example itself is not touched) with its own uv
environment, including its pre-render analysis, then saves the first page of the report PDF and
of the white paper (macOS Quick Look draws a PDF's first page, _pdf.py) and screenshots the dashboard,
the council slides and the blog post in Chrome. Run from book/media/capture:
    uv run --with playwright python water_outputs.py
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

from _pdf import first_page_png

BOOK = Path(__file__).resolve().parents[2]
EXAMPLE = BOOK.parent / "examples" / "water"
OUT = BOOK / "media" / "figures"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="water-")) / "water"
    shutil.copytree(EXAMPLE, work, ignore=shutil.ignore_patterns(
        ".venv", "_site", ".quarto", "*_files", "outputs", "raw", "__pycache__"))
    subprocess.run(["uv", "run", "quarto", "render"], cwd=work, check=True)
    site = work / "_site"
    for pdf, name in [("report.pdf", "water-report-p1.png"), ("whitepaper.pdf", "water-whitepaper-p1.png")]:
        first_page_png(site / pdf, OUT / name, 1400)
        print("figure", (OUT / name).relative_to(BOOK))
    post = next(site.glob("posts/*/index.html"))
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        page = b.new_page(viewport={"width": 1400, "height": 860}, device_scale_factor=1)
        page.goto((site / "dashboard.html").as_uri())
        page.wait_for_timeout(9000)  # Plotly draws the maps after load
        page.screenshot(path=str(OUT / "water-dashboard.png"))
        page.goto((site / "slides.html").as_uri() + "#/3")
        page.wait_for_timeout(2500)
        page.screenshot(path=str(OUT / "water-slides.png"))
        page.set_viewport_size({"width": 1200, "height": 860})
        page.goto(post.as_uri())
        page.wait_for_timeout(2000)
        page.screenshot(path=str(OUT / "water-post.png"))
        b.close()
    for name in ("water-dashboard.png", "water-slides.png", "water-post.png"):
        print("figure", (OUT / name).relative_to(BOOK))
    shutil.rmtree(work.parent, ignore_errors=True)


if __name__ == "__main__":
    main()
