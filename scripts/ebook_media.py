"""Make the e-book landing page's media (ebook/media/) and its <head> (ebook/_head.html).

Everything the page shows that is not text is made here, from the book's own files, so it can
be remade at any time. Run from the repository root with `make ebook-media`, or name steps:

    make ebook-media STEPS="cover og"

Steps, in order:

  fonts   Newsreader, Nunito Sans and JetBrains Mono from google/fonts at a pinned commit,
          cut to Latin and set axes, as WOFF2 (the download is cached in ~/.cache/quarto-book)
  cover   book/media/cover.png as WebP at three widths, and a small copy for the deck's slide;
          first checks that the PNG's colours are the ones ebook/_source.py reads from cover.svg
  og      the 1200 x 627 share image: the cover beside the title, on the cover's navy
  icons   favicon.svg, a 32 px PNG and a 180 px Apple touch icon
  clips   two of the book's GIFs as short MP4s (a tenth of the size), with WebP posters
  inside  pictures of the book's pages: a three-part box, a catch-up box and a chart from the
          website edition (docs/book/, dark theme), and an EPUB page on a phone at night
  head    ebook/_head.html: share card, icons and structured data, from book/_quarto.yml

Needs Google Chrome (driven by Playwright) and ffmpeg; `make ebook-media` brings the Python
packages with `uv run --with`.
"""
from __future__ import annotations

import io
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ebook"))
import _source as S  # noqa: E402

OUT = ROOT / "ebook" / "media"
FONT_DIR = OUT / "fonts"
CACHE = Path.home() / ".cache" / "quarto-book" / "fonts"

# google/fonts at the commit used on 2026-11-13; bump it to take newer font releases.
FONTS_SHA = "3e5667764ccfea32ce0c3d58a3a4756de890adc1"
FONTS = {  # output name: (path in google/fonts, axis settings: a pin or a (min, max) range)
    "newsreader": ("ofl/newsreader/Newsreader[opsz,wght].ttf", {"opsz": 36, "wght": (500, 700)}),
    "nunito-sans": ("ofl/nunitosans/NunitoSans[YTLC,opsz,wdth,wght].ttf",
                    {"YTLC": 500, "opsz": 12, "wdth": 100, "wght": (400, 800)}),
    "jetbrains-mono": ("ofl/jetbrainsmono/JetBrainsMono[wght].ttf", {"wght": 400}),
}
# Google Fonts' "latin" range, plus arrows; Spanish place names are inside Latin-1.
LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,"
         "U+0329,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD")

CLIPS = {  # name: GIF in book/media/gifs/ (its still, in book/media/stills/, is the poster)
    "london-map": "london-map-orbit",
    "colombia-relief": "colombia-relief-orbit",  # real data; the k-means GIF is toy points
}


def run(*cmd: str) -> None:
    subprocess.run(cmd, check=True)


def kb(p: Path) -> str:
    return f"{p.stat().st_size / 1000:.0f} KB"


# ---- fonts -----------------------------------------------------------------------------

def fonts() -> None:
    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    FONT_DIR.mkdir(parents=True, exist_ok=True)
    licences = []
    for name, (path, axes) in FONTS.items():
        src = CACHE / FONTS_SHA / Path(path).name
        lic = src.parent / f"{Path(path).parent.name}-OFL.txt"
        for url_path, dest in ((path, src), (str(Path(path).parent / "OFL.txt"), lic)):
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                url = (f"https://raw.githubusercontent.com/google/fonts/{FONTS_SHA}/"
                       + urllib.parse.quote(url_path))
                with urllib.request.urlopen(url) as r:
                    dest.write_bytes(r.read())
        font = TTFont(src, lazy=False)
        limits = {k: instancer.AxisTriple(v[0], None, v[1]) if isinstance(v, tuple) else v
                  for k, v in axes.items()}
        font = instancer.instantiateVariableFont(font, limits)
        buf = io.BytesIO()  # a round trip, or the subsetter misses glyphs in the new gvar
        font.save(buf)
        buf.seek(0)
        font = TTFont(buf, lazy=False)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk",
                                "onum", "lnum", "tnum", "c2sc", "smcp", "case"]
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=subset.parse_unicodes(LATIN))
        sub.subset(font)
        out = FONT_DIR / f"{name}.woff2"
        font.flavor = "woff2"
        font.save(out)
        licences.append(f"== {name}.woff2, from google/fonts {FONTS_SHA[:7]} {path}\n\n"
                        + lic.read_text())
        print(f"{out.relative_to(ROOT)}: {kb(out)}")
    (FONT_DIR / "OFL.txt").write_text("\n\n".join(licences))


