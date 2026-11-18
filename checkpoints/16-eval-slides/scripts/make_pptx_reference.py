"""Write templates/acme-reference.pptx, the PowerPoint template for slides.qmd.

Run from the project root:  uv run python scripts/make_pptx_reference.py

It starts from Quarto's default reference document (`quarto pandoc
--print-default-data-file reference.pptx`) and changes only its theme: the colours of
acme.scss, Arial for headings and text, and navy, left-aligned slide titles. PowerPoint
cannot use a CSS font list, so it gets Arial, the list's last named font, which every
Windows and macOS machine has. The template keeps the default's seven layouts, which
pandoc fills by name.
"""

import re
import subprocess
import zipfile
from io import BytesIO
from pathlib import Path

OUT = Path("templates/acme-reference.pptx")
THEME = "ppt/theme/theme1.xml"
MASTER = "ppt/slideMasters/slideMaster1.xml"
FONT = "Arial"

# The theme's colour slots, from acme.scss and the figures' colour-blind-safe palette.
COLOURS = {
    "dk1": "1B2733",      # text: $acme-ink
    "lt1": "FBFAF7",      # background: $acme-paper
    "dk2": "0B3D63",      # titles: $acme-navy
    "lt2": "D9D6CF",      # hairlines: $acme-rule
    "accent1": "0B3D63",  # navy
    "accent2": "0072B2",  # v2 in the figures (Okabe-Ito blue)
    "accent3": "D55E00",  # v3 in the figures (Okabe-Ito vermillion)
    "accent4": "999999",  # v1 in the figures
    "accent5": "009E73",  # Okabe-Ito bluish green
    "accent6": "E69F00",  # Okabe-Ito orange
    "hlink": "0B5CAD",    # links: $acme-link
    "folHlink": "5A3D8A",
}


def default_reference() -> bytes:
    """Quarto's default reference.pptx, as bytes."""
    return subprocess.run(
        ["quarto", "pandoc", "--print-default-data-file", "reference.pptx"],
        check=True, capture_output=True).stdout


def retheme(xml: str) -> str:
    """Set every colour slot and the heading and body fonts of a theme."""
    for slot, value in COLOURS.items():
        xml, n = re.subn(rf"<a:{slot}>.*?</a:{slot}>",
                         f'<a:{slot}><a:srgbClr val="{value}"/></a:{slot}>', xml, count=1)
        assert n == 1, f"no {slot} colour in the theme"
    for kind in ["majorFont", "minorFont"]:
        xml, n = re.subn(rf'(<a:{kind}><a:latin typeface=")[^"]*(")',
                         rf"\g<1>{FONT}\g<2>", xml, count=1)
        assert n == 1, f"no {kind} in the theme"
    return xml


def restyle_titles(xml: str) -> str:
    """Make the master's slide titles navy (dk2) and left-aligned."""
    style = re.search(r"<p:titleStyle>.*?</p:titleStyle>", xml, flags=re.S)
    assert style, "no title style in the slide master"
    new = (style.group(0).replace('algn="ctr"', 'algn="l"', 1)
           .replace('<a:schemeClr val="tx1"/>', '<a:schemeClr val="tx2"/>', 1))
    return xml.replace(style.group(0), new)


def main() -> None:
    source = zipfile.ZipFile(BytesIO(default_reference()))
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            content = source.read(item.filename)
            if item.filename == THEME:
                content = retheme(content.decode("utf-8")).encode("utf-8")
            elif item.filename == MASTER:
                content = restyle_titles(content.decode("utf-8")).encode("utf-8")
            item.date_time = (2026, 1, 1, 0, 0, 0)  # the same bytes on every run
            target.writestr(item, content)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
