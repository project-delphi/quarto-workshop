"""The parameter checks stop on values the documents cannot report, and words follow numbers."""

import re
from pathlib import Path

import pandas as pd
import pytest

from acme_eval import params

MONTHS = ["2026-01", "2026-02", "2026-03"]
SEGMENTS = pd.DataFrame({"factor": ["age_band", "age_band", "job"],
                         "segment": ["18-29", "60+", "retired"]})


def test_latest_month_is_the_last():
    assert params.month("latest", reversed(MONTHS)) == "2026-03"


def test_a_known_month_is_kept():
    assert params.month("2026-02", MONTHS) == "2026-02"


@pytest.mark.parametrize("bad", ["2026-13", "2026-2", "March", "2025-12"])
def test_bad_or_missing_months_stop(bad):
    with pytest.raises(params.ParameterError):
        params.month(bad, MONTHS)


def test_known_segments_are_kept():
    assert params.segment("job", "retired", SEGMENTS) == ("job", "retired")


@pytest.mark.parametrize("factor, segment", [("age", "60+"), ("job", "60+"), ("age_band", "70+")])
def test_unknown_segments_stop(factor, segment):
    with pytest.raises(params.ParameterError):
        params.segment(factor, segment, SEGMENTS)


@pytest.mark.parametrize("now, before, word", [(3, 2, "up"), (2, 3, "down"), (2, 2, "unchanged")])
def test_direction(now, before, word):
    assert params.direction(now, before) == word


@pytest.mark.parametrize("a, b, word", [(0.8, 0.7, "above"), (0.7, 0.8, "below"),
                                        (0.7, 0.7, "level with")])
def test_relation(a, b, word):
    assert params.relation(a, b) == word


@pytest.mark.parametrize("document", ["update.qmd", "segment.qmd"])
def test_defaults_are_in_a_parameters_cell(document):
    text = Path(document).read_text()
    cell = re.search(r"```\{python\}\n#\| tags: \[parameters\]\n(.*?)```", text, re.S)
    assert cell, f"{document} has no cell tagged parameters"
    assert "=" in cell.group(1)
