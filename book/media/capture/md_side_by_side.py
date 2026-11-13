"""media/gifs/md-*.gif: Markdown's marks, typed on the left and rendered by Quarto on the right (Ch. 4).

One animation per mark (DEMOS): headings, paragraphs, emphasis, lists, a quotation, a horizontal
rule, a link, a picture and a picture that is a link. Each demo is a few steps, each step the
whole source after it. Every step's source is written to a scratch folder and rendered with
`quarto render`, and the right-hand pane shows a screenshot of that real page: Quarto's own HTML,
laid out so its text column is about SHOWN CSS pixels wide (a demo can ask for a laptop's width)
and drawn at ZOOM times the pixel density, so its text is as large as the source's. Between steps the new characters are typed a few per frame,
with the lines being typed highlighted, and the page changes only when a step is complete and
rendered. A note under both panes says what the step shows; a note that names a link's address
reads it from the rendered page. Each GIF starts on its finished frame (media/build.py
poster_first), so the first frame is a usable still.

The photo is examples/london/images/natural-history-museum.jpg (copied to media/london/ by the
`deck` step), credited in ATTRIBUTION.md; it is copied unchanged as hall.jpg, a name short
enough for one line of the source. Plain Markdown needs no Python, so Quarto runs without uv.
Run from book/: uv run --with playwright python media/capture/md_side_by_side.py [md-name ...]
"""
from __future__ import annotations

import difflib
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BOOK / "media"))
from build import MAX_GIF_WIDTH, poster_first  # noqa: E402

GIFS = BOOK / "media" / "gifs"
PHOTO = BOOK / "media" / "london" / "natural-history-museum.jpg"

W = MAX_GIF_WIDTH            # the GIF's width: 800 px, no scaling afterwards
SRC_W = 480                  # the source pane, 27 characters of SRC_FONT; OUT_W is the page's
OUT_W = W - SRC_W
ZOOM = 1.7                   # Quarto's 17 px body text becomes about 29 px
SHOWN = round(OUT_W / ZOOM)  # CSS pixels of the page shown across the pane (188)
MARGIN = 8                   # CSS pixels kept beside and above the page's content
HEAD, NOTE = 50, 58          # the label bars above the panes and the note strip below
SRC_FONT = 28                # px, the source's monospace text; labels and notes are 26 px
FPS = 10
PER_FRAME = 2                # characters typed per frame
PAUSE, HOLD, FIRST, FINAL = 3, 22, 10, 20  # frames: before a render shows, after, at the start and end


@dataclass
class Demo:
    """A GIF: its steps as (whole source, note), an optional starting source already typed, and
    the note on the finished frame. {href} in a note is the first link's address in the page."""
    steps: list[tuple[str, str]]
    final: str
    start: tuple[str, str] | None = None
    files: dict[str, Path] = field(default_factory=dict)
    view: int | None = None  # CSS pixels: render the page this wide, not as narrow as the pane


VISIT = "https://www.visitlondon.com/"          # data/churches.csv's source; the dashboard links it
NHM = "https://www.nhm.ac.uk/visit.html"        # the museum's official page in data/sights.csv
DEMOS = {
    "md-headings": Demo([
        ("# London", "One `#`: the biggest heading"),
        ("# London\n\n## Museums", "`##`: one level down"),
        ("# London\n\n## Museums\n\n### Tate Modern", "`###`: one level further down"),
    # At a phone's width Quarto's theme shrinks large headings towards body size; at a laptop's,
    # where readers preview, the three levels differ as designed.
    ], final="More `#` signs, a smaller heading", view=1280),
    "md-paragraphs": Demo([
        ("Welcome to\nLondon.", "Lines next to each other join up"),
        ("Welcome to\nLondon.\n\nSee the sights.", "A blank line starts a new paragraph"),
    ], final="A blank line starts a new paragraph"),
    "md-emphasis": Demo([
        ("Walk by the **river", "No closing `**` yet: the stars just show"),
        ("Walk by the **river**", "Two stars on each side: bold"),
        ("Walk by the **river**\nat *sunset*.", "One star on each side: italic"),
        ("Walk by the **river**\nat *sunset*.\n\nGo by ~~car~~ Tube.", "Two tildes on each side: struck through"),
    ], final="`**bold**`, `*italic*`, `~~struck through~~`"),
    "md-lists": Demo([
        ("- Tube\n- Bus", "`-` and a space: a bulleted item"),
        ("- Tube\n- Bus\n\n1. British Museum\n2. Tate Modern", "`1.` and a space: a numbered item"),
    ], final="Leave a blank line above a list"),
    "md-quote": Demo([
        ("Tip from a local:\n\n> Many big museums\n> are free.", "`>` at the start of a line: a quotation"),
    ], final="`>` at the start of a line: a quotation", start=("Tip from a local:", "A plain line first")),
    "md-rule": Demo([
        ("Day one: museums.\n\n---", "`---` on a line of its own: a line across"),
        ("Day one: museums.\n\n---\n\nDay two: parks.", "A blank line above it, and one below"),
    ], final="`---` between blank lines: a line across", start=("Day one: museums.", "A plain line first")),
    "md-link": Demo([
        ("Plan with\n[Visit London].", "Square brackets alone just show"),
        (f"Plan with\n[Visit London]({VISIT}).", "The address in `( )` right after: a link"),
    ], final="Click it to open {href}", start=("Plan with\nVisit London.", "Plain text first")),
    "md-image": Demo([
        ("![Central Hall](hall.jpg)", "`!`, the caption in `[ ]`, the file in `( )`"),
    ], final="A picture, with its caption below", files={"hall.jpg": PHOTO}),
    "md-image-link": Demo([
        (f"[![Central Hall](hall.jpg)]({NHM})", "The picture as a link's text: `[ ](address)`"),
    ], final="Click the picture to open {href}", start=("![Central Hall](hall.jpg)", "A picture"),
        files={"hall.jpg": PHOTO}),
}

