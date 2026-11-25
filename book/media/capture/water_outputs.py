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


def render_example(prefix: str) -> Path:
    """Copy examples/water to a temporary folder, give it its own locked uv environment and
    render it there. Returns the copy; the caller removes its parent."""
    work = Path(tempfile.mkdtemp(prefix=prefix)) / "water"
    try:
        shutil.copytree(EXAMPLE, work, ignore=shutil.ignore_patterns(
            ".venv", "_site", ".quarto", "*_files", "outputs", "raw", "__pycache__"))
        env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}  # uv picks the folder's own
        subprocess.run(["uv", "sync", "--frozen"], cwd=work, env=env, check=True)
        env["JUPYTER_PATH"] = str(work / ".venv" / "share" / "jupyter")  # not a user-level kernel
        subprocess.run(["uv", "run", "--frozen", "quarto", "render"], cwd=work, env=env, check=True)
    except BaseException:
        shutil.rmtree(work.parent, ignore_errors=True)
        raise
    return work


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
    subprocess.run(["uv", "sync", "--frozen"], cwd=work, env=env, check=True)
    env["JUPYTER_PATH"] = str(work / ".venv" / "share" / "jupyter")  # not a user-level kernel
    subprocess.run(["uv", "run", "--frozen", "quarto", "render", "explore.qmd"], cwd=work, env=env, check=True)
    png = OUT / "water-explore.png"
    got = shoot_explore(work / "explore.html", png)
    # For pagefit.yml's screenshots: the text's height in the image's own pixels.
    w, h = got["css"]
    print("figure", png.relative_to(BOOK), f"{w:.0f} x {h:.0f} CSS px at {SCALE}x (h/w {h / w:.2f});",
          f"body text {got['body']:.0f} px, table text {got['table']:.0f} px in the image")
    shutil.rmtree(work.parent, ignore_errors=True)


LAST_SLIDE = "What this does and does not show"

# Reveal.js scales its 1050-pixel-wide slide to the viewport's width, so at a phone's width the
# bullets could be drawn far too small. The picture measures what is drawn (font size times the
# scale Reveal applies); the bullets must be at least 9 px in the 340 px column the book shows.
SLIDE_BOX = """title => {
    const h = [...document.querySelectorAll(".reveal h2")].find(e => e.textContent.trim() === title);
    if (!h) return null;
    const sec = h.closest("section");
    sec.scrollIntoView();
    const items = [...sec.querySelectorAll("li")];
    const px = e => parseFloat(getComputedStyle(e).fontSize) * (e.getBoundingClientRect().height / e.offsetHeight);
    const r = sec.getBoundingClientRect();
    const end = items[items.length - 1].getBoundingClientRect().bottom;  // the slide's lower half is empty
    return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: Math.min(r.height, end - r.top + 12), n: items.length,
            bullet: Math.min(...items.map(px)), title: px(h)};
}"""


def shoot_council(site: Path) -> None:
    png = OUT / "water-slides-last.png"
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        page = b.new_page(viewport={"width": PHONE, "height": 844}, device_scale_factor=3)
        page.goto((site / "slides.html").as_uri())
        page.wait_for_function("window.Reveal && Reveal.isReady()")
        page.wait_for_timeout(1500)
        at = page.evaluate(SLIDE_BOX, LAST_SLIDE)
        if at is None:
            raise SystemExit(f"slides.html has no slide titled {LAST_SLIDE!r}")
        page.wait_for_timeout(500)
        at = page.evaluate(SLIDE_BOX, LAST_SLIDE)
        print("slide box", at)
        page.screenshot(path=str(png), full_page=True,
                        clip={"x": at["x"], "y": at["y"], "width": at["w"], "height": at["h"]})
        b.close()
    shrink(png)
    w, h = at["w"], at["h"]
    print("figure", png.relative_to(BOOK), f"{w:.0f} x {h:.0f} CSS px at 3x (h/w {h / w:.2f});",
          f"{at['n']} bullets; bullet text {at['bullet'] * 3:.0f} px, title {at['title'] * 3:.0f} px in",
          f"the image; {at['bullet'] * 340 / w:.1f} px and {at['title'] * 340 / w:.1f} px in a",
          "340 px column")


