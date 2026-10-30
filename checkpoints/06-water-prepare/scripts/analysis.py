"""Prepare Colombian municipal zones for clustering (workshop checkpoint 06).

Run from the project folder (the one that holds data/ and scripts/):

    python scripts/analysis.py

Selects municipality rows for 2016-2023 with IRCA, builds nine features, fills
urban coverage of department capitals from the municipal total (flagged),
drops rows missing more than two features, imputes year x zone medians
(flagged) and standardises within each year. Writes outputs/prepared.parquet
and prints the row counts. IRCA is the utility-supplied ("prestadores") IRCA
in INS open data, datos.gov.co nxt2-39c3.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "water_municipal.csv"
OUTPUTS = ROOT / "outputs"

FIRST_YEAR, LAST_YEAR = 2016, 2023      # MDM starts in 2016
FEATURES = ["irca", "water_coverage", "sewer_coverage", "ipm", "rural_share",
            "altitude_m", "rainfall_mm", "mdm", "log_sgp_water_pc"]
MAX_MISSING = 2                          # drop rows missing more features than this
# Resolución 2115 de 2007, art. 15. IRCA has one decimal, so (5, 14] means 5.1-14.
IRCA_BINS = [-0.001, 5, 14, 35, 80, 100]
IRCA_BANDS = ["No risk", "Low", "Medium", "High", "Unfit"]


# --- 1. load and select --------------------------------------------------------
def load(path: Path | str = DATA) -> pd.DataFrame:
    """Read the analysis table, keeping DIVIPOLA codes as text."""
    return pd.read_csv(path, dtype={"divipola": str, "dpto_code": str})


def irca_band(irca: pd.Series) -> pd.Series:
    """Resolución 2115 risk band for each IRCA value."""
    return pd.cut(irca, bins=IRCA_BINS, labels=IRCA_BANDS)


def prepare(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Select rows, transform, impute with flags and standardise within year.

    Returns the prepared rows (raw features, ``z_<feature>``, flags, outcomes)
    and a dict of row counts for each step.
    """
    counts = {}
    win = df[df["year"].between(FIRST_YEAR, LAST_YEAR)]
    counts["rows_2016_2023"] = len(win)
    # Municipalities only. San Andrés (entity_type "island") has no TerriData
    # values (data/README.md, caveat 11), so it would miss 5 of 9 features.
    d = win[win["entity_type"] == "municipality"].copy()
    counts["dropped_not_municipality"] = len(win) - len(d)
    counts["municipality_rows"] = len(d)

    has_irca = d["irca"].notna()
    counts["dropped_no_irca"] = int((~has_irca).sum())
    d = d[has_irca].copy()

    # Department capitals (code ends in 001) have no urban/rural REC split.
    # Urban capital rows take the municipal total, flagged; rural rows are not
    # filled from the total and go through the usual imputation below.
    capital_urban = d["divipola"].str.endswith("001") & (d["zone"] == "urban")
    for col in ["water_coverage", "sewer_coverage"]:
        fill = capital_urban & d[col].isna() & d[f"{col}_total"].notna()
        d[f"{col}_from_total"] = fill.astype(int)
        d.loc[fill, col] = d.loc[fill, f"{col}_total"]
    counts["capital_urban_rows_filled_from_total"] = int(d["water_coverage_from_total"].sum())

    d["log_sgp_water_pc"] = np.log(d["sgp_water_pc"])  # all values > 0

    n_missing = d[FEATURES].isna().sum(axis=1)
    keep = n_missing <= MAX_MISSING
    counts["dropped_too_many_missing"] = int((~keep).sum())
    d = d[keep].copy()

    medians = d.groupby(["year", "zone"])[FEATURES].transform("median")
    for col in FEATURES:
        d[f"{col}_imputed"] = d[col].isna().astype(int)
        d[col] = d[col].fillna(medians[col])
        counts[f"imputed_{col}"] = int(d[f"{col}_imputed"].sum())
    counts["rows_with_any_imputed"] = int(d[[f"{c}_imputed" for c in FEATURES]].any(axis=1).sum())

    # Standardise within year: removes nominal-peso drift and year-level shifts.
    grp = d.groupby("year")[FEATURES]
    z = (d[FEATURES] - grp.transform("mean")) / grp.transform(lambda s: s.std(ddof=0))
    for col in FEATURES:
        d[f"z_{col}"] = z[col]

    d["irca_band"] = irca_band(d["irca"])
    counts["kept"] = len(d)
    counts["kept_urban"] = int((d["zone"] == "urban").sum())
    counts["kept_rural"] = int((d["zone"] == "rural").sum())
    counts["municipalities"] = int(d["divipola"].nunique())
    return d.reset_index(drop=True), counts


# --- write -----------------------------------------------------------------
def main() -> None:
    prepared, counts = prepare(load())
    for key, value in counts.items():
        print(f"{key}: {value:,}")
    OUTPUTS.mkdir(exist_ok=True)
    prepared.to_parquet(OUTPUTS / "prepared.parquet", index=False)
    print("wrote outputs/prepared.parquet")


if __name__ == "__main__":
    main()