FRAME = """<!doctype html><html><head><meta charset="utf-8"><style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; width: {w}px; height: {h}px; overflow: hidden; display: grid;
  grid-template-columns: {src_w}px {out_w}px; grid-template-rows: {head}px 1fr {note}px;
  font-family: "Avenir Next", "Helvetica Neue", Arial, sans-serif; background: #13202e; }}
.bar {{ font-size: 26px; font-weight: 600; padding: 0 14px; display: flex; align-items: center; }}
.bar.src {{ background: #24313f; color: #ffffff; }}
.bar.out {{ background: #e6e9ec; color: #3d4b59; }}
#src {{ background: #1b2836; color: #eef2f6; padding: 12px; font: {font}px/1.42 Menlo, monospace;
  overflow: hidden; }}
.ln {{ white-space: pre-wrap; overflow-wrap: anywhere; padding-left: 2ch; text-indent: -2ch;
  min-height: 1.42em; }}
.ln.new {{ background: rgba(121, 212, 178, 0.24); }}
.mk {{ color: #ffcf6e; font-weight: bold; white-space: nowrap; }}
.url {{ color: #a9cdf0; }}
.cur {{ display: inline-block; width: 0; height: 1.2em; border-left: 3px solid #ffcf6e;
  vertical-align: -0.25em; }}
#out {{ background: #ffffff; overflow: hidden; }}
#shot {{ display: block; width: {out_w}px; }}
#note {{ grid-column: 1 / 3; background: #79d4b2; color: #13202e; font-size: 26px; font-weight: 600;
  padding: 0 18px; display: flex; align-items: center; white-space: pre; }}
#note code {{ font: bold 26px Menlo, monospace; background: rgba(19, 32, 46, 0.12); padding: 0 4px;
  border-radius: 4px; }}
</style></head><body>
<div class="bar src">You type</div><div class="bar out">You get</div>
<div id="src"></div><div id="out"><img id="shot" alt=""></div>
<div id="note"></div>
</body></html>"""

SHOW = """async ([src, img, note]) => {
  document.getElementById('src').innerHTML = src;
  document.getElementById('note').innerHTML = note;
  const shot = document.getElementById('shot');
  if (img) {
    if (shot.getAttribute('src') !== img) { shot.src = img; await shot.decode(); }
    shot.style.visibility = 'visible';
  } else {
    shot.style.visibility = 'hidden';
  }
  const n = document.getElementById('note'), s = document.getElementById('src');
  const used = s.lastElementChild.getBoundingClientRect().bottom - s.getBoundingClientRect().top + 12;
  return [used, n.scrollWidth > n.clientWidth];
}"""

# The rendered content, in CSS pixels: the top and bottom of the elements in <main>, its left edge,
# the right edge of its text and pictures (to check that the pane shows all of it), and the
# address of its first link.
CONTENT = """() => {
  const main = document.querySelector('main');
  const boxes = [...main.querySelectorAll('*')].map(e => e.getBoundingClientRect()).filter(b => b.height > 0);
  const ink = [...main.querySelectorAll('img, hr')].map(e => e.getBoundingClientRect());
  const walk = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
  for (let n = walk.nextNode(); n; n = walk.nextNode()) {
    if (!n.textContent.trim()) continue;
    const r = document.createRange();
    r.selectNodeContents(n);
    ink.push(...r.getClientRects());
  }
  const a = main.querySelector('a[href]');
  return {top: Math.min(...boxes.map(b => b.top)) + scrollY, bottom: Math.max(...boxes.map(b => b.bottom)) + scrollY,
          left: main.getBoundingClientRect().left, right: Math.max(...ink.map(b => b.right)),
          href: a ? a.getAttribute('href') : null};
}"""

