"""Generate a reproducible synthetic classroom dataset, not official IRCA data."""

from pathlib import Path
import random

import numpy as np
import pandas as pd


np.random.seed(42)
random.seed(42)
n_rows = 5000

municipios_dict = {
    "Boyacá": ["Tunja", "Duitama", "Sogamoso", "Paipa", "Villa de Leyva", "Samacá", "Chiquinquirá"],
    "Cundinamarca": ["Bogotá", "Chía", "Zipaquirá", "Soacha", "Facatativá", "Girardot"],
    "Santander": ["Bucaramanga", "Floridablanca", "San Gil", "Socorro", "Barrancabermeja"],
}

data = []
for _ in range(n_rows):
    dep = random.choice(list(municipios_dict))
    mun = random.choice(municipios_dict[dep])

    ph = np.clip(np.random.normal(7.0, 0.8), 0, 14)
    turbiedad = np.random.exponential(3.0)
    cloro = np.clip(np.random.normal(1.0, 0.5), 0, 3.0)
    coliformes = int(np.random.exponential(15))

    # Teaching formula supplied for this exercise; this is not the legal IRCA formula.
    risk_base = (turbiedad * 2) + ((2.0 - cloro) * 10) + (abs(7.0 - ph) * 3) + (coliformes * 0.5)
    irca_score = np.clip(risk_base + np.random.normal(0, 2), 0, 100)

    if irca_score <= 5:
        clasificacion = "Sin riesgo"
    elif irca_score <= 14:
        clasificacion = "Riesgo bajo"
    elif irca_score <= 35:
        clasificacion = "Riesgo medio"
    elif irca_score <= 80:
        clasificacion = "Riesgo alto"
    else:
        clasificacion = "Inviable sanitariamente"

    data.append([dep, mun, round(ph, 2), round(turbiedad, 2), round(cloro, 2),
                 coliformes, round(irca_score, 1), clasificacion])

df = pd.DataFrame(data, columns=[
    "departamento", "municipio", "ph", "turbiedad_ntu", "cloro_residual_mg_l",
    "coliformes_totales", "irca_score", "irca_clasificacion",
])
df.to_csv(Path(__file__).with_name("irca_andina_dataset.csv"), index=False)
print(f"Wrote {len(df)} synthetic rows")
