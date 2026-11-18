"""Write data/gradebook.csv: a SYNTHETIC gradebook, invented for teaching.

No student, course or mark in it is real. Students are ids (S001, S002, ...), never names.
The fixed seed makes the file the same on every run:

    uv run python scripts/make_gradebook.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261118
SECTIONS = {"A": 20, "B": 21, "C": 19}  # students per section
SECTION_SHIFT = {"A": 3.0, "B": -2.5, "C": 0.0}  # invented: how far each section's marks move
ASSIGNMENTS = {"quiz_1": 72, "essay": 66, "quiz_2": 70, "project": 76}  # invented mean marks
ABILITY_SD = 8.0  # spread of the students' general level, in marks
NOISE_SD = 7.0  # spread of one mark around a student's level
MISSING = 0.03  # share of marks left blank: work not submitted
OUT = Path("data/gradebook.csv")


def make(seed: int = SEED) -> pd.DataFrame:
    """One row per student: id, section, and a mark out of 100 per assignment (blank if missing)."""
    rng = np.random.default_rng(seed)
    rows, number = [], 0
    for section, size in SECTIONS.items():
        for _ in range(size):
            number += 1
            ability = rng.normal(SECTION_SHIFT[section], ABILITY_SD)
            row = {"student_id": f"S{number:03d}", "section": section}
            for assignment, mean in ASSIGNMENTS.items():
                mark = int(np.clip(round(mean + ability + rng.normal(0, NOISE_SD)), 0, 100))
                row[assignment] = pd.NA if rng.random() < MISSING else mark
            rows.append(row)
    return pd.DataFrame(rows).astype({a: "Int64" for a in ASSIGNMENTS})


if __name__ == "__main__":
    make().to_csv(OUT, index=False)
    print(f"Wrote {OUT} (SYNTHETIC)")