# ---- the cover ---------------------------------------------------------------------------

def check_palette(img) -> None:
    """The PNG's pixels must be the colours read from cover.svg: the background and each dot."""
    rgb = img.convert("RGB")
    hexof = lambda xy: "#%02x%02x%02x" % rgb.getpixel(xy)  # noqa: E731
    c = S.cover()
    found = {"navy": hexof((20, 20))}
    found.update({f["name"]: hexof(f["dot"][:2]) for f in c["fan"]})
    want = {"navy": c["navy"], **{f["name"]: f["colour"] for f in c["fan"]}}
    off = {k: (want[k], v) for k, v in found.items() if v != want[k]}
    if off:
        raise SystemExit(f"cover.png differs from cover.svg (want, found): {off}")
    print("cover.png: background and the eight line colours match cover.svg")


def cover() -> None:
    from PIL import Image

    OUT.mkdir(parents=True, exist_ok=True)
    img = Image.open(ROOT / "book/media/cover.png")
    check_palette(img)
    for w in (240, 480, 720):
        h = round(img.height * w / img.width)
        out = OUT / f"cover-{w}.webp"
        img.convert("RGB").resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=86, method=6)
        print(f"{out.relative_to(ROOT)}: {w} x {h}, {kb(out)}")
    deck = ROOT / "assets" / "ebook-cover.webp"  # the deck's Get the Book slide (embedded)
    img.convert("RGB").resize((360, 576), Image.LANCZOS).save(deck, "WEBP", quality=84, method=6)
    print(f"{deck.relative_to(ROOT)}: {kb(deck)}")


# ---- pictures drawn by Chrome ---------------------------------------------------------------

def font_face_css() -> str:
    base = FONT_DIR.as_uri()
    return f"""
@font-face {{ font-family: Newsreader; src: url({base}/newsreader.woff2) format("woff2");
  font-weight: 500 700; }}
@font-face {{ font-family: "Nunito Sans"; src: url({base}/nunito-sans.woff2) format("woff2");
  font-weight: 400 800; }}
@font-face {{ font-family: "JetBrains Mono"; src: url({base}/jetbrains-mono.woff2) format("woff2"); }}
"""


def shoot_html(markup: str, size: tuple[int, int], out: Path, scale: float = 1) -> None:
    from playwright.sync_api import sync_playwright

    with tempfile.TemporaryDirectory() as tmp:
        page_file = Path(tmp) / "page.html"
        page_file.write_text(markup)
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome")
            page = browser.new_page(viewport={"width": size[0], "height": size[1]},
                                    device_scale_factor=scale)
            page.goto(page_file.as_uri())
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            page.screenshot(path=str(out), type="png")
            browser.close()


