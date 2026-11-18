"""Metrics for a ranked contact list, with bootstrap intervals.

`y` holds the outcomes (1 = subscribed) and `scores` the predicted probabilities,
one per test contact. The call centre calls the top `TOP_SHARE` of the ranked list.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)

TOP_SHARE = 0.10  # the share of the list that is called
N_BOOTSTRAP = 1_000
BOOTSTRAP_SEED = 2026
CONFIDENCE = 0.95
CALIBRATION_BINS = 10  # equal-count bins of predicted probability
CURVE_POINTS = 200  # points kept per ROC or precision-recall curve

METRICS = [
    "roc_auc", "average_precision", "brier",
    "recall_top10", "precision_top10", "lift_top10",
]


def calls_made(n_contacts: int, share: float = TOP_SHARE) -> int:
    """How many contacts are called: the top `share` of the list, rounded up."""
    return int(np.ceil(share * n_contacts))


def called(scores: np.ndarray, share: float = TOP_SHARE) -> np.ndarray:
    """Mark the contacts in the top `share` of the ranking (ties keep list order)."""
    order = np.argsort(-scores, kind="stable")
    mask = np.zeros(len(scores), dtype=bool)
    mask[order[:calls_made(len(scores), share)]] = True
    return mask


def point_metrics(y: np.ndarray, scores: np.ndarray) -> dict[str, float]:
    """Every metric in `METRICS` for one set of outcomes and scores."""
    top = called(scores)
    precision = y[top].mean()
    return {
        "roc_auc": roc_auc_score(y, scores),
        "average_precision": average_precision_score(y, scores),
        "brier": brier_score_loss(y, scores),
        "recall_top10": y[top].sum() / y.sum(),
        "precision_top10": precision,
        "lift_top10": precision / y.mean(),
    }


def bootstrap_indices(n: int, n_bootstrap: int = N_BOOTSTRAP,
                      seed: int = BOOTSTRAP_SEED) -> np.ndarray:
    """Resampled row numbers, one row per resample.

    The same seed gives the same resamples, so every version is scored on the
    same resampled test sets and their intervals can be compared pairwise.
    """
    rng = np.random.default_rng(seed)
    return rng.integers(0, n, size=(n_bootstrap, n))


def with_intervals(y: np.ndarray, scores: np.ndarray,
                   resamples: np.ndarray) -> pd.DataFrame:
    """Point value and percentile interval of each metric.

    Returns one row per metric with columns `value`, `low` and `high`.
    """
    draws = pd.DataFrame([point_metrics(y[rows], scores[rows]) for rows in resamples])
    tail = (1 - CONFIDENCE) / 2
    return pd.DataFrame({
        "value": pd.Series(point_metrics(y, scores)),
        "low": draws.quantile(tail),
        "high": draws.quantile(1 - tail),
    }).loc[METRICS]


def calibration(y: np.ndarray, scores: np.ndarray,
                bins: int = CALIBRATION_BINS) -> pd.DataFrame:
    """Mean predicted probability and observed rate in equal-count bins."""
    frame = pd.DataFrame({"y": y, "score": scores})
    rank = frame["score"].rank(method="first")
    frame["bin"] = pd.qcut(rank, q=bins, labels=False) + 1
    return (frame.groupby("bin")
            .agg(n=("y", "size"), mean_predicted=("score", "mean"),
                 observed_rate=("y", "mean"))
            .reset_index())


def curves(y: np.ndarray, scores: np.ndarray,
           points: int = CURVE_POINTS) -> pd.DataFrame:
    """ROC and precision-recall points, thinned to about `points` each.

    For `roc`, x is the false-positive rate and y the true-positive rate;
    for `pr`, x is recall and y is precision.
    """
    fpr, tpr, _ = roc_curve(y, scores)
    precision, recall, _ = precision_recall_curve(y, scores)
    parts = []
    for name, x, y_axis in [("roc", fpr, tpr), ("pr", recall, precision)]:
        keep = np.unique(np.linspace(0, len(x) - 1, points).round().astype(int))
        parts.append(pd.DataFrame({"curve": name, "x": x[keep], "y": y_axis[keep]}))
    return pd.concat(parts, ignore_index=True)


def by_segment(y: np.ndarray, scores: np.ndarray, groups: pd.Series) -> pd.DataFrame:
    """Metrics within each group, for one factor such as age band.

    `share_called` and `recall_top10` use the whole list's top 10%: of a group's
    contacts, how many are called, and of its subscribers, how many are reached.
    ROC AUC is within the group (empty when a group has only one outcome).
    """
    frame = pd.DataFrame({"y": y, "score": scores, "called": called(scores),
                          "group": groups.to_numpy()})
    rows = []
    for group, part in frame.groupby("group", sort=True):
        both_outcomes = part["y"].nunique() == 2
        rows.append({
            "segment": group,
            "n": len(part),
            "subscribers": int(part["y"].sum()),
            "base_rate": part["y"].mean(),
            "share_called": part["called"].mean(),
            "recall_top10": part.loc[part["y"] == 1, "called"].mean(),
            "roc_auc": roc_auc_score(part["y"], part["score"]) if both_outcomes else np.nan,
        })
    return pd.DataFrame(rows)
