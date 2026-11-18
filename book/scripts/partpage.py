"""The "Where we are" roadmap on a part page, with its alt text read from the drawing.

scripts/roadmaps.py draws media/roadmaps/<part>.svg and writes its description (every chapter
of the part, numbered, with what the reader builds there) into the SVG's <desc>. A part page
prints the figure with this function, so the alt text always matches the drawing and the
chapter numbers are the ones the book now has:

    ```{python}
    #| output: asis
    from scripts.partpage import roadmap
    print(roadmap("part-1"))
    ```
"""
from __future__ import annotations

import html
import re
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]


def roadmap(name: str) -> str:
    svg = (BOOK / "media" / "roadmaps" / f"{name}.svg").read_text()
    desc = html.unescape(re.search(r"<desc[^>]*>(.*?)</desc>", svg, re.S).group(1))
    label = re.match(r"(?:Where we are|Dónde estamos): (.*?), (?:highlighted|resaltada)", desc).group(1)
    label = label.split(":")[0]
    where = "Dónde estamos" if desc.startswith("Dónde") else "Where we are"
    alt = desc.replace('"', "&quot;")
    return f'![{where}: {label}.](media/roadmaps/{name}){{.on-light fig-alt="{alt}"}}'
