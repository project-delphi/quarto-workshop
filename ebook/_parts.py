"""HTML for the landing page's sections (ebook/index.qmd). The data come from _source.py;
this module only draws them. Each function returns markup that `raw()` prints as a raw HTML
block, so Pandoc passes it through untouched."""
from __future__ import annotations

import html
import inspect
import math
import re
from urllib.parse import quote as urlquote

from PIL import Image

import _source as S

e = lambda s: html.escape(str(s), quote=True)  # noqa: E731

ICON = {
    "down": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v12m0 0-5-5m5 5 5-5M5 20h14"/></svg>',
    "right": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m0 0-6-6m6 6-6 6"/></svg>',
    "link": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>',
    "share": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9.5V19M6 5.5v.01M10.5 19v-5.5a3 3 0 0 1 6 0V19m-6-9.5V19"/></svg>',
}


def raw(markup: str) -> None:
    """Print markup as a raw HTML block (the cell needs `output: asis`)."""
    print("```{=html}\n" + markup.strip() + "\n```\n")


def size(rel: str) -> tuple[int, int]:
    with Image.open(S.ROOT / "ebook" / rel) as im:
        return im.size


def cta_buttons(size_text: str, where: str) -> str:
    return f"""<div class="ctas">
  <a class="btn primary" href="{S.EPUB_URL}" data-where="{where}">{ICON["down"]}<span>Download the EPUB</span><span class="size">{size_text}</span></a>
  <a class="btn secondary" href="{S.BOOK_URL}">Read online, free{ICON["right"]}</a>
</div>"""


INAPP = ('<p class="inapp" hidden>In LinkedIn’s browser? If the download does not start, open '
         "this page in your phone’s browser from LinkedIn’s menu.</p>")


# ---- 1. hero -------------------------------------------------------------------------------

def hero(promise: str, size_text: str) -> str:
    m = S.meta()
    title = m["title"].replace(", ", ",<br>")
    return f"""<header class="hero" id="top">
<div class="wrap hero-grid">
  <a class="cover" href="{S.BOOK_URL}">
    <img src="media/cover-480.webp" srcset="media/cover-240.webp 240w, media/cover-480.webp 480w, media/cover-720.webp 720w"
      sizes="(max-width: 699px) 112px, 340px" width="480" height="768" fetchpriority="high"
      alt="{e(S.cover_desc())}">
  </a>
  <div class="hero-head">
    <p class="eyebrow">A practitioner’s guide</p>
    <h1>{title}</h1>
  </div>
  <div class="hero-body">
    <p class="subtitle">{e(m["subtitle"])}</p>
    <p class="promise">{e(promise)}</p>
    <p class="byline">Free · by {e(m["author"])} · PhD, Oxford</p>
    {cta_buttons(size_text, "hero")}
    {INAPP}
    <ul class="badges" aria-label="Editions"><li>EPUB</li><li>Web</li><li class="plain">no sign-up</li></ul>
    {hero_qr()}
  </div>
</div>
</header>"""


def hero_qr() -> str:
    """A QR code to this page, for a room watching it on a projector (wide screens only).

    It is the deck's 📖 Get the Book code, assets/ebook-qr.svg (scripts/deck_qr.py), inlined;
    the render stops if that code no longer opens this page."""
    svg = S.read("assets/ebook-qr.svg").strip()
    if f"<title>QR code: {S.PAGE_URL}</title>" not in svg:
        raise ValueError(f"assets/ebook-qr.svg does not open {S.PAGE_URL}: run scripts/deck_qr.py")
    svg = svg.replace("<title>", '<title id="qr-title">', 1).replace(
        "<svg ", '<svg role="img" aria-labelledby="qr-title" ', 1)
    short = S.PAGE_URL.split("://", 1)[1].rstrip("/")
    return f"""<figure class="hero-qr">
      {svg}
      <figcaption><strong>Scan to open this page</strong><span>{e(short)}</span></figcaption>
    </figure>"""


# ---- 2. the loop -----------------------------------------------------------------------------

