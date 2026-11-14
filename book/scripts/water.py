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
    """The analysis module, with its labels in Spanish."""

    def __init__(self, module) -> None:
        self._module = module

    def __getattr__(self, name):
        return LABELS_ES[name] if name in LABELS_ES else getattr(self._module, name)


def name_es(name: str) -> str:
    """"Rural, low-coverage, high-risk water" -> "Rural, baja cobertura, agua de riesgo alto"."""
    parts = name.split(", ")
    return ", ".join(SETTINGS_ES.get(p, RISK_ES.get(p, p)) for p in parts)


A = _Spanish(analysis) if language() == "es" else analysis


@cache
def res() -> dict:
    """The full in-memory run (about 5 seconds): summary, prepared, clusters, profiles, k table."""
    out = analysis.run()
    if language() == "es":
        out = dict(out)
        out["profiles"] = out["profiles"].assign(name=out["profiles"]["name"].map(name_es))
        if "cluster_name" in out["clusters"]:
            out["clusters"] = out["clusters"].assign(cluster_name=out["clusters"]["cluster_name"].map(name_es))
    return out


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
