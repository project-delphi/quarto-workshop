"""Metrics behave as defined on small, known examples, and repeat exactly."""

import numpy as np
import pytest

from acme_eval import metrics

# 20 contacts, 4 subscribers; the scores rank two subscribers first.
Y = np.array([1, 1, 0, 0, 1, 0, 0, 0, 0, 1] + [0] * 10)
SCORES = np.linspace(0.95, 0.05, 20)


def test_calls_made_rounds_up():
    assert metrics.calls_made(20) == 2
    assert metrics.calls_made(11_303) == 1_131


def test_top_ten_percent():
    result = metrics.point_metrics(Y, SCORES)
    assert result["recall_top10"] == pytest.approx(2 / 4)
    assert result["precision_top10"] == pytest.approx(1.0)
    assert result["lift_top10"] == pytest.approx(1.0 / (4 / 20))


def test_perfect_ranking():
    y = np.array([0] * 90 + [1] * 10)
    result = metrics.point_metrics(y, y * 0.9 + 0.05)
    assert result["roc_auc"] == 1.0
    assert result["recall_top10"] == 1.0


def test_metrics_in_range():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 500)
    scores = rng.random(500)
    for name, value in metrics.point_metrics(y, scores).items():
        if name != "lift_top10":
            assert 0 <= value <= 1, name


def test_intervals_repeat_and_contain_the_value():
    rng = np.random.default_rng(1)
    y = rng.integers(0, 2, 300)
    scores = np.clip(y * 0.3 + rng.random(300) * 0.7, 0, 1)
    first = metrics.with_intervals(y, scores, metrics.bootstrap_indices(300, 200))
    second = metrics.with_intervals(y, scores, metrics.bootstrap_indices(300, 200))
    assert first.equals(second)
    assert (first["low"] <= first["value"]).all()
    assert (first["value"] <= first["high"]).all()


def test_calibration_bins_have_equal_counts():
    table = metrics.calibration(Y, SCORES, bins=4)
    assert list(table["n"]) == [5, 5, 5, 5]
