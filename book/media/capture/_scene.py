"""Record a live 3-D scene from the HTML edition as a GIF (book/PLAN.md §4).

Opens a chapter of _book/html in Chrome (Playwright, software WebGL), sizes the scene's
element to the GIF's frame, then plays a script of steps: hold, press a view button, drag to
orbit. Frames are captured at FPS while the steps run, assembled with ffmpeg's palette
filters, given a poster frame (the last frame first, so readers that do not animate show a
finished view) and shrunk to fit the 2 MB budget. Build the HTML edition first.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BOOK / "media"))
from build import optimise, poster_first  # noqa: E402

W, H, FPS = 800, 460, 10


def record(page_rel: str, out_name: str, steps: list[tuple], index: int = 0,
           hide: str = "") -> Path:
    """steps: ("hold", seconds) | ("view", name, seconds) | ("drag", dx, dy, seconds) |
    ("click", css, seconds); index picks the scene when a page holds several. hide: CSS
    selectors inside the scene to leave out of the frames (made transparent, so the steps
    can still click them), such as buttons that mean nothing in a GIF."""
    site = BOOK / "_book" / "html" / page_rel
    frames = Path(tempfile.mkdtemp(prefix="scene-"))
    n = 0
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader",
                                                      "--enable-unsafe-swiftshader"])
        page = b.new_page(viewport={"width": 1100, "height": 900}, device_scale_factor=1)
        page.goto(site.as_uri())
        scene = page.locator(".deck-3d").nth(index)
        scene.scroll_into_view_if_needed()
        # Pin the scene above the page (its sidebars and margin notes) at the GIF's size.
        scene.evaluate(f"el => Object.assign(el.style, {{ position: 'fixed', left: '0', top: '0', "
                       f"width: '{W}px', height: '{H}px', margin: '0', borderRadius: '0', zIndex: '9999' }})")
        if hide:
            page.add_style_tag(content=f".deck-3d :is({hide}) {{ opacity: 0 !important; }}")
        page.evaluate("dispatchEvent(new Event('resize'))")
        page.wait_for_function("el => el.classList.contains('is-drawn')", arg=scene.element_handle(),
                               timeout=30000)
        page.wait_for_timeout(1500)
        box = scene.bounding_box()
        cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2

        def snap_for(seconds: float, during=None) -> None:
            nonlocal n
            end = time.time() + seconds
            while time.time() < end:
                t0 = time.time()
                if during:
                    during((t0 - (end - seconds)) / seconds)
                scene.screenshot(path=str(frames / f"f{n:04d}.png"))
                n += 1
                time.sleep(max(0, 1 / FPS - (time.time() - t0)))

        for step in steps:
            kind = step[0]
            if kind == "hold":
                snap_for(step[1])
            elif kind == "view":
                section = scene.locator("xpath=ancestor::section[1]")
                section.locator(f".view-buttons button[data-view='{step[1]}']").first.click()
                snap_for(step[2])
            elif kind == "click":
                page.locator(step[1]).click()
                snap_for(step[2])
            elif kind == "drag":
                _, dx, dy, seconds = step
                page.mouse.move(cx, cy)
                page.mouse.down()
                last = [0.0]

                def move(f, dx=dx, dy=dy):
                    f = min(1.0, f)
                    page.mouse.move(cx + dx * f, cy + dy * f, steps=2)
                    last[0] = f

                snap_for(seconds, during=move)
                page.mouse.up()
        b.close()
    out = BOOK / "media" / "gifs" / out_name
    raw = frames / "raw.gif"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS),
                    "-i", str(frames / "f%04d.png"),
                    "-vf", "split[x][y];[x]palettegen=stats_mode=diff[p];"
                           "[y][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle",
                    "-loop", "0", str(raw)], check=True)
    poster_first(raw, out, hold=1.5, fps=FPS)
    optimise(out)
    shutil.rmtree(frames, ignore_errors=True)
    print("gif", out.relative_to(BOOK), f"{out.stat().st_size / 1e6:.2f} MB, {n} frames")
    return out
