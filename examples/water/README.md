# Water quality in Colombian municipalities: finished Part 2 project

The finished project for Part 2 of the workshop. One script computes everything once; a
Quarto website publishes it many ways. The pages are explore, clusters, a report (html,
docx and Typst PDF), council slides (pptx), Excel tables, a blog post and a dashboard.

The question: which kinds of municipal zone exist, judged by drinking-water quality,
services and context, and how do health and education outcomes differ between them? One
row is a **municipality × zone (urban/rural) × year**, 2016–2023. IRCA is the
**utility-supplied ("prestadores") IRCA** in INS open data (datos.gov.co `nxt2-39c3`).
Comparisons between clusters are descriptive and do not establish a causal effect of
water quality.

## Layout

| path | what it is |
|---|---|
| `data/` | the committed dataset, its dictionary and caveats (`data/README.md`) |
| `scripts/analysis.py` | all computation; importable (`analysis.run()`) and runnable |
| `outputs/` | written by the script, ignored by Git (see below) |
| `explore.qmd` | first look: shape, missing values, IRCA by band, zone and year |
| `clusters.qmd` | choosing k, PCA picture, profiles, outcomes, correlation ≠ causation |
| `report.qmd` | report: html page, `report.docx` and `report.pdf` (Typst) |
| `slides.qmd` | six-slide council briefing, `slides.pptx` |
| `tables.qmd` | writes `cluster_tables.xlsx` (one sheet per table, dictionary, notes) |
| `posts/four-kinds-of-municipal-zone/` | blog post, titled with the actual k |
| `dashboard.qmd` | IRCA band maps with a year slider and a searchable table |
| `index.qmd`, `_quarto.yml` | the website: listing, navbar, freeze, pre-render |

## Rebuild

From this folder, with a Python that has pandas, numpy, matplotlib, scikit-learn, pyarrow,
openpyxl, tabulate, plotly, itables and Jupyter:

```bash
python scripts/analysis.py   # writes outputs/ and prints the row counts and the k table
quarto render                # runs the script again (pre-render), then renders every page
quarto preview               # live preview at a local URL
```

`scripts/analysis.py` writes:

- `outputs/clusters.parquet`: keys, cluster id and name, PCA coordinates, raw and z
  features, flags (`*_imputed`, `*_from_total`) and outcomes.
- `outputs/cluster_profiles.csv`: one row per cluster, with rows, distinct municipalities,
  mean raw and z features, and outcome means, medians and n.
- `outputs/k_selection.csv` and `outputs/stability.csv`: inertia, silhouette and ARI.
- `outputs/outcomes_by_year.csv` and `outputs/irca_infant*.csv`: the outcome comparisons.
- `outputs/summary.json`: the counts, k and the reason for choosing it.

Every page reads these files. None of them recomputes the clusters.

## Freeze and stale pages

`_quarto.yml` sets `execute: freeze: auto`: a page is re-executed only when **its own
source** changes. The pre-render step rebuilds `outputs/` before every render, but frozen
pages do not notice. After you change `data/` or `scripts/analysis.py`:

```bash
rm -rf _freeze && quarto render     # re-execute every page
quarto render clusters.qmd          # or re-execute one page: rendering a single file ignores freeze
```

Rendering a single file inside the project still runs the pre-render script first.
`tables.qmd` sets `freeze: false`, so the workbook is rewritten on every render even when
the rest of the site is frozen.

## Design decisions

- **Rows.** Only `entity_type == "municipality"`. San Andrés (`island`) has no TerriData
  values (data README, caveat 11), and non-municipalised areas have almost no data. Years
  are 2016–2023, because MDM starts in 2016. Rows without IRCA are dropped, and so are rows
  missing more than two of the nine features; the script prints both counts.
- **Features.** `irca`, `water_coverage`, `sewer_coverage`, `ipm`, `rural_share`,
  `altitude_m`, `rainfall_mm`, `mdm` and `log(sgp_water_pc)`. `idf` is left out because its
  method changes in 2020 (`idf_new` is a different scale). Outcomes are never clustered on.
- **Department capitals.** They have no urban/rural coverage split. Urban capital rows take
  `water_coverage_total` / `sewer_coverage_total`, flagged in `*_from_total`; rural capital
  rows are left empty and then imputed.
- **Imputation.** Median within year × zone, with a `<feature>_imputed` flag.
- **Standardisation.** z-scores within each year, after the log transform. This removes the
  nominal-peso drift and year-level shifts, so one pooled k-means gives labels comparable
  over time, and a municipality can move between clusters. The rural IRCA sampling change
  around 2020 is only partly absorbed, because the year's mean pools both zones.
- **k.** k-means for k = 2–8 (`random_state=42`, `n_init=20`); silhouette on a fixed sample
  of 5,000 rows. k = 2 is excluded because it mostly splits urban from rural rows (see the
  `ari_vs_zone` column). The rule: the smallest k ≥ 3 after which one more cluster cuts
  inertia by less than 10%, provided its silhouette is within 0.01 of the best k ≥ 3.
  Stability: the adjusted Rand index against refits with five other seeds.
- **Cluster ids and names.** Ids are ordered by centroid IRCA, low to high, so a re-run with
  the same seed keeps them. Names come from `name_rule()`: the setting (share of urban rows,
  rural share, altitude), "unserved" if water coverage is at least 0.5 SD below average, and
  the Resolución 2115 band of the cluster's median IRCA. Colours follow the id on every page.
  A name describes the cluster's typical profile, not every member: some urban zones fall in
  the "Rural, unserved" cluster (Leticia's head town in 2022–2023, for example).
- **Outcomes.** Infant mortality uses 2017–2019 and 2021–2023 only (one method regime; a
  blank may mean no recorded deaths). Saber 11 uses its published years. Infant mortality
  and dropout are municipal values repeated on both zone rows: an ecological mismatch.

## Notes

- The GeoJSON follows RFC 7946 (exterior rings counter-clockwise). Plotly's maps expect the
  opposite winding, so `analysis.load_geojson()` reverses the rings in memory; the file in
  `data/` is unchanged.
- Each Plotly figure loads MathJax from a CDN, so the dashboard's browser console may report
  one harmless MathJax error. The interactive table also loads its library from a CDN, so
  the dashboard needs an internet connection.
- The dashboard is about 12 MB: Plotly (about 4 MB) plus one copy of the 2.7 MB GeoJSON per
  map. Each year's frame carries only the band codes.

## Sources

See `data/README.md` for every source, licence, retrieval date and caveat. IRCA risk bands:
[Resolución 2115 de 2007, art. 15](https://normas.cra.gov.co/gestor/docs/resolucion_minproteccion_2115_2007.htm).
National context (report only): MinVivienda and INS,
[INCA 2023](https://www.minvivienda.gov.co/sites/default/files/documentos/informe-nacional-de-calidad-del-agua-para-consumo-humano-inca-2023.pdf),
Tabla 4.
