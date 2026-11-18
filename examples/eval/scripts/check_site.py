"""Check the rendered site for basic accessibility and metadata, after `quarto render`.

Run from the project root:  uv run python scripts/check_site.py

For every page `_site/*.html` it fails when:

- an `<img>` has no alt text, or an empty one (WCAG 2.2, 1.1.1 Non-text Content). Every
  image on this site carries information, so none may be marked decorative with `alt=""`;
- the `<html>` element has no `lang` (3.1.1 Language of Page);
- the page has no `<title>`, or an empty one (2.4.2 Page Titled);
- the page has no `<meta name="description">`, or an empty one: search results and link
  previews show it;
- a heading skips a level going down, such as an `<h1>` followed by an `<h3>` (headings
  are how screen-reader users move around a page; 1.3.1 Info and Relationships).

It also checks that every text colour in _brand.yml has a contrast of at least 4.5:1 on the
brand's background (1.4.3 Contrast (Minimum)), with `acme_eval.brand`. It prints one line
per page and every failure, and exits with status 1 if there is any.
"""

import sys
from html.parser import HTMLParser
from pathlib import Path

from acme_eval import brand

SITE = Path("_site")


class Page(HTMLParser):
    """What the checks need from one page: language, title, description, images, headings."""

    def __init__(self) -> None:
        super().__init__()
        self.lang = None
        self.title = None
        self.in_title = False
        self.description = None
        self.images: list[dict] = []
        self.headings: list[int] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attributes = dict(attrs)
        if tag == "html":
            self.lang = attributes.get("lang")
        elif tag == "title" and self.title is None:
            self.in_title, self.title = True, ""
        elif tag == "meta" and attributes.get("name") == "description":
            self.description = attributes.get("content")
        elif tag == "img":
            self.images.append(attributes)
        elif len(tag) == 2 and tag[0] == "h" and tag[1] in "123456":
            self.headings.append(int(tag[1]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def problems(page: Page) -> list[str]:
    """Everything wrong with one parsed page."""
    found = []
    for image in page.images:
        if not (image.get("alt") or "").strip():
            found.append(f"image without alt text: {image.get('src')}")
    if not (page.lang or "").strip():
        found.append("no lang on <html>")
    if not (page.title or "").strip():
        found.append("no <title>")
    if not (page.description or "").strip():
        found.append('no <meta name="description">')
    for before, after in zip(page.headings, page.headings[1:]):
        if after > before + 1:
            found.append(f"heading skips a level: h{before} then h{after}")
    return found


def brand_problems() -> list[str]:
    """Brand text colours with too little contrast on the brand's background."""
    identity = brand.load()
    background = brand.colour(identity, "background")
    found = []
    for use, text in brand.text_colours(identity).items():
        ratio = brand.contrast(text, background)
        print(f"_brand.yml  {use} {text} on {background}: {ratio:.2f}:1")
        if ratio < brand.MINIMUM:
            found.append(f"_brand.yml: {use} has contrast {ratio:.2f}:1, below {brand.MINIMUM}:1")
    return found


def main() -> int:
    pages = sorted(SITE.glob("*.html"))
    if not pages:
        print(f"No pages in {SITE}/: run `uv run quarto render` first.", file=sys.stderr)
        return 1
    failures = brand_problems()
    for path in pages:
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        found = problems(page)
        print(f"{path}  {len(page.images)} images, headings "
              f"{''.join(map(str, page.headings)) or 'none'}: {'ok' if not found else 'FAIL'}")
        failures += [f"{path}: {problem}" for problem in found]
    for failure in failures:
        print(failure, file=sys.stderr)
    print(f"{len(pages)} pages checked, {len(failures)} problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