MAX_HW = 1.25  # tallest a picture may be, as height over width

# The smallest text drawn between two page heights, and the page's boxes for the two crops.
MIN_TEXT = """([top, bottom]) => {
    let min = 1e9;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        if (!n.textContent.trim()) continue;
        const e = n.parentElement, r = e.getBoundingClientRect();
        if (r.width === 0 || r.top + scrollY < top || r.bottom + scrollY > bottom) continue;
        min = Math.min(min, parseFloat(getComputedStyle(e).fontSize));
    }
    return min;
}"""
DASH_BOXES = """() => {
    const b = [...document.querySelectorAll(".bslib-value-box")].slice(0, 2).map(e => e.getBoundingClientRect());
    return b.length < 2 ? null : [b[0].top + scrollY, b[1].bottom + scrollY];
}"""
POST_BOX = """limit => {
    const h = document.querySelector("h1.title, .quarto-title h1");
    const para = document.querySelector("#quarto-document-content p");
    if (!h || !para) return null;
    const top = h.getBoundingClientRect().top + scrollY;
    const range = document.createRange();
    range.selectNodeContents(para);
    const lines = [...range.getClientRects()].map(r => r.bottom + scrollY).filter(y => y - top <= limit);
    return [top, Math.max(...lines)];
}"""


def shoot_phone(site: Path) -> None:
    from io import BytesIO

    from PIL import Image

    post = next(site.glob("posts/*/index.html"))
    limit = MAX_HW * PHONE
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        for html, name, wait in [(site / "dashboard.html", "water-dashboard-phone.png", 9000),
                                 (post, "water-post-phone.png", 2000)]:
            page = b.new_page(viewport={"width": PHONE, "height": 844}, device_scale_factor=SCALE)
            page.goto(html.as_uri())
            page.wait_for_timeout(wait)
            span = page.evaluate(DASH_BOXES if "dashboard" in name else POST_BOX, *([] if "dashboard" in name else [limit]))
            if span is None:
                raise SystemExit(f"{html.name}: nothing to crop to for {name}")
            top, bottom = max(span[0] - PAD, 0), span[1] + PAD
            small = page.evaluate(MIN_TEXT, [span[0], span[1]])
            png = OUT / name
            clip = {"x": 0, "y": top, "width": PHONE, "height": bottom - top}
            Image.open(BytesIO(page.screenshot(full_page=True, clip=clip))).convert("RGB").save(png, optimize=True)
            w, h = clip["width"], clip["height"]
            print("figure", png.relative_to(BOOK), f"{w:.0f} x {h:.0f} CSS px at {SCALE}x (h/w {h / w:.2f});",
                  f"smallest text {small * SCALE:.0f} px in the image, {small * 340 / w:.1f} px in a 340 px column")
        b.close()


def step_phone() -> None:
    work = render_example("water-phone-")
    try:
        shoot_phone(work / "_site")
    finally:
        shutil.rmtree(work.parent, ignore_errors=True)


def step_council() -> None:
    work = render_example("water-council-")
    try:
        shoot_council(work / "_site")
    finally:
        shutil.rmtree(work.parent, ignore_errors=True)


def shrink(png: Path) -> None:
    """Re-save a screenshot as an optimised PNG."""
    from PIL import Image
    Image.open(png).convert("RGB").save(png, optimize=True)


STEPS = {"outputs": step_outputs, "explore": step_explore, "council": step_council, "phone": step_phone}


def main(names: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # CAPTURE_STEPS is read by every capture script that `make media STEPS=capture` runs, so
    # names another script owns are left to it; names given as arguments must exist here.
    named = os.environ.get("CAPTURE_STEPS", "").split()
    unknown = [n for n in names if n not in STEPS]
    names = names or ([n for n in named if n in STEPS] if named else list(STEPS))
    if unknown:
        raise SystemExit(f"unknown step(s) {unknown}; the steps are {list(STEPS)}")
    for name in names:
        STEPS[name]()


if __name__ == "__main__":
    main(sys.argv[1:])