def loop_svg() -> str:
    c = S.cover()
    fan = {f["name"]: f["colour"] for f in c["fan"]}
    cx, cy, r, nr = 220, 196, 136, 54
    nodes = [("Prompt", -90, fan["html"], "you ask"),
             ("Check", 30, fan["pdf"], "you, always"),
             ("Publish", 150, fan["epub"], "Quarto")]
    ring = f"M{cx},{cy - r} A{r},{r} 0 0 1 {cx},{cy + r} A{r},{r} 0 0 1 {cx},{cy - r}"
    parts = [f'<path class="ring" d="{ring}" pathLength="300"/>',
             f'<path class="comet" d="{ring}" pathLength="300"/>']
    for a in (-30, 90, 210):  # chevrons between the nodes, pointing clockwise
        t = math.radians(a)
        x, y = cx + r * math.cos(t), cy + r * math.sin(t)
        dx, dy = -math.sin(t), math.cos(t)
        ang = math.degrees(math.atan2(dy, dx))
        parts.append(f'<path class="chev" d="M-7,-8 L4,0 L-7,8" '
                     f'transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})"/>')
    for i, (label, a, colour, who) in enumerate(nodes):
        t = math.radians(a)
        x, y = cx + r * math.cos(t), cy + r * math.sin(t)
        ring2 = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{nr + 7}" class="halo" stroke="{colour}"/>'
                 if label == "Check" else "")
        parts.append(f'<g class="node n{i}">{ring2}<circle cx="{x:.1f}" cy="{y:.1f}" r="{nr}" '
                     f'stroke="{colour}"/><text x="{x:.1f}" y="{y + 2:.1f}" class="lbl">{label}</text>'
                     f'<text x="{x:.1f}" y="{y + 22:.1f}" class="who" fill="{colour}">{who}</text></g>')
    parts.append(f'<text x="{cx}" y="{cy - 4}" class="mid">small steps,</text>'
                 f'<text x="{cx}" y="{cy + 20}" class="mid">each one checked</text>')
    return (f'<svg class="loop-svg" data-draw viewBox="0 0 440 400" aria-hidden="true" '
            f'focusable="false">{"".join(parts)}</svg>')


def loop(steps: list[tuple[str, str]]) -> str:
    fan = {f["name"]: f["colour"] for f in S.cover()["fan"]}
    colours = [fan["html"], fan["pdf"], fan["epub"]]
    items = "".join(f'<li style="--c:{col}"><h3>{e(t)}</h3><p>{e(d)}</p></li>'
                    for (t, d), col in zip(steps, colours))
    return f'<div class="loop">{loop_svg()}<ol class="steps">{items}</ol></div>'


# ---- 3. one source, eight outputs ---------------------------------------------------------