def og() -> None:
    from PIL import Image

    m, c = S.meta(), S.cover()
    w, h = S.OG_SIZE
    markup = f"""<!doctype html><meta charset="utf-8"><style>{font_face_css()}
html, body {{ margin: 0; width: {w}px; height: {h}px; background: {c["navy"]}; overflow: hidden; }}
.cover {{ position: absolute; left: 92px; top: 56px; height: 515px; border-radius: 3px 8px 8px 3px;
  transform: perspective(1400px) rotateY(16deg) rotateX(2deg); transform-origin: left center;
  box-shadow: -6px 0 0 rgba(255,255,255,.06) inset, 24px 30px 60px rgba(0,0,0,.55),
              4px 6px 14px rgba(0,0,0,.4); }}
.text {{ position: absolute; left: 500px; right: 64px; top: 0; bottom: 0; display: flex;
  flex-direction: column; justify-content: center; }}
.eyebrow {{ font: 700 25px/1 "Nunito Sans"; letter-spacing: .2em; color: {c["label"]};
  text-transform: uppercase; margin: 0 0 22px; }}
h1 {{ font: 700 84px/1.0 Newsreader; color: {c["cream"]}; margin: 0 0 22px; letter-spacing: -.01em; }}
.sub {{ font: 500 29px/1.25 Newsreader; color: {c["subtitle"]}; margin: 0 0 26px; }}
.by {{ font: 600 25px/1 "Nunito Sans"; color: {c["cream"]}; letter-spacing: .06em; margin: 0 0 26px; }}
.chips {{ display: flex; gap: 12px; }}
.chips span {{ font: 400 21px/1 "JetBrains Mono"; padding: 9px 14px; border-radius: 8px;
  border: 2px solid currentColor; }}
</style>
<img class="cover" src="{(ROOT / 'book/media/cover.png').as_uri()}">
<div class="text">
  <p class="eyebrow">Free e-book</p>
  <h1>{m["title"].replace(", Publish", ",<br>Publish")}</h1>
  <p class="sub">{m["subtitle"].replace(" with ", "<br>with ", 1)}</p>
  <p class="by">{m["author"].upper()}</p>
  <div class="chips"><span style="color:{c["fan"][3]["colour"]}">epub</span><span
    style="color:{c["fan"][5]["colour"]}">website</span></div>
</div>"""
    out = OUT / "og-image.png"
    shoot_html(markup, (w, h), out)
    img = Image.open(out).convert("RGB")
    if img.size != (w, h):
        raise SystemExit(f"og-image.png is {img.size}, not {(w, h)}")
    img.save(out, optimize=True)
    if out.stat().st_size > 1_000_000:
        raise SystemExit(f"og-image.png is {kb(out)}: LinkedIn needs it under 1 MB")
    print(f"{out.relative_to(ROOT)}: {w} x {h}, {kb(out)}")


def icon_svg() -> str:
    """The mark: four of the cover's lines fanning out of a stem, on its navy."""
    c = S.cover()
    pick = [c["fan"][i]["colour"] for i in (0, 2, 4, 7)]
    xs = [12, 25, 39, 52]
    lines = "".join(f'<path d="M32 22 C32 38 {x} 38 {x} 50" stroke="{col}"/>'
                    f'<circle cx="{x}" cy="51" r="4" fill="{col}"/>' for x, col in zip(xs, pick))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            f'<rect width="64" height="64" rx="14" fill="{c["navy"]}"/>'
            f'<rect x="21" y="9" width="22" height="13" rx="3.5" fill="none" stroke="{c["cream"]}" stroke-width="3.5"/>'
            f'<g fill="none" stroke-width="4" stroke-linecap="round">{lines}</g></svg>\n')


def icons() -> None:
    svg = icon_svg()
    (OUT / "favicon.svg").write_text(svg)
    for name, px in (("favicon-32.png", 32), ("apple-touch-icon.png", 180)):
        markup = (f'<!doctype html><style>html,body{{margin:0;background:transparent}}'
                  f'svg{{display:block;width:{px}px;height:{px}px}}</style>{svg}')
        if name.startswith("apple"):  # iOS rounds the corners itself and wants no transparency
            markup = markup.replace('rx="14"', 'rx="0"')
        shoot_html(markup, (px, px), OUT / name)
        print(f"ebook/media/{name}: {px} px, {kb(OUT / name)}")


# ---- clips -----------------------------------------------------------------------------------

