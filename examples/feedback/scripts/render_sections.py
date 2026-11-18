"""Render feedback.qmd once per section into reports/feedback-<section>.pdf, and check each.

Run from the project root:  uv run python scripts/render_sections.py

For each section in data/gradebook.csv (SYNTHETIC) it runs

    quarto render feedback.qmd --to typst -P section:A --output feedback-A.pdf

which writes the PDF next to feedback.qmd (`--output` takes a file name, not a folder), moves
it into reports/, and checks that its text names the section ("Section A") and carries the
SYNTHETIC label. It prints a table and exits with status 1 if any check fails.
"""

import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd
from pypdf import PdfReader

REPORTS = Path("reports")


def main() -> int:
    sections = sorted(pd.read_csv("data/gradebook.csv", dtype={"section": str})["section"].unique())
    REPORTS.mkdir(exist_ok=True)
    rows, failures = [], 0
    for section in sections:
        name = f"feedback-{section}.pdf"
        command = ["quarto", "render", "feedback.qmd", "--to", "typst",
                   "-P", f"section:{section}", "--output", name]
        start = time.perf_counter()
        result = subprocess.run(command, capture_output=True, text=True)
        seconds = time.perf_counter() - start
        if result.returncode != 0:
            print(result.stderr[-3000:], file=sys.stderr)
            raise SystemExit(f"quarto render failed: {' '.join(command)}")
        target = REPORTS / name
        shutil.move(name, target)
        reader = PdfReader(target)
        text = re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in reader.pages))
        lacking = [w for w in (f"Section {section}", "SYNTHETIC") if w not in text]
        status = "ok" if not lacking else "lacks " + ", ".join(repr(w) for w in lacking)
        failures += status != "ok"
        rows.append((section, str(target), str(len(reader.pages)), f"{seconds:.0f} s", status))

    header = ("section", "file", "pages", "render", "check")
    widths = [max(len(r[i]) for r in [header, *rows]) for i in range(len(header))]
    for row in [header, tuple("-" * w for w in widths), *rows]:
        print("  ".join(cell.ljust(w) for cell, w in zip(row, widths)).rstrip())
    print(f"{len(rows)} sheets, {failures} problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
