"""The book's chapter list (_chapters.yml), as each edition sees it.

Chapters and part pages written after the Spanish edition was translated are listed under
`english_only` until they are translated (translation/PLAN.md, "Not yet translated"). The
English edition has every entry; the Spanish one leaves those out, and a part with none of
its own pages left is left out whole. Every script that reads the chapter list goes through
`load()`, so the two editions cannot disagree about which files exist.
"""
from __future__ import annotations

from pathlib import Path

import yaml

BOOK = Path(__file__).resolve().parents[1]


def load(edition: str = "en", path: Path | None = None) -> dict:
    """_chapters.yml for one edition ("en" or "es"), without its `english_only` key."""
    spec = yaml.safe_load((path or BOOK / "_chapters.yml").read_text())
    skip = set(spec.pop("english_only", None) or [])
    if edition == "en":
        return spec
    keep = lambda files: [f for f in files if f not in skip]
    out = {k: keep(v) if isinstance(v, list) and all(isinstance(f, str) for f in v) else v
           for k, v in spec.items() if k != "parts"}
    out["parts"] = [{**p, "chapters": keep(p["chapters"])} for p in spec["parts"]
                    if p["file"] not in skip]
    return out


def english_only(path: Path | None = None) -> set[str]:
    """The files only the English edition has."""
    return set(yaml.safe_load((path or BOOK / "_chapters.yml").read_text()).get("english_only") or [])
