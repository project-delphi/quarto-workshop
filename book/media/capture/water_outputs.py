"""media/figures/water-*.png: pictures of the water project's outputs (Chapters 14 and 18).

Two steps, both run by default; name some, as arguments or in CAPTURE_STEPS, to run only those:

- outputs (Chapter 14): renders a temporary copy of examples/water (the example itself is not
  touched) with its own uv environment, including its pre-render analysis, then saves the first
  page of the report PDF and of the white paper (macOS Quick Look draws a PDF's first page,
  _pdf.py) and screenshots the dashboard, the council slides and the blog post in Chrome.
- explore (Chapter 18's payoff, water-explore.png): renders checkpoints/05-water-explore/
  explore.qmd in a temporary folder with examples/water/data/ copied in, as a reader's folder
  holds them, and screenshots its title and its table of missing values by zone at a phone's
  width, drawn at twice the pixel density so the text stays sharp.

Run from book/media/capture:
    uv run --with playwright python water_outputs.py [outputs] [explore]
or from the repository root:
    CAPTURE_STEPS=explore make media STEPS="capture" ONLY=water_outputs
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

from _pdf import first_page_png

BOOK = Path(__file__).resolve().parents[2]
EXAMPLE = BOOK.parent / "examples" / "water"
CHECKPOINT = BOOK.parent / "checkpoints" / "05-water-explore"
OUT = BOOK / "media" / "figures"
PHONE, SCALE = 390, 2  # the explore picture: CSS pixels wide, and device pixels per CSS pixel
PAD = 12  # CSS pixels kept round each crop
GAP = 16  # CSS pixels between the two crops, with a dashed rule across the middle


def step_outputs() -> None:
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


# Where the explore picture's two crops start and end, in CSS pixels from the page's top, and the
# text sizes. The whole page, and even its table (a row for every column with gaps), is taller
# than a phone's screen, so the picture keeps the table's rows down to irca, the row the chapter
# is about, and fades out the next.
EXPLORE_PARTS = """() => {
    const span = e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.bottom + scrollY]; };
    const px = e => parseFloat(getComputedStyle(e).fontSize);
    const title = document.querySelector("#title-block-header .quarto-title");  // title, subtitle
    const caption = document.querySelector("#tbl-missing figcaption");
    const rows = [...document.querySelectorAll("#tbl-missing tbody tr")];
    const irca = rows.findIndex(r => r.firstElementChild.textContent.trim() === "irca");
    const body = document.querySelector("main > p, main section > p");
    if (!title || !caption || irca < 0 || irca + 1 >= rows.length || !body) return null;
    return {title: span(title), caption: span(caption), irca: span(rows[irca]), next: span(rows[irca + 1]),
            body: px(body), table: px(rows[irca].lastElementChild)};
}"""


def shoot_explore(html: Path, png: Path) -> dict:
    """Screenshot explore.html at a phone's width: its title block, then its table of missing
    values from the caption to the irca row, with the next row faded out, stacked with a dashed
    rule where the page between them (a paragraph, the section's heading and a folded code
    cell) is left out."""
    from io import BytesIO

    from PIL import Image, ImageDraw

    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        page = b.new_page(viewport={"width": PHONE, "height": 844}, device_scale_factor=SCALE)
        page.goto(html.as_uri(), wait_until="load")
        page.wait_for_timeout(1000)
        at = page.evaluate(EXPLORE_PARTS)
        if at is None:
            raise SystemExit(f"{html.name}: no title block, missing-values table or irca row to picture")

        def crop(top: float, bottom: float) -> Image.Image:
            clip = {"x": 0, "y": top, "width": PHONE, "height": bottom - top}
            return Image.open(BytesIO(page.screenshot(full_page=True, clip=clip))).convert("RGB")

        head = crop(at["title"][0] - PAD, at["title"][1] + PAD)
        table = crop(at["caption"][0] - PAD, at["next"][1])
        b.close()
    # Fade the row after irca into the page's white, so the table reads as continuing.
    fade = round((at["next"][1] - at["next"][0]) * SCALE)
    white = Image.new("RGB", (table.width, fade), "white")
    mask = Image.linear_gradient("L").resize((table.width, fade))
    region = (0, table.height - fade, table.width, table.height)
    table.paste(Image.composite(white, table.crop(region), mask), region)
    gap = GAP * SCALE
    out = Image.new("RGB", (head.width, head.height + gap + table.height), "white")
    out.paste(head, (0, 0))
    out.paste(table, (0, head.height + gap))
    rule, y = ImageDraw.Draw(out), head.height + gap // 2
    for x in range(PAD * SCALE, out.width - PAD * SCALE, 8 * SCALE):
        rule.line([(x, y), (x + 4 * SCALE, y)], fill="#b4bcc4", width=SCALE)
    out.save(png, optimize=True)
    return {"css": (out.width / SCALE, out.height / SCALE),
            "body": at["body"] * SCALE, "table": at["table"] * SCALE}


def step_explore() -> None:
    work = Path(tempfile.mkdtemp(prefix="water-explore-")) / "water-quality"
    shutil.copytree(CHECKPOINT, work, ignore=shutil.ignore_patterns(".venv", ".quarto", "*_files", "*.html"))
    shutil.copytree(EXAMPLE / "data", work / "data", ignore=shutil.ignore_patterns("raw"))
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}  # uv picks the folder's own
    subprocess.run(["uv", "sync"], cwd=work, env=env, check=True)
    env["JUPYTER_PATH"] = str(work / ".venv" / "share" / "jupyter")  # not a user-level kernel
    subprocess.run(["uv", "run", "quarto", "render", "explore.qmd"], cwd=work, env=env, check=True)
    png = OUT / "water-explore.png"
    got = shoot_explore(work / "explore.html", png)
    # For pagefit.yml's screenshots: the text's height in the image's own pixels.
    w, h = got["css"]
    print("figure", png.relative_to(BOOK), f"{w:.0f} x {h:.0f} CSS px at {SCALE}x (h/w {h / w:.2f});",
          f"body text {got['body']:.0f} px, table text {got['table']:.0f} px in the image")
    shutil.rmtree(work.parent, ignore_errors=True)


STEPS = {"outputs": step_outputs, "explore": step_explore}


def main(names: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    names = names or os.environ.get("CAPTURE_STEPS", "").split() or list(STEPS)
    unknown = [n for n in names if n not in STEPS]
    if unknown:
        raise SystemExit(f"unknown step(s) {unknown}; the steps are {list(STEPS)}")
    for name in names:
        STEPS[name]()


if __name__ == "__main__":
    main(sys.argv[1:])
