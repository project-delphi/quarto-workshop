"""The two toy files as Quarto renders them (Chapters 6 and 7).

Copies media/examples/toy.md and toy.qmd into a scratch folder with what they need (the photo
toy.md shows, examples/london/images/big-ben.jpg, and the data toy.qmd reads,
examples/london/data/attractions.csv), renders each with the book's own environment (uv run
in book/, with JUPYTER_PATH set to its kernels as the Makefile does), and screenshots the
page in Chrome. The toy files themselves are not touched, and the chapters print them from the
same files, so the pictures and the text cannot drift apart.

Steps (arguments, or CAPTURE_STEPS; names another capture script owns are ignored):
- md:  toy-md-1.png and toy-md-2.png, the halves of toy.md either side of its `---` rule
       (line 23: the first picture ends above the rule, the second starts with it), each cropped
       from toy.html at a 480 px viewport and drawn at twice the pixel density. They have new
       names because the Spanish edition reads media/figures through a symlink and keeps showing
       toy-md.png until it is translated; this script no longer writes that file.
- qmd: toy-qmd.png, the whole of toy.qmd's page at a larger phone's width.

Run from book/media/capture: uv run --with playwright python toy_examples.py [md] [qmd]
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[2]
LONDON = BOOK.parent / "examples" / "london"
TOYS = BOOK / "media" / "examples"
OUT = BOOK / "media" / "figures"
WIDTH, SCALE = 460, 2  # CSS pixels and device pixels per CSS pixel: a large phone, drawn sharp
PHONE = 480  # the md pair: CSS pixels wide (each half then about as tall as wide), drawn at SCALE
PAD = 20  # CSS pixels kept above and below the page's content

BIG_BEN = {"big-ben.jpg": LONDON / "images" / "big-ben.jpg"}
ATTRACTIONS = {"data/attractions.csv": LONDON / "data" / "attractions.csv"}

# Top and bottom (CSS px from the page's top) of the content above the rule, and of the rule and
# what follows it, with the smallest text size drawn in each half.
# Each half's extent and smallest text, from every line of text (a paragraph with bold or a
# link in it is measured line by line) and the boxes of pictures, rules, tables and code.
MD_PARTS = """() => {
    const main = document.querySelector("main"), hr = main && main.querySelector("hr");
    if (!hr) return null;
    const cut = hr.getBoundingClientRect().top + scrollY;
    const items = [];  // [top, bottom, font size, or null for a box]
    const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        if (!n.textContent.trim()) continue;
        const range = document.createRange();
        range.selectNodeContents(n);
        const size = parseFloat(getComputedStyle(n.parentElement).fontSize);
        for (const r of range.getClientRects())
            if (r.width > 1 && r.height > 1) items.push([r.top + scrollY, r.bottom + scrollY, size]);
    }
    for (const e of main.querySelectorAll("img, hr, table, pre, input")) {
        const r = e.getBoundingClientRect();
        if (r.height > 0) items.push([r.top + scrollY, r.bottom + scrollY, null]);
    }
    const part = list => ({top: Math.min(...list.map(i => i[0])), bottom: Math.max(...list.map(i => i[1])),
        text: Math.min(...list.filter(i => i[2] !== null).map(i => i[2]))});
    return {first: part(items.filter(i => i[1] <= cut)), second: part(items.filter(i => i[0] >= cut))};
}"""


def render(work: Path, name: str) -> Path:
    """Render work/name with the book's environment and return the HTML file it wrote."""
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}  # uv picks book/.venv
    env["JUPYTER_PATH"] = str(BOOK / ".venv" / "share" / "jupyter")  # not a user-level kernel
    subprocess.run(["uv", "run", "--project", str(BOOK), "quarto", "render", name],
                   cwd=work, env=env, check=True)
    return work / (Path(name).stem + ".html")


def prepare(root: Path, name: str, extras: dict) -> Path:
    """Copy a toy file and what it needs into its own folder (both write toy.html); render it."""
    work = root / Path(name).suffix.lstrip(".")
    work.mkdir()
    shutil.copy(TOYS / name, work / name)
    for rel, src in extras.items():
        (work / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, work / rel)
    return render(work, name)


def step_md() -> None:
    from PIL import Image

    root = Path(tempfile.mkdtemp(prefix="toy-"))
    try:
        html = prepare(root, "toy.md", BIG_BEN)
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome")
            page = b.new_page(viewport={"width": PHONE, "height": 800}, device_scale_factor=SCALE)
            page.goto(html.as_uri(), wait_until="load")
            page.wait_for_timeout(800)
            at = page.evaluate(MD_PARTS)
            if at is None:
                raise SystemExit(f"{html.name}: no rule (---) to split the picture at")
            for n, key in ((1, "first"), (2, "second")):
                part = at[key]
                top = max(0, part["top"] - PAD)
                clip = {"x": 0, "y": top, "width": PHONE, "height": part["bottom"] + PAD - top}
                png = OUT / f"toy-md-{n}.png"
                page.screenshot(path=str(png), full_page=True, clip=clip)
                if n == 1:  # text only: a palette keeps the file small; the photo stays full colour
                    Image.open(png).convert("RGB").quantize(colors=128, dither=Image.Dither.NONE).save(png, optimize=True)
                h = clip["height"]
                print("figure", png.relative_to(BOOK),
                      f"{PHONE} x {h:.0f} CSS px at {SCALE}x (h/w {h / PHONE:.2f});",
                      f"smallest text {part['text'] * SCALE:.0f} px in the image")
            b.close()
    finally:
        shutil.rmtree(root, ignore_errors=True)


def step_qmd() -> None:
    root = Path(tempfile.mkdtemp(prefix="toy-"))
    try:
        html = prepare(root, "toy.qmd", ATTRACTIONS)
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome")
            page = b.new_page(viewport={"width": WIDTH, "height": 800}, device_scale_factor=SCALE)
            png = OUT / "toy-qmd.png"
            page.goto(html.as_uri(), wait_until="load")
            page.wait_for_timeout(800)
            # The whole page, cropped to its innermost elements: no empty margins above or below.
            top, bottom = page.evaluate("""() => {
                const r = [...document.querySelectorAll("main *")].filter(e => !e.children.length)
                    .map(e => e.getBoundingClientRect()).filter(b => b.height > 0);
                if (!r.length) return null;
                return [Math.min(...r.map(b => b.top)) + scrollY, Math.max(...r.map(b => b.bottom)) + scrollY];
            }""") or (None, None)
            if top is None:
                raise SystemExit(f"{html.name}: the rendered page shows nothing to picture")
            top = max(0, top - PAD)
            clip = {"x": 0, "y": top, "width": WIDTH, "height": bottom + PAD - top}
            page.screenshot(path=str(png), full_page=True, clip=clip)
            print("figure", png.relative_to(BOOK), f"{WIDTH} x {clip['height']:.0f} CSS px")
            b.close()
    finally:
        shutil.rmtree(root, ignore_errors=True)


STEPS = {"md": step_md, "qmd": step_qmd}


def main(names: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # CAPTURE_STEPS is read by every capture script that `make media STEPS=capture` runs, so
    # names another script owns are left to it; names given as arguments must exist here.
    named = os.environ.get("CAPTURE_STEPS", "").split()
    unknown = [n for n in names if n not in STEPS]
    if unknown:
        raise SystemExit(f"unknown step(s) {unknown}; the steps are {list(STEPS)}")
    for name in names or ([n for n in named if n in STEPS] if named else list(STEPS)):
        STEPS[name]()


if __name__ == "__main__":
    main(sys.argv[1:])
