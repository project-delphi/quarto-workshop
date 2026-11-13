"""Write the workshop deck's QR codes: assets/deck-qr.svg and assets/ebook-qr.svg.

The title slide's code opens the published deck, so participants can follow the slides on their
own screens; the 📖 Get the Book slide's code opens the e-book's landing page. Each URL and
image path is read from index.qmd's header (`title-qr:` and `ebook-qr:`), which the slides
also link to, so a code and its link always agree. Dark modules in the deck's background colour
on a warm off-white, with the standard four-module quiet zone; the viewBox lets theme.scss size
them. Run from the repository root after changing either URL:

    uv run --with segno python scripts/deck_qr.py
"""
import io
import re
from pathlib import Path

import segno

DECK = Path("index.qmd")
KEYS = ("title-qr", "ebook-qr")


def field(key: str, name: str) -> str:
    """A field of one of the header's QR blocks, such as title-qr: url:."""
    m = re.search(rf'^{key}:\n(?:  .*\n)*?  {name}: "([^"]+)"', DECK.read_text(), re.M)
    if not m:
        raise SystemExit(f"{DECK} has no {key}: {name}:")
    return m.group(1)


for key in KEYS:
    url, out = field(key, "url"), Path(field(key, "image"))
    qr = segno.make(url, error="m", micro=False)
    size = qr.symbol_size(scale=1, border=4)[0]
    buf = io.BytesIO()
    qr.save(buf, kind="svg", scale=1, border=4, dark="#191919", light="#f4f1ea", xmldecl=False,
            svgns=True, omitsize=True, title="QR code: " + url)
    svg = buf.getvalue().decode()
    if "viewBox" not in svg:
        svg = svg.replace("<svg ", f'<svg viewBox="0 0 {size} {size}" ', 1)
    out.write_text(svg + "\n")
    print(f"{out}: {url}, version {qr.version}, error level {qr.error}, "
          f"{size} modules with the quiet zone")
