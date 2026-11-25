"""media/figures/eval-*: pictures of the evaluation project's outputs (Parts III and IV).

Each step works on a temporary copy of a checkpoint (the checkpoint itself is not touched), with
the checkpoint's own locked uv environment, and computes its results as a reader would.

  deck        Chapter 11 (chapters/slides.qmd). Copies checkpoints/16-eval-slides/, runs its
              evaluation, renders slides.qmd to Reveal.js and opens it in Chrome. Saves the title
              slide's title band, eval-deck-title.png, cropped so that the subtitle stays at
              least 9 px tall when the picture fills a phone's column, and writes the deck's
              slide titles as rendered to eval-deck-titles.json, which the chapter prints and
              checks.
  report      Chapter 3 (chapters/fast-path.qmd). checkpoints/14-eval-start/report.html at a
              phone's width: eval-report.png, the title block and the paragraph whose second
              sentence (guarded) names the best release and its ROC AUC.
  card        Chapter 10 (chapters/results.qmd). checkpoints/15-eval-results/model-card.html:
              eval-card-top.png, the title and subtitle, then (after a dashed cut) the whole of
              section 2, "Intended use". It is taken at 430 px, the widest common phone, since
              at 390 px the two parts are half as tall again as they are wide.
  site        Chapter 12 (chapters/sites.qmd). Renders checkpoints/17-eval-site/ as a site:
              eval-site-home.png, the home page's navbar and title, then (after a dashed cut)
              the "The documents" heading and the listing down to its first entry; and the
              navbar alone, eval-site-navbar-after.png. Then removes the navbar's
              `background: light` from the copy's _quarto.yml, renders the home page again and
              saves eval-site-navbar-before.png, but only if the bar then takes the colour the
              logo is drawn in, so that the bar hides the logo as the chapter's story says.
  whitepaper  Chapter 13 (chapters/white-papers.qmd). Renders checkpoints/18-eval-whitepaper/
              whitepaper.qmd to a Typst PDF and draws its first page 1400 px wide (_pdf.py):
              eval-whitepaper-p1.png, the house title block and the abstract, cropped to the
              text column, or the title block alone if the abstract's text would show under
              9 px on a phone. The text sizes come from the PDF itself (the checkpoint's pypdf).
  update      Chapter 14 (chapters/parameters.qmd). Renders checkpoints/19-eval-params/
              update.qmd to html for the last two months of data/synthetic_business.csv
              (SYNTHETIC: invented for teaching), `-P month:…` as the chapter does:
              eval-update-a.png (the earlier month) and eval-update-b.png, each the "This update
              covers" sentence, then (after a dashed cut) the business figures, every one marked
              "(synthetic)". Writes eval-update-sentences.json, each month's sentences as
              rendered, which the chapter prints and checks.

The HTML pictures are taken at 390 CSS px (the card at 430), drawn at twice the pixel density,
and the full width of the page, so a phone's 340 px column shows the body text at about 14 px
(13 px for the card). Every step checks that no text in its picture would show under 9 px on
that column (the white paper only warns: see its function) and that no picture is taller than
MAX_RATIO times its width, then prints the sizes pagefit.yml's `screenshots` records.

Run from book/, all steps or the ones named (as arguments, or in CAPTURE_STEPS):
    make media STEPS="capture" ONLY=eval_outputs
    CAPTURE_STEPS=deck make media STEPS="capture" ONLY=eval_outputs
    uv run --with playwright python media/capture/eval_outputs.py deck
"""
from __future__ import annotations

import csv
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime
from io import BytesIO
from pathlib import Path

from playwright.sync_api import sync_playwright

from _pdf import first_page_png

