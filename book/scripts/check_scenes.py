"""Check that the book's live scenes show the same data as the deck's (book/README.md).

scripts/scenes.py repeats the deck cells' computations for the 3-D scenes and the Tunja
explorer, so the two can drift apart. This compares the JSON each embeds: the rendered deck
(../docs/index.html) against the HTML edition (_book/html). Text may differ only in the deck's
decorations: emoji, and circled step numbers (① becomes "1."). Run from book/ after
`make book-html`, with the deck rendered from its current sources:

    uv run python scripts/check_scenes.py
"""
from __future__ import annotations

import json
import math
import re
import sys
import unicodedata
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
DECK = BOOK.parent / "docs" / "index.html"
HTML = BOOK / "_book" / "html" / "chapters"
SCENE = re.compile(r'data-scene="([a-z-]+)".*?<script type="application/json"[^>]*>(.*?)</script>', re.S)
TUNJA = re.compile(r'class="tunja">.*?<script type="application/json"[^>]*>(.*?)</script>', re.S)
CIRCLED = {chr(0x2460 + i): f"{i + 1}." for i in range(20)}
# (name, which occurrence in the deck, book page): the deck's order is London's map, then
# Colombia's relief, both drawn by the "relief" scene.
PAIRS = [("relief", 0, "06-audiences.html"), ("kmeans", 0, "11-cluster.html"),
         ("cloud", 0, "11-cluster.html"), ("relief", 1, "11-cluster.html"),
         ("tunja", 0, "09-explore.html")]


def embedded(text: str) -> dict[str, list]:
    found: dict[str, list] = {}
    for name, data in SCENE.findall(text):
        found.setdefault(name, []).append(json.loads(data))
    found["tunja"] = [json.loads(d) for d in TUNJA.findall(text)]
    return found


def plain(s: str) -> str:
    """Text without the deck's decorations: emoji (symbols, their variation selectors and
    joiners) removed, circled numbers written as "1.", spaces collapsed."""
    s = "".join(CIRCLED.get(ch, ch) for ch in s)
    s = "".join(ch for ch in s if unicodedata.category(ch) not in ("So", "Sk", "Mn", "Cf"))
    return " ".join(s.split())


def differences(a, b, path: str = "") -> list[str]:
    if isinstance(a, dict) and isinstance(b, dict):
        out = [f"{path}.{k}: only in the deck" for k in a.keys() - b.keys()]
        out += [f"{path}.{k}: only in the book" for k in b.keys() - a.keys()]
        for k in sorted(a.keys() & b.keys()):
            out += differences(a[k], b[k], f"{path}.{k}")
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [f"{path}: {len(a)} items in the deck, {len(b)} in the book"]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in differences(x, y, f"{path}[{i}]")]
    if isinstance(a, str) and isinstance(b, str):
        return [] if plain(a) == plain(b) else [f"{path}: {a!r:.60} vs {b!r:.60}"]
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return [] if math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12) else [f"{path}: {a} vs {b}"]
    return [] if a == b else [f"{path}: {a!r:.60} vs {b!r:.60}"]


def main() -> None:
    deck = embedded(DECK.read_text())
    pages: dict[str, dict] = {}
    bad = 0
    for name, n, page in PAIRS:
        if page not in pages:
            pages[page] = embedded((HTML / page).read_text())
        try:
            ours, theirs = pages[page][name][0], deck[name][n]  # one of each per book page
        except (KeyError, IndexError):
            print(f"MISSING {name} in the deck or in {page}")
            bad += 1
            continue
        diffs = differences(theirs, ours)
        if diffs:
            bad += 1
            print(f"DIFFERENT {name} ({page}): {len(diffs)} differences, first: " + "; ".join(diffs[:3]))
    print(f"{len(PAIRS)} scenes compared with the deck, {bad} different")
    if bad:
        print("Make book/scripts/scenes.py match the deck cell, or render the deck (make deck).")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
