"""The data file is the one the analysis was written for, and loads as expected."""

import pandas as pd

from acme_eval import data


def test_checksum_matches():
    assert data.sha256() == data.EXPECTED_SHA256


def test_raw_shape():
    raw = pd.read_csv(data.DATA_PATH, sep=";")
    assert raw.shape == (data.EXPECTED_ROWS, 17)  # 16 inputs and the target `y`
    assert list(raw.columns) == data.COLUMNS


def test_load_drops_duration_and_codes_target():
    frame = data.load()
    assert data.LEAKY not in frame.columns
    assert list(frame.columns) == data.FEATURES + [data.TARGET]
    assert set(frame[data.TARGET]) == {0, 1}
    assert len(data.FEATURES) == 15


def test_split_is_stratified_and_repeatable():
    frame = data.load()
    train, test = data.split(frame)
    _, test_again = data.split(frame)
    assert len(train) + len(test) == len(frame)
    assert test.index.equals(test_again.index)
    assert abs(train[data.TARGET].mean() - test[data.TARGET].mean()) < 0.001


def test_every_age_has_a_band():
    bands = data.age_band(data.load()["age"])
    assert set(bands) == set(data.AGE_LABELS)
