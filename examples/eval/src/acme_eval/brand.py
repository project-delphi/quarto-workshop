"""Acme's brand colours, read from _brand.yml, and the WCAG contrast of text on them.

WCAG 2.2 success criterion 1.4.3, Contrast (Minimum),
https://www.w3.org/TR/WCAG22/#contrast-minimum, asks for 4.5:1 between text and its
background (3:1 for large text). The formulas for relative luminance and contrast ratio are
WCAG 2.2's definitions: https://www.w3.org/TR/WCAG22/#dfn-relative-luminance and
https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio.
"""

import re
from pathlib import Path

import yaml

BRAND = Path("_brand.yml")
MINIMUM = 4.5


def load(path: Path = BRAND) -> dict:
    """The parsed brand file."""
    return yaml.safe_load(path.read_text())


def colour(brand: dict, name: str) -> str:
    """A brand colour as `#rrggbb`: a palette name, a role (`primary`) or a hex value."""
    palette, roles = brand["color"]["palette"], brand["color"]
    for _ in range(3):  # a role may name a palette colour, or another role
        if name in palette:
            name = palette[name]
        elif name in roles and name != "palette":
            name = roles[name]
    assert re.fullmatch(r"#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6}", name), f"not a colour: {name}"
    return name.lower()


def text_colours(brand: dict) -> dict[str, str]:
    """Every colour the brand sets for text, by what it colours."""
    typography = brand.get("typography", {})
    return {
        "body text (foreground)": colour(brand, "foreground"),
        "headings": colour(brand, typography.get("headings", {}).get("color", "foreground")),
        "links": colour(brand, typography.get("link", {}).get("color", "primary")),
        # A brand need not set `secondary`; muted text then falls back to the foreground.
        "muted text (secondary)": colour(brand, "secondary" if "secondary" in brand["color"]
                                         else "foreground"),
    }


def rgb(hex_colour: str) -> tuple[float, float, float]:
    """A `#rrggbb` or `#rgb` colour as three channels between 0 and 1."""
    digits = hex_colour.lstrip("#")
    if len(digits) == 3:
        digits = "".join(d * 2 for d in digits)
    assert re.fullmatch(r"[0-9a-fA-F]{6}", digits), f"not a hex colour: {hex_colour}"
    return tuple(int(digits[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(hex_colour: str) -> float:
    """WCAG relative luminance: linearise each sRGB channel, then weight them."""
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
              for c in rgb(hex_colour)]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first: str, second: str) -> float:
    """WCAG contrast ratio, (lighter + 0.05) / (darker + 0.05), from 1 to 21."""
    lighter, darker = sorted([luminance(first), luminance(second)], reverse=True)
    return (lighter + 0.05) / (darker + 0.05)
