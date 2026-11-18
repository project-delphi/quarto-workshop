"""Facts that change (../facts.yml): prices, plans, accounts and free allowances, each with its
source and the date it was checked.

Chapters quote a fact instead of typing it, so updating one is one edit to facts.yml and a
rebuild, and Appendix K (appendices/k-facts.qmd) lists them all with their dates:

    from scripts.facts import fact, checked
    `{python} fact("agents.claude_code_accounts")` (checked `{python} checked("agents.claude_code_accounts")`)

A key is "<section>.<item>". The landing page (ebook/_source.py) reads the same file.
"""
from __future__ import annotations

import datetime as dt
from functools import cache
from pathlib import Path

import yaml

FILE = Path(__file__).resolve().parents[1] / "facts.yml"


@cache
def facts() -> dict:
    return yaml.safe_load(FILE.read_text())


def entry(key: str) -> dict:
    """One fact's entry: its text, url, checked date and any `also` sources."""
    section, item = key.split(".", 1)
    try:
        return facts()[section]["items"][item]
    except KeyError:
        raise KeyError(f"facts.yml has no {key}") from None


def _date(value) -> str:
    return value.isoformat() if isinstance(value, dt.date) else str(value)


def fact(key: str) -> str:
    """The fact's text, as it reads in a sentence."""
    return entry(key)["text"]


def checked(key: str) -> str:
    """The date the fact was checked, YYYY-MM-DD."""
    return _date(entry(key)["checked"])


def table(section: str, name: str) -> dict:
    """A table of facts (such as models.prices), with its checked date as text."""
    t = dict(facts()[section][name])
    t["checked"] = _date(t["checked"])
    return t


def all_items() -> list[tuple[str, str, dict]]:
    """Every sentence fact, as (section title, key, entry), in the file's order."""
    return [(sec["title"], f"{name}.{item}", {**e, "checked": _date(e["checked"])})
            for name, sec in facts().items() for item, e in sec.get("items", {}).items()]
