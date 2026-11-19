"""Facts that change (../facts.yml): prices, plans, accounts and free allowances, each with its
source and the date it was checked.

Chapters quote a fact instead of typing it, so updating one is one edit to facts.yml and a
rebuild, and Appendix K (appendices/k-facts.qmd) lists them all with their dates:

    from scripts.facts import fact, checked
    `{python} fact("agents.claude_code_accounts")` (checked `{python} checked("agents.claude_code_accounts")`)

A key is "<section>.<item>". The landing page (ebook/_source.py) reads the same file.

Every English string has a Spanish twin beside it, its key ending in `_es` (`text_es`,
`label_es`, `title_es`, ...). In a document with `lang: es` (scripts/prose.py, `language()`) the
functions below return the Spanish strings under the English keys, so a cell reads the same in
both editions and the Spanish chapters' code stays identical to the English.
"""
from __future__ import annotations

import datetime as dt
from functools import cache
from pathlib import Path

import yaml

from scripts.prose import language

FILE = Path(__file__).resolve().parents[1] / "facts.yml"


@cache
def facts() -> dict:
    return yaml.safe_load(FILE.read_text())


# The keys whose values are English words, each of which must have its `_es` twin.
WORDS = ("title", "label", "text", "caption", "note", "for", "free")


def localised(d: dict, lang: str | None = None) -> dict:
    """A copy of one mapping in the edition's language: in Spanish, each `<key>_es` value
    replaces `<key>`; the `_es` keys are dropped in both editions. A word key without its
    twin stops the render in either edition, so the Spanish book never prints English."""
    missing = [k for k in WORDS if k in d and f"{k}_es" not in d]
    if missing:
        raise KeyError(f"facts.yml: {', '.join(missing)} without {', '.join(k + '_es' for k in missing)} "
                       f"in the entry that begins {str(d)[:80]}")
    out = {k: v for k, v in d.items() if not k.endswith("_es")}
    if (lang or language()) == "es":
        out.update({k[:-3]: v for k, v in d.items() if k.endswith("_es")})
    return out


def entry(key: str) -> dict:
    """One fact's entry: its text, url, checked date and any `also` sources."""
    section, item = key.split(".", 1)
    try:
        return localised(facts()[section]["items"][item])
    except KeyError:
        raise KeyError(f"facts.yml has no {key}") from None


def _date(value) -> str:
    return value.isoformat() if isinstance(value, dt.date) else str(value)


def fact(key: str, capital: bool = False) -> str:
    """The fact's text, as it reads in a sentence; `capital=True` where it starts one."""
    text = entry(key)["text"]
    return text[0].upper() + text[1:] if capital else text


def checked(key: str) -> str:
    """The date the fact was checked, YYYY-MM-DD."""
    return _date(entry(key)["checked"])


def table(section: str, name: str) -> dict:
    """A table of facts (such as models.prices), with its checked date as text."""
    t = localised(facts()[section][name])
    t["rows"] = [localised(r) for r in t["rows"]]
    t["checked"] = _date(t["checked"])
    return t


def all_items() -> list[tuple[str, str, dict]]:
    """Every sentence fact, as (section title, key, entry), in the file's order."""
    out = []
    for name, sec in facts().items():
        for item, raw in sec.get("items", {}).items():
            e = localised(raw)
            out.append((localised(sec)["title"], f"{name}.{item}", {**e, "checked": _date(e["checked"])}))
    return out
