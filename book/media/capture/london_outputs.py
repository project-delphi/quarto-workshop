"""media/figures/london-*: pictures of the finished London project's outputs (Chapters 6 to 9).

Renders a temporary copy of examples/london (the example itself is not touched) with its own
locked uv environment (uv sync --frozen; no network), then makes the steps asked for:

- london:    the first page of the flyer, the square advert and the white paper (macOS Quick
             Look draws a PDF's first page, _pdf.py; the advert, a full-bleed photo, as a JPEG)
             and desktop screenshots of the dashboard and the guide.
- guide:     london-guide-phone.png (Chapter 6's payoff): london.html at a 390 px viewport, drawn
             at twice the pixel density, from the navbar to the end of "Five sights".
- dashboard: london-dashboard-phone.png (Chapter 8): the dashboard's three value boxes at 390 px.
- audiences: london-audiences.png (Chapter 8's payoff): the first value box, the partner brief's
             first heading and bullet, and the flyer's title block, stacked with dashed rules.
             The brief is london-email.qmd's own HTML at 390 px: no Word-to-PDF converter is
             installed, and Quick Look's page of the .docx shows its text under 9 px at a
             phone's column, even cropped to the text's width.
- live:      london-live-phone.png (Chapter 9's payoff): the local render's navbar, title and
             first lines at 390 px, as a visitor's phone shows the published site (no network).

The new pictures have new names because the Spanish edition reads media/figures through a
symlink and keeps the old ones until it is translated.

Run from book/media/capture, all steps or the ones named (as arguments, or in CAPTURE_STEPS):
    uv run --with playwright python london_outputs.py [london] [guide] [dashboard] [audiences] [live]
or from book/: CAPTURE_STEPS="live" make media STEPS="capture" ONLY=london_outputs
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path

from playwright.sync_api import sync_playwright

from _pdf import first_page_png

BOOK = Path(__file__).resolve().parents[2]
EXAMPLE = BOOK.parent / "examples" / "london"
OUT = BOOK / "media" / "figures"
PHONE, SCALE = 390, 2  # the phone pictures: CSS pixels wide, and device pixels per CSS pixel
PAD = 12  # CSS pixels kept round each crop
GAP = 16  # CSS pixels between stacked crops, with a dashed rule across the middle
FLYER_TOP = 0.21  # the share of the flyer's height kept: the title and subtitle, above the photo
FLYER_SIDE_CM, FLYER_WIDTH_CM = 1.0, 14.8  # trim the A5 page's margin to this, so text is larger


@contextmanager
def site():
    """Yield the _site folder of a fresh render of examples/london in a temporary folder."""
    work = Path(tempfile.mkdtemp(prefix="london-")) / "london"
    try:
        shutil.copytree(EXAMPLE, work, ignore=shutil.ignore_patterns(".venv", "_site", ".quarto", "*_files"))
        env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}  # uv picks the folder's own
        subprocess.run(["uv", "sync", "--frozen"], cwd=work, env=env, check=True)
        env["JUPYTER_PATH"] = str(work / ".venv" / "share" / "jupyter")  # not a user-level kernel
        subprocess.run(["uv", "run", "--frozen", "quarto", "render"], cwd=work, env=env, check=True)
        # The partner brief is a .docx; its HTML twin (same source) is what the audiences picture shows.
        subprocess.run(["uv", "run", "--frozen", "quarto", "render", "london-email.qmd", "--to", "html"],
                       cwd=work, env=env, check=True)
        yield work / "_site"
    finally:
        shutil.rmtree(work.parent, ignore_errors=True)


def step_outputs(s: Path) -> None:
    for pdf, name, size in [("london-flyer.pdf", "london-flyer.png", 1400),
                            ("london-social.pdf", "london-social.jpg", 1200),
                            ("london-whitepaper.pdf", "london-whitepaper-p1.png", 1400)]:
        first_page_png(s / pdf, OUT / name, size)
        print("figure", (OUT / name).relative_to(BOOK))
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        page = b.new_page(viewport={"width": 1400, "height": 860}, device_scale_factor=1)
        page.goto((s / "london-dashboard.html").as_uri())
        page.wait_for_timeout(6000)  # Plotly draws after load
        page.screenshot(path=str(OUT / "london-dashboard.png"))
        print("figure", (OUT / "london-dashboard.png").relative_to(BOOK))
        page.goto((s / "london.html").as_uri())
        page.wait_for_timeout(1500)
        page.screenshot(path=str(OUT / "london-guide.png"))
        print("figure", (OUT / "london-guide.png").relative_to(BOOK))
        b.close()


# The smallest text drawn between two heights of the page, in CSS pixels.
SMALLEST = """([top, bottom]) => {
    const sizes = [];
    for (const e of document.querySelectorAll("body *")) {
        if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
        const r = e.getBoundingClientRect();
        if (r.height === 0 || r.bottom + scrollY <= top || r.top + scrollY >= bottom) continue;
        const cs = getComputedStyle(e);
        if (cs.visibility === "hidden" || cs.display === "none") continue;
        sizes.push(parseFloat(cs.fontSize));
    }
    return Math.min(...sizes);
}"""


class Phone:
    """A Chrome page at a phone's width, from which stacked crops are taken."""

    def __init__(self, p, html: Path, wait: int = 1500):
        self.browser = p.chromium.launch(channel="chrome")
        self.page = self.browser.new_page(viewport={"width": PHONE, "height": 844}, device_scale_factor=SCALE)
        self.page.goto(html.as_uri(), wait_until="load")
        self.page.wait_for_timeout(wait)

    def span(self, selector: str, nth: int = 0) -> tuple[float, float]:
        got = self.page.evaluate("""([sel, n]) => { const e = document.querySelectorAll(sel)[n]; if (!e) return null;
            const r = e.getBoundingClientRect(); return [r.top + scrollY, r.bottom + scrollY]; }""", [selector, nth])
        if got is None:
            raise SystemExit(f"no {selector!r} (number {nth}) on the page to crop at")
        return tuple(got)

    def crop(self, top: float, bottom: float):
        """The page from top to bottom (CSS px): a PIL image, and the smallest text in it, in CSS px."""
        from PIL import Image

        top = max(0, top)
        clip = {"x": 0, "y": top, "width": PHONE, "height": bottom - top}
        img = Image.open(BytesIO(self.page.screenshot(full_page=True, clip=clip))).convert("RGB")
        return img, self.page.evaluate(SMALLEST, [top, bottom])

    def close(self):
        self.browser.close()


