"""Link each page of the website edition to its other-language twin (translation/PLAN.md).

The English edition is published at book/ and the Spanish one at book/es/, with the same
relative paths, so chapters/09-explore.html in one is chapters/09-explore.html in the other.
For every HTML page of each built edition this adds, once (it is safe to run again):

- <link rel="alternate" hreflang> to both editions, and x-default to the English one, in <head>;
- a visible EN | ES switch in the sidebar beside the book's tools, and in the narrow screen's
  top bar, the current language marked with aria-current.

Run from book/ after rendering an edition:  uv run python scripts/lang_switch.py
It processes whichever of _book/html and ../book-es/_book/html exist.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
SITE = "https://project-delphi.github.io/quarto-workshop/book/"
EDITIONS = {"en": (BOOK / "_book" / "html", ""), "es": (BOOK.parent / "book-es" / "_book" / "html", "es/")}
LABEL = {"en": ("EN", "English"), "es": ("ES", "Español")}
MARK = re.compile(r"<!-- lang-switch -->.*?<!-- /lang-switch -->", re.S)
TOOLS_END = re.compile(r'(<div class="sidebar-tools-main[^"]*">.*?</div>)', re.S)
SEARCH = '<button type="button" class="btn quarto-search-button"'


def url(lang: str, rel: str) -> str:
    page = "" if rel == "index.html" else rel
    return SITE + EDITIONS[lang][1] + page


def switch(lang: str, rel: str, cls: str) -> str:
    """EN | ES, each a relative link to that edition's twin of this page."""
    here = Path(EDITIONS[lang][1]) / rel
    links = []
    for other in EDITIONS:
        short, name = LABEL[other]
        if other == lang:
            links.append(f'<span lang="{other}" aria-current="true" title="{name}">{short}</span>')
            continue
        there = Path(EDITIONS[other][1]) / rel
        href = os.path.relpath(there, here.parent)
        links.append(f'<a href="{href}" hreflang="{other}" lang="{other}" title="{name}">{short}</a>')
    return (f'<!-- lang-switch --><nav class="lang-switch {cls}" aria-label="Language / Idioma">'
            + ' <span aria-hidden="true">|</span> '.join(links) + "</nav><!-- /lang-switch -->")


def add(path: Path, lang: str, rel: str) -> bool:
    text = MARK.sub("", path.read_text(encoding="utf-8"))
    head = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(l, rel)}">' for l in EDITIONS)
    head += f'<link rel="alternate" hreflang="x-default" href="{url("en", rel)}">'
    text = text.replace("</head>", f"<!-- lang-switch -->{head}<!-- /lang-switch -->\n</head>", 1)
    text, n_side = TOOLS_END.subn(lambda m: m.group(1) + switch(lang, rel, "lang-switch-sidebar"), text, 1)
    if SEARCH in text:
        text = text.replace(SEARCH, switch(lang, rel, "lang-switch-top") + SEARCH, 1)
    path.write_text(text, encoding="utf-8")
    return bool(n_side)


def main() -> None:
    for lang, (root, _) in EDITIONS.items():
        if not root.exists():
            continue
        pages = sorted(p for p in root.rglob("*.html") if "site_libs" not in p.parts)
        n = sum(add(p, lang, p.relative_to(root).as_posix()) for p in pages)
        print(f"lang_switch: {lang}: {len(pages)} pages linked to their twins, {n} with a sidebar switch")


if __name__ == "__main__":
    main()
