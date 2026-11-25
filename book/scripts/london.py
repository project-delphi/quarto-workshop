"""Part II's London guide, read from examples/london/data/ for the pages that quote it:

    from scripts import london
    P = london.planted_visits()
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[2] / "examples" / "london" / "data"

# The Tower of London's visits in Part II's change task (Chapter 9's Try it, Exercise II.5): the
# chapters that say it makes the Tower the most visited of the ten check against this one value.
TOWER_NEW = 8_000_000


def planted_visits() -> dict:
    """The planted value of Part II's exercises (chapters/exercises-london.qmd): the five
    sights' latest visits, sorted, with the third sight's count replaced by its own count a
    year earlier. The exercises print `shown` and Appendix E answers it, both by calling this,
    so the puzzle and its answer cannot drift. Returns the year, the real and shown series,
    the planted sight, and its printed and true counts."""
    from scripts.prose import text_holds

    visits = pd.read_csv(DATA / "visits.csv")
    year = int(visits["year"].max())
    real = (visits[visits["year"] == year].set_index("attraction")["visits"]
            .sort_values(ascending=False))
    before = visits[visits["year"] == year - 1].set_index("attraction")["visits"]
    sight = real.index[2]
    shown = real.copy()
    shown[sight] = before[sight]
    text_holds(shown[sight] != real[sight], "the planted value differing from the real one")
    text_holds(list(shown.sort_values(ascending=False).index) == list(real.index),
               "the planted table keeping the real order")
    return {"year": year, "real": real, "shown": shown, "sight": sight,
            "printed": int(shown[sight]), "true": int(real[sight])}