def clips() -> None:
    from PIL import Image

    for name, gif in CLIPS.items():
        src = ROOT / "book/media/gifs" / f"{gif}.gif"
        out = OUT / f"{name}.mp4"
        run("ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-an", "-c:v", "libx264",
            "-preset", "veryslow", "-crf", "30", "-tune", "animation", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos", str(out))
        poster = OUT / f"{name}.webp"
        Image.open(ROOT / "book/media/stills" / f"{gif}.png").convert("RGB").save(
            poster, "WEBP", quality=80, method=6)
        print(f"{out.relative_to(ROOT)}: {kb(out)} (the GIF is {kb(src)}); poster {kb(poster)}")


# ---- inside the book -----------------------------------------------------------------------

INSIDE = {  # name: (page in the website edition, element)
    "box": ("chapters/05-compute.html", "#sec-yaml .agent-box"),
    "catch-up": ("chapters/04-markdown.html", ".tryit:has(.catchup)"),
    "chart": ("chapters/05-compute.html", "#fig-ldn-top10 figure"),
}
NIGHT = "html, body { background: #111 !important; color: #ddd !important; }"
EPUB_PAGE = "body { margin: 1.2em 1.1em !important; max-width: 40em; }"


def save_webp(png: bytes, out: Path, width: int) -> None:
    from PIL import Image

    img = Image.open(io.BytesIO(png)).convert("RGB")
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    img.save(out, "WEBP", quality=82, method=6)
    print(f"{out.relative_to(ROOT)}: {img.width} x {img.height}, {kb(out)}")


def inside() -> None:
    from playwright.sync_api import sync_playwright

    site = ROOT / "docs" / "book"
    epub = site / S.EPUB_NAME
    if not (site / "index.html").exists() or not epub.exists():
        raise SystemExit("inside: docs/book/ is missing; run `make book book-publish` first")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": 1100, "height": 1000}, device_scale_factor=2,
                                color_scheme="dark")
        for name, (rel, sel) in INSIDE.items():
            page.goto((site / rel).as_uri())
            page.evaluate("window.quartoToggleColorScheme && "
                          "document.body.classList.contains('quarto-light') && "
                          "window.quartoToggleColorScheme()")
            # Copy buttons are controls, not content; in a picture one can sit on wrapped code.
            page.add_style_tag(content=".code-copy-button { display: none !important; }")
            page.wait_for_timeout(500)
            el = page.locator(sel).last if name == "catch-up" else page.locator(sel).first
            el.scroll_into_view_if_needed()
            save_webp(el.screenshot(), OUT / f"inside-{name}.webp", 1040)
        page.close()

        # An EPUB chapter opening at night on a phone, read as an e-reader shows it
        # (book/scripts/shoot_epub.py), then set in a plain phone frame.
        with tempfile.TemporaryDirectory() as tmp:
            zipfile.ZipFile(epub).extractall(tmp)
            text = Path(tmp, "EPUB", "text")
            title = S.contents()["parts"][1]["chapters"][1]["title"]  # Chapter 5
            chapter = next(f for f in sorted(text.glob("ch*.xhtml"))
                           if f"{title}</" in f.read_text(encoding="utf-8"))
            phone = browser.new_page(viewport={"width": 390, "height": 760}, device_scale_factor=2,
                                     color_scheme="dark")
            phone.goto(chapter.as_uri())
            phone.add_style_tag(content=EPUB_PAGE + NIGHT)
            phone.wait_for_timeout(500)
            screen = Path(tmp) / "screen.png"
            phone.screenshot(path=str(screen))
            phone.close()
            frame = browser.new_page(viewport={"width": 430, "height": 820}, device_scale_factor=2)
            frame_file = Path(tmp) / "frame.html"  # a file page, so it may load the file image
            frame_file.write_text(f"""<!doctype html><style>html,body{{margin:0;background:{S.cover()['navy']}}}
.phone{{margin:12px auto;width:406px;border-radius:44px;background:#05080c;padding:8px;
  box-shadow:0 0 0 2px #2b3644 inset}}
.phone img{{display:block;width:390px;height:760px;border-radius:36px}}</style>
<div class="phone"><img src="{screen.as_uri()}"></div>""")
            frame.goto(frame_file.as_uri())
            frame.wait_for_timeout(300)
            save_webp(frame.locator(".phone").screenshot(), OUT / "inside-epub.webp", 640)
            frame.close()
        browser.close()


# ---- the page's <head> ------------------------------------------------------------------------

def head() -> None:
    out = ROOT / "ebook" / "_head.html"
    out.write_text(S.head_html())
    print(f"{out.relative_to(ROOT)}: written from book/_quarto.yml")


STEPS = {"fonts": fonts, "cover": cover, "og": og, "icons": icons, "clips": clips,
         "inside": inside, "head": head}

if __name__ == "__main__":
    names = sys.argv[1:] or list(STEPS)
    unknown = [n for n in names if n not in STEPS]
    if unknown:
        raise SystemExit(f"unknown step(s) {unknown}; choose from {list(STEPS)}")
    if not shutil.which("ffmpeg") and "clips" in names:
        raise SystemExit("clips: ffmpeg is not installed")
    OUT.mkdir(parents=True, exist_ok=True)
    for n in names:
        STEPS[n]()