BOOK = Path(__file__).resolve().parents[2]
CHECKPOINTS = BOOK.parent / "checkpoints"
OUT = BOOK / "media" / "figures"
PHONE_COLUMN = 340   # CSS px: the width a "scaled" picture fills on a 390 px phone (epub.css)
MIN_TEXT = 9         # CSS px on that phone (pagefit.yml, min_text_px)
SCALE = 2            # device pixels per CSS pixel in the capture
PAD = 36             # CSS px of the slide's paper kept round the cropped text
PHONE = 390          # CSS px: the viewport of the HTML pictures, a phone's width
WIDE_PHONE = 430     # CSS px: the widest common phone, for the model card
EDGE = 12            # CSS px of the page kept above and below each part of an HTML page
GAP = 16             # CSS px between stacked parts, with a dashed rule across the middle
RULE = "#b4bcc4"     # the dashed rule's colour (as in water_outputs.py)
MAX_RATIO = 1.3      # height over width: epub.css caps a picture at 55vh, which would shrink
                     # a taller one, and its text with it, on a phone
PAGE_WIDTH = 1400    # px: the white paper's first page, as drawn
PAGE_PAD = 8         # pt of the PDF page kept round the white paper's text column


def project_copy(checkpoint: str) -> tuple[Path, dict]:
    """A temporary copy of a checkpoint, and an environment for its own `uv run`."""
    work = Path(tempfile.mkdtemp(prefix="eval-")) / "acme-eval"
    shutil.copytree(CHECKPOINTS / checkpoint, work, ignore=shutil.ignore_patterns(
        ".venv", "outputs", "*_files", ".quarto", "__pycache__", ".pytest_cache", "*.html"))
    # The book's environment must not leak into the project's: uv picks the project's .venv,
    # and Jupyter finds the project's kernel before any user-level python3 kernelspec.
    env = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "JUPYTER_PATH")}
    env["JUPYTER_PATH"] = str(work / ".venv" / "share" / "jupyter")
    return work, env


def step_deck() -> None:
    work, env = project_copy("16-eval-slides")
    try:
        _deck(work, env)
    finally:
        shutil.rmtree(work.parent, ignore_errors=True)


