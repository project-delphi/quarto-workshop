# Data

## gradebook.csv

**SYNTHETIC: INVENTED FOR TEACHING, NOT REAL STUDENT DATA.** A gradebook for a fictional
course, written by `scripts/make_gradebook.py` with a fixed seed
(`uv run python scripts/make_gradebook.py` rewrites the same file). No student, course or
mark is real. It is the only data file, and it is read-only: change the script, not the file.

One row per student: 60 students in three sections (A, B and C), four assignments. Students
are ids, never names; the feedback sheets show only section totals.

| Column | Description |
|---|---|
| `student_id` | `S001` to `S060`, an id with no meaning |
| `section` | `A`, `B` or `C` |
| `quiz_1`, `essay`, `quiz_2`, `project` | Mark out of 100, a whole number; blank when the work was not submitted |
