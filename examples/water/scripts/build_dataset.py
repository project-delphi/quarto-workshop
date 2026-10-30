# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.32",
#   "pandas>=2.2",
#   "numpy>=1.26",
#   "openpyxl>=3.1",
#   "geopandas>=1.1",
#   "shapely>=2.1",
#   "pyogrio>=0.10",
#   "rasterio>=1.4",
#   "exactextract>=0.2",
# ]
# ///
"""Build the Colombian municipal water-quality dataset used in Part 2 of the workshop.

Run from the repository root:

    uv run examples/water/scripts/build_dataset.py            # reuse cached downloads
    uv run examples/water/scripts/build_dataset.py --refresh  # re-download every source

Outputs (all under examples/water/data/):

* water_municipal.csv  one row per DIVIPOLA municipality x zone (urban/rural) x year, 2010-2023
* municipios.geojson   simplified DANE MGN 2023 municipal polygons (WGS84)
* README.md            the generated blocks between <!-- BEGIN GENERATED: ... --> markers
                       (coverage table, join coverage, raw-file checksums) are rewritten
* raw/                 cached downloads and raw/manifest.json (URL, date, SHA-256); gitignored

Every value comes from a public source whose URL is defined in the constants below and
documented in data/README.md. Nothing is imputed or synthesised: a value that a source does
not provide is left empty. Downloads are treated as untrusted data: they are cached under
data/raw/<source>/, zips are extracted into their own emptied folders with path checks, and
nothing downloaded is ever executed.

Known gaps (deliberately NOT filled; see README "Known gaps"):

* TODO service continuity (continuidad del servicio de acueducto): SUI, Superintendencia de
  Servicios Publicos Domiciliarios, https://sui.superservicios.gov.co/ is behind Incapsula
  bot protection and cannot be scripted politely.
* TODO under-5 acute diarrhoeal disease (EDA) incidence: SIVIGILA open data
  (https://portalsivigila.ins.gov.co/) only publishes EDA deaths (event 590), which are sparse.
* TODO Saber 11 calendar-A sittings 2018-2 and 2021-2 are not in the datos.gov.co open API
  (kgxf-xxbe stops at 2018-1 and 2021-1 for those years); microdata would have to come from
  ICFES DataIcfes, https://www.icfes.gov.co/investigaciones/data-icfes/ . 2018 and 2021 are
  therefore left empty for saber11_mean / saber11_n.
* TODO sgp_water_pc_real (deflated SGP): DANE CPI index series,
  https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc
  has no stable machine-readable URL; sgp_water_pc is nominal (current pesos).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import zipfile
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
WATER = HERE.parent
DATA = WATER / "data"
RAW = DATA / "raw"
OUT_CSV = DATA / "water_municipal.csv"
OUT_GEOJSON = DATA / "municipios.geojson"
README = DATA / "README.md"
MANIFEST_PATH = RAW / "manifest.json"

USER_AGENT = "quarto-workshop-data-build/1.0 (+https://github.com/project-delphi/quarto-workshop)"
YEARS = list(range(2010, 2024))
ZONES = ["urban", "rural"]
GEOJSON_MAX_BYTES = 3 * 1024 * 1024

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})
REFRESH = False
MANIFEST: dict = {}
REPORT: dict = {"join": [], "notes": []}

SODA = "https://www.datos.gov.co/resource"
TERRIDATA = "https://terridata.dnp.gov.co/assets/docs/txt/dimensiones/TerriData_Dim{d}.txt.zip"
DANE_POP_2005 = ("https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/"
                 "DCD-area-proypoblacion-Mun-2005-2017_VP.xlsx")
DANE_POP_2018 = ("https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/"
                 "PPED-AreaMun-2018-2042_VP.xlsx")
MGN_ZIP = "https://geoportal.dane.gov.co/descargas/mgn_2023/MGN2023_MPIO_POLITICO.zip"
CHIRPS = "https://data.chc.ucsb.edu/products/CHIRPS/v3.0/annual/latam/tifs/chirps-v3.0.{y}.tif"
CHIRPS_README = "https://data.chc.ucsb.edu/products/CHIRPS/v3.0/README-CHIRPSv3.0.txt"
OPENTOPO = "https://api.opentopodata.org/v1/srtm90m"

# Saber 11 sittings mapped to calendar years. Calendar B ("1") sits in the first half of the
# year, calendar A ("2", or "4" from 2019) in the second half. Both sittings of a year are
# pooled, weighting by the number of students. Excluded on purpose:
#   20141 (punt_global empty before 2014-2), 20181 and 20211 (the calendar-A sittings 2018-2
#   and 2021-2 are not published on datos.gov.co, and a calendar-B-only mean is not
#   comparable), and a8xr-en99 (2020-1, an exact copy of kgxf-xxbe periodo 20201).
ICFES_PERIODS = [
    ("kgxf-xxbe", "20142", 2014),
    ("kgxf-xxbe", "20151", 2015), ("kgxf-xxbe", "20152", 2015),
    ("kgxf-xxbe", "20161", 2016), ("kgxf-xxbe", "20162", 2016),
    ("kgxf-xxbe", "20171", 2017), ("kgxf-xxbe", "20172", 2017),
    ("kgxf-xxbe", "20191", 2019), ("kgxf-xxbe", "20194", 2019),
    ("kgxf-xxbe", "20201", 2020), ("rnvb-vnyh", "20204", 2020),
    ("kgxf-xxbe", "20221", 2022), ("kgxf-xxbe", "20224", 2022),
]
ICFES_YEARS = sorted({y for _, _, y in ICFES_PERIODS})


# --------------------------------------------------------------------------------------
# Download helpers
# --------------------------------------------------------------------------------------
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def save_manifest() -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(MANIFEST, indent=2, sort_keys=True, ensure_ascii=False))


def fetch(url: str, dest: Path, params: dict | None = None, pause: float = 1.0,
          retries: int = 6, timeout: int = 600) -> Path:
    """Download url (GET) to dest unless it is already cached; record URL, date and SHA-256.

    Retries with exponential backoff on network errors, 429 and 5xx responses.
    """
    key = dest.relative_to(RAW).as_posix()
    if dest.exists() and not REFRESH:
        entry = MANIFEST.setdefault(key, {"url": url, "params": params, "retrieved": "unknown"})
        if entry.get("bytes") != dest.stat().st_size or "sha256" not in entry:
            entry.update(sha256=sha256(dest), bytes=dest.stat().st_size)
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    delay = 5.0
    for attempt in range(1, retries + 1):
        try:
            print(f"  GET {url}" + (f" {params}" if params else ""), flush=True)
            with SESSION.get(url, params=params, timeout=timeout, stream=True) as r:
                if r.status_code == 429 or r.status_code >= 500:
                    raise requests.HTTPError(f"HTTP {r.status_code}: {r.text[:200]}")
                r.raise_for_status()
                tmp = dest.with_name(dest.name + ".part")
                with tmp.open("wb") as fh:
                    for chunk in r.iter_content(1 << 20):
                        fh.write(chunk)
                tmp.replace(dest)
                final_url = r.url
            break
        except (requests.RequestException, OSError) as exc:
            if attempt == retries:
                raise RuntimeError(f"giving up on {url}: {exc}") from exc
            print(f"    retry {attempt}/{retries - 1} after error: {exc}; sleeping {delay:.0f}s")
            time.sleep(delay)
            delay *= 2
    MANIFEST[key] = {"url": final_url, "params": params, "retrieved": date.today().isoformat(),
                     "sha256": sha256(dest), "bytes": dest.stat().st_size}
    save_manifest()
    time.sleep(pause)
    return dest


def extract(zip_path: Path, out_dir: Path) -> Path:
    """Extract a zip into its own directory, emptied first; refuse unsafe member paths."""
    digest = MANIFEST[zip_path.relative_to(RAW).as_posix()]["sha256"]
    marker = out_dir / ".extracted"
    if marker.exists() and marker.read_text() == digest:
        return out_dir
    if out_dir.exists():
        for p in sorted(out_dir.rglob("*"), reverse=True):
            p.unlink() if (p.is_file() or p.is_symlink()) else p.rmdir()
    out_dir.mkdir(parents=True, exist_ok=True)
    root = out_dir.resolve()
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            target = (out_dir / info.filename).resolve()
            if root not in target.parents and target != root:
                raise ValueError(f"unsafe path in {zip_path.name}: {info.filename}")
        zf.extractall(out_dir)
    marker.write_text(digest)
    return out_dir


def soda_csv(dataset: str, dest: Path, params: dict) -> pd.DataFrame:
    """Run a SoQL query against datos.gov.co, cache the CSV answer, and read it as text."""
    fetch(f"{SODA}/{dataset}.csv", dest, params=params, pause=1.5)
    return pd.read_csv(dest, dtype=str, keep_default_na=False)


def join_report(source: str, codes: pd.Series, universe: set[str], note: str = "") -> None:
    found = set(codes.dropna().unique())
    REPORT["join"].append({
        "source": source,
        "codes_in_source": len(found),
        "matched": len(found & universe),
        "universe_without_data": len(universe - found),
        "source_codes_not_in_divipola": ", ".join(sorted(found - universe)) or "none",
        "note": note,
    })


# --------------------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------------------
def load_divipola() -> pd.DataFrame:
    path = fetch(f"{SODA}/gdxc-w37w.json", RAW / "divipola" / "gdxc-w37w.json",
                 params={"$limit": 5000, "$order": "cod_mpio"})
    d = pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))
    num = lambda s: pd.to_numeric(s.str.replace(",", ".", regex=False), errors="raise")
    out = pd.DataFrame({
        "divipola": d["cod_mpio"].str.zfill(5),
        "municipio": d["nom_mpio"].str.strip(),
        "dpto_code": d["cod_dpto"].str.zfill(2),
        "departamento": d["dpto"].str.strip(),
        "entity_type": d["tipo_municipio"].map({
            "Municipio": "municipality", "Isla": "island",
            "Área no municipalizada": "non_municipalised_area"}),
        "lat": num(d["latitud"]),
        "lon": num(d["longitud"]),
    })
    assert out["entity_type"].notna().all(), "unexpected tipo_municipio value"
    assert out["divipola"].is_unique and len(out) > 1100
    return out.sort_values("divipola").reset_index(drop=True)


TD_NUM = re.compile(r"^-?\d{1,3}(\.\d{3})*(,\d+)?$")


def td_number(s: pd.Series) -> pd.Series:
    """TerriData numbers use '.' for thousands and ',' for decimals ("1.156.728.348,00")."""
    s = s.fillna("").str.strip()
    bad = (s != "") & ~s.str.match(TD_NUM)
    if bad.any():
        raise ValueError(f"unexpected TerriData number format: {s[bad].head().tolist()}")
    return pd.to_numeric(s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
                         errors="coerce")


def load_terridata(dim: int, wanted: dict[str, tuple[str, str, str | None]]) -> pd.DataFrame:
    """Return long rows (var, divipola, year, value, text) for the wanted indicators.

    wanted maps an output variable to (Subcategoría, Indicador, Unidad de Medida or None).
    """
    z = fetch(TERRIDATA.format(d=dim), RAW / "terridata" / f"TerriData_Dim{dim}.txt.zip")
    folder = extract(z, RAW / "terridata" / f"Dim{dim}")
    txt = folder / f"TerriData_Dim{dim}.txt"
    cols = ["Código Entidad", "Subcategoría", "Indicador", "Dato Numérico", "Dato Cualitativo",
            "Año", "Mes", "Unidad de Medida"]
    parts = []
    for chunk in pd.read_csv(txt, sep="|", dtype=str, usecols=cols, encoding="utf-8",
                             chunksize=500_000, keep_default_na=False):
        for var, (sub, ind, unit) in wanted.items():
            m = (chunk["Subcategoría"] == sub) & (chunk["Indicador"] == ind)
            if unit is not None:
                m &= chunk["Unidad de Medida"] == unit
            if m.any():
                parts.append(chunk[m].assign(var=var))
    df = pd.concat(parts, ignore_index=True)
    missing = set(wanted) - set(df["var"])
    if missing:
        raise ValueError(f"TerriData Dim{dim}: indicators not found: {missing}")
    out = pd.DataFrame({
        "var": df["var"],
        "divipola": df["Código Entidad"].str.zfill(5),
        "year": pd.to_numeric(df["Año"]).astype(int),
        "month": pd.to_numeric(df["Mes"]).astype(int),
        "value": td_number(df["Dato Numérico"]),
        "text": df["Dato Cualitativo"].replace("", np.nan),
    })
    # Some indicators carry two cuts of the same year (e.g. total REC coverage in 2016 and
    # 2018 has a September and a December row). Keep the latest month and report conflicts.
    key = ["var", "divipola", "year"]
    dup = out.duplicated(key, keep=False)
    if dup.any():
        d = out[dup]
        conflicts = d.groupby(key)["value"].nunique(dropna=False).gt(1)
        for var, n in d.drop_duplicates(key)["var"].value_counts().items():
            nc = int(conflicts[conflicts.index.get_level_values("var") == var].sum())
            yrs = sorted(map(int, d.loc[d["var"] == var, "year"].unique()))
            REPORT["notes"].append(
                f"TerriData Dim{dim} {var}: {n} entity-years have two monthly cuts "
                f"(years {yrs}); kept the latest month; {nc} of them differ in value")
        out = out.sort_values("month").drop_duplicates(key, keep="last")
    return out.drop(columns="month")


def load_irca() -> pd.DataFrame:
    path = fetch(f"{SODA}/nxt2-39c3.csv", RAW / "ins_irca" / "nxt2-39c3.csv",
                 params={"$limit": 50000, "$order": "departamentocodigo,municipiocodigo,a_o"})
    d = pd.read_csv(path, dtype=str, keep_default_na=False)
    d = d[d["municipiocodigo"] != "#TODOS"]  # department aggregates
    rows = []
    for zone, col in (("urban", "ircaurbano"), ("rural", "ircarural")):
        v = d[col].str.strip()
        bad = ~v.str.match(r"^(ND|\d+(\.\d+)?)$")
        if bad.any():
            raise ValueError(f"IRCA {col}: unexpected values {v[bad].unique()[:5]}")
        rows.append(pd.DataFrame({"divipola": d["municipiocodigo"].str.zfill(5),
                                  "year": d["a_o"].astype(int), "zone": zone,
                                  "irca": pd.to_numeric(v.replace("ND", np.nan))}))
    out = pd.concat(rows, ignore_index=True)
    assert not out.duplicated(["divipola", "year", "zone"]).any()
    oor = out[(out["irca"] < 0) | (out["irca"] > 100)]
    if len(oor):
        raise ValueError(f"IRCA outside [0, 100]: {len(oor)} rows")
    return out


def load_population(universe: set[str]) -> pd.DataFrame:
    frames = []
    for url, name in ((DANE_POP_2005, "DCD-area-proypoblacion-Mun-2005-2017_VP.xlsx"),
                      (DANE_POP_2018, "PPED-AreaMun-2018-2042_VP.xlsx")):
        path = fetch(url, RAW / "dane_population" / name)
        xl = pd.ExcelFile(path, engine="openpyxl")
        sheet = [s for s in xl.sheet_names if s not in ("Índice", "PPED")][0]
        raw = pd.read_excel(xl, sheet, header=None, dtype=object)
        hdr = raw.index[raw.iloc[:, 0].astype(str).str.strip() == "DP"][0]
        df = raw.iloc[hdr + 1:].copy()
        df.columns = [str(c).strip() for c in raw.iloc[hdr]]
        popcol = [c for c in df.columns if c.upper() in ("POBLACIÓN", "TOTAL")][0]
        df = df[df["MPIO"].notna() & df["AÑO"].notna()]
        frames.append(pd.DataFrame({
            "divipola": df["MPIO"].astype(str).str.strip().str.zfill(5),
            "year": pd.to_numeric(df["AÑO"]).astype(int),
            "area": df["ÁREA GEOGRÁFICA"].astype(str).str.strip(),
            "pop": pd.to_numeric(df[popcol]),
        }))
    p = pd.concat(frames, ignore_index=True)
    p = p[p["year"].isin(YEARS)]
    area = {"Cabecera Municipal": "urban", "Centros Poblados y Rural Disperso": "rural",
            "Total": "total"}
    unknown = set(p["area"]) - set(area)
    if unknown:
        raise ValueError(f"unexpected DANE area labels: {unknown}")
    p["area"] = p["area"].map(area)
    wide = p.pivot_table(index=["divipola", "year"], columns="area", values="pop",
                         aggfunc="sum").reset_index()
    gap = (wide["urban"] + wide["rural"] - wide["total"]).abs().max()
    REPORT["notes"].append(f"DANE population: max |urban + rural - total| = {gap:.0f} people")
    join_report("DANE population projections by area", wide["divipola"], universe)
    wide["rural_share"] = wide["rural"] / wide["total"].where(wide["total"] > 0)
    long = wide.melt(id_vars=["divipola", "year", "rural_share", "total"],
                     value_vars=["urban", "rural"], var_name="zone", value_name="population")
    return long.rename(columns={"total": "population_total"})


def load_altitude(div: pd.DataFrame) -> pd.DataFrame:
    """SRTM 90 m elevation at each DIVIPOLA head-town point via the OpenTopoData public API.

    Public API limits (opentopodata.org): 100 locations per request, 1 call/s, 1000 calls/day.
    """
    rows = []
    pts = div[["divipola", "lat", "lon"]].reset_index(drop=True)
    for i, start in enumerate(range(0, len(pts), 100)):
        batch = pts.iloc[start:start + 100]
        locs = "|".join(f"{la:.6f},{lo:.6f}" for la, lo in zip(batch["lat"], batch["lon"]))
        dest = RAW / "opentopodata" / f"srtm90m_batch{i:02d}.json"
        if dest.exists() and not REFRESH:
            cached = json.loads(dest.read_text())
            got = [(round(r["location"]["lat"], 5), round(r["location"]["lng"], 5))
                   for r in cached.get("results", [])]
            want = [(round(a, 5), round(b, 5)) for a, b in zip(batch["lat"], batch["lon"])]
            if got != want:  # DIVIPOLA changed since the cache was written
                dest.unlink()
        fetch(OPENTOPO, dest, params={"locations": locs, "interpolation": "bilinear"}, pause=1.2)
        res = json.loads(dest.read_text())
        if res.get("status") != "OK":
            raise RuntimeError(f"OpenTopoData error in {dest.name}: {res}")
        for code, r in zip(batch["divipola"], res["results"]):
            rows.append({"divipola": code, "altitude_m": r["elevation"]})
    out = pd.DataFrame(rows)
    out["altitude_m"] = pd.to_numeric(out["altitude_m"])
    return out


def load_saber11(universe: set[str]) -> pd.DataFrame:
    """Mean Saber 11 global score by school municipality x school area x year.

    Several periods of kgxf-xxbe contain exact duplicate student records (e.g. periodo 20194
    has 1,096,524 rows for 546,211 distinct estu_consecutivo), so each query first collapses
    to one row per student and then aggregates (SoQL pipe |>).
    """
    rows, checks = [], []
    for ds, per, year in ICFES_PERIODS:
        query = (
            "SELECT estu_consecutivo, cole_cod_mcpio_ubicacion AS m, cole_area_ubicacion AS a, "
            "max(punt_global::number) AS g "
            f"WHERE periodo = '{per}' AND punt_global IS NOT NULL "
            "GROUP BY estu_consecutivo, m, a "
            "|> SELECT m, a, avg(g) AS mean_global, count(*) AS n GROUP BY m, a "
            "ORDER BY m, a LIMIT 100000")
        d = soda_csv(ds, RAW / "icfes" / f"{ds}_{per}_by_mpio_area.csv", {"$query": query})
        ctrl = soda_csv(ds, RAW / "icfes" / f"{ds}_{per}_count.csv", {
            "$select": "count(*) AS n, count(distinct estu_consecutivo) AS students",
            "$where": f"periodo = '{per}' AND punt_global IS NOT NULL"})
        n_students = int(ctrl.loc[0, "students"])
        d["n"] = d["n"].astype(int)
        checks.append({"dataset": ds, "periodo": per, "year": year,
                       "rows_with_score": int(ctrl.loc[0, "n"]), "distinct_students": n_students,
                       "students_aggregated": int(d["n"].sum()),
                       "no_area": int(d.loc[~d["a"].isin(["URBANO", "RURAL"]), "n"].sum())})
        # A student could only be counted twice if one record had two locations; check.
        if d["n"].sum() != n_students:
            raise ValueError(f"Saber 11 {ds} {per}: aggregated {d['n'].sum()} students, "
                             f"expected {n_students}")
        d = d[d["a"].isin(["URBANO", "RURAL"]) & (d["m"] != "")]
        rows.append(pd.DataFrame({
            "divipola": d["m"].str.zfill(5), "zone": d["a"].map({"URBANO": "urban",
                                                                  "RURAL": "rural"}),
            "year": year, "n": d["n"], "sum": pd.to_numeric(d["mean_global"]) * d["n"]}))
    s = pd.concat(rows, ignore_index=True).groupby(["divipola", "zone", "year"], as_index=False)[
        ["n", "sum"]].sum()
    s["saber11_mean"] = s["sum"] / s["n"]
    REPORT["saber11_checks"] = checks
    join_report("ICFES Saber 11 (school municipality)", s["divipola"], universe)
    return s.rename(columns={"n": "saber11_n"})[["divipola", "zone", "year", "saber11_mean",
                                                  "saber11_n"]]


def check_saber11_duplicate_2020() -> None:
    """a8xr-en99 (Saber 11 2020-1) should be identical to kgxf-xxbe periodo 20201."""
    params = {"$select": "count(*) AS n, count(distinct estu_consecutivo) AS students, "
                         "sum(punt_global::number) AS total"}
    a = soda_csv("a8xr-en99", RAW / "icfes" / "a8xr-en99_20201_check.csv", params)
    b = soda_csv("kgxf-xxbe", RAW / "icfes" / "kgxf-xxbe_20201_check.csv",
                 {**params, "$where": "periodo = '20201'"})
    same = a.iloc[0].astype(float).equals(b.iloc[0].astype(float))
    REPORT["notes"].append(
        f"Saber 11 2020-1: a8xr-en99 {a.iloc[0].to_dict()} vs kgxf-xxbe 20201 "
        f"{b.iloc[0].to_dict()} -> {'identical totals, a8xr-en99 not used' if same else 'DIFFERENT'}")


def load_dropout(universe: set[str]) -> pd.DataFrame:
    d = soda_csv("nudc-7mev", RAW / "men" / "nudc-7mev_desercion.csv", {
        "$select": "a_o, c_digo_municipio, deserci_n", "$limit": 100000,
        "$order": "a_o, c_digo_municipio"})
    # Code "0" is a NACIONAL total (2019-2021) published as a fraction, not a percentage.
    nat = d["c_digo_municipio"].str.strip() == "0"
    REPORT["notes"].append(f"MEN dropout: dropped {int(nat.sum())} national rows (code 0); "
                           "municipal codes are zero-padded (2011 codes lack the leading 0)")
    d = d[~nat]
    out = pd.DataFrame({"divipola": d["c_digo_municipio"].str.zfill(5),
                        "year": d["a_o"].astype(int),
                        "dropout_rate": pd.to_numeric(d["deserci_n"].replace("", np.nan))})
    dup = out.duplicated(["divipola", "year"], keep=False)
    if dup.any():
        REPORT["notes"].append(f"MEN dropout: {dup.sum()} duplicated municipality-year rows "
                               f"{out[dup].drop_duplicates().to_dict('records')[:4]}")
        # identical duplicates are harmless; conflicting ones are an error
        if out[dup].drop_duplicates().duplicated(["divipola", "year"]).any():
            raise ValueError("MEN dropout: conflicting duplicates")
        out = out.drop_duplicates()
    join_report("MEN dropout (nudc-7mev)", out["divipola"], universe)
    return out


def load_polygons() -> "gpd.GeoDataFrame":
    import geopandas as gpd
    z = fetch(MGN_ZIP, RAW / "mgn" / "MGN2023_MPIO_POLITICO.zip", timeout=1800)
    folder = extract(z, RAW / "mgn" / "MGN2023_MPIO_POLITICO")
    shp = next(folder.rglob("*.shp"))
    g = gpd.read_file(shp)
    g = g.rename(columns={"mpio_cdpmp": "divipola"})
    g["divipola"] = g["divipola"].astype(str).str.zfill(5)
    assert g["divipola"].is_unique
    return g[["divipola", "mpio_cnmbr", "dpto_cnmbr", "geometry"]]


def load_rainfall(polys) -> pd.DataFrame:
    """Coverage-weighted mean annual CHIRPS v3.0 rainfall over each municipal polygon."""
    import rasterio
    from rasterio.io import MemoryFile
    from exactextract import exact_extract
    fetch(CHIRPS_README, RAW / "chirps" / "README-CHIRPSv3.0.txt")
    g = polys[["divipola", "geometry"]].to_crs("EPSG:4326")
    frames = []
    for y in YEARS:
        tif = fetch(CHIRPS.format(y=y), RAW / "chirps" / f"chirps-v3.0.{y}.tif")
        with rasterio.open(tif) as src:
            if src.crs.to_epsg() != 4326:
                raise ValueError(f"unexpected CHIRPS CRS {src.crs}")
            arr, prof = src.read(1), src.profile
        # The LatAm annual GeoTIFFs mark ocean/no data as -9999 without declaring a nodata
        # value; declare it so those cells are excluded from the polygon means.
        prof.update(nodata=-9999.0)
        with MemoryFile() as mem:
            with mem.open(**prof) as dst:
                dst.write(arr, 1)
            with mem.open() as ds:
                r = exact_extract(ds, g, ["mean", "count"], include_cols=["divipola"],
                                  output="pandas")
        r = r.rename(columns={"mean": "rainfall_mm"})
        r.loc[r["count"] <= 0, "rainfall_mm"] = np.nan
        r["year"] = y
        frames.append(r[["divipola", "year", "rainfall_mm"]])
    out = pd.concat(frames, ignore_index=True)
    if (out["rainfall_mm"] < 0).any():
        raise ValueError("negative CHIRPS rainfall after masking")
    return out


def write_geojson(polys, div: pd.DataFrame) -> dict:
    import shapely
    g = polys.to_crs("EPSG:4326").merge(div[["divipola", "municipio", "departamento"]],
                                         on="divipola", how="left")
    g["municipio"] = g["municipio"].fillna(g["mpio_cnmbr"])
    g["departamento"] = g["departamento"].fillna(g["dpto_cnmbr"])
    g = g[["divipola", "municipio", "departamento", "geometry"]].sort_values("divipola")
    tolerance, info = 0.002, {}
    while True:
        s = g.copy()
        # simplify_coverage keeps shared borders shared (no gaps or slivers between neighbours)
        s["geometry"] = s.geometry.simplify_coverage(tolerance)
        s["geometry"] = shapely.set_precision(s.geometry.values, 1e-4)  # ~11 m grid
        s["geometry"] = s.geometry.make_valid()
        s = s.explode(index_parts=False).loc[lambda x: x.geom_type == "Polygon"]
        s = s.dissolve(by="divipola", as_index=False, aggfunc="first")
        OUT_GEOJSON.unlink(missing_ok=True)
        s.to_file(OUT_GEOJSON, driver="GeoJSON", engine="pyogrio",
                  layer_options={"COORDINATE_PRECISION": "4", "RFC7946": "YES"})
        size = OUT_GEOJSON.stat().st_size
        info = {"tolerance_deg": tolerance, "bytes": size, "features": len(s),
                "invalid": int((~s.geometry.is_valid).sum()),
                "lost": sorted(set(g["divipola"]) - set(s["divipola"]))}
        if size <= GEOJSON_MAX_BYTES:
            return info
        tolerance *= 1.25


# --------------------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------------------
COLUMNS = ["divipola", "municipio", "dpto_code", "departamento", "region", "entity_type",
           "zone", "year", "irca", "irca_missing", "water_coverage", "sewer_coverage",
           "water_coverage_total", "sewer_coverage_total", "population", "rural_share", "rurality_category", "altitude_m", "ipm", "mdm", "idf",
           "idf_new", "sgp_water_pc", "rainfall_mm", "infant_mortality", "saber11_mean",
           "saber11_n", "dropout_rate"]
ZONE_SPECIFIC = ["irca", "irca_missing", "water_coverage", "sewer_coverage", "population", "ipm",
                 "saber11_mean", "saber11_n"]
ROUNDING = {"irca": 1, "water_coverage": 2, "sewer_coverage": 2, "water_coverage_total": 2,
            "sewer_coverage_total": 2, "rural_share": 4,
            "ipm": 2, "mdm": 2, "idf": 2, "idf_new": 2, "sgp_water_pc": 0, "rainfall_mm": 0,
            "altitude_m": 0, "infant_mortality": 2, "saber11_mean": 1, "dropout_rate": 2}
INT_COLS = ["year", "irca_missing", "population", "saber11_n", "altitude_m", "sgp_water_pc",
            "rainfall_mm"]


def build() -> pd.DataFrame:
    print("DIVIPOLA universe")
    div = load_divipola()
    universe = set(div["divipola"])

    print("TerriData")
    td1 = load_terridata(1, {"region": ("Descripción general", "Región", None),
                             "rurality_category": ("Descripción general",
                                                   "Categoría de ruralidad", None)})
    sub3 = "Vivienda y acceso a servicios públicos"
    td3 = load_terridata(3, {
        "water_urban": (sub3, "Cobertura de acueducto urbana (REC)", None),
        "water_rural": (sub3, "Cobertura de acueducto rural (REC)", None),
        "sewer_urban": (sub3, "Cobertura de alcantarillado urbana (REC)", None),
        "sewer_rural": (sub3, "Cobertura de alcantarillado rural (REC)", None),
        # TerriData publishes no urban/rural REC rows for department capitals (codes ddd001),
        # so the municipal totals are kept as separate, municipality-level columns.
        "water_coverage_total": (sub3, "Cobertura de acueducto (REC)", None),
        "sewer_coverage_total": (sub3, "Cobertura de alcantarillado (REC)", None)})
    td5 = load_terridata(5, {"infant_mortality": (
        "Tasas y coberturas",
        "Tasa de mortalidad infantil en menores de 1 año (x cada 1.000 nacidos vivos)", None)})
    td7 = load_terridata(7, {
        "idf": ("Desempeño fiscal", "Indicador de desempeño fiscal", None),
        "idf_new": ("Nuevo Índice de Desempeño Fiscal",
                    "Puntaje nuevo Índice de Desempeño Fiscal", None),
        "sgp_water": ("SGP - Distribución asignaciones SGP por sectores", "Agua potable",
                      "Pesos corrientes")})
    td8 = load_terridata(8, {"mdm": ("Resumen MDM", "MDM", None)})
    td14 = load_terridata(14, {
        "ipm_urban": ("Indicadores agregados de IPM", "IPM - Cabecera (Censo)", None),
        "ipm_rural": ("Indicadores agregados de IPM",
                      "IPM - Centros poblados y rural disperso (Censo)", None)})
    td = pd.concat([td1, td3, td5, td7, td8, td14], ignore_index=True)
    td_muni = td[td["divipola"].isin(universe)]
    for var, grp in td.groupby("var"):
        muni = grp[~grp["divipola"].str.endswith("000") & (grp["divipola"] != "01001")]
        join_report(f"TerriData {var}", muni.loc[muni["value"].notna() | muni["text"].notna(),
                                                 "divipola"], universe)

    # Region: TerriData gives a DANE region for each department (code ddd000); use the
    # department value so non-municipalised areas get one too, and check consistency.
    reg = td1[td1["var"] == "region"]
    dept_region = (reg[reg["divipola"].str.endswith("000")]
                   .assign(dpto_code=lambda x: x["divipola"].str[:2])
                   .set_index("dpto_code")["text"])
    muni_region = reg[reg["divipola"].isin(universe)].set_index("divipola")["text"].dropna()
    div["region"] = div["dpto_code"].map(dept_region)
    # Bogotá D.C. is both department 11 and municipality 11001
    div.loc[div["region"].isna(), "region"] = div["divipola"].map(muni_region)
    both = div.set_index("divipola")["region"].reindex(muni_region.index)
    clash = both[both != muni_region]
    REPORT["notes"].append(
        f"Region: TerriData department-level region used; municipality-level region exists for "
        f"{len(muni_region)} codes and differs from its department's for {len(clash)} "
        f"{list(clash.index)[:10]}; codes without region: "
        f"{div.loc[div['region'].isna(), 'divipola'].tolist()}")
    rur = td1[(td1["var"] == "rurality_category")].set_index("divipola")["text"]
    div["rurality_category"] = div["divipola"].map(rur)

    print("INS IRCA")
    irca = load_irca()
    join_report("INS IRCA (nxt2-39c3)", irca.loc[irca["irca"].notna(), "divipola"], universe)

    print("DANE population")
    pop = load_population(universe)

    print("OpenTopoData altitude")
    alt = load_altitude(div)

    print("ICFES Saber 11")
    check_saber11_duplicate_2020()
    sab = load_saber11(universe)

    print("MEN dropout")
    drop = load_dropout(universe)

    print("MGN polygons and CHIRPS rainfall")
    polys = load_polygons()
    join_report("DANE MGN 2023 polygons", polys["divipola"], universe)
    rain = load_rainfall(polys)

    # ---- grid -------------------------------------------------------------------------
    grid = (div[["divipola", "municipio", "dpto_code", "departamento", "region",
                 "entity_type", "rurality_category"]]
            .merge(pd.DataFrame({"zone": ZONES}), how="cross")
            .merge(pd.DataFrame({"year": YEARS}), how="cross"))

    def zoned(prefix_map: dict[str, str], name: str) -> pd.DataFrame:
        parts = []
        for var, zone in prefix_map.items():
            x = td_muni[td_muni["var"] == var][["divipola", "year", "value"]]
            parts.append(x.assign(zone=zone).rename(columns={"value": name}))
        return pd.concat(parts, ignore_index=True)

    def muni_level(var: str, name: str) -> pd.DataFrame:
        return td_muni[td_muni["var"] == var][["divipola", "year", "value"]].rename(
            columns={"value": name})

    df = grid.merge(irca, on=["divipola", "year", "zone"], how="left")
    df = df.merge(zoned({"water_urban": "urban", "water_rural": "rural"}, "water_coverage"),
                  on=["divipola", "year", "zone"], how="left")
    df = df.merge(zoned({"sewer_urban": "urban", "sewer_rural": "rural"}, "sewer_coverage"),
                  on=["divipola", "year", "zone"], how="left")
    for v in ("water_coverage_total", "sewer_coverage_total"):
        df = df.merge(muni_level(v, v), on=["divipola", "year"], how="left")
    df = df.merge(pop, on=["divipola", "year", "zone"], how="left")
    df = df.merge(alt, on="divipola", how="left")
    ipm = zoned({"ipm_urban": "urban", "ipm_rural": "rural"}, "ipm")
    ipm = ipm[ipm["year"] == 2018].drop(columns="year")  # 2018 census, repeated every year
    df = df.merge(ipm, on=["divipola", "zone"], how="left")
    df = df.merge(muni_level("mdm", "mdm"), on=["divipola", "year"], how="left")
    df = df.merge(muni_level("idf", "idf"), on=["divipola", "year"], how="left")
    df = df.merge(muni_level("idf_new", "idf_new"), on=["divipola", "year"], how="left")
    df = df.merge(muni_level("sgp_water", "sgp_water"), on=["divipola", "year"], how="left")
    df["sgp_water_pc"] = df["sgp_water"] / df["population_total"].where(df["population_total"] > 0)
    df = df.merge(rain, on=["divipola", "year"], how="left")
    df = df.merge(muni_level("infant_mortality", "infant_mortality"), on=["divipola", "year"],
                  how="left")
    df = df.merge(sab, on=["divipola", "zone", "year"], how="left")
    # In a year with published Saber 11 results, a zone with no tested students has n = 0.
    in_icfes = df["year"].isin(ICFES_YEARS)
    df.loc[in_icfes & df["saber11_n"].isna(), "saber11_n"] = 0
    df = df.merge(drop, on=["divipola", "year"], how="left")
    df["irca_missing"] = df["irca"].isna().astype(int)

    # Notes on source values that need a caveat (not altered).
    my = df.drop_duplicates(["divipola", "year"])
    for c in ("water_coverage", "sewer_coverage", "water_coverage_total", "sewer_coverage_total"):
        x = df[c] if c in ZONE_SPECIFIC else my[c]
        unit = "zone-years" if c in ZONE_SPECIFIC else "municipality-years"
        REPORT["notes"].append(
            f"{c}: {int((x > 100).sum())} {unit} > 100, {int((x < 0).sum())} < 0, "
            f"{int((x == 100).sum())} exactly 100, {int((x == 0).sum())} exactly 0, out of "
            f"{int(x.notna().sum())} non-missing (2010-2023; values not altered)")
    has_zone = df.groupby("divipola")["water_coverage"].transform("count") > 0
    has_total = df.groupby("divipola")["water_coverage_total"].transform("count") > 0
    only_total = sorted(df.loc[~has_zone & has_total, "divipola"].unique())
    neither = sorted(df.loc[~has_zone & ~has_total, "divipola"].unique())
    REPORT["notes"].append(
        f"REC coverage: {len(only_total)} codes have municipal totals but no urban/rural "
        f"split in any year ({', '.join(only_total)}); {len(neither)} codes have neither "
        f"({', '.join(neither)})")
    REPORT["notes"].append(
        f"idf (old method): {int((my['idf'] == 0).sum())} municipality-years equal 0 "
        f"(kept as published; likely no fiscal report); idf_new: "
        f"{int((my['idf_new'] == 0).sum())} zeros")
    for code, g in df[df["population"].isna()].groupby("divipola"):
        REPORT["notes"].append(f"population: {code} missing in {sorted(map(int, g['year'].unique()))}"
                               " (not in the DANE series for those years)")
    zero_tot = my.loc[my["rural_share"].isna() & my["population"].notna()]
    for code, g in zero_tot.groupby("divipola"):
        REPORT["notes"].append(f"population: DANE lists {code} with 0 people in "
                               f"{sorted(map(int, g['year'].unique()))}, so rural_share and "
                               "sgp_water_pc are empty there")
    REPORT["notes"].append(
        f"infant_mortality: {int((my['infant_mortality'] > 100).sum())} municipality-years "
        f"> 100 per 1,000 live births (max {my['infant_mortality'].max():.1f}); these are "
        "small-number rates and are not altered")
    REPORT["notes"].append(f"sgp_water_pc: max {df['sgp_water_pc'].max():,.0f} COP/person")
    REPORT["polys"] = polys
    REPORT["div"] = div

    df = df[COLUMNS].copy()
    for c, nd in ROUNDING.items():
        df[c] = df[c].round(nd)
    for c in INT_COLS:
        df[c] = df[c].round().astype("Int64")
    return df.sort_values(["divipola", "zone", "year"],
                          key=lambda s: s.map({"urban": 0, "rural": 1}) if s.name == "zone"
                          else s).reset_index(drop=True)


def validate(df: pd.DataFrame) -> None:
    assert not df.duplicated(["divipola", "zone", "year"]).any(), "duplicate key"
    assert df["divipola"].str.fullmatch(r"\d{5}").all(), "divipola must be 5 digits"
    assert set(df["year"]) == set(YEARS), "years"
    assert set(df["zone"]) == set(ZONES), "zones"
    assert df["irca"].dropna().between(0, 100).all(), "IRCA outside [0, 100]"
    for c in ("water_coverage", "sewer_coverage", "water_coverage_total", "sewer_coverage_total"):
        bad = df[c].dropna()[~df[c].dropna().between(0, 100)]
        assert bad.empty, f"{c} outside [0, 100]: {bad.head().tolist()}"
    assert df["dropout_rate"].dropna().between(0, 100).all()
    assert df["ipm"].dropna().between(0, 100).all()
    assert df["rural_share"].dropna().between(0, 1).all()
    assert ((df["irca_missing"] == 1) == df["irca"].isna()).all()
    for c in ("mdm", "idf", "idf_new"):
        assert df[c].dropna().between(0, 100).all(), c
    assert df["saber11_mean"].dropna().between(0, 500).all()
    assert (df["saber11_mean"].isna() | (df["saber11_n"] > 0)).all()
    num = df.select_dtypes("number").astype(float)
    assert np.isfinite(num.fillna(0)).all().all(), "infinite values"
    assert df[["divipola", "municipio", "departamento", "zone", "year"]].notna().all().all()
    assert len(df) == df["divipola"].nunique() * len(ZONES) * len(YEARS)
    print(f"validation passed: {len(df):,} rows x {df.shape[1]} columns")


# --------------------------------------------------------------------------------------
# README generated blocks
# --------------------------------------------------------------------------------------
def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def coverage_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for c in COLUMNS:
        nonmiss = df[c].notna()
        years = sorted(df.loc[nonmiss, "year"].unique())
        if years:
            span = df["year"].isin(years)
            within = f"{100 * nonmiss[span].mean():.1f}"
            yr = f"{years[0]}–{years[-1]}"
            gaps = sorted(set(range(years[0], years[-1] + 1)) - set(years))
            if gaps:
                yr += " (none in " + ", ".join(map(str, gaps)) + ")"
            if c in ZONE_SPECIFIC:
                by = nonmiss[span].groupby(df.loc[span, "zone"]).mean() * 100
                within += f" (urban {by['urban']:.1f} / rural {by['rural']:.1f})"
        else:
            within, yr = "0.0", "–"
        rows.append({"column": f"`{c}`", "all rows, 2010–2023 (%)": f"{100 * nonmiss.mean():.1f}",
                     "years with data": yr, "rows in years with data (%)": within})
    return pd.DataFrame(rows)


def replace_block(text: str, name: str, body: str) -> str:
    pat = re.compile(rf"(<!-- BEGIN GENERATED: {name} -->\n).*?(<!-- END GENERATED: {name} -->)",
                     re.S)
    if not pat.search(text):
        print(f"  README has no '{name}' block; skipped")
        return text
    return pat.sub(lambda m: m.group(1) + body.rstrip("\n") + "\n" + m.group(2), text)


def update_readme(df: pd.DataFrame, geo: dict) -> None:
    cov = coverage_table(df)
    print(cov.to_string(index=False))
    join = pd.DataFrame(REPORT["join"])
    join.columns = ["source", "codes in source", "matched DIVIPOLA", "DIVIPOLA codes without data",
                    "source codes not in DIVIPOLA (dropped)", "note"]
    join = join.drop(columns="note")
    print(join.to_string(index=False))
    man = pd.DataFrame([{"file": f"`{k}`", "retrieved": v.get("retrieved"),
                         "bytes": f"{v.get('bytes', 0):,}", "SHA-256": f"`{v.get('sha256')}`"}
                        for k, v in sorted(MANIFEST.items())])
    sab = pd.DataFrame(REPORT["saber11_checks"])
    summary = (f"Rows: **{len(df):,}** ({df['divipola'].nunique():,} DIVIPOLA codes × 2 zones × "
               f"{df['year'].nunique()} years); columns: **{df.shape[1]}**; file size "
               f"{OUT_CSV.stat().st_size / 1e6:.1f} MB. GeoJSON: {geo['features']:,} polygons, "
               f"{geo['bytes'] / 1e6:.2f} MB, simplification tolerance "
               f"{geo['tolerance_deg']:.4f}°; CSV codes without a polygon: "
               f"{', '.join(geo['csv_without_polygon']) or 'none'}. Built {date.today()}.")
    notes = "\n".join(f"- {n}" for n in REPORT["notes"])
    if not README.exists():
        print("  README.md not found; generated blocks not written")
        return
    text = README.read_text(encoding="utf-8")
    text = replace_block(text, "summary", summary)
    text = replace_block(text, "coverage", md_table(cov))
    text = replace_block(text, "join", md_table(join))
    text = replace_block(text, "saber11", md_table(sab))
    text = replace_block(text, "notes", notes)
    text = replace_block(text, "manifest", md_table(man))
    README.write_text(text, encoding="utf-8")


def main() -> None:
    global REFRESH, MANIFEST
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--refresh", action="store_true", help="re-download every source")
    args = ap.parse_args()
    REFRESH = args.refresh
    RAW.mkdir(parents=True, exist_ok=True)
    MANIFEST = json.loads(MANIFEST_PATH.read_text()) if MANIFEST_PATH.exists() else {}
    if REFRESH:
        MANIFEST = {}
    t0 = time.time()
    df = build()
    validate(df)
    df.to_csv(OUT_CSV, index=False, na_rep="", encoding="utf-8", lineterminator="\n")
    print(f"wrote {OUT_CSV.relative_to(WATER.parent.parent)} "
          f"({OUT_CSV.stat().st_size / 1e6:.2f} MB)")
    geo = write_geojson(REPORT["polys"], REPORT["div"])
    geo["csv_without_polygon"] = sorted(set(df["divipola"]) - set(REPORT["polys"]["divipola"]))
    print(f"wrote {OUT_GEOJSON.relative_to(WATER.parent.parent)}: {geo}")
    save_manifest()
    update_readme(df, geo)
    for n in REPORT["notes"]:
        print("note:", n)
    print(f"done in {time.time() - t0:.0f}s (python {sys.version.split()[0]}, "
          f"pandas {pd.__version__})")


if __name__ == "__main__":
    main()
