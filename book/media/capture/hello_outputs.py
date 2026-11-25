"""media/figures/hello-42.png: what Chapter 4's test run ends with (its payoff picture).

Renders the chapter's hello.qmd (the file the agent writes in Step 6) in a temporary folder with
the book's own locked environment (uv run in book/, JUPYTER_PATH set to its kernels as the
Makefile does), as both formats it names: hello.html and hello.pdf (Quarto's bundled Typst; no
TeX). The picture stacks two crops, each showing "The answer is 42.": the web page at a 390 px
viewport (drawn at twice the pixel density) and the left of the PDF's first page below its title
(macOS Quick Look draws it, _pdf.py), its right edge faded, with a dashed rule between them. The 42 is the file's own output.

Run from book/media/capture (or CAPTURE_STEPS=hello; names another script owns are ignored):
    uv run --with playwright python hello_outputs.py [hello]
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from io import BytesIO
from pathlib import Path

from playwright.sync_api import sync_playwright

from _pdf import first_page_png

BOOK = Path(__file__).resolve().parents[2]
OUT = BOOK / "media" / "figures"
PHONE, SCALE = 390, 2  # CSS pixels wide, and device pixels per CSS pixel
PAD = 12  # CSS pixels kept round the web page's crop
GAP = 16  # CSS pixels between the crops, with a dashed rule across the middle

# The file Chapter 4's Step 6 has the agent write, as Chapter 1 prints it (01-quarto.qmd); Chapter 4
# points to that listing.
HELLO = '''---
title: "Hello"
format:
  html: default
  typst: default
---

```{python}
answer = 6 * 7
```

The answer is `{python} answer`.
'''


def render(work: Path) -> None:
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}  # uv picks book/.venv
    env["JUPYTER_PATH"] = str(BOOK / ".venv" / "share" / "jupyter")  # not a user-level kernel
    subprocess.run(["uv", "run", "--project", str(BOOK), "quarto", "render", "hello.qmd"],
                   cwd=work, env=env, check=True)


def web_crop(html: Path):
    """hello.html at a phone's width, cropped from the top to the answer's sentence."""
    from PIL import Image

    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        page = b.new_page(viewport={"width": PHONE, "height": 844}, device_scale_factor=SCALE)
        page.goto(html.as_uri(), wait_until="load")
        page.wait_for_timeout(800)
        at = page.evaluate("""() => {
            const p = [...document.querySelectorAll("main p")].find(e => e.textContent.includes("The answer is"));
            if (!p || !p.textContent.includes("42")) return null;
            const r = p.getBoundingClientRect();
            const sizes = [...document.querySelectorAll("main h1, main p")].map(e => parseFloat(getComputedStyle(e).fontSize));
            return {bottom: r.bottom + scrollY, text: Math.min(...sizes)};
        }""")
        if at is None:
            raise SystemExit(f"{html.name}: no sentence \"The answer is 42\" to picture")
        clip = {"x": 0, "y": 0, "width": PHONE, "height": at["bottom"] + PAD}
        img = Image.open(BytesIO(page.screenshot(full_page=True, clip=clip))).convert("RGB")
        b.close()
    return img, at["text"]


def pdf_crop(pdf: Path, width: int):
    """The top of the PDF's first page, side margins trimmed, scaled to width pixels."""
    from PIL import Image

    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "page.png"
        first_page_png(pdf, png, 2600)
        page = Image.open(png).convert("RGB")
    # Keep the page's ink above its page number, below its title (the web page above shows the
    # same title), from the text's left edge: the page's full width would draw the text too small
    # for a phone. The code block's grey band runs on past the crop, so the right edge fades to
    # white, a crop that says so.
    body = page.crop((0, 0, page.width, round(page.height * 0.85)))
    ink = Image.eval(body.convert("L"), lambda v: 255 if v < 200 else 0)
    if ink.getbbox() is None:
        raise SystemExit(f"{pdf.name}: the first page is blank")
    rows = [any(ink.getpixel((x, y)) for x in range(0, ink.width, 4)) for y in range(ink.height)]
    first = rows.index(True)
    after_title = next(y for y in range(first, len(rows)) if not rows[y])
    left, top, right, bottom = ink.crop((0, after_title, ink.width, ink.height)).getbbox()
    top, bottom = top + after_title, bottom + after_title
    page = page.crop((max(0, left - 40), max(0, top - 60), right + 120, bottom + 40))
    fade = round(page.width * 0.12)
    for i in range(fade):
        a = (i + 1) / fade
        col = page.crop((page.width - fade + i, 0, page.width - fade + i + 1, page.height))
        page.paste(Image.blend(col, Image.new("RGB", col.size, "white"), a), (page.width - fade + i, 0))
    return page.resize((width, round(page.height * width / page.width)), Image.LANCZOS)


def step_hello() -> None:
    from PIL import Image, ImageDraw

    work = Path(tempfile.mkdtemp(prefix="hello-")) / "quarto-test"
    try:
        work.mkdir()
        (work / "hello.qmd").write_text(HELLO)
        render(work)
        web, text = web_crop(work / "hello.html")
        pdf = pdf_crop(work / "hello.pdf", web.width)
    finally:
        shutil.rmtree(work.parent, ignore_errors=True)
    gap = GAP * SCALE
    out = Image.new("RGB", (web.width, web.height + gap + pdf.height), "white")
    out.paste(web, (0, 0))
    out.paste(pdf, (0, web.height + gap))
    rule, y = ImageDraw.Draw(out), web.height + gap // 2
    for x in range(PAD * SCALE, out.width - PAD * SCALE, 8 * SCALE):
        rule.line([(x, y), (x + 4 * SCALE, y)], fill="#b4bcc4", width=SCALE)
    png = OUT / "hello-42.png"
    out.save(png, optimize=True)
    w, h = out.width / SCALE, out.height / SCALE
    print("figure", png.relative_to(BOOK), f"{w:.0f} x {h:.0f} CSS px at {SCALE}x (h/w {h / w:.2f});",
          f"web page text {text * SCALE:.0f} px in the image ({text * 340 / PHONE:.1f} CSS px on a 340 px column)")


STEPS = {"hello": step_hello}


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
