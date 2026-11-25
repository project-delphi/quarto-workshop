"""The evaluation project's results, for the chapters that quote them (Parts I and III).

The project is examples/eval/, the finished version of what the fast path (Chapter 3) and
Part III build: Acme Signals, a fictional company, evaluating releases of a model on the real
UCI Bank Marketing data. Its own script, run in its own environment (its uv.lock), computes
every result once into examples/eval/outputs/, exactly as a reader runs it; the chapters read
those files, so the book quotes what the project computes and never types a result.

    from scripts import evaluation as ev
    S = ev.summary()          # outputs/summary.json
    M = ev.metrics()          # outputs/metrics.csv, one row per version and metric

The outputs are rebuilt when they are missing or older than any of the project's inputs.
"""
from __future__ import annotations

import json
import os
import subprocess
from functools import cache
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parents[2] / "examples" / "eval"
OUTPUTS = PROJECT / "outputs"
STARTER = PROJECT.parents[1] / "starters" / "eval-repo"
INPUTS = ["data", "src", "scripts", "releases.yml", "pyproject.toml", "uv.lock"]


def _newest_input() -> float:
    times = []
    for name in INPUTS:
        path = PROJECT / name
        files = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file()
                                                  and "__pycache__" not in p.parts]
        times += [p.stat().st_mtime for p in files]
    return max(times)


@cache
def run() -> Path:
    """Run the project's evaluate.py if its outputs are missing or stale; return outputs/."""
    summary = OUTPUTS / "summary.json"
    if not summary.exists() or summary.stat().st_mtime < _newest_input():
        env = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "JUPYTER_PATH")}
        subprocess.run(["uv", "run", "--frozen", "python", "scripts/evaluate.py"], cwd=PROJECT,
                       env=env, check=True, capture_output=True, text=True)
    return OUTPUTS


def summary() -> dict:
    return json.loads((run() / "summary.json").read_text())


def metrics() -> pd.DataFrame:
    return pd.read_csv(run() / "metrics.csv")


def segments() -> pd.DataFrame:
    return pd.read_csv(run() / "segments.csv")


def calibration() -> pd.DataFrame:
    return pd.read_csv(run() / "calibration.csv")


def value(version: str, metric: str) -> pd.Series:
    """One version's metric, with its interval: a Series with value, low and high."""
    m = metrics()
    return m[(m["version"] == version) & (m["metric"] == metric)].iloc[0]


def rival() -> str:
    """The release with the next-highest ROC AUC after the best one: the version whose number a
    planted error puts under the best release's name (Chapters 3, 11 and 15, and Appendix E's
    answers; PLAN-improvement-briefs-2.md, lead decision 1). Each plant guards that the two
    numbers differ as printed."""
    m = metrics()
    auc = m[m["metric"] == "roc_auc"].sort_values("value", ascending=False)
    best = summary()["best_version"]
    if auc["version"].iloc[0] != best:
        raise ValueError(f"metrics.csv ranks {auc['version'].iloc[0]} first by roc_auc, summary.json {best}")
    return str(auc["version"].iloc[1])


def fast_plant() -> dict:
    """The planted error that opens Chapter 3 (chapters/fast-path.qmd): the best release's name
    with the ROC AUC of rival(). Returns the sentence, the wrong and the right ROC AUC as
    printed, and whose the wrong one is. The chapter prints it and Appendix E answers it, both
    by calling this, so the two cannot drift."""
    from scripts.prose import text_holds

    best, other = summary()["best_version"], rival()
    wrong = f"{value(other, 'roc_auc')['value']:.3f}"
    right = f"{value(best, 'roc_auc')['value']:.3f}"
    text_holds(wrong != right, "the planted ROC AUC differs from the best release's as printed")
    from scripts.prose import language

    words = "es la mejor, con un ROC AUC de" if language() == "es" else "ranks best, with a ROC AUC of"
    return {"sentence": f"{best} {words} {wrong}.", "wrong": wrong, "right": right, "rival": other}


def team_plant() -> dict:
    """The planted recall of Chapter 15 (chapters/team.qmd): rival()'s recall in the top tenth,
    with its interval, under the best release's name. Returns the best and rival releases and,
    as printed to three decimals, the planted value, low and high, and the best release's own
    value. The chapter prints it and Appendix E answers it, both by calling this."""
    from scripts.prose import text_holds

    best, other = summary()["best_version"], rival()
    r, own = value(other, "recall_top10"), value(best, "recall_top10")
    planted, right = f"{r['value']:.3f}", f"{own['value']:.3f}"
    text_holds(planted != right, "Chapter 15's two recalls differing at three decimals")
    return {"best": best, "rival": other, "value": planted, "low": f"{r['low']:.3f}",
            "high": f"{r['high']:.3f}", "right": right}


def interval(version: str, metric: str, digits: int = 3) -> str:
    """'0.799 (0.785 to 0.813)': a value and its 95% interval, as the report writes it."""
    r = value(version, metric)
    return f"{r['value']:.{digits}f} ({r['low']:.{digits}f} to {r['high']:.{digits}f})"


def percent(share: float, digits: int = 1) -> str:
    return f"{100 * share:.{digits}f}%"


def files(folder: Path) -> list[str]:
    """A folder's tracked-looking files (no .venv, outputs or caches), relative, sorted."""
    skip = {".venv", "outputs", "__pycache__", ".pytest_cache", ".quarto"}
    return sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*")
                  if p.is_file() and not skip & set(p.relative_to(folder).parts))
