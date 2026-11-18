"""outputs/ has the files, columns and values that reports read."""

import json
from pathlib import Path

import pandas as pd
import pytest

from acme_eval import data, metrics

OUTPUTS = Path("outputs")
pytestmark = pytest.mark.skipif(
    not (OUTPUTS / "summary.json").exists(),
    reason="no outputs/ yet: run `uv run python scripts/evaluate.py` first",
)

COLUMNS = {
    "metrics": ["version", "month", "metric", "value", "low", "high"],
    "segments": ["version", "factor", "segment", "n", "subscribers", "base_rate",
                 "share_called", "recall_top10", "roc_auc"],
    "calibration": ["version", "bin", "n", "mean_predicted", "observed_rate"],
    "curves": ["version", "curve", "x", "y"],
}


@pytest.mark.parametrize("name", COLUMNS)
def test_columns(name):
    assert list(pd.read_csv(OUTPUTS / f"{name}.csv").columns) == COLUMNS[name]


def test_metrics_complete_and_in_range():
    table = pd.read_csv(OUTPUTS / "metrics.csv")
    assert set(table["metric"]) == set(metrics.METRICS)
    assert len(table) == 3 * len(metrics.METRICS)
    assert (table["low"] <= table["value"]).all()
    assert (table["value"] <= table["high"]).all()
    bounded = table[table["metric"] != "lift_top10"]
    assert bounded[["value", "low", "high"]].stack().between(0, 1).all()


def test_segments_cover_the_test_set():
    table = pd.read_csv(OUTPUTS / "segments.csv")
    summary = json.loads((OUTPUTS / "summary.json").read_text())
    totals = table.groupby(["version", "factor"])["n"].sum()
    assert (totals == summary["test_rows"]).all()
    ages = table[table["factor"] == "age_band"]["segment"]
    assert set(ages) == set(data.AGE_LABELS)


def test_summary_agrees_with_metrics():
    table = pd.read_csv(OUTPUTS / "metrics.csv")
    summary = json.loads((OUTPUTS / "summary.json").read_text())
    auc = table[table["metric"] == "roc_auc"].set_index("version")["value"]
    assert summary["best_version"] == auc.idxmax()
    assert summary["best_roc_auc"] == pytest.approx(auc.max())
    assert summary["data_sha256"] == data.EXPECTED_SHA256
    assert summary["split_seed"] == data.SPLIT_SEED
