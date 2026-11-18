"""Clear the frozen results of every page that reads a file freeze cannot see.

`freeze: auto` re-runs a page only when the page's own source changes (README.md, "Cached
results and when to clear them"). Some inputs change on their own: facts.yml, the facts that
change, is edited without touching the chapters that quote it. This script keeps a hash of each
such input in _freeze/inputs.json (committed with _freeze/), and when an input's hash differs,
deletes the frozen results of every page whose source names it, so the next render re-runs
just those pages. `make book` runs it before rendering (book-sync).

Run from book/:  uv run python scripts/thaw.py [--book ../book-es]
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
# Each watched input, and the text that marks a page as reading it.
INPUTS = {"facts.yml": ("scripts.facts", "facts.yml")}


def main() -> None:
    root = (Path.cwd() / sys.argv[sys.argv.index("--book") + 1]).resolve() if "--book" in sys.argv else BOOK
    record = root / "_freeze" / "inputs.json"
    seen = json.loads(record.read_text()) if record.exists() else {}
    for name, marks in INPUTS.items():
        digest = hashlib.sha256((BOOK / name).read_bytes()).hexdigest()
        if seen.get(name) == digest:
            continue
        for qmd in sorted(root.glob("**/*.qmd")):
            if "_book" in qmd.parts or not any(m in qmd.read_text() for m in marks):
                continue
            frozen = root / "_freeze" / qmd.relative_to(root).with_suffix("")
            if frozen.exists():
                shutil.rmtree(frozen)
                print(f"thaw: {name} changed; cleared {frozen.relative_to(root)}")
        seen[name] = digest
    record.parent.mkdir(exist_ok=True)
    record.write_text(json.dumps(seen, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
