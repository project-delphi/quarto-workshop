"""Build the model versions listed in `releases.yml`."""

from dataclasses import dataclass
from pathlib import Path

import yaml
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from acme_eval.data import CATEGORICAL, FEATURES, NUMERIC

RELEASES_PATH = Path("releases.yml")
MODEL_SEED = 2026


@dataclass(frozen=True)
class Release:
    """One released model version."""

    version: str
    month: str
    model: str
    features: list[str]
    description: str


def load_releases(path: Path = RELEASES_PATH) -> list[Release]:
    """Read `releases.yml`; `features: all` means every column in `FEATURES`."""
    entries = yaml.safe_load(Path(path).read_text())["releases"]
    releases = []
    for entry in entries:
        features = FEATURES if entry["features"] == "all" else entry["features"]
        unknown = set(features) - set(FEATURES)
        if unknown:
            raise ValueError(f"{entry['version']} uses columns outside FEATURES: {unknown}")
        releases.append(Release(
            version=entry["version"],
            month=entry["month"],
            model=entry["model"],
            features=list(features),
            description=entry["description"],
        ))
    return releases


def logistic_regression(features: list[str]) -> Pipeline:
    """One-hot encode categories, scale numbers, then fit a logistic regression."""
    prepare = ColumnTransformer([
        ("categories", OneHotEncoder(handle_unknown="ignore"),
         [f for f in features if f in CATEGORICAL]),
        ("numbers", StandardScaler(), [f for f in features if f in NUMERIC]),
    ])
    model = LogisticRegression(max_iter=1_000, random_state=MODEL_SEED)
    return Pipeline([("prepare", prepare), ("model", model)])


def gradient_boosting(features: list[str]) -> Pipeline:
    """Code categories as integers and let the trees treat them as categories."""
    categories = [f for f in features if f in CATEGORICAL]
    prepare = ColumnTransformer([
        ("categories", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
         categories),
        ("numbers", "passthrough", [f for f in features if f in NUMERIC]),
    ])
    model = HistGradientBoostingClassifier(
        categorical_features=list(range(len(categories))), random_state=MODEL_SEED
    )
    return Pipeline([("prepare", prepare), ("model", model)])


def build(release: Release) -> Pipeline:
    """Return an unfitted pipeline for one release."""
    builders = {"logistic_regression": logistic_regression,
                "gradient_boosting": gradient_boosting}
    return builders[release.model](release.features)
