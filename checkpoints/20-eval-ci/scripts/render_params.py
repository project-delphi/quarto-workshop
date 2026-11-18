"""Render the parameterised documents once per value, into reports/, and check each file.

Run from the project root, after `uv run python scripts/evaluate.py`:

    uv run python scripts/render_params.py                     # every month and age band
    uv run python scripts/render_params.py 2026-06 2026-10     # these two months only (and the bands)
    uv run python scripts/render_params.py --formats pdf       # PDFs only, faster

It renders `update.qmd` for every month in data/synthetic_business.csv (SYNTHETIC) and
`segment.qmd` for every age band in outputs/segments.csv, one Quarto run per value:

    quarto render update.qmd -P month:2026-10 -M output-file:update-2026-10 --to html,docx,typst

One run executes the document once and writes every format, each named by the parameter
(`-M output-file` without an extension; each format adds its own). Then it moves the files
into reports/ and checks that each exists and that its text contains the parameter value
(and, for the update, the SYNTHETIC label). It prints a table and exits with status 1 if
any check fails.

Where Quarto writes. This folder is a website project, but neither document is in
`project.render` in _quarto.yml, so Quarto renders each one as a single file: the outputs
appear next to the source, not in _site/, and the site's post-render step does not run.
`--output-dir` is refused for such a file ("can only be used when rendering projects"), and
`--output` takes a file name only, no folder, so this script moves the files itself. If a
document is ever added to `project.render`, Quarto writes into _site/ instead; the script
looks there too, so it keeps working, but the site would then also carry the last value.
"""

import argparse
import re
import shutil
import subprocess
import sys
import time
import zipfile
from html.parser import HTMLParser
from pathlib import Path

import pandas as pd
from pypdf import PdfReader

from acme_eval import data

REPORTS = Path("reports")
SITE = Path("_site")
FORMATS = {"html": "html", "docx": "docx", "pdf": "typst"}  # file extension: Quarto format


class Text(HTMLParser):
    """The visible text of an HTML page."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        self.skip += tag in ("script", "style")

    def handle_endtag(self, tag: str) -> None:
        self.skip -= tag in ("script", "style")

    def handle_data(self, text: str) -> None:
        if not self.skip:
            self.parts.append(text)


def text_of(path: Path) -> str:
    """The text of a rendered pdf, docx or html file, with runs of white space as one space."""
    if path.suffix == ".pdf":
        raw = " ".join(page.extract_text() or "" for page in PdfReader(path).pages)
        raw = raw.replace("­\n", "").replace("­", "")  # Typst's soft hyphens
    elif path.suffix == ".docx":
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml").decode("utf-8")
        raw = re.sub(r"<[^>]+>", "", re.sub(r"</w:p>", " ", xml))
    else:
        parser = Text()
        parser.feed(path.read_text(encoding="utf-8"))
        raw = " ".join(parser.parts)
    return re.sub(r"\s+", " ", raw)


def render(source: str, stem: str, values: dict[str, str], formats: list[str]) -> list[Path]:
    """Render `source` once with `values` into reports/<stem>.<ext>; return the files."""
    command = ["quarto", "render", source, "-M", f"output-file:{stem}",
               "--to", ",".join(FORMATS[f] for f in formats)]
    for name, value in values.items():
        command += ["-P", f"{name}:{value}"]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-3000:], file=sys.stderr)
        raise SystemExit(f"quarto render failed: {' '.join(command)}")
    REPORTS.mkdir(exist_ok=True)
    moved = []
    for extension in formats:
        name = f"{stem}.{extension}"
        found = next((p for p in (Path(name), SITE / name) if p.exists()), None)
        target = REPORTS / name
        if found is not None:
            shutil.move(found, target)
        moved.append(target)
    shutil.rmtree(f"{stem}_files", ignore_errors=True)  # html support files, if not embedded
    return moved


def months(argv: list[str]) -> list[str]:
    """Every month in the synthetic business file, or those from FIRST to LAST."""
    present = pd.read_csv("data/synthetic_business.csv", dtype={"month": str})["month"].tolist()
    if not argv:
        return present
    first, last = argv[0], argv[-1]
    for month in (first, last):
        if month not in present:
            raise SystemExit(f"{month} is not in data/synthetic_business.csv "
                             f"({present[0]} to {present[-1]})")
    return [m for m in present if first <= m <= last]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("months", nargs="*", metavar="YYYY-MM",
                        help="first and last month to render (default: every month)")
    parser.add_argument("--formats", default="pdf,docx,html",
                        help="comma-separated: pdf, docx, html (default: all three)")
    args = parser.parse_args()
    formats = [f.strip() for f in args.formats.split(",")]
    unknown = set(formats) - set(FORMATS)
    if unknown:
        raise SystemExit(f"unknown format(s): {', '.join(sorted(unknown))}")

    jobs = [("update.qmd", f"update-{m}", {"month": m}, m, ["SYNTHETIC"])
            for m in months(args.months)]
    jobs += [("segment.qmd", f"segment-age-{band.replace('+', 'plus')}",
              {"factor": "age_band", "segment": band}, band, ["fictional"])
             for band in data.AGE_LABELS]

    rows, failures = [], 0
    for source, stem, values, expected, labels in jobs:
        start = time.perf_counter()
        files = render(source, stem, values, formats)
        seconds = time.perf_counter() - start
        for path in files:
            if not path.exists():
                status = "MISSING"
            else:
                text = text_of(path)
                lacking = [w for w in [expected, *labels] if w not in text]
                status = "ok" if not lacking else "lacks " + ", ".join(repr(w) for w in lacking)
            failures += status != "ok"
            rows.append((source, ", ".join(f"{k}={v}" for k, v in values.items()), str(path),
                         f"{path.stat().st_size / 1024:,.0f} KB" if path.exists() else "-",
                         f"{seconds:.0f} s", status))
        print(f"rendered {stem} in {seconds:.0f} s", file=sys.stderr)

    header = ("document", "parameters", "file", "size", "render", "check")
    widths = [max(len(str(r[i])) for r in [header, *rows]) for i in range(len(header))]
    for row in [header, tuple("-" * w for w in widths), *rows]:
        print("  ".join(str(cell).ljust(w) for cell, w in zip(row, widths)).rstrip())
    print(f"{len(rows)} files, {failures} problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
