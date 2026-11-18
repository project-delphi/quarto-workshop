"""The slide theme's text is readable: WCAG 2.2 contrast of at least 4.5:1.

Success criterion 1.4.3, Contrast (Minimum), https://www.w3.org/TR/WCAG22/#contrast-minimum,
asks for 4.5:1 between text and its background (3:1 for large text). Headings are large on
a slide, but this test holds them to 4.5:1 too, with body text, links and the muted text of
captions, the footer and the slide number. The formulas for relative
luminance and contrast ratio are WCAG 2.2's definitions:
https://www.w3.org/TR/WCAG22/#dfn-relative-luminance and
https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio.
"""

import re
from pathlib import Path

import pytest

THEME = Path("acme.scss")
MINIMUM = 4.5
TEXT = ["$body-color", "$link-color", "$presentation-heading-color", "$text-muted"]


def variables(scss: str) -> dict[str, str]:
    """Every `$name: value;` in the theme, with `$other` references resolved."""
    found = dict(re.findall(r"^\s*(\$[\w-]+)\s*:\s*([^;]+);", scss, flags=re.M))
    for _ in range(len(found)):
        found = {name: found.get(value.strip(), value).strip() for name, value in found.items()}
    return found


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


def test_formula_matches_known_ratios():
    assert contrast("#000000", "#ffffff") == pytest.approx(21)
    assert contrast("#777777", "#ffffff") == pytest.approx(4.48, abs=0.01)
    assert contrast("#fff", "#ffffff") == pytest.approx(1)


@pytest.mark.parametrize("name", TEXT)
def test_text_on_background(name):
    colours = variables(THEME.read_text())
    ratio = contrast(colours[name], colours["$body-bg"])
    print(f"{name} {colours[name]} on $body-bg {colours['$body-bg']}: {ratio:.2f}:1")
    assert ratio >= MINIMUM, f"{name} has contrast {ratio:.2f}:1 on the background"
