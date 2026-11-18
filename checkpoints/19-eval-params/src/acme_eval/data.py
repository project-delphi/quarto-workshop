"""Load the UCI Bank Marketing table and split it for evaluation.

Run everything from the project root: paths here are relative to it.
"""

import hashlib
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

DATA_PATH = Path("data/bank-full.csv")
EXPECTED_SHA256 = "d1513ec63b385506f7cfce9f2c5caa9fe99e7ba4e8c3fa264b3aaf0f849ed32d"
EXPECTED_ROWS = 45_211

TARGET = "y"
# Known only after the call ends, so it leaks the outcome (see data/README.md).
LEAKY = "duration"

NUMERIC = ["age", "balance", "day", "campaign", "pdays", "previous"]
CATEGORICAL = [
    "job", "marital", "education", "default", "housing",
    "loan", "contact", "month", "poutcome",
]
# Every column a model may use: all 16 inputs except `duration`.
FEATURES = NUMERIC + CATEGORICAL
COLUMNS = [
    "age", "job", "marital", "education", "default", "balance", "housing", "loan",
    "contact", "day", "month", "duration", "campaign", "pdays", "previous",
    "poutcome", "y",
]

# One stratified split for every release.
TEST_SIZE = 0.25
SPLIT_SEED = 2026

# Factors for the slice tables: age bands [lower, upper) in years, and `job` as given.
AGE_EDGES = [18, 30, 40, 50, 60, 200]
AGE_LABELS = ["18-29", "30-39", "40-49", "50-59", "60+"]


def sha256(path: Path = DATA_PATH) -> str:
    """Return the SHA-256 checksum of a file, as hex."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_checksum(path: Path = DATA_PATH) -> None:
    """Stop if the data file is not the one the analysis was written for."""
    found = sha256(path)
    if found != EXPECTED_SHA256:
        raise ValueError(f"{path} has SHA-256 {found}, expected {EXPECTED_SHA256}")


def load(path: Path = DATA_PATH) -> pd.DataFrame:
    """Read the table, check its columns and types, and return the model inputs.

    The result holds the columns in `FEATURES` plus `y` as 0/1 (1 = subscribed).
    `duration` is dropped here, so no model can see it.
    """
    raw = pd.read_csv(path, sep=";")
    if list(raw.columns) != COLUMNS:
        raise ValueError(f"unexpected columns: {list(raw.columns)}")
    for column in NUMERIC + [LEAKY]:
        if not pd.api.types.is_integer_dtype(raw[column]):
            raise TypeError(f"{column} should be integer, found {raw[column].dtype}")
    for column in CATEGORICAL + [TARGET]:
        if not pd.api.types.is_string_dtype(raw[column]):
            raise TypeError(f"{column} should be text, found {raw[column].dtype}")
    if set(raw[TARGET]) != {"yes", "no"}:
        raise ValueError(f"{TARGET} should be 'yes' or 'no'")

    frame = raw[FEATURES].copy()
    frame[TARGET] = (raw[TARGET] == "yes").astype(int)
    return frame


def split(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split into training and test rows, keeping the subscription rate in both."""
    train, test = train_test_split(
        frame, test_size=TEST_SIZE, stratify=frame[TARGET], random_state=SPLIT_SEED
    )
    return train, test


def age_band(age: pd.Series) -> pd.Series:
    """Label each age with its band from `AGE_EDGES`."""
    return pd.cut(age, bins=AGE_EDGES, labels=AGE_LABELS, right=False).astype(str)
