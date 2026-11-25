"""The water analysis, run once per chapter, for Part III's computed numbers and figures.

Imports the finished project's script (examples/water/scripts/analysis.py), exactly as the
workshop deck does, and runs it in memory: nothing is written to examples/water/outputs/.
Every number Part III quotes about the water data comes from here or from analysis.load().
Run from book/ (execute-dir: project).
"""
from __future__ import annotations

import sys
from functools import cache
from pathlib import Path

SCRIPTS = Path("../examples/water/scripts").resolve()
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import analysis  # noqa: E402

from scripts.prose import language  # noqa: E402

# The Spanish edition (book-es/, translation/glossary.md) reads the analysis's labels and
# cluster names in Spanish; its logic (IRCA bands, column names) stays the project's own.
LABELS_ES = {
    "FEATURE_LABELS": {
        "irca": "IRCA de prestadores (0–100)",
        "water_coverage": "Cobertura de acueducto (%)",
        "sewer_coverage": "Cobertura de alcantarillado (%)",
        "ipm": "Pobreza multidimensional, 2018 (%)",
        "rural_share": "Proporción rural de la población",
        "altitude_m": "Altitud de la cabecera, punto SRTM derivado (m)",
        "rainfall_mm": "Precipitación (mm/año)",
        "mdm": "Desempeño municipal, MDM",
        "log_sgp_water_pc": "Transferencias para agua por persona (log SGP)",
    },
    "SHORT_LABELS": {
        "irca": "IRCA", "water_coverage": "Cob. acueducto", "sewer_coverage": "Cob. alcantarillado",
        "ipm": "Pobreza", "rural_share": "Proporción rural", "altitude_m": "Altitud (derivada)",
        "rainfall_mm": "Precipitación", "mdm": "MDM", "log_sgp_water_pc": "log SGP/persona",
    },
    "OUTCOMES": {
        "infant_mortality": "Mortalidad infantil (por 1,000 nacidos vivos)",
        "saber11_mean": "Puntaje medio de Saber 11 (0–500)",
        "dropout_rate": "Deserción escolar, colegios públicos (%)",
    },
}
SETTINGS_ES = {"Rural": "Rural", "Cities and large towns": "Ciudades y pueblos grandes",
               "Lowland towns": "Pueblos de tierras bajas", "Highland towns": "Pueblos de tierras altas",
               "Towns": "Pueblos", "low-coverage": "baja cobertura"}
RISK_ES = {"no-risk water": "agua sin riesgo", "low-risk water": "agua de riesgo bajo",
           "medium-risk water": "agua de riesgo medio", "high-risk water": "agua de riesgo alto",
           "unfit water": "agua inviable sanitariamente"}


class _Spanish:
    """The analysis module, with its labels and run()'s cluster names in Spanish. Settings
    assigned to it (a chapter's `A.MAX_MISSING = 1`) are set on the module itself."""

    def __init__(self, module) -> None:
        object.__setattr__(self, "_module", module)

    def __getattr__(self, name):
        if name in LABELS_ES:
            return LABELS_ES[name]
        if name == "run":
            return lambda *args, **kwargs: _localize(self._module.run(*args, **kwargs))
        return getattr(self._module, name)

    def __setattr__(self, name, value) -> None:
        setattr(self._module, name, value)


def name_es(name: str) -> str:
    """"Rural, low-coverage, high-risk water" -> "Rural, baja cobertura, agua de riesgo alto"."""
    parts = name.split(", ")
    return ", ".join(SETTINGS_ES.get(p, RISK_ES.get(p, p)) for p in parts)


A = _Spanish(analysis) if language() == "es" else analysis


def _localize(out: dict) -> dict:
    """A run's cluster names in Spanish (the Spanish edition only)."""
    out = dict(out)
    out["profiles"] = out["profiles"].assign(name=out["profiles"]["name"].map(name_es))
    if "cluster_name" in out["clusters"]:
        out["clusters"] = out["clusters"].assign(cluster_name=out["clusters"]["cluster_name"].map(name_es))
    return out


@cache
def res() -> dict:
    """The full in-memory run (about 5 seconds): summary, prepared, clusters, profiles, k table."""
    out = analysis.run()
    return _localize(out) if language() == "es" else out


@cache
def raw():
    """The analysis table as published: one row per municipality, zone and year."""
    return analysis.load()


def fmt(x) -> str:
    return f"{x:,}"


def names() -> dict[int, str]:
    return res()["profiles"]["name"].to_dict()


def colors() -> dict[int, str]:
    return res()["profiles"]["color"].to_dict()


# The water exercises' opening puzzle (D5-c; PLAN-improvement-briefs.md §2.1): three true
# sentences about the kinds, read from cluster_profiles.csv, one of them given a causal verb.
# The exercises print `planted`; Appendix E's answer prints `honest[CLAIM_PLANTED]`, from this
# one function, so the answer cannot drift from the puzzle.
CLAIM_CAUSAL = ("because", "causes", "leads to", "due to")  # words that claim a cause
CLAIM_PLANTED = 2                                           # the third sentence claims one
CLAIM_CAUSE = "because its water is less safe"


def council_claims(out: dict) -> tuple[list[str], list[str]]:
    """The three sentences as an honest analyst writes them, and as the draft prints them."""
    if language() == "es":
        raise ValueError("council_claims: the Spanish sentences come with the translation of "
                         "exercises-water.qmd (translation/pending.yml)")
    from scripts.prose import number_words, spans, text_holds

    word = number_words()
    prof = out["profiles"]
    kind = {c: n.rsplit(", ", 1)[0] for c, n in prof["name"].items()}
    worst = int(prof["irca_median"].idxmax())  # the least safe water
    im = int(prof["infant_mortality_mean"].idxmax())
    top = int(prof["saber11_mean_median"].idxmax())
    sab = prof["saber11_mean_median"]
    text_holds(sab[worst] < sab[top] and prof.loc[worst, "irca_median"] > prof.loc[top, "irca_median"],
               "the planted comparison, true as a description")
    first = (f'The "{kind[worst]}" kind had the highest median utility-supplied IRCA of the '
             f'{word[len(prof)]}, {prof.loc[worst, "irca_median"]:.1f}.')
    second = (f'Recorded infant mortality was highest, on average, in the "{kind[im]}" kind: '
              f'{prof.loc[im, "infant_mortality_mean"]:.1f} deaths per 1,000 live births in '
              f'{spans(A.OUTCOME_YEARS["infant_mortality"])}.')
    third = (f'The median Saber 11 score was lower in the "{kind[worst]}" kind than in '
             f'"{kind[top]}", {sab[worst]:.0f} against {sab[top]:.0f}')
    honest = [first, second, third + ", and its utility-supplied water also scored worse; the "
              "comparison describes the kinds and does not show that the water caused the gap."]
    planted = [first, second, f"{third}, {CLAIM_CAUSE}."]
    text_holds(0 <= CLAIM_PLANTED < len(planted) and CLAIM_CAUSE in planted[CLAIM_PLANTED]
               and not any(v in t for t in honest for v in CLAIM_CAUSAL)
               and not any(v in t for i, t in enumerate(planted) if i != CLAIM_PLANTED
                           for v in CLAIM_CAUSAL),
               "one planted causal claim")
    return honest, planted