def _numbers(d: str) -> list[float]:
    return [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", d)]


def fan_wide(formats: list[dict], squash: float = 0.5) -> str:
    """The cover's fan, as drawn there, squashed vertically to suit a wide screen."""
    x, y, w, h, rx = S.cover()["box"]
    y0 = y + h  # the lines leave the source box's bottom edge
    sy = lambda y: y0 + (y - y0) * squash  # noqa: E731
    out = []
    for i, f in enumerate(formats):
        n = _numbers(f["d"])
        pts = [(n[k], sy(n[k + 1])) for k in range(0, len(n), 2)]
        d = "M{:.0f},{:.1f} C{:.0f},{:.1f} {:.0f},{:.1f} {:.0f},{:.1f}".format(
            *[v for p in pts for v in p])
        cx, cy, rr = f["dot"]
        out.append(f'<path d="{d}" stroke="{f["colour"]}" pathLength="1" style="--i:{i}"/>'
                   f'<circle cx="{cx}" cy="{sy(cy):.1f}" r="{rr}" fill="{f["colour"]}" style="--i:{i}"/>')
    cream, navy = S.cover()["cream"], S.cover()["navy"]
    sx, sy_ = S.cover()["src"]
    left = min(f["dot"][0] for f in formats) - 80
    right = max(f["dot"][0] for f in formats) + 80
    top = y - 12
    bottom = sy(formats[0]["dot"][1]) + 24
    return (f'<svg class="fan fan-wide" data-draw viewBox="{left} {top} {right - left} {bottom - top:.0f}" '
            f'aria-hidden="true" focusable="false"><g class="lines">{"".join(out)}</g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{navy}" stroke="{cream}" stroke-width="5"/>'
            f'<text x="{sx}" y="{sy_}" class="src">.qmd</text></svg>')


def fan_tall(formats: list[dict]) -> str:
    """The same fan turned on its side for a phone: the source on the left, one row per format.
    The cover's dots are 163 units apart, so each row is 163 units tall."""
    gap = formats[1]["dot"][0] - formats[0]["dot"][0]
    x_first = formats[0]["dot"][0] - gap / 2
    x, y, w, h, _ = S.cover()["box"]
    y0, centre = y + h, x + w / 2  # where the lines leave the source box
    k = 0.145  # how far the cover's 524 units of fan reach across the narrow strip
    out = []
    for i, f in enumerate(formats):
        n = _numbers(f["d"])
        pts = [(110 + (n[j + 1] - y0) * k, n[j] - x_first) for j in range(0, len(n), 2)]
        d = "M{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}".format(
            *[v for p in pts for v in p])
        end = pts[-1]
        out.append(f'<path d="{d}" stroke="{f["colour"]}" pathLength="1" style="--i:{i}"/>'
                   f'<circle cx="{end[0] + 4:.1f}" cy="{end[1]:.1f}" r="13" fill="{f["colour"]}" style="--i:{i}"/>')
    h = gap * len(formats)
    mid = centre - x_first
    cream, navy = S.cover()["cream"], S.cover()["navy"]
    return (f'<svg class="fan fan-tall" data-draw viewBox="0 0 210 {h:.0f}" aria-hidden="true" '
            f'focusable="false"><g class="lines">{"".join(out)}</g>'
            f'<rect x="6" y="{mid - 40:.1f}" width="100" height="80" rx="12" fill="{navy}" stroke="{cream}" stroke-width="4"/>'
            f'<text x="56" y="{mid + 10:.1f}" class="src">.qmd</text></svg>')


def fan(formats: list[dict]) -> str:
    items = "".join(
        f'<li style="--c:{f["colour"]}"><a href="{e(f["href"])}"><code>{f["name"]}</code>'
        f'<span class="t">{e(f["title"])}</span><span class="n">{e(f["note"])}</span></a></li>'
        for f in formats)
    return (f'<div class="fanout">{fan_wide(formats)}{fan_tall(formats)}'
            f'<ul class="formats">{items}</ul></div>')


# ---- 4. what you'll build ---------------------------------------------------------------------

def clip(name: str, gif: str) -> str:
    fig = S.gif_figure(gif)
    w, h = size(f"media/{name}.webp")
    return f"""<figure class="clip">
  <div class="frame">
    <img src="media/{name}.webp" loading="lazy" decoding="async" width="{w}" height="{h}" alt="{e(fig["alt"])}">
    <video muted loop playsinline preload="none" data-src="media/{name}.mp4" width="{w}" height="{h}" aria-hidden="true" tabindex="-1"></video>
    <button class="pause" type="button" hidden aria-pressed="false">Pause</button>
  </div>
  <figcaption>{e(fig["caption"])}</figcaption>
</figure>"""


def card(colour: str, part: str, title: str, number: str, what: str, text: str,
         media: str, links: list[tuple[str, str]]) -> str:
    ls = "".join(f'<a href="{e(h)}">{e(t)}{ICON["right"]}</a>' for t, h in links)
    return f"""<article class="card" style="--c:{colour}">
  {media}
  <div class="card-body">
    <p class="eyebrow">{e(part)}</p>
    <h3>{e(title)}</h3>
    <p class="stat"><span class="num">{number}</span><span class="what">{what}</span></p>
    <p>{text}</p>
    <p class="more">{ls}</p>
  </div>
</article>"""


def code(fn) -> str:
    """A function's source, shown as it runs when the page is built."""
    src = inspect.getsource(fn)
    src = re.sub(r'\n    """.*?"""\n', "\n", src, count=1, flags=re.S)  # the docstring
    return f'<pre class="code"><code>{e(src.rstrip())}</code></pre>'


# ---- 6. contents ------------------------------------------------------------------------------

def _entry(c: dict, solo: bool = False) -> str:
    n = "" if solo else f'<span class="n">{c["label"]}</span>'
    return f'<li><a href="{e(c["href"])}">{n}<span>{e(c["title"])}</span></a></li>'


def toc(t: dict) -> str:
    blocks = [f'<ul class="toc-solo">{"".join(_entry(c, True) for c in t["front"][:1])}</ul>']
    for p in t["parts"]:
        numbered = [c for c in p["chapters"] if c["label"]]
        span = f'Chapters {numbered[0]["label"]}–{numbered[-1]["label"]}'
        blocks.append(f"""<details>
  <summary><span class="pl">{e(p["label"])}</span><span class="pt">{e(p["title"])}</span><span class="pc">{span}</span></summary>
  <ul>{"".join(_entry(c) for c in p["chapters"])}</ul>
</details>""")
    blocks.append(f'<ul class="toc-solo">{"".join(_entry(c, True) for c in t["back"])}</ul>')
    a = t["appendices"]
    blocks.append(f"""<details>
  <summary><span class="pl">{a[0]["label"]}–{a[-1]["label"]}</span><span class="pt">Appendices</span><span class="pc">{e(a[0]["title"])} … {e(a[-1]["title"])}</span></summary>
  <ul>{"".join(_entry(c) for c in a)}</ul>
</details>""")
    return f'<div class="toc">{"".join(blocks)}</div>'


# ---- 7. inside the book -------------------------------------------------------------------------

def inside(items: list[dict]) -> str:
    figs = []
    for it in items:
        w, h = size(f"media/{it['img']}")
        extra = f'<span class="alt"><b>Alt text:</b> {e(it["alt_shown"])}</span>' if it.get("alt_shown") else ""
        figs.append(f"""<figure class="shot {it.get('cls', '')}">
  <a href="{e(it['href'])}"><img src="media/{it['img']}" loading="lazy" decoding="async" width="{w}" height="{h}" alt="{e(it['alt'])}"></a>
  <figcaption>{it['caption']}{extra}</figcaption>
</figure>""")
    return f'<div class="shots">{"".join(figs)}</div>'


# ---- 11, 12. the last word, the footer and the sticky bar ------------------------------------------

def share_row() -> str:
    li = "https://www.linkedin.com/sharing/share-offsite/?url=" + urlquote(S.PAGE_URL, safe="")
    return f"""<div class="share">
  <a class="btn ghost" href="{li}" target="_blank" rel="noopener">{ICON["share"]}Share on LinkedIn</a>
  <button class="btn ghost" type="button" data-copy="{S.PAGE_URL}">{ICON["link"]}<span>Copy link</span></button>
  <span class="copied" role="status" aria-live="polite"></span>
</div>"""


def footer() -> str:
    m, t = S.meta(), S.contents()
    g = next(a for a in t["appendices"] if a["label"] == "G")
    # The copyright page's credits, word for word; its cross-reference becomes a link.
    credits = e(S.paragraph_after("book/copyright.qmd", "**Data and images.**")).replace(
        "@sec-sources", f'<a href="{e(g["href"])}">Appendix G, {e(g["title"])}</a>')
    return f"""<footer class="foot">
<div class="wrap">
  <p>{e(m["rights"])} · <a href="{S.REPO}">Source on GitHub</a> · <a href="{S.REPO}/blob/main/ebook/index.qmd">This page’s source</a></p>
  <p><b>Data and images.</b> {credits}</p>
</div>
</footer>"""


def sticky(size_text: str) -> str:
    return f"""<div class="sticky" hidden>
  <a class="btn primary" href="{S.EPUB_URL}" data-where="sticky">{ICON["down"]}<span>Download EPUB</span><span class="size">{size_text}</span></a>
  <a class="btn secondary" href="{S.BOOK_URL}">Read online</a>
</div>"""
