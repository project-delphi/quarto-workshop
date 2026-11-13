"""media/figures/toy-md.png and toy-qmd.png: the two toy files as Quarto renders them (Ch. 4, 5).

Copies media/examples/toy.md and toy.qmd into a scratch folder with what they need (the photo
toy.md shows, examples/london/images/big-ben.jpg, and the data toy.qmd reads,
examples/london/data/attractions.csv), renders each with the book's own environment (uv run
in book/, with JUPYTER_PATH set to its kernels as the Makefile does), and screenshots each
page in Chrome, whole, at a phone's width. The toy files themselves are not touched, and the
chapters print them from the same files, so the pictures and the text cannot drift apart.
Run from book/media/capture: uv run --with playwright python toy_examples.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[2]
LONDON = BOOK.parent / "examples" / "london"
TOYS = BOOK / "media" / "examples"
OUT = BOOK / "media" / "figures"
WIDTH, SCALE = 460, 2  # CSS pixels and device pixels per CSS pixel: a large phone, drawn sharp
PAD = 20  # CSS pixels kept above and below the page's content


def render(work: Path, name: str) -> Path:
    """Render work/name with the book's environment and return the HTML file it wrote."""
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}  # uv picks book/.venv
    env["JUPYTER_PATH"] = str(BOOK / ".venv" / "share" / "jupyter")  # not a user-level kernel
    subprocess.run(["uv", "run", "--project", str(BOOK), "quarto", "render", name],
                   cwd=work, env=env, check=True)
    return work / (Path(name).stem + ".html")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="toy-"))
    shots = []
    for name, extras in [("toy.md", {"big-ben.jpg": LONDON / "images" / "big-ben.jpg"}),
                         ("toy.qmd", {"data/attractions.csv": LONDON / "data" / "attractions.csv"})]:
        work = root / Path(name).suffix.lstrip(".")  # one folder each: both write toy.html
        work.mkdir()
        shutil.copy(TOYS / name, work / name)
        for rel, src in extras.items():
            (work / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, work / rel)
        shots.append((render(work, name), OUT / f"toy-{Path(name).suffix.lstrip('.')}.png"))
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        page = b.new_page(viewport={"width": WIDTH, "height": 800}, device_scale_factor=SCALE)
        for html, png in shots:
            page.goto(html.as_uri(), wait_until="load")
            page.wait_for_timeout(800)
            # The whole page, cropped to its innermost elements: no empty margins above or below.
            top, bottom = page.evaluate("""() => {
                const r = [...document.querySelectorAll("main *")].filter(e => !e.children.length)
                    .map(e => e.getBoundingClientRect()).filter(b => b.height > 0);
                return [Math.min(...r.map(b => b.top)) + scrollY, Math.max(...r.map(b => b.bottom)) + scrollY];
            }""")
            top = max(0, top - PAD)
            clip = {"x": 0, "y": top, "width": WIDTH, "height": bottom + PAD - top}
            page.screenshot(path=str(png), full_page=True, clip=clip)
            print("figure", png.relative_to(BOOK), f"{WIDTH} x {clip['height']:.0f} CSS px")
        b.close()
    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
