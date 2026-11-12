"""The book's plot style: dark ink on a transparent background (book/PLAN.md §5.4–5.5).

Figures carry the `.on-light` class in the chapters, which gives them a light panel in the
EPUB's night themes and in the HTML edition's dark mode, so the ink stays readable. The
cluster and IRCA band colours come from examples/water/scripts/analysis.py.

    from scripts.figures import style, INK, MUTED, ACCENT
    with style():
        fig, ax = plt.subplots(figsize=(7, 3))
"""
from __future__ import annotations

import os
from contextlib import contextmanager

import matplotlib.pyplot as plt

# Reproducible SVGs, so a re-executed chapter leaves its frozen figures unchanged: a fixed
# date in the SVG metadata (the book's date, 2026-11-12) and fixed element ids. Set at import,
# because figures are saved after the cell ends, outside style().
os.environ.setdefault("SOURCE_DATE_EPOCH", "1794441600")
plt.rcParams["svg.hashsalt"] = "one-source-every-format"

INK = "#24313f"
MUTED = "#5b6b7b"
ACCENT = "#2f72b0"
GRID = "#d5dbe1"

RC = {
    "figure.facecolor": "none", "axes.facecolor": "none", "savefig.facecolor": "none",
    "savefig.transparent": True, "savefig.bbox": "tight",
    "font.family": ["Avenir Next", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 11, "axes.titlesize": 11, "axes.labelsize": 11,
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": MUTED,
    "xtick.color": INK, "ytick.color": INK, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": False, "grid.color": GRID, "legend.frameon": False,
    "lines.linewidth": 2.2,
}


@contextmanager
def style():
    with plt.rc_context(RC):
        yield
