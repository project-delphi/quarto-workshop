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
from functools import cache

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


def grid(n: int, square: bool = False) -> tuple[int, int]:
    """Rows and columns for n panels: one row in HTML; in the EPUB a column, or 2 x 2 for four.

    square=True lays three panels out 2 x 2 in the EPUB too (the fourth cell is left for a
    legend or a note, which the cell draws or hides), so the chart is not taller than a page
    (PLAN-improvement.md §3.2). A cell that asks for it must unpack four axes and describe the
    layout in its caption and alt text; cells that do not are unchanged."""
    if not is_epub() or n == 1:
        return 1, n
    if n == 4 or (square and n == 3):
        return 2, 2
    return n, 1


def figsize(w: float, h: float, rows: int = 1, epub: tuple[float, float] | None = None
            ) -> tuple[float, float]:
    """(w, h) in the HTML edition. In the EPUB: `epub` if given, else EPUB_WIDTH wide (or w if
    narrower) and h tall for each row of panels."""
    if not is_epub():
        return w, h
    if epub:
        return epub
    return min(w, EPUB_WIDTH), h * rows


# The Spanish edition (book-es/, translation/glossary.md): the charts' own words, which the
# cells take from data keys ("urban", "High") as well as from literals, are translated where
# the chart is shown, so every cell's code stays the English edition's. Exact texts first, then
# patterns for texts that carry a number.
TERMS_ES = {
    "urban": "urbana", "rural": "rural", "both": "ambas",
    "No IRCA": "Sin IRCA", "No risk": "Sin riesgo", "Low": "Bajo", "Medium": "Medio",
    "High": "Alto", "Unfit": "Inviable sanitariamente",
    "Share of rows (%)": "Proporción de filas (%)", "Median IRCA": "Mediana del IRCA",
    "IRCA, utility-supplied": "IRCA de prestadores",
    "Aqueduct coverage (%)": "Cobertura de acueducto (%)", "new method": "método nuevo",
    "Infant mortality (per 1,000 live births)": "Mortalidad infantil (por 1,000 nacidos vivos)",
    "raw units": "unidades originales", "z-scores": "puntajes z",
    "Share of squared distance (%)": "Proporción de la distancia al cuadrado (%)",
    "random start": "inicio al azar", "first assignment": "primera asignación",
    "halfway": "a mitad de camino", "stable": "estable",
    "Inertia (thousands)": "Inercia (miles)", "Silhouette": "Silueta",
    "cluster": "clúster",
    "Utility-supplied IRCA (0–100)": "IRCA de prestadores (0–100)",
    "Infant mortality\nper 1,000": "Mortalidad infantil\npor 1,000",
}
PATTERNS_ES: list[tuple[str, str]] = [
    (r"^Cluster (\d+)$", r"Clúster \1"),
    (r"^PC(\d) \((\d+%) of variance\)$", r"PC\1 (\2 de la varianza)"),
]


# English function words: chart text containing one and left untranslated is reported.
import re as _re
ENGLISH = _re.compile(r"\b(the|of|and|per|in|by|with|from|to|share|visits|rows)\b", _re.I)


@cache
def _proper_names() -> frozenset[str]:
    """Names that stay English in any edition: the London attractions, as the charts write them."""
    import csv
    try:
        with open("../examples/london/data/attractions.csv", newline="") as f:
            names = {r["attraction"] for r in csv.DictReader(f)}
    except OSError:
        return frozenset()
    return frozenset(names | {n.replace(" (South Kensington)", "") for n in names})


def _translate(text: str) -> str:
    import re
    if text in TERMS_ES:
        return TERMS_ES[text]
    for pattern, repl in PATTERNS_ES:
        if re.match(pattern, text):
            return re.sub(pattern, repl, text)
    return text


def translate_figures() -> None:
    """Put the open figures' texts and tick labels in Spanish (only called for lang: es)."""
    from matplotlib.category import StrCategoryFormatter
    from matplotlib.text import Text
    from matplotlib.ticker import FixedFormatter, FuncFormatter

    import warnings
    for num in plt.get_fignums():
        fig = plt.figure(num)
        for text in fig.findobj(Text):
            new = _translate(text.get_text())
            if new != text.get_text():
                text.set_text(new)
            elif ENGLISH.search(new) and new not in _proper_names():
                # Shown as a render warning, so a label added to an English chapter without its
                # Spanish twin in TERMS_ES is noticed rather than published in English.
                warnings.warn(f"chart text with no Spanish in TERMS_ES: {new!r}")
        for ax in fig.axes:
            for axis in (ax.xaxis, ax.yaxis):
                fmt = axis.get_major_formatter()
                # Only formatters that can give words (set_ticks with labels makes a FuncFormatter);
                # numeric ones such as ScalarFormatter need their own set_locs, so stay as they are.
                if (isinstance(fmt, (StrCategoryFormatter, FixedFormatter, FuncFormatter))
                        and not getattr(fmt, "translated", False)):
                    wrapped = FuncFormatter(lambda x, pos, f=fmt: _translate(f(x, pos)))
                    wrapped.translated = True
                    axis.set_major_formatter(wrapped)


@contextmanager
def style():
    from matplotlib.figure import Figure

    from scripts.prose import language

    spanish = language() == "es"
    show, savefig = plt.show, Figure.savefig
    if spanish:
        def translated_show(*args, **kwargs):
            translate_figures()
            return show(*args, **kwargs)

        def translated_savefig(self, *args, **kwargs):
            translate_figures()
            return savefig(self, *args, **kwargs)
        plt.show, Figure.savefig = translated_show, translated_savefig
    try:
        with plt.rc_context(RC):
            yield
    finally:
        if spanish:
            translate_figures()
            plt.show, Figure.savefig = show, savefig
