"""Helpers the chapters share for writing prose from computed values (book/README.md,
"Conventions"). A chapter imports what it needs:

    from scripts.prose import alt_text_holds, number_words, spans, text_holds
    WORD = number_words()            # WORD[9] -> "nine", WORD[0] -> "zero"
    NUM = number_words(zero="no")    # NUM[0] -> "no", as in "no rows were dropped"

The guards stop a render when a sentence, alt text or caption typed in the source no longer
matches the data, so that it is rewritten rather than published wrong.

The words follow the document's `lang`: the Spanish edition (book-es/) gets "nueve" and
"2014–2017, 2019 y 2020" from the same calls (`language()`).
"""
from __future__ import annotations

import json
import os
from collections.abc import Iterable
from functools import cache

_WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen "
          "fourteen fifteen sixteen seventeen eighteen nineteen twenty").split()
_WORDS_ES = ("cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece "
             "catorce quince dieciséis diecisiete dieciocho diecinueve veinte").split()
_AND = {"en": " and ", "es": " y "}


def language() -> str:
    """"es" when the document being rendered has `lang: es...`, else "en". Read from the
    execute info Quarto passes to the kernel, as scripts/figures.py reads the format; each
    document has its own execute-info file, so the answer is cached per file."""
    return _language(os.environ.get("QUARTO_EXECUTE_INFO", ""))


@cache
def _language(info: str) -> str:
    try:
        with open(info) as f:
            lang = json.load(f)["format"]["metadata"].get("lang") or ""
    except (KeyError, OSError, ValueError):
        return "en"
    return "es" if str(lang).startswith("es") else "en"


class NumberWords:
    """Words for 1 to 20, the chosen word for 0, and digits with separators beyond."""

    def __init__(self, zero: str = "zero") -> None:
        spanish = language() == "es"
        # The default zero is the edition's own word; a chosen one ("no") is kept as given.
        self.zero = "cero" if spanish and zero == "zero" else zero
        self.words = _WORDS_ES if spanish else _WORDS

    def __getitem__(self, n) -> str:
        n = int(n)
        if n == 0:
            return self.zero
        return self.words[n] if 0 < n < len(self.words) else f"{n:,}"

    def get(self, n, default=None) -> str:
        return self[n]

    def __len__(self) -> int:
        return len(_WORDS)


def number_words(zero: str = "zero") -> NumberWords:
    return NumberWords(zero)


def spans(years: Iterable) -> str:
    """[2014, 2015, 2016, 2017, 2019, 2020, 2022] -> "2014–2017, 2019, 2020 and 2022"."""
    ys, out = sorted(int(y) for y in years), []
    start = ys[0]
    for a, b in zip(ys, ys[1:] + [None]):
        if b != a + 1:
            out += [f"{start}–{a}"] if a - start > 1 else [str(y) for y in range(start, a + 1)]
            start = b
    return out[0] if len(out) == 1 else ", ".join(out[:-1]) + _AND[language()] + out[-1]


def text_holds(ok: bool, what: str) -> None:
    """Stop the render when a typed sentence about `what` no longer matches the data."""
    if not ok:
        raise ValueError(f"the text about {what} no longer matches the data: rewrite it")


def alt_text_holds(ok: bool, figure: str) -> None:
    """Alt texts and captions are static cell options, so they cannot quote computed values:
    stop the render when the data no longer match what one says."""
    if not ok:
        raise ValueError(f"the alt text or caption of {figure} no longer matches the data: "
                         "rewrite it")