LINE_START = re.compile(r"^(#{1,6} |> ?|- |\d+\. |---$)")
INLINE = re.compile(r"(\]\()([^)]*)(\)?)|(\*\*|~~|\*|!\[|\[|\])")


def tokens(line: str) -> list[tuple[str, str]]:
    """A source line as (text, class) pieces: Markdown's marks "mk", a link's address "url"."""
    out: list[tuple[str, str]] = []
    m = LINE_START.match(line)
    pos = 0
    if m:
        out.append((m.group(1), "mk"))
        pos = m.end()
    for t in INLINE.finditer(line, pos):
        if t.start() > pos:
            out.append((line[pos:t.start()], ""))
        if t.group(1):
            out += [(t.group(1), "mk"), (t.group(2), "url"), (t.group(3), "mk")]
        else:
            out.append((t.group(4), "mk"))
        pos = t.end()
    if pos < len(line):
        out.append((line[pos:], ""))
    return [(s, c) for s, c in out if s]


def piece_html(s: str, c: str) -> str:
    """A piece of a source line. A line too long for the pane wraps where an editor's would:
    before a link's "](", or after a slash of its address (<wbr>), and not inside a name."""
    if c == "cur":
        return '<span class="cur"></span>'
    text = html.escape(s)
    if c == "url":
        head, sep, rest = s.partition("://")
        text = (html.escape(head + sep) + "<wbr>" + html.escape(rest).replace("/", "/<wbr>")
                if sep else text)
    if c == "mk" and s.startswith("]"):
        return f'<wbr><span class="mk">{text}</span>'
    return f'<span class="{c}">{text}</span>' if c else text


def source_html(text: str, new: set[int], cursor: int | None) -> str:
    """The source pane: one div per line, marks coloured, the lines holding a new character (or a
    new blank line) highlighted, and a cursor at character index `cursor`."""
    lines, start = [], 0
    for line in text.split("\n"):
        end = start + len(line)
        touched = any(i in new for i in range(start, end)) or (
            not line and (end in new or start - 1 in new))
        pieces = tokens(line)
        if cursor is not None and start <= cursor <= end:
            col, cut, placed = cursor - start, [], False
            for s, c in pieces:
                if not placed and col <= len(s):
                    cut += [(s[:col], c), ("", "cur"), (s[col:], c)]
                    placed = True
                else:
                    cut.append((s, c))
                    if not placed:
                        col -= len(s)
            if not placed:  # an empty line
                cut.append(("", "cur"))
            pieces = [(s, c) for s, c in cut if s or c == "cur"]
        body = "".join(piece_html(s, c) for s, c in pieces)
        lines.append(f'<div class="ln{" new" if touched else ""}">{body}</div>')
        start = end + 1
    return "".join(lines)


def note_html(note: str, href: str | None) -> str:
    note = note.replace("{href}", href or "")
    parts = note.split("`")  # `…` is set as code
    return "<span>" + "".join(f"<code>{html.escape(p)}</code>" if i % 2 else html.escape(p)
                              for i, p in enumerate(parts)) + "</span>"


def typing(old: str, new: str) -> list[tuple[str, set[int], int]]:
    """The texts on the way from old to new, PER_FRAME characters at a time, each with the
    indices of the characters typed so far in this step and the cursor's index. The steps only
    insert characters."""
    ops = difflib.SequenceMatcher(a=old, b=new, autojunk=False).get_opcodes()
    if any(tag not in ("equal", "insert") for tag, *_ in ops):
        raise SystemExit(f"a step may only insert characters: {old!r} -> {new!r}")
    inserted = [j for tag, _, _, j1, j2 in ops if tag == "insert" for j in range(j1, j2)]
    frames = []
    for k in list(range(PER_FRAME, len(inserted), PER_FRAME)) + [len(inserted)]:
        typed = set(inserted[:k])
        kept = [j for j in range(len(new)) if j in typed or j not in inserted]
        index = {j: i for i, j in enumerate(kept)}  # index in new -> index in the partial text
        frames.append(("".join(new[j] for j in kept), {index[j] for j in typed},
                       index[inserted[k - 1]] + 1))
    return frames


def render(work: Path, name: str, text: str) -> Path:
    (work / f"{name}.md").write_text(text + "\n")
    subprocess.run(["quarto", "render", f"{name}.md", "--quiet"], cwd=work, check=True)
    return work / f"{name}.html"


