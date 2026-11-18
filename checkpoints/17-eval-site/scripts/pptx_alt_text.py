"""Give the figures in _site/slides.pptx their alt text, after `quarto render`.

_quarto.yml runs it after every render (`post-render`); by hand, from the project root:
uv run python scripts/pptx_alt_text.py

Reveal.js gets each figure's `fig-alt`, but pandoc's PowerPoint writer (pandoc 3.10, in
Quarto 1.10) writes the image's file name as its description. That file name contains the
cell's label (`slides_files/figure-pptx/<label>-output-1.png`), so this script reads each
label's `#| fig-alt:` from slides.qmd and puts it in the picture's description. It stops if
a picture has no alt text to give it. After a render that did not write the PowerPoint deck
(Quarto lists a render's files in QUARTO_PROJECT_OUTPUT_FILES), it has nothing to do.
"""

import os
import re
import sys
import zipfile
from html import escape
from io import BytesIO
from pathlib import Path

SOURCE = Path("slides.qmd")
DECK = Path("_site/slides.pptx")


def alt_texts(qmd: str) -> dict[str, str]:
    """Each cell label with a `fig-alt` option, mapped to that alt text."""
    found = {}
    for cell in re.findall(r"```\{python\}\n((?:#\|.*\n)+)", qmd):
        options = dict(re.findall(r'#\|\s*([\w-]+):\s*"?(.*?)"?\s*$', cell, flags=re.M))
        if "label" in options and "fig-alt" in options:
            found[options["label"]] = options["fig-alt"]
    return found


def main() -> int:
    rendered = os.environ.get("QUARTO_PROJECT_OUTPUT_FILES")
    if rendered is not None and DECK.name not in {Path(f).name for f in rendered.split()}:
        return 0  # a render of other pages: the deck is as it was
    alts = alt_texts(SOURCE.read_text())
    missing = []

    def describe(match: re.Match) -> str:
        label = re.search(r"([\w-]+)-output-\d+\.\w+$", match.group(1))
        if not label or label.group(1) not in alts:
            missing.append(match.group(1))
            return match.group(0)
        return f'descr="{escape(alts[label.group(1)], quote=True)}"'

    source = zipfile.ZipFile(BytesIO(DECK.read_bytes()))
    out = BytesIO()
    pictures = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            content = source.read(item.filename)
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", item.filename):
                xml = content.decode("utf-8")
                xml, n = re.subn(r'descr="([^"]*figure-pptx/[^"]*)"', describe, xml)
                pictures += n
                content = xml.encode("utf-8")
            target.writestr(item, content)
    if missing:
        print(f"No fig-alt in {SOURCE} for: {', '.join(missing)}", file=sys.stderr)
        return 1
    DECK.write_bytes(out.getvalue())
    print(f"Gave {pictures} pictures in {DECK} their alt text")
    return 0


if __name__ == "__main__":
    sys.exit(main())
