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


def _prompt_values_hold() -> None:
    """Stop the render if a value typed into a printed prompt no longer matches analysis.py.

    Prompts are literal text, so the water chapters type some settings into them: the years and
    the missing-feature limit (10-prepare's prompts), k's range, the seed and n_init
    (11-cluster's), and the naming rule's thresholds (12-interpret's rule list). Both editions
    import this module, so one check covers both; the naming rule is tested by its behaviour,
    since its thresholds are literals inside name_rule().
    """
    from scripts.prose import text_holds
    text_holds((analysis.FIRST_YEAR, analysis.LAST_YEAR) == (2016, 2023),
               "the prepare prompts' years, 2016–2023")
    text_holds(analysis.MAX_MISSING == 2, "the prepare prompt's 'more than 2 features'")
    text_holds(list(analysis.K_RANGE) == list(range(2, 9)), "the cluster prompt's k=2–8")
    text_holds((analysis.SEED, analysis.N_INIT) == (42, 20),
               "the cluster prompt's random_state=42, n_init=20")

    def name(**z) -> str:
        p = {"urban_row_share": 0.5, "z_rural_share": 0.0, "z_altitude_m": 0.0,
             "z_water_coverage": 0.0, "irca_median_band": "Low", **z}
        return analysis.name_rule(p).split(",")[0]
    text_holds(name(urban_row_share=0.39) == "Rural" and name(urban_row_share=0.4) == "Towns",
               "the naming rule's 40% urban threshold")
    text_holds(name(z_rural_share=-0.5) == "Cities and large towns"
               and name(z_rural_share=-0.49) == "Towns"
               and name(z_altitude_m=-0.5) == "Lowland towns"
               and name(z_altitude_m=0.5) == "Highland towns"
               and "low-coverage" in analysis.name_rule({"urban_row_share": 0.5, "z_rural_share": 0,
                   "z_altitude_m": 0, "z_water_coverage": -0.5, "irca_median_band": "Low"})
               and "low-coverage" not in analysis.name_rule({"urban_row_share": 0.5,
                   "z_rural_share": 0, "z_altitude_m": 0, "z_water_coverage": -0.49,
                   "irca_median_band": "Low"}),
               "the naming rule's half a standard deviation")


_prompt_values_hold()


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
