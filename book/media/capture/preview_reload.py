"""media/gifs/quarto-preview-reload.gif: a real `quarto preview` reloading on each save (Ch. 4).

Starts `quarto preview london.md` in a scratch folder, shows the file's source beside the live
page, saves three edits one after another (the edits the assistant makes in Chapter 4), and
captures the page as the preview re-renders it. Plain Markdown needs no Python. The result
starts on its final frame (media/build.py poster_first), so the first frame is a usable still.
Run from book/: uv run --with playwright python media/capture/preview_reload.py
"""
from __future__ import annotations

import html
import os
import re
import signal
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BOOK / "media"))
from build import MAX_GIF_WIDTH, optimise, poster_first  # noqa: E402

OUT = BOOK / "media" / "gifs" / "quarto-preview-reload.gif"
W, H = 800, 450
STEPS = [
    "# Visit London\n\nWelcome to **London**: free museums, royal history and *riverside walks*.\n",
    "\n## Five sights to start with\n\n1. British Museum\n2. Natural History Museum\n3. Tate Modern\n"
    "4. National Gallery\n5. Tower of London\n",
    "\n## Plan your visit\n\nPlan your route with the [TfL Journey Planner](https://tfl.gov.uk/plan-a-journey/).\n\n"
    "> **Tip from a local:** many big museums are free.\n",
    "\n## Before you go\n\n```text\n[ ] Contactless card or Oyster card\n[ ] Free museum tickets booked\n```\n",
]

FRAME = """<!doctype html><html><head><style>
body {{ margin: 0; width: {w}px; height: {h}px; display: grid; grid-template-columns: 330px 1fr;
  font-family: "Avenir Next", "Helvetica Neue", Arial, sans-serif; background: #13202e; }}
.src {{ background: #1b2836; color: #e8edf2; padding: 0; overflow: hidden; display: grid; grid-template-rows: auto 1fr; }}
pre {{ overflow: hidden; }}
.bar {{ font-size: 13px; padding: 8px 12px; background: #24313f; color: #b8c2cc; }}
.bar b {{ color: #fff; }}
pre {{ margin: 0; padding: 10px 12px; font: 12.5px/1.45 Menlo, monospace; white-space: pre-wrap; }}
pre .new {{ background: rgba(121, 212, 178, 0.25); }}
.page {{ display: grid; grid-template-rows: auto 1fr; }}
.page .bar {{ background: #e6e9ec; color: #3d4b59; }}
iframe {{ border: 0; width: 100%; height: 100%; background: #fff; }}
.note {{ position: absolute; left: 0; bottom: 0; width: 330px; box-sizing: border-box; padding: 8px 12px;
  font-size: 13px; color: #13202e; background: #79d4b2; }}
</style></head><body>
<div class="src"><div class="bar"><b>london.md</b> · saved by the assistant</div><pre id="src"></pre></div>
<div class="page"><div class="bar">localhost · quarto preview</div><iframe id="view" src="{url}"></iframe></div>
<div class="note" id="note">quarto preview london.md</div>
</body></html>"""


def main() -> None:
    work = Path(tempfile.mkdtemp(prefix="preview-"))
    md = work / "london.md"
    md.write_text(STEPS[0])
    # Preview's output goes to a log file: an unread pipe would fill up and block quarto.
    log = work / "preview.log"
    proc = subprocess.Popen(["quarto", "preview", "london.md", "--port", "4877", "--no-browser"],
                            cwd=work, stdout=log.open("w"), stderr=subprocess.STDOUT,
                            start_new_session=True)  # its own group: stop quarto's server too

    def stop() -> None:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

    url = None
    deadline = time.time() + 90
    while time.time() < deadline and not url:
        time.sleep(1)
        plain = re.sub(r"\x1b\[[0-9;]*m", "", log.read_text())  # drop colour codes
        m = re.search(r"Browse at (http://\S+)", plain)
        if m:
            url = m.group(1)
    if not url:
        stop()
        sys.exit("quarto preview did not start")
    frames = Path(tempfile.mkdtemp(prefix="frames-"))
    n = 0
    text = STEPS[0]
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome")
            page = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
            page.set_content(FRAME.format(w=W, h=H, url=url))
            page.wait_for_timeout(2500)

            def show_source(old: str, new: str) -> None:
                body = html.escape(old) + (f'<span class="new">{html.escape(new)}</span>' if new else "")
                page.evaluate("s => document.getElementById('src').innerHTML = s", body)

            def snap(count: int, every: float = 0.25) -> None:
                nonlocal n
                for _ in range(count):
                    page.screenshot(path=str(frames / f"f{n:04d}.png"))
                    n += 1
                    time.sleep(every)

            show_source("", STEPS[0])
            snap(8)
            for step in STEPS[1:]:
                old = text
                text += step
                show_source(old, step)
                page.evaluate("t => document.getElementById('note').textContent = t",
                              "saved: the preview re-renders")
                page.evaluate("() => { const s = document.getElementById('src'); s.scrollTop = s.scrollHeight; }")
                snap(3)
                md.write_text(text)
                snap(6)
                # After the reload, bring the new section into view in the rendered page.
                for f in page.frames[1:]:
                    try:
                        f.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
                    except Exception:
                        pass
                snap(8)
            page.evaluate("t => document.getElementById('note').textContent = t",
                          "every save shows up in the page")
            snap(10)
            b.close()
    finally:
        stop()
        proc.wait(timeout=20)
    raw = frames / "raw.gif"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "4", "-i", str(frames / "f%04d.png"),
                    "-vf", f"scale='min({MAX_GIF_WIDTH},iw)':-2,split[x][y];[x]palettegen=stats_mode=diff[p];"
                           "[y][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle",
                    "-loop", "0", str(raw)], check=True)
    poster_first(raw, OUT, hold=2.0, fps=4)
    optimise(OUT)
    shutil.rmtree(frames, ignore_errors=True)
    shutil.rmtree(work, ignore_errors=True)
    print("gif", OUT.relative_to(BOOK))


if __name__ == "__main__":
    main()
