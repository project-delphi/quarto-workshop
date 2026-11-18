"""WCAG 2.2 contrast, for chapters that report a theme's or a brand's colours.

The formula is the guideline's (https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio): each sRGB
channel is linearised, the channels are weighted into a relative luminance, and the ratio of
the lighter to the darker, each plus 0.05, runs from 1 to 21. The evaluation project's own
tests use the same formula; the chapters read the same files those tests check.
"""
from __future__ import annotations

import re


def luminance(hex_colour: str) -> float:
    digits = hex_colour.lstrip("#")
    if len(digits) == 3:
        digits = "".join(d * 2 for d in digits)
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
              for c in (int(digits[i:i + 2], 16) / 255 for i in (0, 2, 4))]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first: str, second: str) -> float:
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def scss_variables(scss: str) -> dict[str, str]:
    """Every `$name: value;` in a Sass file, with `$other` references resolved, as the
    project's contrast test reads them."""
    found = dict(re.findall(r"^\s*(\$[\w-]+)\s*:\s*([^;]+);", scss, flags=re.M))
    for _ in range(len(found)):
        found = {name: found.get(value.strip(), value).strip() for name, value in found.items()}
    return {k: re.sub(r"\s*//.*$", "", v).strip() for k, v in found.items()}
