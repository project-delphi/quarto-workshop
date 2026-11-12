"""media/figures/pelican-grid.png: the 12 pelicans in one image, for the EPUB.

A 5-column table of images does not fit a phone, so the EPUB shows one composite: a row per
model, a column per effort, each cell's cost below its picture. Images and costs come from
media/deck/pelicans/ and the deck's assets/pelicans/README.md (Simon Willison's runs; costs
at API list prices checked 2026-11-06). Run from book/ (media/build.py capture).
"""
from __future__ import annotations

import re
from pathlib import Path

from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[2]
PELICANS = BOOK / "media" / "deck" / "pelicans"
README = BOOK.parent / "assets" / "pelicans" / "README.md"
OUT = BOOK / "media" / "figures" / "pelican-grid.png"
MODELS = [("haiku", "Haiku 5.5"), ("sonnet", "Sonnet 5.5"), ("opus", "Opus 5.5"), ("fable", "Fable 5.1")]
EFFORTS = ["low", "medium", "high"]

cost = {m.group(1): m.group(2) for m in re.finditer(
    r"\| `([a-z]+-[a-z]+)\.svg` \|.*\| ([\d.]+) \|\s*$", README.read_text(), re.M)}
assert len(cost) == 12, cost

cells = []
for key, name in MODELS:
    row = [f'<div class="lab">{name}</div>']
    for effort in EFFORTS:
        stem = f"{key}-{effort}"
        pick = " pick" if effort == "medium" and key in ("haiku", "sonnet") else ""
        row.append(f'<div class="cell{pick}"><img src="{(PELICANS / f"{stem}.svg").as_uri()}">'
                   f'<span>{cost[stem]}¢{" · enough" if pick else ""}</span></div>')
    cells.append("".join(row))
html = f"""<!doctype html><html><head><style>
body {{ margin: 0; background: transparent; font-family: "Avenir Next", "Helvetica Neue", Arial, sans-serif; color: #24313f; }}
.grid {{ display: grid; grid-template-columns: 110px repeat(3, 196px); gap: 10px 12px; padding: 12px; width: max-content; }}
.head {{ font-weight: 700; font-size: 18px; text-align: center; }}
.lab {{ font-weight: 700; font-size: 18px; align-self: center; }}
.cell {{ text-align: center; font-size: 16px; }}
.cell img {{ width: 192px; height: 144px; object-fit: contain; border: 2px solid #d5dbe1; border-radius: 6px; background: #fff; }}
.cell.pick img {{ border-color: #2f9e77; }}
.cell span {{ display: block; margin-top: 2px; }}
</style></head><body><div class="grid" id="g">
<div></div>{"".join(f'<div class="head">{e} effort</div>' for e in EFFORTS)}
{"".join(cells)}
</div></body></html>"""
OUT.parent.mkdir(parents=True, exist_ok=True)
page_file = OUT.with_suffix(".html")
page_file.write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    page = b.new_page(device_scale_factor=2)
    page.goto(page_file.as_uri())
    page.wait_for_timeout(300)
    page.locator("#g").screenshot(path=str(OUT), omit_background=True)
    b.close()
page_file.unlink()
print("figure", OUT.relative_to(BOOK))
