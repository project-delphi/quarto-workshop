"""Build the book's media (book/PLAN.md §4). Run from book/ through `make media`:

    uv run --with playwright --with segno python media/build.py [step ...]

Steps (all by default, in this order):
  deck      copy the deck assets the book reuses (DECK_ASSETS) into media/deck/ and the
            London photos (examples/london/images) into media/london/
  cover     media/cover.svg -> media/cover.png (1600 x 2560)
  roadmaps  media/roadmaps/part-N.svg from _chapters.yml (scripts/roadmaps.py)
  diagrams  media/diagrams/*.svg and media/roadmaps/*.svg -> PNG at 2x, beside each SVG
  qr        media/qr/*.png from QR_TARGETS below
  tapes     media/tapes/*.tape -> media/gifs/*.gif with VHS (real, local commands only)
  capture   media/capture/*.py -> media/gifs/*.gif (Playwright scripts)
  posters   book versions of the deck's GIFs in media/gifs/: the last frame held first (so
            the first frame is a usable still), then the animation, at most 800 px wide
  stills    the first frame of every media/gifs/*.gif -> media/stills/*.png
  check     every GIF <= 2 MB and <= 800 px wide, with a still

Playwright drives the installed Google Chrome (channel "chrome"), so no browser download
is needed. Nothing here runs a network, publishing or paid-assistant command: the tapes
replay local commands, and the agent session is a scripted illustration.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MEDIA = Path(__file__).resolve().parent
BOOK = MEDIA.parent
LIVE = "https://project-delphi.github.io/quarto-workshop/book/"
# QR codes for the EPUB's "live version" links: name -> URL.
QR_TARGETS = {
    "london-map": LIVE + "chapters/06-audiences.html#sec-london-3d",
    "kmeans": LIVE + "chapters/11-cluster.html#sec-kmeans-steps",
    "cluster-cloud": LIVE + "chapters/11-cluster.html#sec-cloud-3d",
    "colombia-relief": LIVE + "chapters/11-cluster.html#sec-relief",
    "tunja": LIVE + "chapters/09-explore.html#sec-tunja",
    "explorations": "https://project-delphi.github.io/quarto-workshop/#/water-meta-terrain",
}
# Deck assets the book reuses, copied so both editions resolve them inside book/.
DECK_ASSETS = ["chat-prompt.gif", "windows-session.gif", "threejs-visits.png",
               "pelicans/*.svg", "windows-steps/*.svg"]
MAX_GIF_BYTES = 2_000_000  # 2 MB, decimal
MAX_GIF_WIDTH = 800


def browser(p):
    return p.chromium.launch(channel="chrome",
                             args=["--enable-unsafe-swiftshader", "--use-angle=swiftshader"])


def svg_size(svg: Path) -> tuple[int, int]:
    import re
    head = svg.read_text()[:600]
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', head)
    return int(float(m.group(1))), int(float(m.group(2)))


def rasterise(svgs: list[Path], scale: float, transparent: bool = True) -> None:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = browser(p)
        for svg in svgs:
            w, h = svg_size(svg)
            page = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
            # An SVG document without width/height fills the viewport, which is its viewBox.
            page.goto(svg.as_uri())
            page.screenshot(path=str(svg.with_suffix(".png")), omit_background=transparent,
                            clip={"x": 0, "y": 0, "width": w, "height": h})
            page.close()
            print("png", svg.with_suffix(".png").relative_to(BOOK))
        b.close()


def step_deck() -> None:
    import shutil
    copies = [(BOOK.parent / "assets", pattern, MEDIA / "deck") for pattern in DECK_ASSETS]
    copies += [(BOOK.parent / "examples" / "london" / "images", "*.jpg", MEDIA / "london")]
    # The deck's three.js bundle and Tunja explorer, run unchanged in the HTML edition.
    copies += [(BOOK.parent / "assets", name, BOOK / "assets")
               for name in ("deck-3d.min.js", "tunja-explorer.js")]
    for src, pattern, dest_dir in copies:
        for f in sorted(src.glob(pattern)):
            dest = dest_dir / f.relative_to(src)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
            print("copy", dest.relative_to(BOOK))


def step_cover() -> None:
    rasterise([MEDIA / "cover.svg"], scale=1, transparent=False)


def step_roadmaps() -> None:
    subprocess.run([sys.executable, str(BOOK / "scripts" / "roadmaps.py")], cwd=BOOK, check=True)


def step_diagrams() -> None:
    svgs = sorted([*MEDIA.glob("diagrams/*.svg"), *MEDIA.glob("roadmaps/*.svg"),
                   *MEDIA.glob("deck/windows-steps/*.svg")])
    if svgs:
        rasterise(svgs, scale=2)


def step_qr() -> None:
    import segno
    out = MEDIA / "qr"
    out.mkdir(exist_ok=True)
    for name, url in QR_TARGETS.items():
        segno.make(url, error="m").save(out / f"{name}.png", scale=8, border=2,
                                        dark="#13202e", light="#ffffff")
        print("qr", name, url)


def step_tapes() -> None:
    """Record each tape; a tape with a "# poster:" line gets its last frame held first."""
    import re
    for tape in sorted(MEDIA.glob("tapes/*.tape")):
        print("vhs", tape.name)
        subprocess.run(["vhs", tape.name], cwd=tape.parent, check=True)
        text = tape.read_text()
        out = (tape.parent / re.search(r"^Output (\S+)", text, re.M).group(1)).resolve()
        if re.search(r"^# poster:", text, re.M):
            poster_first(out, out)
        else:
            optimise(out)


def step_capture() -> None:
    for script in sorted(MEDIA.glob("capture/*.py")):
        if script.name.startswith("_"):
            continue
        print("capture", script.name)
        subprocess.run([sys.executable, str(script)], cwd=BOOK, check=True)


def optimise(gif: Path) -> None:
    """Shrink a GIF in place with gifsicle, more lossy (then fewer colours) until it fits
    MAX_GIF_BYTES."""
    for colors, lossy in ((128, 0), (128, 30), (128, 60), (128, 90), (128, 120), (64, 120), (48, 160)):
        args = ["gifsicle", "-O3", "--colors", str(colors), "-o", str(gif), str(gif)]
        if lossy:
            args.insert(1, f"--lossy={lossy}")
        subprocess.run(args, check=True, capture_output=True)
        if gif.stat().st_size <= MAX_GIF_BYTES:
            return


def poster_first(src: Path, dest: Path, hold: float = 2.5, fps: int = 10) -> None:
    """Write dest: src's last frame for `hold` seconds, then src, scaled to <= 800 px."""
    import tempfile
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                            "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(src)],
                           capture_output=True, text=True, check=True).stdout.strip())
    with tempfile.TemporaryDirectory() as tmp:
        last = Path(tmp, "last.png")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-vf",
                        f"select=eq(n\\,{n - 1})", "-frames:v", "1", str(last)], check=True)
        scale = f"scale='min({MAX_GIF_WIDTH},iw)':-2:flags=lanczos,setsar=1,fps={fps}"
        graph = (f"[0:v]{scale}[a];[1:v]{scale}[b];[a][b]concat=n=2:v=1[v];"
                 "[v]split[x][y];[x]palettegen=stats_mode=diff[p];"
                 "[y][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle")
        tmp_gif = Path(tmp, "out.gif")  # src may be dest: never write over the input
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-t", str(hold),
                        "-framerate", str(fps), "-i", str(last), "-i", str(src),
                        "-filter_complex", graph, "-loop", "0", str(tmp_gif)], check=True)
        tmp_gif.replace(dest)
    optimise(dest)


