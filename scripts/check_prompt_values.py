"""Check that the values typed into the water prompts match the analysis that computes them.

Prompts are literal text, so the water chapters (English and Spanish) and the deck type some of
examples/water/scripts/analysis.py's settings into them: the years, the missing-feature limit,
the features, k's range, the seed, n_init, the number of stability seeds, and the naming rule's
thresholds. This script reads each file's text and checks that it holds the value analysis.py
has now, so a changed setting, or an edited prompt, stops `make book` and `make deck` with the
file and the value to rewrite. It does not depend on frozen results: it runs on every build.

The naming thresholds are literals inside name_rule(); they are read from its source and then
confirmed by its behaviour just either side of each one.

Run from the repository root, in the book's environment:
    cd book && uv run python ../scripts/check_prompt_values.py
"""
from __future__ import annotations

import inspect
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples" / "water" / "scripts"))
import analysis as A  # noqa: E402

problems: list[str] = []


def holds(path: str, needle: str, what: str) -> None:
    if needle not in (ROOT / path).read_text(encoding="utf-8"):
        problems.append(f"{path}: expected {needle!r} ({what}); rewrite the text to match analysis.py")


def behaves(ok: bool, what: str) -> None:
    if not ok:
        problems.append(f"analysis.name_rule: {what}")


years = f"{A.FIRST_YEAR}–{A.LAST_YEAR}"
k = f"k={A.K_RANGE.start}–{A.K_RANGE.stop - 1}"
seeds = f"random_state={A.SEED}, n_init={A.N_INIT}"
features = [f"log({f.removeprefix('log_')})" if f.startswith("log_") else f for f in A.FEATURES]
prepare = {"book/chapters/10-prepare.qmd": f"more than {A.MAX_MISSING} features",
           "book-es/chapters/10-prepare.qmd": f"más de {A.MAX_MISSING} características",
           "slides/_water.qmd": f"more than {A.MAX_MISSING} features"}
for path, missing in prepare.items():
    holds(path, years, "the analysis years")
    holds(path, missing, "MAX_MISSING")
    holds(path, "features " + ", ".join(features) if "book-es" not in path
          else "características " + ", ".join(features), "FEATURES, in order")
cluster = {"book/chapters/11-cluster.qmd": f"{len(A.STABILITY_SEEDS)}-seed ARI",
           "book-es/chapters/11-cluster.qmd": f"ARI con {len(A.STABILITY_SEEDS)} semillas",
           "slides/_water.qmd": f"{len(A.STABILITY_SEEDS)}-seed ARI"}
for path, ari in cluster.items():
    holds(path, k, "K_RANGE")
    holds(path, seeds, "SEED and N_INIT")
    holds(path, ari, "STABILITY_SEEDS")
holds("slides/_water.qmd", f"n_init={A.N_INIT}`", "N_INIT, in the k-means notes")

# The naming rule: thresholds from the source, confirmed by behaviour on both sides.
source = inspect.getsource(A.name_rule)
urban = float(re.search(r'urban_row_share"\]\s*<\s*([\d.]+)', source).group(1))
sd = {m: float(v) for m, v in re.findall(r'"z_(rural_share|altitude_m|water_coverage)"\]\s*[<>]=\s*-?([\d.]+)', source)}
half = set(sd.values())
behaves(len(half) == 1, f"expected one SD threshold for every z-score rule, found {sorted(half)}")
t = half.pop() if len(half) == 1 else 0.5
eps = 0.01


def name(**z) -> str:
    p = {"urban_row_share": 0.5, "z_rural_share": 0.0, "z_altitude_m": 0.0,
         "z_water_coverage": 0.0, "irca_median_band": "Low", **z}
    return A.name_rule(p)


def setting(**z) -> str:
    return name(**z).split(",")[0]


behaves(setting(urban_row_share=urban - eps) == "Rural" and setting(urban_row_share=urban) == "Towns",
        f"the urban-share threshold is not {urban:.0%}")
behaves(setting(z_rural_share=-t) == "Cities and large towns" and setting(z_rural_share=-t + eps) == "Towns",
        f"the rural-share threshold is not -{t} SD")
behaves(setting(z_altitude_m=-t) == "Lowland towns" and setting(z_altitude_m=-t + eps) == "Towns",
        f"the lowland threshold is not -{t} SD")
behaves(setting(z_altitude_m=t) == "Highland towns" and setting(z_altitude_m=t - eps) == "Towns",
        f"the highland threshold is not +{t} SD")
behaves("low-coverage" in name(z_water_coverage=-t) and "low-coverage" not in name(z_water_coverage=-t + eps),
        f"the low-coverage threshold is not -{t} SD")
pct = f"{urban:.0%}"
for path, words in {"book/chapters/12-interpret.qmd": [f"fewer than {pct}", f"{t} SD or more below", f"{t} SD or more above"],
                    "book-es/chapters/12-interpret.qmd": [f"menos del {pct}", f"{t} DE o más por debajo", f"{t} DE o más por encima"],
                    "slides/_water.qmd": [f"fewer than {pct}", f"≤ −{t} SD", f"≥ +{t} SD"]}.items():
    for w in words:
        holds(path, w, "the naming rule's thresholds")

for p in problems:
    print(f"check_prompt_values: {p}", file=sys.stderr)
files = {*prepare, *cluster, "book/chapters/12-interpret.qmd", "book-es/chapters/12-interpret.qmd"}
print(f"water prompts: typed values in {len(files)} files checked against analysis.py, "
      f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
