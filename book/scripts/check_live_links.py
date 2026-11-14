"""Check the EPUB's links into the website edition (book/README.md, "Checking a build").

Every link in the EPUB to the published HTML edition, and every QR code target in
media/build.py, must name a page that exists in _book/html and, if it has a #fragment, an id
on that page. Links to the workshop deck (#/slide-id) are checked against ../docs/index.html.
Run from book/ after building both editions:

    uv run python scripts/check_live_links.py _book/epub/prompt-check-publish.epub

For the Spanish edition, name its folder: its links go to the Spanish website edition (book/es/):

    uv run python scripts/check_live_links.py ../book-es/_book/epub/prompt-check-publish-es.epub --edition ../book-es
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK / "media"))
from build import LIVE, QR_TARGETS  # noqa: E402

DECK = "https://project-delphi.github.io/quarto-workshop/#/"
EDITION, BASE, TARGETS = BOOK, LIVE, QR_TARGETS   # main() switches them for --edition


def problem(url: str) -> str | None:
    if url.startswith(DECK):
        slide = url[len(DECK):]
        deck = (BOOK.parent / "docs" / "index.html").read_text()
        return None if f'id="{slide}"' in deck else "no such slide in docs/index.html"
    page, _, frag = url[len(BASE):].partition("#")
    path = EDITION / "_book" / "html" / (page or "index.html")
    if path.is_dir():
        path = path / "index.html"
    if not path.exists():
        return f"no page _book/html/{page}"
    if frag and f'id="{frag}"' not in path.read_text():
        return f"no id {frag!r} on {page}"
    return None


def main(epub: str) -> None:
    global EDITION, BASE, TARGETS
    if "--edition" in sys.argv:
        EDITION = (Path.cwd() / sys.argv[sys.argv.index("--edition") + 1]).resolve()
        BASE = LIVE + "es/"
        TARGETS = {name: url.replace(LIVE, BASE, 1) for name, url in QR_TARGETS.items()}
    with zipfile.ZipFile(epub) as z:
        text = "".join(z.read(n).decode("utf-8") for n in z.namelist() if n.endswith(".xhtml"))
    urls = set(re.findall(r'href="((?:%s|%s)[^"]*)"' % (re.escape(BASE), re.escape(DECK)), text))
    urls |= set(TARGETS.values())
    bad = [(u, p) for u in sorted(urls) if (p := problem(u))]
    for url, why in bad:
        print(f"BROKEN {url}: {why}")
    print(f"{len(urls)} links into the website edition and the deck checked, {len(bad)} broken")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1])
