"""Write data/synthetic_business.csv: SYNTHETIC monthly figures for Acme Signals.

Acme Signals is a fictional company, and these numbers are invented for teaching.
They are not real company data. The fixed seed makes the file the same on every run:

    uv run python scripts/make_synthetic_business.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260101
MONTHS = pd.period_range("2026-01", "2026-10", freq="M")
PRICE_GBP = 3_500  # invented monthly subscription per customer
CALLS_PER_CUSTOMER = 18_000  # invented ranked calls per customer per month
CALLS_PER_PILOT = 4_000
FIRST_RELEASE = pd.Period("2026-03", freq="M")  # v1 in releases.yml: no sales before it
OUT = Path("data/synthetic_business.csv")


def make(seed: int = SEED) -> pd.DataFrame:
    """Invent customers, pilots, revenue and ranked calls for each month."""
    rng = np.random.default_rng(seed)
    customers, pilots = 0, 1  # pilots convert to paying customers once v1 exists
    rows = []
    for month in MONTHS:
        converted = rng.binomial(pilots, 0.35) if month >= FIRST_RELEASE else 0
        customers += converted
        pilots = pilots - converted + rng.poisson(1.0)
        rows.append({
            "month": str(month),
            "customers": customers,
            "pilots": pilots,
            "monthly_recurring_revenue_gbp": customers * PRICE_GBP,
            "calls_ranked": int(rng.normal(1.0, 0.08)
                                * (customers * CALLS_PER_CUSTOMER + pilots * CALLS_PER_PILOT)),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    make().to_csv(OUT, index=False)
    print(f"Wrote {OUT}")
