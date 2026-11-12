"""The water analysis, run once per chapter, for Part III's computed numbers and figures.

Imports the finished project's script (examples/water/scripts/analysis.py), exactly as the
workshop deck does, and runs it in memory: nothing is written to examples/water/outputs/.
Every number Part III quotes about the water data comes from here or from analysis.load().
Run from book/ (execute-dir: project).
"""
from __future__ import annotations

import sys
from functools import cache
from pathlib import Path

SCRIPTS = Path("../examples/water/scripts").resolve()
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import analysis  # noqa: E402

A = analysis


@cache
def res() -> dict:
    """The full in-memory run (about 5 seconds): summary, prepared, clusters, profiles, k table."""
    return analysis.run()


@cache
def raw():
    """The analysis table as published: one row per municipality, zone and year."""
    return analysis.load()


def fmt(x) -> str:
    return f"{x:,}"


def names() -> dict[int, str]:
    return res()["profiles"]["name"].to_dict()


def colors() -> dict[int, str]:
    return res()["profiles"]["color"].to_dict()
