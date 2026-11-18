"""Check that the newest evaluation checkpoint is the finished example, file for file.

examples/eval/ is the Acme project as the book leaves it, and the newest checkpoint is the same
state for readers to catch up to; only their READMEs differ. A fix made to one and not the other
(as happened once, when a review's fixes reached examples/eval/ but not the checkpoint) stops
`make book` here. Compares the files Git tracks, so outputs and environments are ignored.

Run from book/:  uv run python scripts/check_latest_checkpoint.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "eval"


def tracked(folder: Path) -> set[str]:
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=folder, capture_output=True, text=True, check=True).stdout
    return set(out.split("\n")) - {""}


def main() -> int:
    latest = max((ROOT / "checkpoints").glob("*-eval-*"))
    a, b = tracked(EXAMPLE) - {"README.md"}, tracked(latest) - {"README.md"}
    problems = [f"only in examples/eval: {f}" for f in sorted(a - b)]
    problems += [f"only in {latest.name}: {f}" for f in sorted(b - a)]
    problems += [f"differs: {f}" for f in sorted(a & b)
                 if (EXAMPLE / f).read_bytes() != (latest / f).read_bytes()]
    for p in problems:
        print(f"check_latest_checkpoint: {p}", file=sys.stderr)
    print(f"examples/eval and checkpoints/{latest.name}: {len(a & b)} files compared, "
          f"{len(problems)} difference(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
