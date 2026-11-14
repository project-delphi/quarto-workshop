"""Give every Spanish heading the section ID its English twin has.

Pandoc makes an ID from a heading's text when the heading has none, so an untranslated
"## Who this book is for {.unnumbered}" is #who-this-book-is-for, and its translation would
become #para-quien-es-este-libro. This writes the English ID into each Spanish heading that has
no explicit one, so links and fragments line up one-to-one across the editions.

The English IDs come from pandoc_id(), which follows Pandoc's auto_identifiers rule; the
English website edition, when built (book/_book/html), is used to check them.

    python3 translation/heading_ids.py          # rewrite book-es/ files in place
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "translation"))
from compare import EN, ES, HEADING, blocks, repeated_auto_ids  # noqa: E402

ID_IN = re.compile(r"(?<![\w&])#([A-Za-z][\w:.-]*)")


def pandoc_id(text: str) -> str:
    """Pandoc's auto_identifiers: drop formatting and punctuation, lower-case, spaces to hyphens,
    and drop everything before the first letter."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)      # links keep their text
    text = re.sub(r"[`*_]", "", text) if "`" in text or "*" in text else text
    text = text.lower()
    text = "".join(ch for ch in text if ch.isalnum() or ch in " _-.")
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"^[^a-z]+", "", text)
    return text or "section"


def headings(text: str):
    """(line index, level, text, attribute block) for each heading outside fences."""
    out, lines, inside = [], text.split("\n"), False
    fence = None
    for i, line in enumerate(lines):
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if m:
            if fence is None:
                fence = m.group(1)
            elif line.strip().startswith(fence[0] * len(fence)) and line.strip().strip(fence[0]) == "":
                fence = None
            continue
        if fence is None:
            h = HEADING.match(line)
            if h:
                out.append((i, len(h.group(1)), h.group(2), h.group(3) or ""))
    return out


def english_html_ids(rel: str) -> list[str] | None:
    page = EN / "_book" / "html" / Path(rel).with_suffix(".html")
    if not page.exists():
        return None
    return re.findall(r'<section id="([^"]+)" class="level[1-6]', page.read_text())


def main() -> int:
    changed, repeated = 0, repeated_auto_ids()
    for pattern in ("*.qmd", "chapters/*.qmd", "appendices/*.qmd"):
        for es_path in sorted(ES.glob(pattern)):
            rel = str(es_path.relative_to(ES))
            en_h, es_lines = headings((EN / rel).read_text()), es_path.read_text().split("\n")
            es_h = headings("\n".join(es_lines))
            if len(en_h) != len(es_h):
                print(f"{rel}: {len(en_h)} English headings, {len(es_h)} Spanish: fix the headings first")
                return 1
            html_ids = english_html_ids(rel)
            for (_, level, text, attrs), (j, _, es_text, es_attrs) in zip(en_h, es_h):
                explicit = ID_IN.search(attrs)
                if explicit:
                    continue
                if ID_IN.search(es_attrs):
                    continue
                want = pandoc_id(text)
                if want in repeated:  # numbered by Pandoc in the EPUB; see compare.repeated_auto_ids
                    continue
                if html_ids is not None and level > 1 and want not in html_ids:  # an h1 is the page title
                    print(f"{rel}: computed #{want} for {text!r} is not in the English HTML")
                    return 1
                if es_attrs:  # the ID first: Pandoc reads no #id after a key=value pair
                    new_attrs = "{#" + want + " " + es_attrs[1:]
                else:
                    new_attrs = "{#" + want + "}"
                line = es_lines[j]
                es_lines[j] = (line[: line.rindex(es_attrs)] + new_attrs) if es_attrs else line.rstrip() + " " + new_attrs
                changed += 1
            es_path.write_text("\n".join(es_lines))
    print(f"{changed} Spanish headings given their English IDs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