def _deck(work: Path, env: dict) -> None:
    for command in (["uv", "run", "--frozen", "python", "scripts/evaluate.py"],
                    ["uv", "run", "--frozen", "quarto", "render", "slides.qmd", "--to", "revealjs"]):
        subprocess.run(command, cwd=work, env=env, check=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        # The deck is 1280 x 720; the wider viewport leaves the theme's paper on both sides of
        # the slide, drawn at scale 1, so the crop below can keep a margin round the text.
        view = {"width": 1280 + 2 * PAD, "height": 720}
        page = browser.new_page(viewport=view, device_scale_factor=SCALE)
        page.goto((work / "slides.html").as_uri())
        page.wait_for_function("window.Reveal && Reveal.isReady()")
        page.evaluate("Reveal.configure({margin: 0, controls: false, progress: false})")
        page.evaluate("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(1000)
        titles = page.evaluate("""Reveal.getSlides().map(s => {
            const h = s.querySelector('h1.title, h2');
            return h ? h.textContent.replace(/\\s+/g, ' ').trim() : '';
        })""")
        # The extent of the title's and subtitle's text (a Range, since a block spans the
        # slide's width), and the subtitle's size as drawn.
        box = page.evaluate("""() => {
            const parts = ['#title-slide .title', '#title-slide .subtitle'].map(q => document.querySelector(q));
            const rects = parts.map(e => { const r = document.createRange(); r.selectNodeContents(e);
                                           return r.getBoundingClientRect(); });
            return {left: Math.min(...rects.map(r => r.left)), right: Math.max(...rects.map(r => r.right)),
                    top: Math.min(...rects.map(r => r.top)), bottom: Math.max(...rects.map(r => r.bottom)),
                    subtitle_px: parseFloat(getComputedStyle(parts[1]).fontSize) * Reveal.getScale(),
                    subtitle: parts[1].textContent.replace(/\\s+/g, ' ').trim()};
        }""")
        # The title band: the title and subtitle, with a margin of the slide's paper round them.
        clip = {"x": max(0, box["left"] - PAD), "y": max(0, box["top"] - PAD)}
        clip["width"] = min(view["width"], box["right"] + PAD) - clip["x"]
        clip["height"] = min(view["height"], box["bottom"] + PAD) - clip["y"]
        phone = box["subtitle_px"] * PHONE_COLUMN / clip["width"]
        if phone < MIN_TEXT:
            sys.exit(f"eval-deck-title.png: the subtitle would show at {phone:.1f} px on a phone, "
                     f"under {MIN_TEXT}: crop tighter")
        expected = 1 + len(re.findall(r"^## ", (work / "slides.qmd").read_text(), re.M))
        if len(titles) != expected or not all(titles):
            sys.exit(f"eval-deck-titles.json: expected {expected} titled slides, found {titles}")
        page.screenshot(path=str(OUT / "eval-deck-title.png"), clip=clip)
        chrome = browser.version
        browser.close()
    quarto = subprocess.run(["quarto", "--version"], capture_output=True, text=True,
                            check=True).stdout.strip()
    # The PNG's own size, from its header (the clip is in fractional CSS pixels).
    width, height = struct.unpack(">II", (OUT / "eval-deck-title.png").read_bytes()[16:24])
    record = {
        "source": "checkpoints/16-eval-slides/slides.qmd",
        "rendered_with": {"quarto": quarto, "chrome": chrome},
        "titles": titles,
        "subtitle": box["subtitle"],
        "title_png": {"file": "eval-deck-title.png", "width_px": width, "height_px": height,
                      # for pagefit.yml's screenshots: the subtitle's size in the image's pixels
                      "subtitle_px": round(box["subtitle_px"] * SCALE),
                      "subtitle_px_on_phone": round(box["subtitle_px"] * SCALE * PHONE_COLUMN / width, 1)},
    }
    (OUT / "eval-deck-titles.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    for name in ("eval-deck-title.png", "eval-deck-titles.json"):
        print("figure", (OUT / name).relative_to(BOOK))
    print(f"subtitle: {box['subtitle_px'] * SCALE:.0f} px in the image, about {phone:.1f} px on a phone")


@contextmanager
def checkpoint_copy(checkpoint: str):
    """project_copy() as a context: the temporary folder is removed however the step ends."""
    work, env = project_copy(checkpoint)
    try:
        yield work, env
    finally:
        shutil.rmtree(work.parent, ignore_errors=True)


def run(work: Path, env: dict, *command: str, **kwargs) -> subprocess.CompletedProcess:
    """A command in the project copy, in its own locked environment."""
    return subprocess.run(["uv", "run", "--frozen", *command], cwd=work, env=env, check=True, **kwargs)


def evaluate(work: Path, env: dict) -> None:
    run(work, env, "python", "scripts/evaluate.py")


def built(work: Path, name: str) -> Path:
    """A rendered file: beside its source, or in _site/ for a page of a website project."""
    for path in (work / name, work / "_site" / name):
        if path.exists():
            return path
    sys.exit(f"{name}: not found after the render, beside its source or in _site/")


def versions(chrome: str) -> dict:
    quarto = subprocess.run(["quarto", "--version"], capture_output=True, text=True,
                            check=True).stdout.strip()
    return {"quarto": quarto, "chrome": chrome}


# Each picture's parts, top to bottom: a script that returns [top, bottom, text] for each, in
# CSS px from the top of the page, or null if one is missing. Every page is a Quarto HTML page,
# whose body is #quarto-document-content and whose title block is #title-block-header.
SPAN = """const span = q => {
    const e = typeof q === 'string' ? document.querySelector(q) : q;
    if (!e) return null;
    const r = e.getBoundingClientRect();
    return [r.top + scrollY, r.bottom + scrollY, e.innerText.replace(/\\s+/g, ' ').trim()];
};"""
FIRST_PARAGRAPH = "#quarto-document-content > p"
REPORT_PARTS = f"""() => {{ {SPAN}
    const head = span('#title-block-header'), first = span('{FIRST_PARAGRAPH}');
    return head && first ? [[head[0], first[1], first[2]]] : null;
}}"""
CARD_PARTS = f"""() => {{ {SPAN}
    const title = span('#title-block-header .quarto-title'), use = span('#sec-use');
    return title && use ? [title, use] : null;
}}"""
SITE_PARTS = f"""() => {{ {SPAN}
    const title = span('#title-block-header h1.title');
    const row = document.querySelector('#listing-documents tbody tr');
    const section = row && row.closest('section');
    const heading = section && span(section.querySelector('h2'));
    const first = row && span(row);
    return title && heading && first
        ? [[0, title[1], title[2]], [heading[0], first[1], heading[2] + ' | ' + first[2]]] : null;
}}"""
NAVBAR_PARTS = f"""() => {{ {SPAN}
    const bar = span('#quarto-header');
    return bar ? [bar] : null;
}}"""
UPDATE_PARTS = f"""() => {{ {SPAN}
    const covers = span('{FIRST_PARAGRAPH}'), figures = span('#the-business > ul');
    return covers && figures ? [covers, figures] : null;
}}"""
# The navbar's background, and the logo's height as drawn (CSS px).
NAVBAR_PROBE = """() => ({
    background: getComputedStyle(document.querySelector('#quarto-header .navbar')).backgroundColor,
    logo_height: document.querySelector('#quarto-header .navbar-logo').getBoundingClientRect().height,
})"""
# The update's text as a reader sees it, block by block in page order: the description in the
# title block, then every paragraph, list item and caption of the body (callouts included;
# headings, the title, the date and table cells left out); and the business figures' items.
UPDATE_PROBE = f"""() => {{
    const text = e => e.innerText.replace(/\\s+/g, ' ').trim();
    const blocks = [...document.querySelectorAll(
        '#title-block-header .description, #quarto-document-content p, '
        + '#quarto-document-content li, #quarto-document-content figcaption')]
        .filter(e => !e.closest('#title-block-header') || e.matches('.description'))
        .filter(e => !(e.matches('p') && e.parentElement.closest('li, figcaption, .description')))
        .map(text).filter(Boolean);
    return {{blocks, items: [...document.querySelectorAll('#the-business > ul > li')].map(text)}};
}}"""
# The font size (CSS px), start and length of every visible text node with a line inside one of
# the regions ([top, bottom] in CSS px); text hidden for screen readers only (1 px boxes) is not seen.
TEXT_SIZES = """regions => {
    const found = [];
    const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n = walk.nextNode(); n; n = walk.nextNode()) {
        const text = n.textContent.replace(/\\s+/g, ' ').trim();
        if (!text) continue;
        const range = document.createRange();
        range.selectNodeContents(n);
        const lines = [...range.getClientRects()].filter(r => r.width > 1 && r.height > 1
            && r.right > 0 && r.left < innerWidth);
        if (lines.some(r => regions.some(([t, b]) => r.top + scrollY < b && r.bottom + scrollY > t)))
            found.push([parseFloat(getComputedStyle(n.parentElement).fontSize), text.slice(0, 40), text.length]);
    }
    return found;
}"""
BACKGROUND = """() => {
    const c = getComputedStyle(document.body).backgroundColor.match(/[\\d.]+/g).map(Number);
    return c.length > 3 && c[3] === 0 ? [255, 255, 255] : c.slice(0, 3);
}"""


def save_png(image, path: Path) -> None:
    """Save without loss: as a palette PNG (about a third of the size) when the picture has 256
    colours or fewer and the palette gives back every pixel, else as an optimised RGB PNG."""
    from PIL import Image, ImageChops

    image = image.convert("RGB")
    if image.getcolors(256) is not None:
        palette = image.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        if ImageChops.difference(palette.convert("RGB"), image).getbbox() is None:
            image = palette
    image.save(path, optimize=True)


def shoot(html: Path, png: Path, parts: str, width: int = PHONE, edge: int = EDGE,
          probe: str | None = None) -> dict:
    """Screenshot html `width` CSS px wide at SCALE, keep the parts `parts` finds, each with
    `edge` px of the page above and below, and stack them into png with a dashed rule where the
    page between two parts is left out. Stops if a part is missing, if text would show under
    MIN_TEXT px on a phone, or if the picture is taller than MAX_RATIO times its width.
    Returns the picture's sizes, the parts' text and what `probe` (a script) returns."""
    from PIL import Image, ImageDraw

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": width, "height": 844}, device_scale_factor=SCALE)
        page.goto(html.as_uri(), wait_until="load")
        page.evaluate("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(1000)
        found = page.evaluate(parts)
        if not found:
            sys.exit(f"{png.name}: {html.name} lacks a part the picture shows")
        regions = [[max(0.0, top - edge), bottom + edge] for top, bottom, _ in found]
        sizes = page.evaluate(TEXT_SIZES, regions)
        paper = tuple(page.evaluate(BACKGROUND))
        probed = page.evaluate(probe) if probe else None
        crops = [Image.open(BytesIO(page.screenshot(full_page=True, clip={
            "x": 0, "y": top, "width": width, "height": bottom - top}))).convert("RGB")
            for top, bottom in regions]
        chrome = browser.version
        browser.close()
    gap = GAP * SCALE
    out = Image.new("RGB", (crops[0].width, sum(c.height for c in crops) + gap * (len(crops) - 1)), paper)
    draw, y = ImageDraw.Draw(out), 0
    for i, crop in enumerate(crops):
        if i:
            middle = y + gap // 2
            for x in range(EDGE * SCALE, out.width - EDGE * SCALE, 8 * SCALE):
                draw.line([(x, middle), (x + 4 * SCALE, middle)], fill=RULE, width=SCALE)
            y += gap
        out.paste(crop, (0, y))
        y += crop.height

    def on_phone(px: float) -> float:
        return round(px * PHONE_COLUMN / width, 1)

    if out.height > MAX_RATIO * out.width:
        sys.exit(f"{png.name}: {out.height / out.width:.2f} times as tall as wide, over {MAX_RATIO}")
    got = {"file": png.name, "width_px": out.width, "height_px": out.height, "viewport_px": width}
    if sizes:  # a navbar's only text is the logo's, inside its image
        smallest = min(sizes)
        if on_phone(smallest[0]) < MIN_TEXT:
            sys.exit(f"{png.name}: {smallest[1]!r} would show at {on_phone(smallest[0])} px on a "
                     f"phone, under {MIN_TEXT}: crop tighter")
        # The body text: the size most of the picture's characters are set in. For pagefit.yml's
        # screenshots, in the image's own pixels.
        chars: dict[float, int] = {}
        for size, _, length in sizes:
            chars[size] = chars.get(size, 0) + length
        body = max(chars, key=chars.get)
        got.update(body_px=round(body * SCALE), body_px_on_phone=on_phone(body),
                   smallest_px=round(smallest[0] * SCALE), smallest_px_on_phone=on_phone(smallest[0]),
                   smallest_text=smallest[1])
    save_png(out, png)
    return {**got, "parts": [text for *_, text in found], "probe": probed, "chrome": chrome}


def show(got: dict) -> None:
    """The line each picture prints: what pagefit.yml's `screenshots` needs, and the shape."""
    line = (f"figure {(OUT / got['file']).relative_to(BOOK)}: {got['width_px']} x {got['height_px']} px "
            f"(h/w {got['height_px'] / got['width_px']:.2f}, {got['viewport_px']} px viewport)")
    if "body_px" in got:
        line += (f"; body text {got['body_px']} px, {got['body_px_on_phone']} px on a phone; smallest "
                 f"{got['smallest_px']} px, {got['smallest_px_on_phone']} px ({got['smallest_text']!r})")
    else:
        line += "; no page text"
    print(line)


def step_report() -> None:
    with checkpoint_copy("14-eval-start") as (work, env):
        evaluate(work, env)
        run(work, env, "quarto", "render", "report.qmd", "--to", "html")
        got = shoot(built(work, "report.html"), OUT / "eval-report.png", REPORT_PARTS)
        if "ranks best" not in got["parts"][0]:
            sys.exit("eval-report.png: the first paragraph no longer holds the guarded sentence")
        show(got)


def step_card() -> None:
    with checkpoint_copy("15-eval-results") as (work, env):
        evaluate(work, env)
        run(work, env, "quarto", "render", "model-card.qmd", "--to", "html")
        got = shoot(built(work, "model-card.html"), OUT / "eval-card-top.png", CARD_PARTS,
                    width=WIDE_PHONE)
        if not got["parts"][1].startswith("2 Intended use"):
            sys.exit(f"eval-card-top.png: section 2 is not Intended use: {got['parts'][1][:40]!r}")
        show(got)


def rgb_hex(css: str) -> str:
    """'rgb(11, 61, 99)' as '#0b3d63'."""
    return "#" + "".join(f"{int(v):02x}" for v in re.findall(r"[\d.]+", css)[:3])


def step_site() -> None:
    import yaml

    with checkpoint_copy("17-eval-site") as (work, env):
        evaluate(work, env)
        run(work, env, "quarto", "render")
        home = built(work, "index.html")
        got = shoot(home, OUT / "eval-site-home.png", SITE_PARTS, probe=NAVBAR_PROBE)
        # The logo's name is text in an SVG, out of the page's reach: its size as drawn is the
        # logo's height times the name's font size over the SVG's height.
        svg = (work / "brand" / "logo.svg").read_text()
        box_height = float(re.search(r'viewBox="[\d.]+ [\d.]+ [\d.]+ ([\d.]+)"', svg).group(1))
        name_size = float(re.search(r'<text[^>]*font-size="([\d.]+)"', svg).group(1))
        logo_text = got["probe"]["logo_height"] * name_size / box_height
        if logo_text * PHONE_COLUMN / PHONE < MIN_TEXT:
            (OUT / "eval-site-navbar-before.png").unlink(missing_ok=True)
            sys.exit(f"eval-site-navbar: the logo's name would show at "
                     f"{logo_text * PHONE_COLUMN / PHONE:.1f} px on a phone, under {MIN_TEXT}")
        show(got)
        print(f"  the logo's name: {logo_text * SCALE:.0f} px in the image, "
              f"{logo_text * PHONE_COLUMN / PHONE:.1f} px on a phone")
        after = shoot(home, OUT / "eval-site-navbar-after.png", NAVBAR_PARTS, edge=0, probe=NAVBAR_PROBE)
        show(after)
        # The chapter's story: without `background: light`, the navbar took the brand's primary
        # colour, the navy the logo is drawn in. Render the home page again without that line.
        config = work / "_quarto.yml"
        text, removed = re.subn(r"^[ \t]+background: light\b.*\n", "", config.read_text(), flags=re.M)
        if removed != 1:
            sys.exit("_quarto.yml: no single navbar `background: light` line to remove")
        config.write_text(text)
        run(work, env, "quarto", "render", "index.qmd")
        brand = yaml.safe_load((work / "_brand.yml").read_text())["color"]
        primary = brand["palette"].get(brand["primary"], brand["primary"]).lower()
        before_png = OUT / "eval-site-navbar-before.png"
        before = shoot(home, before_png, NAVBAR_PARTS, edge=0, probe=NAVBAR_PROBE)
        bar = rgb_hex(before["probe"]["background"])
        if bar != primary or primary not in svg.lower():
            before_png.unlink()
            print(f"  without `background: light` the navbar is {bar}, not the logo's {primary}: "
                  "the hidden logo does not reproduce, so there is no 'before' picture")
            return
        show(before)
        print(f"  navbar {rgb_hex(after['probe']['background'])} after, {bar} before: "
              f"the brand's primary, the colour of the logo's tile and name")


# The text on a PDF's first page, from the checkpoint's own pypdf: each run's x and baseline
# (pt from the page's top left), its font size as drawn (pt) and its text.
PDF_TEXT = r"""
import json, sys
from pypdf import PdfReader
page = PdfReader(sys.argv[1]).pages[0]
height = float(page.mediabox.height)
runs = []
def visit(text, cm, tm, font, size):
    if text.strip():
        x, y = tm[4], tm[5]
        runs.append([cm[0] * x + cm[2] * y + cm[4], height - (cm[1] * x + cm[3] * y + cm[5]),
                     size * abs(tm[3] * cm[3]), text.strip()])
page.extract_text(visitor_text=visit)
print(json.dumps({"width": float(page.mediabox.width), "height": height, "runs": runs}))
"""


def step_whitepaper() -> None:
    with checkpoint_copy("18-eval-whitepaper") as (work, env):
        _whitepaper(work, env)


def _whitepaper(work: Path, env: dict) -> None:
    import numpy as np
    from PIL import Image

    evaluate(work, env)
    run(work, env, "quarto", "render", "whitepaper.qmd", "--to", "typst")
    pdf = built(work, "whitepaper.pdf")
    text = json.loads(run(work, env, "python", "-c", PDF_TEXT, str(pdf),
                          capture_output=True, text=True).stdout)
    drawn = work / "page-1.png"
    first_page_png(pdf, drawn, round(PAGE_WIDTH * text["height"] / text["width"]))
    page = Image.open(drawn).convert("RGB")
    k = page.width / text["width"]  # image px per pt
    pixels = np.asarray(page).astype(int)
    off = np.abs(pixels - pixels[2, 2]).sum(axis=2)  # how far each pixel is from the paper
    ink = off > 60
    # The house rule under the logo is the first row inked across most of the page: its ends
    # are the text column's. The title block starts at the logo (page 1 has no running header).
    rule = np.flatnonzero(ink.mean(axis=1) > 0.5)
    if not len(rule):
        sys.exit("whitepaper.pdf: no rule across page 1, so no house title block to crop")
    left, right = np.flatnonzero(ink[rule[0]])[[0, -1]]
    top = np.flatnonzero(ink.any(axis=1))[0]
    # The abstract's box, filled with a tint of the paper, holds the "Abstract" label; its fill
    # runs down the column's left edge, inside the box's inset.
    label = next((r for r in text["runs"] if r[3] == "Abstract"), None)
    if label is None:
        sys.exit("whitepaper.pdf: no abstract on page 1")
    fill = off[:, left + round(4 * k)] > 6
    box_top = box_bottom = round(label[1] * k)
    while box_top > 0 and fill[box_top - 1]:
        box_top -= 1
    while box_bottom + 1 < len(fill) and fill[box_bottom + 1]:
        box_bottom += 1
    block_bottom = top + np.flatnonzero(ink[top:box_top, left:right + 1].any(axis=1))[-1]
    pad = round(PAGE_PAD * k)
    png = OUT / "eval-whitepaper-p1.png"
    for what, bottom in (("the title block and the abstract", box_bottom), ("the title block", block_bottom)):
        crop = (left - pad, top - pad, right + 1 + pad, bottom + 1 + pad)
        width = crop[2] - crop[0]
        # Each size of text in the crop, in pt, with the first run drawn at that size.
        sizes = {}
        for x, baseline, size, words in text["runs"]:
            if crop[1] <= baseline * k <= crop[3]:
                sizes.setdefault(round(size, 1), words)
        if not sizes:
            sys.exit(f"whitepaper.pdf: no text inside {what}")
        phone = {size: round(size * k * PHONE_COLUMN / width, 1) for size in sizes}
        if min(phone.values()) >= MIN_TEXT:
            break
    # Below the floor only where SMALL_TEXT says why, checked before the picture is written.
    if min(phone.values()) < MIN_TEXT and png.name not in SMALL_TEXT:
        sys.exit(f"{png.name}: {what} has text under {MIN_TEXT} px on a phone")
    save_png(page.crop(crop), png)
    height = crop[3] - crop[1]
    print(f"figure {png.relative_to(BOOK)}: {what}, {width} x {height} px (h/w {height / width:.2f}), "
          f"from a page drawn {page.width} px wide")
    for size in sorted(sizes, reverse=True):
        print(f"  {size:>5} pt: {size * k:.0f} px in the image, {phone[size]} px on a phone "
              f"({sizes[size][:40]!r})")
    if min(phone.values()) < MIN_TEXT:
        print(f"  allowed: text under {MIN_TEXT} px on a phone, because {SMALL_TEXT[png.name]}")


# Pictures allowed to show text under MIN_TEXT on a phone, each with its reason (book/pagefit.yml
# notes the same beside the figure's text size). Any other picture under the floor stops its step.
SMALL_TEXT = {
    "eval-whitepaper-p1.png": "it is an A4 page's title block: no crop of whole lines is narrower "
                              "than the 16.6 cm column, and its title stays legible",
}


def step_update() -> None:
    with checkpoint_copy("19-eval-params") as (work, env):
        _update(work, env)


SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z“\"])|(?<=[.!?][”’\"])\s+(?=[A-Z“\"])")


def _update(work: Path, env: dict) -> None:
    evaluate(work, env)
    with open(work / "data" / "synthetic_business.csv", newline="") as f:
        months = sorted(row["month"] for row in csv.DictReader(f))[-2:]
    record = {
        "source": "checkpoints/19-eval-params/update.qmd",
        "data": "data/synthetic_business.csv (SYNTHETIC: invented for teaching)",
        "command": "quarto render update.qmd -P month:MONTH -M output-file:update-MONTH --to html",
        "rendered_with": None,
        "months": months,
        "sentences": {},
        "pictures": {},
    }
    for month, name in zip(months, ("eval-update-a.png", "eval-update-b.png")):
        stem = f"update-{month}"
        run(work, env, "quarto", "render", "update.qmd", "-P", f"month:{month}",
            "-M", f"output-file:{stem}", "--to", "html")
        got = shoot(built(work, stem + ".html"), OUT / name, UPDATE_PARTS, probe=UPDATE_PROBE)
        covers = f"This update covers {datetime.strptime(month, '%Y-%m'):%B %Y}"
        items = got["probe"]["items"]
        if not got["parts"][0].startswith(covers):
            sys.exit(f"{name}: the update does not open {covers!r}: {got['parts'][0]!r}")
        if not items or not all("(synthetic)" in item for item in items):
            sys.exit(f"{name}: a business figure is not marked (synthetic): {items}")
        record["sentences"][month] = [s for block in got["probe"]["blocks"]
                                      for s in SENTENCE_BREAK.split(block) if s]
        record["pictures"][month] = {k: v for k, v in got.items() if k not in ("parts", "probe", "chrome")}
        record["rendered_with"] = versions(got["chrome"])
        show(got)
    a, b = (set(record["sentences"][m]) for m in months)
    if not a & b or not a ^ b:
        sys.exit(f"eval-update-sentences.json: {months[0]} and {months[1]} should share a sentence "
                 "and differ in another")
    json_path = OUT / "eval-update-sentences.json"
    json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    print("figure", json_path.relative_to(BOOK), f"({len(a & b)} sentences in both months, "
          f"{len(a - b)} in {months[0]} only, {len(b - a)} in {months[1]} only)")


STEPS = {"deck": step_deck, "report": step_report, "card": step_card, "site": step_site,
         "whitepaper": step_whitepaper, "update": step_update}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    # Steps named as arguments must exist; CAPTURE_STEPS is read by every capture script that
    # `make media STEPS=capture` runs, so names another script owns are left to it.
    unknown = [n for n in sys.argv[1:] if n not in STEPS]
    if unknown:
        sys.exit(f"eval_outputs.py: no step {', '.join(unknown)}; steps: {', '.join(STEPS)}")
    named = os.environ.get("CAPTURE_STEPS", "").split()
    for name in sys.argv[1:] or ([n for n in named if n in STEPS] if named else list(STEPS)):
        STEPS[name]()
