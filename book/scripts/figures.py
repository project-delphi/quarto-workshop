"""The book's plot style: dark ink on a transparent background (book/PLAN.md §5.4–5.5).

Figures carry the `.on-light` class in the chapters, which gives them a light panel in the
EPUB's night themes and in the HTML edition's dark mode, so the ink stays readable. The
cluster and IRCA band colours come from examples/water/scripts/analysis.py.

    from scripts.figures import style, figsize, grid, INK, MUTED, ACCENT
    with style():
        fig, ax = plt.subplots(figsize=figsize(7, 3))

Sizes for the EPUB. A figure is scaled to the reader's column, so on a phone (about 340 CSS
px) a 7-inch chart's 11 pt labels shrink to 6 or 7 px. In the EPUB, figsize() narrows a chart
to EPUB_WIDTH inches at the same height, which keeps its labels near 11 px, and grid() stacks
panels that sit side by side in the HTML edition. Execution runs once per format, so each
edition gets its own figures.

    rows, cols = grid(3)                       # (1, 3) in HTML, (3, 1) in the EPUB
    fig, axes = plt.subplots(rows, cols, figsize=figsize(7.2, 3.0, rows=rows))
    for ax in axes.flat: ...
"""
from __future__ import annotations

import json
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


EPUB_WIDTH = 4.6  # inches: with 11 pt text, labels of about 11 CSS px on a 390 px phone


def target() -> str:
    """The format being rendered ("html", "epub", ...), from the execute info Quarto passes
    to the kernel; "" outside a render. Read on every call, as a kernel may be reused."""
    try:
        with open(os.environ["QUARTO_EXECUTE_INFO"]) as f:
            return json.load(f)["format"]["identifier"]["base-format"]
    except (KeyError, OSError, ValueError):
        return ""


def is_epub() -> bool:
    return target() == "epub"


def grid(n: int) -> tuple[int, int]:
    """Rows and columns for n panels: one row in HTML; in the EPUB a column, or 2 x 2 for four."""
    if not is_epub() or n == 1:
        return 1, n
    return (2, 2) if n == 4 else (n, 1)


def figsize(w: float, h: float, rows: int = 1, epub: tuple[float, float] | None = None
            ) -> tuple[float, float]:
    """(w, h) in the HTML edition. In the EPUB: `epub` if given, else EPUB_WIDTH wide (or w if
    narrower) and h tall for each row of panels."""
    if not is_epub():
        return w, h
    if epub:
        return epub
    return min(w, EPUB_WIDTH), h * rows


@contextmanager
def style():
    with plt.rc_context(RC):
        yield
