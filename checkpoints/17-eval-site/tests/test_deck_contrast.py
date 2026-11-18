"""The brand's text is readable: WCAG 2.2 contrast of at least 4.5:1 on its background.

_brand.yml sets the colours of the site, the Reveal.js deck and the PDFs; acme.scss adds the
deck's muted text (footer and slide number), as a brand colour. Headings are
large on a slide, but this test holds them to 4.5:1 too, with body text, links and muted
text. The formulas are in `acme_eval.brand` (WCAG 2.2's definitions).
"""

import re
from pathlib import Path

import pytest

from acme_eval import brand

THEME = Path("acme.scss")
BRAND = brand.load()
BACKGROUND = brand.colour(BRAND, "background")


def test_formula_matches_known_ratios():
    assert brand.contrast("#000000", "#ffffff") == pytest.approx(21)
    assert brand.contrast("#777777", "#ffffff") == pytest.approx(4.48, abs=0.01)
    assert brand.contrast("#fff", "#ffffff") == pytest.approx(1)


@pytest.mark.parametrize("use", brand.text_colours(BRAND))
def test_brand_text_on_background(use):
    text = brand.text_colours(BRAND)[use]
    ratio = brand.contrast(text, BACKGROUND)
    print(f"{use} {text} on background {BACKGROUND}: {ratio:.2f}:1")
    assert ratio >= brand.MINIMUM, f"{use} has contrast {ratio:.2f}:1 on the background"


def test_deck_muted_text_on_background():
    scss = THEME.read_text()
    muted = re.search(r"^\$text-muted:\s*\$brand-([\w-]+)\s*;", scss, flags=re.M)
    assert muted, "acme.scss sets $text-muted to a brand colour"
    ratio = brand.contrast(brand.colour(BRAND, muted.group(1)), BACKGROUND)
    assert ratio >= brand.MINIMUM, f"$text-muted has contrast {ratio:.2f}:1 on the background"


def test_deck_theme_takes_its_colours_from_the_brand():
    code = re.sub(r"//.*", "", THEME.read_text())  # comments may mention colours
    assert not re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", code), \
        "acme.scss sets a colour of its own: add it to _brand.yml's palette instead"
