"""Write the Word and PowerPoint templates in templates/, in Acme's colours and font.

Run from the project root:  uv run python scripts/make_reference_docs.py

Quarto applies _brand.yml to the web pages, the Reveal.js deck and the Typst PDFs, but not to
Word or PowerPoint: those take their styles from a reference document (`reference-doc`). This
script makes both from Quarto's defaults (`quarto pandoc --print-default-data-file
reference.docx` and `reference.pptx`), with the colours read from _brand.yml, so the brand
stays the one place a colour is set:

- templates/acme-reference.docx, for report.qmd and model-card.qmd: the theme's colours and
  fonts, navy title and headings, ink body text and cobalt links. Word prints on white paper,
  so the brand's paper colour is the theme's background slot only. Word colours headings with
  the theme's accent1 (shaded darker by default), so accent1 is navy and the shade is removed.
- templates/acme-reference.pptx, for slides.qmd: the theme's colours and fonts, and navy,
  left-aligned slide titles. It keeps the default's seven layouts, which pandoc fills by name.

Office cannot use a CSS font list, so both get the brand's last named font (Arial), which
every Windows and macOS machine has. Rerunning the script gives the same bytes.
"""

import re
import subprocess
import zipfile
from io import BytesIO
from pathlib import Path

import yaml

BRAND = Path("_brand.yml")
TEMPLATES = Path("templates")
GENERIC = {"serif", "sans-serif", "monospace", "system-ui", "cursive", "fantasy"}

# The figures' colour-blind-safe palette (Okabe-Ito), as in the documents' plots.
FIGURE_ACCENTS = {
    "accent2": "0072B2",  # v2 in the figures (blue)
    "accent3": "D55E00",  # v3 in the figures (vermillion)
    "accent4": "999999",  # v1 in the figures
    "accent5": "009E73",  # bluish green
    "accent6": "E69F00",  # orange
}


def brand_colours() -> dict[str, str]:
    """The Office theme's colour slots, from _brand.yml's palette and the figure palette."""
    palette = yaml.safe_load(BRAND.read_text())["color"]["palette"]

    def hex_of(name: str) -> str:
        return palette[name].lstrip("#").upper()

    return {
        "dk1": hex_of("ink"),       # text
        "lt1": hex_of("paper"),     # background
        "dk2": hex_of("navy"),      # titles
        "lt2": hex_of("stone"),     # hairlines
        "accent1": hex_of("navy"),  # Word's headings
        **FIGURE_ACCENTS,
        "hlink": hex_of("cobalt"),  # links
        "folHlink": "5A3D8A",
    }


def office_font() -> str:
    """The last named (not generic) font in the brand's base family list."""
    family = yaml.safe_load(BRAND.read_text())["typography"]["base"]["family"]
    names = [f.strip().strip("'\"") for f in family.split(",")]
    return [name for name in names if name not in GENERIC][-1]


def default_reference(name: str) -> bytes:
    """Quarto's default reference document `name`, as bytes."""
    return subprocess.run(
        ["quarto", "pandoc", "--print-default-data-file", name],
        check=True, capture_output=True).stdout


def retheme(xml: str, colours: dict[str, str], font: str) -> str:
    """Set every colour slot and the heading and body fonts of an Office theme."""
    for slot, value in colours.items():
        xml, n = re.subn(rf"<a:{slot}>.*?</a:{slot}>",
                         f'<a:{slot}><a:srgbClr val="{value}"/></a:{slot}>', xml,
                         count=1, flags=re.S)
        assert n == 1, f"no {slot} colour in the theme"
    for kind in ["majorFont", "minorFont"]:
        xml, n = re.subn(rf'(<a:{kind}>\s*<a:latin typeface=")[^"]*(")',
                         rf"\g<1>{font}\g<2>", xml, count=1)
        assert n == 1, f"no {kind} in the theme"
    return xml


def restyle_titles(xml: str) -> str:
    """PowerPoint: make the master's slide titles navy (dk2) and left-aligned."""
    style = re.search(r"<p:titleStyle>.*?</p:titleStyle>", xml, flags=re.S)
    assert style, "no title style in the slide master"
    new = (style.group(0).replace('algn="ctr"', 'algn="l"', 1)
           .replace('<a:schemeClr val="tx1"/>', '<a:schemeClr val="tx2"/>', 1))
    return xml.replace(style.group(0), new)


def restyle_word(xml: str, colours: dict[str, str], font: str) -> str:
    """Word: navy title and headings, ink body text in the brand's font, cobalt links."""
    navy = f'<w:color w:val="{colours["accent1"]}" w:themeColor="accent1" />'
    # Headings 1 to 5 and the table of contents' heading: accent1, without the darker shade.
    xml, n = re.subn(r'<w:color w:val="[0-9A-F]{6}" w:themeColor="accent1"\s+w:themeShade="BF" />',
                     navy, xml)
    assert n >= 5, f"only {n} heading colours found"
    # The title (the subtitle is based on it). In a run's properties the colour comes after
    # the fonts and before the size, as the schema orders them.
    xml, n = re.subn(r'(<w:style w:type="paragraph" w:styleId="Title">.*?)(<w:sz )',
                     rf"\g<1>{navy}\g<2>", xml, count=1, flags=re.S)
    assert n == 1, "no Title style"
    # Links.
    xml, n = re.subn(r'(<w:style w:type="character" w:styleId="Hyperlink">.*?)<w:color [^>]*/>',
                     rf'\g<1><w:color w:val="{colours["hlink"]}" w:themeColor="hyperlink" />',
                     xml, count=1, flags=re.S)
    assert n == 1, "no Hyperlink colour"
    # Body text: the Normal style, which every paragraph style is based on, in ink and in the
    # font by name, since some viewers (macOS Quick Look) ignore the theme's body font.
    xml, n = re.subn(r'(<w:style w:type="paragraph" w:default="1" w:styleId="Normal">\s*'
                     r'<w:name w:val="Normal" />\s*<w:qFormat />)',
                     rf'\g<1><w:rPr><w:rFonts w:ascii="{font}" w:hAnsi="{font}" />'
                     rf'<w:color w:val="{colours["dk1"]}" w:themeColor="text1" /></w:rPr>',
                     xml, count=1)
    assert n == 1, "no Normal style"
    return xml


def write(name: str, changes: dict) -> None:
    """Copy Quarto's default `name` into templates/, changing the parts in `changes`."""
    source = zipfile.ZipFile(BytesIO(default_reference(name)))
    out = TEMPLATES / f"acme-{name}"
    TEMPLATES.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            content = source.read(item.filename)
            if item.filename in changes:
                content = changes[item.filename](content.decode("utf-8")).encode("utf-8")
            item.date_time = (2026, 1, 1, 0, 0, 0)  # the same bytes on every run
            target.writestr(item, content)
    print(f"Wrote {out}")


def main() -> None:
    colours, font = brand_colours(), office_font()
    write("reference.docx", {
        "word/theme/theme1.xml": lambda xml: retheme(xml, colours, font),
        "word/styles.xml": lambda xml: restyle_word(xml, colours, font),
    })
    write("reference.pptx", {
        "ppt/theme/theme1.xml": lambda xml: retheme(xml, colours, font),
        "ppt/slideMasters/slideMaster1.xml": restyle_titles,
    })


if __name__ == "__main__":
    main()