def save(img, name: str, texts: dict[str, float]) -> None:
    """Write img as an optimised PNG and print what pagefit.yml needs: the size, and each named
    text's height in the image's own pixels."""
    png = OUT / name
    img.save(png, optimize=True)
    w, h = img.width / SCALE, img.height / SCALE
    seen = ", ".join(f"{k} {v * SCALE:.0f} px" for k, v in texts.items())
    print("figure", png.relative_to(BOOK), f"{w:.0f} x {h:.0f} CSS px at {SCALE}x (h/w {h / w:.2f});",
          f"smallest text {seen} in the image; {min(texts.values()) * 340 / PHONE:.1f} CSS px on a 340 px column")


def step_guide(s: Path) -> None:
    with sync_playwright() as p:
        ph = Phone(p, s / "london.html")
        img, text = ph.crop(0, ph.span("main ol")[1] + PAD)
        ph.close()
    save(img, "london-guide-phone.png", {"smallest": text})


def value_boxes(ph: Phone):
    return ph.crop(ph.span(".bslib-value-box", 0)[0] - PAD, ph.span(".bslib-value-box", 2)[1] + PAD)


def step_dashboard(s: Path) -> None:
    with sync_playwright() as p:
        ph = Phone(p, s / "london-dashboard.html", wait=4000)
        img, text = value_boxes(ph)
        ph.close()
    save(img, "london-dashboard-phone.png", {"smallest": text})


def step_live(s: Path) -> None:
    with sync_playwright() as p:
        ph = Phone(p, s / "london.html")
        img, text = ph.crop(0, ph.span("main ol li", 1)[1] + 4)
        ph.close()
    save(img, "london-live-phone.png", {"smallest": text})


def flyer_top(s: Path, width: int):
    """The flyer's top third, margins trimmed, scaled to width pixels."""
    from PIL import Image

    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "flyer.png"
        first_page_png(s / "london-flyer.pdf", png, 2600)
        page = Image.open(png).convert("RGB")
    side = round(page.width * FLYER_SIDE_CM / FLYER_WIDTH_CM)
    page = page.crop((side, side, page.width - side, round(page.height * FLYER_TOP)))
    return page.resize((width, round(page.height * width / page.width)), Image.LANCZOS)


def step_audiences(s: Path) -> None:
    from PIL import Image, ImageDraw

    with sync_playwright() as p:
        ph = Phone(p, s / "london-dashboard.html", wait=4000)
        # The row's first box only: at a phone's width the second (39,692,434) is cut off by the
        # dashboard itself, and the row stacked is 1.4 times as tall as wide.
        boxes, t_boxes = ph.crop(ph.span(".bslib-value-box", 0)[0] - PAD, ph.span(".bslib-value-box", 0)[1] + PAD)
        ph.close()
        ph = Phone(p, s / "london-email.html")
        brief, t_brief = ph.crop(ph.span("main h2")[0] - PAD, ph.span("main ul li")[1] + 4)
        ph.close()
    flyer = flyer_top(s, boxes.width)
    gap = GAP * SCALE
    parts = [boxes, brief, flyer]
    out = Image.new("RGB", (boxes.width, sum(i.height for i in parts) + gap * 2), "white")
    rule, y = ImageDraw.Draw(out), 0
    for n, img in enumerate(parts):
        out.paste(img, (0, y))
        y += img.height
        if n < 2:
            for x in range(PAD * SCALE, out.width - PAD * SCALE, 8 * SCALE):
                rule.line([(x, y + gap // 2), (x + 4 * SCALE, y + gap // 2)], fill="#b4bcc4", width=SCALE)
            y += gap
    save(out, "london-audiences.png", {"dashboard": t_boxes, "brief": t_brief})


STEPS = {"london": step_outputs, "guide": step_guide, "dashboard": step_dashboard,
         "audiences": step_audiences, "live": step_live}


def main(names: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # CAPTURE_STEPS is read by every capture script that `make media STEPS=capture` runs, so
    # names another script owns are left to it; names given as arguments must exist here.
    named = os.environ.get("CAPTURE_STEPS", "").split()
    unknown = [n for n in names if n not in STEPS]
    if unknown:
        raise SystemExit(f"unknown step(s) {unknown}; the steps are {list(STEPS)}")
    names = names or ([n for n in named if n in STEPS] if named else list(STEPS))
    if not names:
        return
    with site() as s:
        for name in names:
            STEPS[name](s)


if __name__ == "__main__":
    main(sys.argv[1:])
