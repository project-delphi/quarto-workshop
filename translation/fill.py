"""Put the English edition's code fences, verbatim, into a Spanish draft.

A draft names each fence it keeps unchanged by a line `@@CODE n@@` (n counts the English
file's fences from 1, executable cells and display fences alike); this writes the draft
with every such line replaced by that fence, opening and closing lines included, so no code is
retyped. Fences the translation changes (prompts) are written out in the draft itself, and a
cell with translated strings can be prepared in a file and placed with `@@INCLUDE path@@`.

    python3 translation/fill.py chapters/01-quarto.qmd < draft.qmd   # writes book-es/<file>
    python3 translation/fill.py --list chapters/01-quarto.qmd        # numbers the fences
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")


def fences(text: str) -> list[str]:
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if m:
            marker, j = m.group(2), i + 1
            close = re.compile(rf"^\s*{re.escape(marker[0])}{{{len(marker)},}}\s*$")
            while j < len(lines) and not close.match(lines[j]):
                j += 1
            out.append("\n".join(lines[i:j + 1]))
            i = j + 1
            continue
        i += 1
    return out


def main(args: list[str]) -> None:
    if args[0] == "--list":
        for n, f in enumerate(fences((ROOT / "book" / args[1]).read_text()), 1):
            first = f.split("\n")
            print(f"{n:3}: {first[0]}  {first[1][:70] if len(first) > 1 else ''}")
        return
    rel = args[0]
    en = fences((ROOT / "book" / rel).read_text())
    draft = sys.stdin.read()
    used = set()

    def put(m: re.Match) -> str:
        n = int(m.group(1))
        used.add(n)
        return en[n - 1]

    out = re.sub(r"^@@CODE (\d+)@@$", put, draft, flags=re.M)
    # A cell whose page-facing strings are translated (decision D3) is prepared in a file.
    out = re.sub(r"^@@INCLUDE (\S+)@@$", lambda m: Path(m.group(1)).read_text().rstrip("\n"), out, flags=re.M)
    (ROOT / "book-es" / rel).write_text(out)
    print(f"wrote book-es/{rel}: {len(used)} of {len(en)} English fences kept verbatim")


if __name__ == "__main__":
    main(sys.argv[1:])
