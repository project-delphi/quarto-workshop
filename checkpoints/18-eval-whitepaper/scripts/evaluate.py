"""Evaluate every release in releases.yml once and write the results to outputs/.

Run from the project root:  uv run python scripts/evaluate.py

Everything that reports a result reads outputs/; nothing else fits a model.
The files are deterministic: running the script twice writes the same bytes.
"""

import json
import platform
import time
from importlib.metadata import version
from pathlib import Path

import pandas as pd

from acme_eval import data, metrics, models

OUTPUTS = Path("outputs")
DECIMALS = 6  # rounding for every number written, so reruns give identical files


def evaluate() -> None:
    """Fit each release on the training rows and score it on the test rows."""
    data.verify_checksum()
    frame = data.load()
    train, test = data.split(frame)
    y_test = test[data.TARGET].to_numpy()
    resamples = metrics.bootstrap_indices(len(test))
    factors = {"age_band": data.age_band(test["age"]), "job": test["job"]}

    tables: dict[str, list[pd.DataFrame]] = {
        "metrics": [], "segments": [], "calibration": [], "curves": []}
    releases = models.load_releases()
    for release in releases:
        pipeline = models.build(release)
        pipeline.fit(train[release.features], train[data.TARGET])
        scores = pipeline.predict_proba(test[release.features])[:, 1]

        scored = metrics.with_intervals(y_test, scores, resamples)
        scored = scored.rename_axis("metric").reset_index()
        tables["metrics"].append(scored.assign(version=release.version, month=release.month))
        for factor, groups in factors.items():
            segments = metrics.by_segment(y_test, scores, groups)
            tables["segments"].append(segments.assign(version=release.version, factor=factor))
        tables["calibration"].append(
            metrics.calibration(y_test, scores).assign(version=release.version))
        tables["curves"].append(metrics.curves(y_test, scores).assign(version=release.version))

    OUTPUTS.mkdir(exist_ok=True)
    for name, parts in tables.items():
        table = pd.concat(parts, ignore_index=True)
        first = ["version", "month", "factor"]
        table = table[[c for c in first if c in table] + [c for c in table if c not in first]]
        table.round(DECIMALS).to_csv(OUTPUTS / f"{name}.csv", index=False)

    write_summary(train, test, pd.concat(tables["metrics"], ignore_index=True), releases)


def write_summary(train: pd.DataFrame, test: pd.DataFrame, scored: pd.DataFrame,
                  releases: list[models.Release]) -> None:
    """Write the headline numbers and the settings that produced them."""
    auc = scored[scored["metric"] == "roc_auc"].set_index("version")
    best = auc["value"].idxmax()
    best_rows = scored[scored["version"] == best].set_index("metric")
    summary = {
        "best_version": best,
        "best_roc_auc": auc.loc[best, "value"],
        "best_roc_auc_low": auc.loc[best, "low"],
        "best_roc_auc_high": auc.loc[best, "high"],
        "best_recall_top10": best_rows.loc["recall_top10", "value"],
        "best_recall_top10_low": best_rows.loc["recall_top10", "low"],
        "best_recall_top10_high": best_rows.loc["recall_top10", "high"],
        "test_rows": len(test),
        "train_rows": len(train),
        "base_rate": test[data.TARGET].mean(),
        "top_share": metrics.TOP_SHARE,
        "calls_made": metrics.calls_made(len(test)),
        "test_size": data.TEST_SIZE,
        "split_seed": data.SPLIT_SEED,
        "model_seed": models.MODEL_SEED,
        "n_bootstrap": metrics.N_BOOTSTRAP,
        "bootstrap_seed": metrics.BOOTSTRAP_SEED,
        "confidence": metrics.CONFIDENCE,
        "age_edges": data.AGE_EDGES,
        "releases": [{"version": r.version, "month": r.month, "model": r.model,
                      "n_features": len(r.features), "description": r.description}
                     for r in releases],
        "data_file": str(data.DATA_PATH),
        "data_sha256": data.sha256(),
        "packages": {"python": platform.python_version(),
                     **{name: version(name) for name in ["numpy", "pandas", "scikit-learn"]}},
    }
    summary = {k: round(float(v), DECIMALS) if isinstance(v, float) else v
               for k, v in summary.items()}
    (OUTPUTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    start = time.perf_counter()
    evaluate()
    print(pd.read_csv(OUTPUTS / "metrics.csv")
          .pivot(index="metric", columns="version", values="value").round(3))
    print(f"Wrote {OUTPUTS}/ in {time.perf_counter() - start:.1f} s")
