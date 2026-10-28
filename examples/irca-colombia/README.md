# Reported municipal IRCA, Boyacá and neighboring departments

`irca_boyaca_cundinamarca_santander.csv` is an unchanged CSV response from the
[Instituto Nacional de Salud (INS) dataset on Colombia's open-data portal](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Calidad-del-Agua-para-Consumo-Humano-en-Colombia/nxt2-39c3),
downloaded 2026-10-28. The API query selects department codes 15 (Boyacá),
25 (Cundinamarca), and 68 (Santander). It returned 5,815 rows for 2007–2024.
The bundled CSV's SHA-256 is
`bb93ecbdc15961c02637c5ad7375905284ca230d970b45075cb550ca0c07d9c9`.
The exact query is:

```text
https://www.datos.gov.co/resource/nxt2-39c3.csv?$where=departamentocodigo in ('15','25','68')&$limit=50000
```

One row is an **annual IRCA summary for one municipality or department**.
Rows with `municipiocodigo == "#TODOS"` are department aggregates; exclude
them when comparing municipalities. `irca`, `ircaurbano`, and `ircarural` are
reported percentages. `ND` means unavailable, especially for rural values.
This table contains neither individual water samples nor pH, turbidity, or
chlorine measurements. Do not interpret a municipality-level summary as a
sample-level sensor alert or a prediction of future water quality.

The 2024 extract has 318 municipality rows: 119 in Boyacá, 113 in
Cundinamarca, and 86 in Santander. It also has three department aggregates.
The 2024 municipal rural IRCA field is numeric for 152 of the 318 rows.
These counts are computed from the bundled CSV, not estimates of a population.
The source was published under CC BY-SA 4.0; retain attribution and source link
when reusing it. The portal's source is INS/SIVICAP. INS describes its IRCA
operation as based on water-quality surveillance records, with municipal and
departmental dissemination: [DANE statistical inventory](https://inventariosen.dane.gov.co/ooee/ooee/97/).

`notebook.qmd` is a worked descriptive analysis. Copy the bundle into a
practice `context/` directory and update relative paths when adapting it.
