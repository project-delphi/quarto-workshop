"""Clear the frozen results of every page that reads a file freeze cannot see.

`freeze: auto` re-runs a page only when the page's own source changes (README.md, "Cached
results and when to clear them"). Some inputs change on their own: facts.yml, the facts that
change, is edited without touching the chapters that quote it, and the evaluation project
(examples/eval/: its data, code and lock file) can change under the chapters that quote its
results. This script keeps a hash of each
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
# Each watched input (files or folders, relative to book/), and the text that marks a page as
# reading it.
EVAL = "../examples/eval"
INPUTS = {
    "facts.yml": (["facts.yml"], ("scripts.facts", "facts.yml")),
    # The evaluation's results: the code and data that compute outputs/.
    "examples/eval": ([f"{EVAL}/{p}" for p in ("data", "src", "scripts", "releases.yml", "uv.lock")],
                      ("scripts import evaluation", "scripts.evaluation")),
    # A chapter that quotes a checkpoint's files names that checkpoint's folder.
    "checkpoints/16-eval-slides": (["../checkpoints/16-eval-slides/acme.scss",
                                    "../checkpoints/16-eval-slides/slides.qmd"],
                                   ("16-eval-slides",)),
    "checkpoints/17-eval-site": (["../checkpoints/17-eval-site/_brand.yml",
                                  "../checkpoints/17-eval-site/_quarto.yml"],
                                 ("17-eval-site",)),
}


def digest(paths: list[str]) -> str:
    """One hash over every file under the given paths, in a fixed order."""
    h = hashlib.sha256()
    for rel in paths:
        path = BOOK / rel
        files = [path] if path.is_file() else sorted(
            p for p in path.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
        for f in files:
            h.update(f.relative_to(BOOK.parent).as_posix().encode() + b"\0" + f.read_bytes())
    return h.hexdigest()


def main() -> None:
    root = (Path.cwd() / sys.argv[sys.argv.index("--book") + 1]).resolve() if "--book" in sys.argv else BOOK
    record = root / "_freeze" / "inputs.json"
    seen = json.loads(record.read_text()) if record.exists() else {}
    for name, (paths, marks) in INPUTS.items():
        current = digest(paths)
        if seen.get(name) == current:
            continue
        for qmd in sorted(root.glob("**/*.qmd")):
            if "_book" in qmd.parts or not any(m in qmd.read_text() for m in marks):
                continue
            frozen = root / "_freeze" / qmd.relative_to(root).with_suffix("")
            if frozen.exists():
                shutil.rmtree(frozen)
                print(f"thaw: {name} changed; cleared {frozen.relative_to(root)}")
        seen[name] = current
    record.parent.mkdir(exist_ok=True)
    record.write_text(json.dumps(seen, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