def step_posters() -> None:
    for src in sorted(MEDIA.glob("deck/*.gif")):
        dest = MEDIA / "gifs" / src.name
        poster_first(src, dest)
        print("poster", dest.relative_to(BOOK))


def step_stills() -> None:
    out = MEDIA / "stills"
    out.mkdir(exist_ok=True)
    for gif in sorted(MEDIA.glob("gifs/*.gif")):
        png = out / (gif.stem + ".png")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(gif), "-frames:v", "1",
                        str(png)], check=True)
        print("still", png.relative_to(BOOK))


def step_check() -> None:
    problems = []
    for gif in sorted(MEDIA.glob("gifs/*.gif")):
        probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                "stream=width,height", "-of", "json", str(gif)],
                               capture_output=True, text=True, check=True)
        stream = json.loads(probe.stdout)["streams"][0]
        size = gif.stat().st_size
        print(f"{gif.name:32} {stream['width']:>4} x {stream['height']:<4} {size / 1e6:5.2f} MB")
        if size > MAX_GIF_BYTES:
            problems.append(f"{gif.name}: {size / 1e6:.2f} MB > 2 MB")
        if stream["width"] > MAX_GIF_WIDTH:
            problems.append(f"{gif.name}: {stream['width']} px wide > {MAX_GIF_WIDTH}")
        if not (MEDIA / "stills" / (gif.stem + ".png")).exists():
            problems.append(f"{gif.name}: no still")
    if problems:
        sys.exit("media check failed:\n  " + "\n  ".join(problems))


STEPS = {"deck": step_deck, "cover": step_cover, "roadmaps": step_roadmaps, "diagrams": step_diagrams, "qr": step_qr, "tapes": step_tapes,
         "capture": step_capture, "posters": step_posters, "stills": step_stills, "check": step_check}

if __name__ == "__main__":
    for name in sys.argv[1:] or list(STEPS):
        STEPS[name]()
