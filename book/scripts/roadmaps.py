"""Write media/roadmaps/part-N.svg: the "Where we are" figure on each part page.

The deck's coloured progress bar becomes, for each part of the book, a static roadmap: a strip
of the three parts with this one highlighted, then this part's chapters in order, each with
what the reader reads about or builds there and the checkpoint it ends at. Titles come from the chapter files
listed in _chapters.yml, so the roadmaps follow the book. Run from book/ (media/build.py
roadmaps), then rasterise with the diagrams step.
"""
from __future__ import annotations

import html
import re
import textwrap
from pathlib import Path

import yaml

BOOK = Path(__file__).resolve().parents[1]
OUT = BOOK / "media" / "roadmaps"
COLORS = ["#2f72b0", "#b07a14", "#7c5cdb", "#2f9e77", "#c2416b", "#3d7fd9", "#8a7f1e", "#c8662a"]
# What the reader comes away with from each chapter (what they read about, or what they
# build), and the checkpoint its hands-on work ends at; "" where a chapter has none.
META = {
    "01-quarto": ("Read: why one source beats copies", ""),
    "02-assistant": ("Read: how to ask for work and check it", ""),
    "03-setup": ("Build: a computer that renders the test run", ""),
    "04-markdown": ("Build: london.md, its rules and environment", "ends at checkpoint 01"),
    "05-compute": ("Build: london.qmd as HTML, Word and PDF", "ends at checkpoint 02"),
    "06-audiences": ("Build: a dashboard, a Word brief, a flyer", "ends at checkpoint 04"),
    "07-publish": ("Build: a published website, a rebuild explained", "ends at examples/london"),
    "exercises-london": ("Practise: five exercises, then your own prompts", ""),
    "08-water-question": ("Build: the project folder, its data and rules", ""),
    "09-explore": ("Build: explore.qmd, a first look at the data", "ends at checkpoint 05"),
    "10-prepare": ("Build: prepare(), nine comparable features", "ends at checkpoint 06"),
    "11-cluster": ("Build: k-means and the clusters page", "ends at checkpoint 07"),
    "12-interpret": ("Build: named clusters and their outcomes", "ends at checkpoint 08"),
    "13-causation": ("Build: the within-cluster check", "ends at checkpoint 09"),
    "14-publish-many": ("Build: report, slides, website and blog", "ends at checkpoints 10–13"),
    "exercises-water": ("Practise: exercises, then your own prompts", ""),
}


def title_of(qmd: Path) -> str:
    line = next(l for l in qmd.read_text().splitlines() if l.startswith("# "))
    return re.sub(r"\s*\{.*\}\s*$", "", line[2:]).strip()


def svg(part_index: int, parts: list[dict], first_number: int) -> str:
    part = parts[part_index]
    rows, y, number = [], 150, first_number
    W = 700
    # Part strip
    strip = []
    pw = (W - 40 - 2 * 12) / len(parts)
    for i, p in enumerate(parts):
        x = 20 + i * (pw + 12)
        on = i == part_index
        label = title_of(BOOK / p["file"]).split(":")[0]
        strip.append(f'<rect x="{x:.0f}" y="20" width="{pw:.0f}" height="48" rx="24" '
                     f'fill="{"#24313f" if on else "none"}" stroke="#5b6b7b" stroke-width="2"/>'
                     f'<text x="{x + pw / 2:.0f}" y="51" text-anchor="middle" '
                     f'class="{"s on" if on else "s"}">{label}</text>')
    name = title_of(BOOK / part["file"]).split(":", 1)[1].strip()
    head = f'<text x="20" y="112" class="h">{html.escape(name)}</text>'
    for k, ch in enumerate(part["chapters"]):
        stem = Path(ch).stem
        title = title_of(BOOK / ch)
        gain, cp = META.get(stem, ("", ""))
        numbered = not stem.startswith("exercises")
        color = COLORS[k % len(COLORS)]
        lines = textwrap.wrap(title, 36)
        extra = [(line, "g") for line in textwrap.wrap(gain, 50)] + ([(cp, "n")] if cp else [])
        h = 34 * len(lines) + 30 * len(extra) + 26
        label = str(number) if numbered else "✓"
        rows.append(f'<circle cx="52" cy="{y + 22}" r="24" fill="{color}"/>'
                    f'<text x="52" y="{y + 30}" text-anchor="middle" class="num">{label}</text>')
        for j, line in enumerate(lines):
            rows.append(f'<text x="96" y="{y + 30 + 34 * j}" class="t">{html.escape(line)}</text>')
        for j, (line, cls) in enumerate(extra):
            rows.append(f'<text x="96" y="{y + 30 + 34 * (len(lines) - 1) + 30 * (j + 1)}" '
                        f'class="{cls}">{html.escape(line)}</text>')
        if k < len(part["chapters"]) - 1:
            rows.append(f'<line x1="52" y1="{y + 46}" x2="52" y2="{y + h - 2}" stroke="#c3ccd5" stroke-width="4"/>')
        y += h
        number += numbered
    height = y + 10
    alt = (f"Where we are: {html.escape(title_of(BOOK / part['file']))}, highlighted among the book's "
           f"{len(parts)} parts. Its chapters in order: "
           + "; ".join(html.escape(title_of(BOOK / c)) for c in part["chapters"]) + ".")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" role="img" aria-labelledby="t d">
<title id="t">Where we are</title>
<desc id="d">{alt}</desc>
<style>
  text {{ font-family: "Avenir Next", "Helvetica Neue", Helvetica, Arial, sans-serif; fill: #24313f; }}
  .h {{ font-size: 28px; font-weight: 700; }}
  .t {{ font-size: 24px; font-weight: 600; }}
  .s {{ font-size: 20px; }}
  .g {{ font-size: 20px; fill: #3d4b59; }}
  .n {{ font-size: 19px; fill: #5b6b7b; }}
  .num {{ font-size: 22px; font-weight: 700; fill: #ffffff; }}
  .on {{ fill: #ffffff; font-weight: 700; }}
</style>
{"".join(strip)}
{head}
{"".join(rows)}
</svg>
'''


def main() -> None:
    spec = yaml.safe_load((BOOK / "_chapters.yml").read_text())
    parts = spec["parts"]
    OUT.mkdir(parents=True, exist_ok=True)
    number = 1
    for i, part in enumerate(parts):
        (OUT / f"part-{i + 1}.svg").write_text(svg(i, parts, number))
        number += sum(not Path(c).stem.startswith("exercises") for c in part["chapters"])
        print("roadmap", f"media/roadmaps/part-{i + 1}.svg")


if __name__ == "__main__":
    main()
