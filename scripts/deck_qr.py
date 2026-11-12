"""Write assets/deck-qr.svg, the QR code on the workshop deck's title slide.

It opens the published deck, so participants can follow the slides on their own screens; the
URL is read from `title-qr: url:` in index.qmd, which the slide also links to.
Dark modules in the deck's background colour on a warm off-white, with the standard
four-module quiet zone; the viewBox lets theme.scss size it. Run from the repository root
after changing that URL:

    uv run --with segno python scripts/deck_qr.py
"""
import io
import re
from pathlib import Path

import segno

DECK = Path("index.qmd")
OUT = Path("assets/deck-qr.svg")
# The URL comes from the deck's own `title-qr: url:`, so the code and the slide's link agree.
m = re.search(r'^title-qr:\n(?:  .*\n)*?  url: "([^"]+)"', DECK.read_text(), re.M)
if not m:
    raise SystemExit(f"{DECK} has no title-qr url")
URL = m.group(1)

qr = segno.make(URL, error="m", micro=False)
size = qr.symbol_size(scale=1, border=4)[0]
buf = io.BytesIO()
qr.save(buf, kind="svg", scale=1, border=4, dark="#191919", light="#f4f1ea", xmldecl=False,
        svgns=True, omitsize=True, title="QR code: " + URL)
svg = buf.getvalue().decode()
if "viewBox" not in svg:
    svg = svg.replace("<svg ", f'<svg viewBox="0 0 {size} {size}" ', 1)
OUT.write_text(svg + "\n")
print(f"{OUT}: version {qr.version}, error level {qr.error}, {size} modules with the quiet zone")
