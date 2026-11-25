"""media/figures/eval-*: pictures of the evaluation project's outputs (Parts III and IV).

Each step works on a temporary copy of a checkpoint (the checkpoint itself is not touched), with
the checkpoint's own locked uv environment, and computes its results as a reader would.

  deck  Chapter 11 (chapters/slides.qmd). Copies checkpoints/16-eval-slides/, runs its
        evaluation, renders slides.qmd to Reveal.js and opens it in Chrome. Saves the title
        slide's title band, eval-deck-title.png, cropped so that the subtitle stays at least
        9 px tall when the picture fills a phone's column, and writes the deck's slide titles
        as rendered to eval-deck-titles.json, which the chapter prints and checks.

Run from book/, all steps or the ones named (as arguments, or in CAPTURE_STEPS):
    make media STEPS="capture" ONLY=eval_outputs
    CAPTURE_STEPS=deck make media STEPS="capture" ONLY=eval_outputs
    uv run --with playwright python media/capture/eval_outputs.py deck
"""
from __future__ import annotations

import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[2]
CHECKPOINTS = BOOK.parent / "checkpoints"
OUT = BOOK / "media" / "figures"
PHONE_COLUMN = 340   # CSS px: the width a "scaled" picture fills on a 390 px phone (epub.css)
MIN_TEXT = 9         # CSS px on that phone (pagefit.yml, min_text_px)
SCALE = 2            # device pixels per CSS pixel in the capture
PAD = 36             # CSS px of the slide's paper kept round the cropped text


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


STEPS = {"deck": step_deck}

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