def make(name: str, demo: Demo, browser, root: Path) -> None:
    work = root / name
    work.mkdir()
    for rel, src in demo.files.items():
        shutil.copy(src, work / rel)
    states = ([demo.start[0]] if demo.start else []) + [text for text, _ in demo.steps]
    pages = [render(work, f"s{i}", text) for i, text in enumerate(states)]

    # Screenshots of each rendered page: its content, MARGIN CSS pixels round it, SHOWN wide.
    view = browser.new_page(viewport={"width": demo.view or SHOWN + 60, "height": 1600},
                            device_scale_factor=ZOOM)
    shots, href, tallest = [], None, 0
    for i, page_html in enumerate(pages):
        view.goto(page_html.as_uri(), wait_until="load")
        view.wait_for_timeout(300)
        box = view.evaluate(CONTENT)
        # Fit the viewport so the page's text column plus MARGIN on each side is SHOWN wide,
        # unless the demo asks for a wider page (whose content must then fit in SHOWN).
        width = demo.view or round(SHOWN - 2 * MARGIN + 2 * box["left"])
        if view.viewport_size["width"] != width:
            view.set_viewport_size({"width": width, "height": 1600})
            view.wait_for_timeout(200)
            box = view.evaluate(CONTENT)
        if box["right"] > box["left"] + SHOWN - MARGIN:
            raise SystemExit(f"{name}: step {i}'s page is wider than the pane shows")
        top = max(0, box["top"] - MARGIN)
        height = box["bottom"] + MARGIN - top
        png = work / f"s{i}.png"
        view.screenshot(path=str(png), clip={"x": box["left"] - MARGIN, "y": top,
                                             "width": SHOWN, "height": height})
        shots.append(png.as_uri())
        tallest = max(tallest, height * ZOOM)
        href = box["href"] or href
    view.close()

    # The frame: measure the finished source's height first, then size the GIF to fit both panes.
    frame_file = work / "frame.html"
    page = browser.new_page(viewport={"width": W, "height": 1200}, device_scale_factor=1)
    frame_file.write_text(FRAME.format(w=W, h=1200, src_w=SRC_W, out_w=OUT_W, head=HEAD, note=NOTE,
                                       font=SRC_FONT))
    page.goto(frame_file.as_uri())
    src_h, _ = page.evaluate(SHOW, [source_html(states[-1], set(), len(states[-1])), None, ""])
    h = HEAD + NOTE + int(max(src_h, tallest)) + 6
    h += h % 2
    page.set_viewport_size({"width": W, "height": h})
    frame_file.write_text(FRAME.format(w=W, h=h, src_w=SRC_W, out_w=OUT_W, head=HEAD, note=NOTE,
                                       font=SRC_FONT))
    page.goto(frame_file.as_uri())

    frames = work / "frames"
    frames.mkdir()
    count = 0

    def snap(src: str, img: str | None, note: str, repeat: int = 1) -> None:
        nonlocal count
        _, too_wide = page.evaluate(SHOW, [src, img, note_html(note, href)])
        if too_wide:
            raise SystemExit(f"{name}: the note does not fit on one line: {note!r}")
        first = frames / f"f{count:05d}.png"
        page.screenshot(path=str(first))
        count += 1
        for _ in range(repeat - 1):
            os.link(first, frames / f"f{count:05d}.png")
            count += 1

    text, shown = "", None
    notes = [note for _, note in demo.steps]
    if demo.start:
        text, shown = demo.start[0], shots[0]
        snap(source_html(text, set(), len(text)), shown, demo.start[1], FIRST)
    else:
        snap(source_html("", set(), 0), None, notes[0], FIRST)
    offset = 1 if demo.start else 0
    for i, (target, note) in enumerate(demo.steps):
        steps = typing(text, target)
        for partial, new, cursor in steps:
            snap(source_html(partial, new, cursor), shown, note)
        _, new, cursor = steps[-1]
        snap(source_html(target, new, cursor), shown, note, PAUSE)
        shown = shots[offset + i]
        snap(source_html(target, new, cursor), shown, note, HOLD)
        text = target
    snap(source_html(text, set(), None), shown, demo.final, FINAL)
    page.close()

    raw = work / "raw.mkv"  # lossless, so the photo is quantised once, by poster_first
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i",
                    str(frames / "f%05d.png"), "-c:v", "ffv1", "-pix_fmt", "bgr0", str(raw)], check=True)
    out = GIFS / f"{name}.gif"
    poster_first(raw, out, hold=2.0, fps=FPS)
    print("gif", out.relative_to(BOOK), f"{W} x {h}, {count} frames, {out.stat().st_size / 1e3:.0f} KB")


def main(names: list[str]) -> None:
    unknown = set(names) - set(DEMOS)
    if unknown:
        sys.exit("unknown demo(s): " + ", ".join(sorted(unknown)))
    GIFS.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="md-side-"))
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome")
            for name in names or DEMOS:
                make(name, DEMOS[name], browser, root)
            browser.close()
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main(sys.argv[1:])
