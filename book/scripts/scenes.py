"""Data for the book's live 3-D scenes, computed from the repository's data.

The deck's 3-D slides compute every point, height and border in their cells and the three.js
bundle (assets/deck-3d.min.js) only draws them. The book runs the same bundle, through
book/assets/deck-host.js, so these functions repeat the deck cells' computations (slides/
_london.qmd #london-map; slides/_water.qmd #water-kmeans, #water-pca-3d, #water-relief) and
return the same JSON. Keep them in step with the deck cells: the duplication is the price of
leaving the deck's sources untouched (book/PLAN.md §8).

Paths are relative to book/, where the chapters run (execute-dir: project).
"""
from __future__ import annotations

import collections
import html
import json
from pathlib import Path

import numpy as np
import pandas as pd

# The cluster cloud's check of how well clusters separate: the share of each zone-year's
# nearest neighbours (this many) in its own cluster. Chapter 11 quotes it.
NEIGHBOURS = 15

LONDON = Path("../examples/london/data")


def scene_html(scene: str, data: dict, alt: str, extra: str = "", fallback: str = "",
               height: str = "460px", views: list[tuple[str, str]] | None = None,
               load_bundle: bool = False) -> str:
    """A raw-HTML block for one live scene: the element the bundle draws into, then its view
    buttons (they stand in for the deck's fragments). load_bundle adds the host and bundle
    scripts; pass it for the first scene on a page."""
    out = ["```{=html}"]
    out.append(f'<div class="deck-3d" data-scene="{scene}" style="height: {height};" role="img" '
               f'aria-label="{html.escape(alt)}">'
               f'<script type="application/json">{json.dumps(data, separators=(",", ":"))}</script>'
               f'{extra}<p class="fallback" hidden>This 3-D view needs WebGL. {html.escape(fallback)}</p></div>')
    if views:
        buttons = "".join(
            f'<button type="button" data-view="{v}" aria-pressed="{str(i == 0).lower()}"'
            f'{" class=\"visible\"" if i == 0 else ""}>{html.escape(label)}</button>'
            for i, (v, label) in enumerate(views))
        out.append(f'<div class="view-buttons" role="group" aria-label="Views">{buttons}</div>')
    if load_bundle:
        out.append('<script src="../assets/deck-host.js"></script>')
        out.append('<script src="../assets/deck-3d.min.js"></script>')
    out.append("```")
    return "\n".join(out)


def london_map() -> dict:
    """The five sights and Visit London's ten churches on the London boroughs, in metres
    (slides/_london.qmd, #london-map)."""
    places = pd.read_csv(LONDON / "places.csv")
    facts = pd.read_csv(LONDON / "sights.csv").pivot(index="sight", columns="fact", values="value")
    v = pd.read_csv(LONDON / "visits.csv")
    year = int(v["year"].max())
    v_year = v[v["year"] == year].set_index("attraction")["visits"]
    sights = places[places["kind"] == "sight"].assign(
        visits=lambda d: d["place"].map(v_year),
        paid=lambda d: d["place"].map(facts["price_band"]).eq("Paid"))
    assert sights["visits"].notna().all() and len(sights) == 5, "a sight lacks visits"
    sights = sights.sort_values("visits", ascending=False)
    churches = places[places["kind"] == "church"]
    assert len(churches) == len(pd.read_csv(LONDON / "churches.csv")), "places.csv lacks a church"

    lat0 = (places["lat"].min() + places["lat"].max()) / 2
    lon0 = (places["lon"].min() + places["lon"].max()) / 2
    kx, ky = 111_320 * np.cos(np.radians(lat0)), 110_574

    def m(lon, lat):
        return (lon - lon0) * kx, (lat - lat0) * ky

    xy_all = np.array([m(o, a) for o, a in zip(places["lon"], places["lat"])])
    x0, y0 = xy_all.min(0) - (1200, 900)
    x1, y1 = xy_all.max(0) + (1200, 900)

    geo = json.loads((LONDON / "london-boroughs.geojson").read_text(encoding="utf-8"))
    edges = collections.Counter()
    owners = collections.defaultdict(set)
    rings = []
    for feat in geo["features"]:
        gm = feat["geometry"]
        polys = [gm["coordinates"]] if gm["type"] == "Polygon" else gm["coordinates"]
        assert all(len(p) == 1 for p in polys), f"{feat['properties']['LAD24NM']} has a hole"
        for ring in (r for p in polys for r in p):
            pts = [tuple(np.round(np.array(q) / 0.0004).astype(int)) for q in ring]
            rings.append((feat["properties"]["LAD24NM"], pts))
            for a, b in zip(pts, pts[1:]):
                if a != b:
                    e = (a, b) if a < b else (b, a)
                    edges[e] += 1
                    owners[e].add(feat["properties"]["LAD24NM"])

    vert = {q: m(q[0] * 0.0004, q[1] * 0.0004) for _, r in rings for q in r}
    banks, borders = [], []
    for (a, b), n in sorted(edges.items()):
        p = (vert[a], vert[b])
        if all(x0 <= x <= x1 and y0 <= y <= y1 for x, y in p):
            (borders if n > 1 else banks).extend(round(c) for q in p for c in q)

    def clip(ring):
        for ax, lim, sgn in ((0, x0, 1), (0, x1, -1), (1, y0, 1), (1, y1, -1)):
            out = []
            for k, q in enumerate(ring):
                o = ring[k - 1]
                qin = (q[ax] - lim) * sgn >= 0
                if qin != ((o[ax] - lim) * sgn >= 0):
                    t = (lim - o[ax]) / (q[ax] - o[ax])
                    out.append(tuple(o[i] + t * (q[i] - o[i]) for i in (0, 1)))
                if qin:
                    out.append(q)
            ring = out
        return ring

    tones = ["#313b47", "#463f31", "#33423a", "#45364a"]
    water = "#2f6db5"
    fills = collections.defaultdict(list)
    for name, pts in rings:
        ring = clip([vert[q] for q in pts[:-1]])
        flat = [(round(x), round(y)) for x, y in ring]
        flat = [q for k, q in enumerate(flat) if q != flat[k - 1]]
        if len(flat) >= 3:
            fills[name].append([c for q in flat for c in q])
    nbrs = collections.defaultdict(set)
    for o in owners.values():
        for name in o:
            nbrs[name] |= o - {name}
    tone = {}
    for name in sorted(fills):
        used = {tone.get(b) for b in nbrs[name]}
        tone[name] = next((i for i in range(len(tones)) if i not in used), None)
        assert tone[name] is not None, f"{name} needs a fifth tone"
    areas = [{"color": c, "polys": [p for b in sorted(fills) if tone[b] == i for p in fills[b]]}
             for i, c in enumerate(tones) if i in tone.values()]

    def area(flat):
        return abs(sum(flat[i] * flat[i - 1] - flat[i - 2] * flat[i + 1]
                       for i in range(0, len(flat), 2))) / 2

    shown = sorted(b for b, ps in fills.items()
                   if sum(map(area, ps)) >= 0.01 * (x1 - x0) * (y1 - y0))
    exag = 0.25  # metres of column per 1,000 visits: a million visits stand 250 m tall
    kinds = [(0, "#86cce8", "free sight"), (1, "#e9b86e", "paid sight"),
             (2, "#b9a0ed", "church · no count, marker only")]
    cols = [(*m(r.lon, r.lat), r.visits, int(r.paid)) for r in sights.itertuples()]
    cols += [(*m(r.lon, r.lat), 0, 2) for r in churches.itertuples()]
    sxy = np.array([c[:2] for c in cols[:5]])
    data = {
        "exaggeration": exag, "footprint": 110,
        "cols": [int(round(x)) for c in cols for x in c],
        "outline": banks, "departments": borders, "water": water, "areas": areas,
        "extent": [round(x) for x in (x0, x1, y0, y1)],
        "clusters": [{"id": k, "color": c} for k, c, _ in kinds],
        "focus": [0, 1],
        "view": [round(x) for x in (*sxy.mean(0), sights["visits"].max() / 1000 * exag / 4)],
    }
    labels = "".join(f'<span class="place-label" translate="no">{html.escape(p)}</span>'
                     for p in [*sights["place"], *churches["place"]])
    legend = "".join(f'<span><span style="color:{c}">■</span> {t}</span>'
                     for _, c, t in [*kinds, (None, water, "the Thames")])
    alt = (f"3-D map of central London: the {len(shown)} boroughs in view, each in a muted tone "
           f"that differs from its neighbours', with the Thames in blue between them. Five columns "
           f"stand at the five sights, as tall as their {year} visits: "
           + "; ".join(f"{r.place} {r.visits / 1e6:.1f} million" for r in sights.itertuples())
           + ". Ten short markers show the cathedrals and churches on Visit London's list.")
    top, paid = sights.iloc[0], sights[sights["paid"]]
    return {
        "data": data, "alt": alt, "year": year, "exaggeration": exag,
        "extra": f'<div class="legend">{legend}</div>{labels}',
        "fallback": f"{year} visits: " + "; ".join(f"{r.place} {r.visits:,}" for r in sights.itertuples()) + ".",
        "sights": sights, "churches": churches, "shown": shown,
        "top": top, "paid": paid,
    }


def tunja(raw: pd.DataFrame) -> dict:
    """Tunja's 28 rows (urban and rural, 2010-2023) and their summary statistics, for the deck's
    explorer (assets/tunja-explorer.js), as in slides/_water.qmd #water-tunja. Labels are the
    deck's, without its emoji."""
    tj = raw[raw["divipola"] == "15001"].sort_values(["year", "zone"])
    assert tj["municipio"].eq("TUNJA").all() and len(tj) == 28
    tvars = [
        ("irca", "IRCA, utility-supplied (0–100 %)", "IRCA (0–100 %)"),
        ("water_coverage_total", "aqueduct coverage, municipality (%)", "aqueduct coverage (%)"),
        ("sewer_coverage_total", "sewer coverage, municipality (%)", "sewer coverage (%)"),
        ("population", "population (people)", "people"),
        ("ipm", "multidimensional poverty IPM, 2018 census (%)", "IPM, 2018 census (%)"),
        ("mdm", "municipal performance MDM (points)", "MDM (points)"),
        ("idf", "fiscal performance, old method (points)", "IDF, old method (points)"),
        ("idf_new", "fiscal performance, new method (points)", "IDF, new method (points)"),
        ("sgp_water_pc", "SGP water, nominal pesos per person", "SGP water (pesos per person)"),
        ("rainfall_mm", "rainfall (mm per year)", "rainfall (mm per year)"),
        ("infant_mortality", "infant mortality (per 1000 births)", "infant deaths per 1000 births"),
        ("saber11_mean", "Saber 11 mean (points)", "Saber 11 mean (points)"),
        ("dropout_rate", "school dropout (%)", "school dropout (%)"),
    ]
    cav = {
        "water_coverage_total": {"note": "hollow = reported as 0, probably “not reported” (data README, caveat 2)"},
        "sewer_coverage_total": {"note": "hollow = reported as 0, probably “not reported” (data README, caveat 2)"},
        "population": {"note": "DANE back-projection to 2017, a newer series from 2018 (data README, caveat 9)",
                       "breaks": [[2018, "new series"]]},
        "infant_mortality": {"note": "modelled to 2016, observed rates from 2017, 2020 from another source: "
                                     "the 2017 drop is not an improvement (data README, caveat 8)",
                             "breaks": [[2017, "new method"], [2020, "2020: other source"], [2021, ""]]},
    }
    piv = {k: tj.pivot(index="year", columns="zone", values=k) for k, _, _ in tvars}

    def lvl(p):
        if ((p.urban == p.rural) | (p.urban.isna() & p.rural.isna())).all():
            return "municipal"
        return "fixed" if all(p[z].dropna().nunique() <= 1 for z in ("urban", "rural")) else "zone"

    def dp(v):
        return next((d for d in range(3) if ((v.dropna() * 10 ** d).round(6) % 1 == 0).all()), 2)

    def stats(v):
        x = v.dropna()
        q = x.quantile([0.25, 0.5, 0.75]) if len(x) else None
        return {"n": int(len(x)), "missing": int(v.isna().sum()),
                "mean": None if x.empty else round(float(x.mean()), 4),
                "sd": None if len(x) < 2 else round(float(x.std()), 4),
                "min": None if x.empty else float(x.min()), "max": None if x.empty else float(x.max()),
                "q1": None if q is None else float(q[0.25]), "median": None if q is None else float(q[0.5]),
                "q3": None if q is None else float(q[0.75])}

    level = {k: lvl(p) for k, p in piv.items()}
    summary = {}
    for key, p in piv.items():
        if level[key] == "municipal":
            summary[key] = {"municipal": stats(p["urban"])}
        elif level[key] == "fixed":
            summary[key] = {z: stats(p[z].drop_duplicates()) for z in ("urban", "rural")}
        else:
            summary[key] = {z: stats(p[z]) for z in ("urban", "rural")}
    data = {
        "years": sorted(int(y) for y in tj["year"].unique()),
        "vars": [{"key": k, "label": lab, "short": sh, "level": level[k], "dp": dp(tj[k]),
                  "suspect": sorted(int(y) for y in tj.loc[tj[k].eq(0), "year"].unique())
                  if k in ("water_coverage_total", "sewer_coverage_total") else [],
                  **cav.get(k, {})} for k, lab, sh in tvars],
        "rows": [{"year": int(r["year"]), "zone": r["zone"],
                  **{k: (None if pd.isna(r[k]) else float(r[k])) for k, _, _ in tvars}}
                 for _, r in tj.iterrows()],
        "summary": summary,
    }
    opts = "".join(f'<option value="{k}">{html.escape(lab)}</option>' for k, lab, _ in tvars)
    block = "\n".join([
        "```{=html}",
        '<div class="tunja">'
        f'<script type="application/json">{json.dumps(data, separators=(",", ":"))}</script>'
        '<div class="tj-bar">'
        '<label>view <select name="view"><option value="table">data</option><option value="summary">summary</option>'
        '<option value="distribution">distribution</option><option value="series">time series</option>'
        '<option value="scatter">scatter</option></select></label>'
        f'<label class="tj-x"><span class="tj-xl">variable</span> <select name="x">{opts}</select></label>'
        f'<label class="tj-y" hidden>y <select name="y">{opts}</select></label>'
        '<label>zone <select name="zone"><option value="both">both zones</option><option value="urban">urban</option>'
        '<option value="rural">rural</option></select></label></div>'
        '<div class="tj-out"></div><p class="tj-note"></p></div>',
        '<script src="../assets/tunja-explorer.js"></script>',
        "```"])
    return {"html": block, "rows": tj, "pivot": piv}


GLYPH = {"o": "●", "s": "■", "^": "▲", "D": "◆", "v": "▼", "P": "✚", "X": "✖", "*": "★"}


def kmeans_toy(cluster_colors: list[str]) -> dict:
    """Synthetic toy points (not the water data) clustered with Lloyd's algorithm written out
    step by step, three random starts (slides/_water.qmd, #water-kmeans)."""
    rng = np.random.default_rng(7)
    toy = np.vstack([rng.normal(m, 0.62, size=(n, 3)) for m, n in
                     (([0, 0, 0], 220), ([3, 0.6, 0.4], 180), ([1.4, 2.8, -0.5], 160))])
    K = 3

    def lloyd(start):
        c = start.copy()
        states = [(c.copy(), None, "drop")]
        while True:
            lab = ((toy[:, None, :] - c[None]) ** 2).sum(-1).argmin(1)
            states.append((c.copy(), lab, "assign"))
            n = np.array([toy[lab == j].mean(0) if (lab == j).any() else c[j] for j in range(K)])
            if np.allclose(n, c):
                return states
            c = n
            states.append((c.copy(), lab, "move"))

    def inertia(c, lab):
        return float(((toy - c[lab]) ** 2).sum())

    runs = [lloyd(toy[np.random.default_rng(sd).choice(len(toy), K, replace=False)]) for sd in (50, 43, 753)]
    assert len({len(r) for r in runs}) == 1
    best = min(inertia(r[-1][0], r[-1][1]) for r in runs)
    assert sum(inertia(r[-1][0], r[-1][1]) > best + 1e-6 for r in runs) == 1
    N = max(len(r) for r in runs)
    mid, span = toy.mean(0), np.abs(toy - toy.mean(0)).max()
    SK = 1000

    def ints(a):
        return np.rint((a - mid) / span * SK).astype(int).ravel().tolist()

    def note(state, last, prev):
        c, lab, kind = state
        if kind == "drop":
            return f"1. drop {K} centres at random points"
        if kind == "move":
            far = np.linalg.norm(c - prev, axis=1).max()
            return f"3. each centre moves to the mean of its points · farthest move {far:.2f}"
        i = inertia(c, lab)
        if not last:
            return f"2. each point joins its nearest centre · inertia {i:.1f}"
        if i <= best + 1e-6:
            return f"4. nothing changes: stable · inertia {i:.1f}, the lowest of the three starts"
        return f"4. stable, but stuck · inertia {i:.1f} vs {best:.1f}: a bad start gives a worse answer"

    data = {
        "k": K, "scale": SK, "colors": list(cluster_colors[:K]), "pts": ints(toy),
        "runs": [{"states": [
            {"c": ints(c), "l": None if lab is None else lab.tolist(),
             "note": note((c, lab, kind), i == len(r) - 1, r[i - 1][0])}
            for i, (c, lab, kind) in enumerate(r)]} for r in runs],
        "states": [{} for _ in range(N)],
    }
    alt = (f"Turning 3-D scatter of {len(toy)} synthetic toy points in three groups. Three centres "
           "drop in, each point takes the colour of its nearest centre, the centres move to their "
           "points' mean, leaving a trail, and the steps repeat until nothing changes.")
    steps = "".join(f'<button data-state="{i}" aria-pressed="false" aria-label="Step {i + 1}">{i + 1}</button>'
                    for i in range(N))
    starts = "".join(f'<button data-cluster="{i}" aria-pressed="false" aria-label="Random start {i + 1}">start {i + 1}</button>'
                     for i in range(len(runs)))
    extra = ('<div class="legend"><span>● point</span><span>◉ centre</span><span>━ its path</span></div>'
             f'<div class="t-picker" role="group" aria-label="Step"><button class="t-play" aria-pressed="true">⏸ fix</button>{steps}</div>'
             f'<div class="c-picker" role="group" aria-label="Random start">{starts}</div>')
    return {"data": data, "alt": alt, "extra": extra, "toy": toy, "runs": runs, "inertia": inertia,
            "best": best, "n_steps": N, "first_note": data["runs"][0]["states"][0]["note"]}


def cloud(res: dict, A) -> dict:
    """The clusters on the first three principal components (slides/_water.qmd, #water-pca-3d)."""
    from sklearn.decomposition import PCA
    from sklearn.neighbors import NearestNeighbors

    clusters = res["clusters"]
    colors = res["profiles"]["color"].to_dict()
    Z = A.zmatrix(res["prepared"])
    pca3 = PCA(n_components=3, random_state=A.SEED).fit(Z)
    xyz = pca3.transform(Z)
    assert np.allclose(xyz[:, :2], clusters[["pc1", "pc2"]].to_numpy())
    var3 = pca3.explained_variance_ratio_
    lab = clusters["cluster"].to_numpy()

    def same(d):
        _, idx = NearestNeighbors(n_neighbors=NEIGHBOURS).fit(xyz[:, :d]).kneighbors()
        return pd.Series((lab[idx] == lab[:, None]).mean(axis=1))

    same2, same3 = same(2), same(3)
    own2, own3 = same2.groupby(lab).mean(), same3.groupby(lab).mean()
    focus = int(own2.idxmin())
    pc3 = pd.Series(pca3.components_[2], index=A.FEATURES)
    top = pc3.abs().nlargest(2).index

    def word(f):
        s = A.SHORT_LABELS.get(f, f)
        return s[0].lower() + s[1:] if s[1:2].islower() else s

    f1, f2 = top
    pc3_text = ("−" if pc3[f1] < 0 else "") + word(f1) + (" + " if pc3[f2] > 0 else " − ") + word(f2)
    means = pd.Series(xyz[:, 2]).groupby(lab).mean()
    others = means.drop(focus)
    side = ("sits below the others" if means[focus] < others.min()
            else "sits above the others" if means[focus] > others.max() else "moves apart")
    data = {
        "scale": 100, "xyz": np.round(xyz * 100).astype(int).ravel().tolist(), "cluster": lab.tolist(),
        "focus": focus,
        "lo": np.percentile(xyz, 1, axis=0).round(2).tolist(),
        "hi": np.percentile(xyz, 99, axis=0).round(2).tolist(),
        "clusters": [{"id": int(c), "color": colors[c], "marker": A.CLUSTER_MARKERS[c - 1]} for c in sorted(colors)],
    }
    legend = "".join(f'<span><span style="color:{c["color"]}">{GLYPH.get(c["marker"], "●")}</span> '
                     f'Cluster {c["id"]}</span>' for c in data["clusters"])
    axes = "".join(f'<span class="axis-label">PC{a + 1} · {var3[a]:.0%}</span>' for a in range(3))
    alt = (f"Turning 3-D scatter of {len(lab):,} zone-years on the first three principal components, "
           f"coloured and shaped by cluster. Face on it is the 2-D picture; turned upright on PC3, "
           f"cluster {focus} {side}.")
    return {"data": data, "alt": alt, "extra": f'<div class="legend">{legend}</div>{axes}',
            "var3": var3, "own2": own2, "own3": own3, "focus": focus, "pc3": pc3, "pc3_top": top,
            "pc3_text": pc3_text, "side": side, "same2": same2, "same3": same3}


def relief(res: dict, raw: pd.DataFrame, A) -> dict:
    """Urban zones as columns at their head towns' altitude, coloured by cluster
    (slides/_water.qmd, #water-relief)."""
    clusters = res["clusters"]
    colors = res["profiles"]["color"].to_dict()
    year = A.LAST_YEAR
    rel = clusters[(clusters["zone"] == "urban") & (clusters["year"] == year)
                   & ~clusters["divipola"].str.startswith("88")]
    filled = int(rel["altitude_m_imputed"].sum())
    rel = rel[rel["altitude_m_imputed"] == 0]

    def part(ring):
        x, y = ring[:, 0], ring[:, 1]
        c = x * np.roll(y, -1) - np.roll(x, -1) * y
        a = c.sum() / 2
        return abs(a), (x + np.roll(x, -1)) @ c / (6 * a), (y + np.roll(y, -1)) @ c / (6 * a)

    centroid, edges, edge_dpts = {}, collections.Counter(), collections.defaultdict(set)
    geo = A.load_geojson(for_plotly=False)
    for feat in geo["features"]:
        code = feat["properties"]["divipola"]
        if code.startswith("88"):
            continue
        gm = feat["geometry"]
        polys = [gm["coordinates"]] if gm["type"] == "Polygon" else gm["coordinates"]
        polys = [[np.asarray(r, dtype=float) for r in p] for p in polys]
        centroid[code] = max((part(p[0]) for p in polys), key=lambda t: t[0])[1:]
        for ring in (r for p in polys for r in p):
            pts = [tuple(v) for v in np.round(ring, 4)]
            for u, v in zip(pts, pts[1:]):
                if u != v:
                    e = (u, v) if u < v else (v, u)
                    edges[e] += 1
                    edge_dpts[e].add(code[:2])
    outline = [e for e, n in edges.items() if n == 1]
    dpt_edges = [e for e, n in edges.items() if n > 1 and len(edge_dpts[e]) > 1]
    ll = np.array([p for e in outline for p in e])
    lon0, lat0 = (ll.min(0) + ll.max(0)) / 2
    kx, ky = 111.32 * np.cos(np.radians(lat0)), 110.57

    def km(lon, lat):
        return (lon - lon0) * kx, (lat - lat0) * ky

    def segments(es, step):
        seen = set()
        for u, v in es:
            a, b = (tuple(np.round(np.array(p) / step).astype(int)) for p in (u, v))
            if a != b:
                seen.add((a, b) if a < b else (b, a))
        return [round(c) for s in sorted(seen) for p in s for c in km(p[0] * step, p[1] * step)]

    exag = 50
    xy = np.array([km(*centroid[c]) for c in rel["divipola"]])
    alt_med = rel.groupby("cluster")["altitude_m"].median()
    high, low = int(alt_med.idxmax()), int(alt_med.idxmin())
    hi_mask = rel["cluster"].to_numpy() == high
    hi_cols = xy[hi_mask]
    hi_i = np.argmin(((hi_cols - np.median(hi_cols, axis=0)) ** 2).sum(axis=1))
    hi_xy, hi_alt = hi_cols[hi_i], rel["altitude_m"].to_numpy()[hi_mask][hi_i]
    ext = np.array([km(*p) for p in ll])
    data = {
        "exaggeration": exag,
        "cols": [int(v) for x, y, a, k in zip(xy[:, 0], xy[:, 1], rel["altitude_m"], rel["cluster"])
                 for v in (round(x), round(y), round(a), k)],
        "outline": segments(outline, 0.03), "departments": segments(dpt_edges, 0.05),
        "extent": [round(v) for v in (ext[:, 0].min(), ext[:, 0].max(), ext[:, 1].min(), ext[:, 1].max())],
        "clusters": [{"id": int(c), "color": colors[c]} for c in sorted(colors)],
        "focus": [high, low],
        "view": [round(hi_xy[0]), round(hi_xy[1]), round(hi_alt / 1000 * exag / 2)],
    }
    towns = raw[(raw["zone"] == "urban") & (raw["year"] == year)
                & (raw["entity_type"] == "municipality")].set_index("divipola")
    col_of = rel.set_index("divipola")[["altitude_m", "cluster"]]
    capitals = towns[(towns["department_capital"] == 1) & towns.index.isin(col_of.index)]
    city_top = list(capitals["population"].nlargest(10).index)
    codes = city_top[:1] + ["15001"] + [c for c in city_top[1:] if c != "15001"]
    short = {"11001": "Bogotá", "76001": "Cali", "13001": "Cartagena", "54001": "Cúcuta"}

    def city(c):
        return short.get(c, towns.loc[c, "municipio"].title())

    data["cities"] = [int(v) for c in codes for v in (*(round(t) for t in km(*centroid[c])),
                                                      round(col_of.loc[c, "altitude_m"]), col_of.loc[c, "cluster"])]
    labels = "".join(f'<span class="place-label" translate="no">{html.escape(city(c))}</span>' for c in codes)
    medians = {c: (f"{alt_med[c]:,.0f} m" if c in alt_med else f"no {year} urban zones") for c in sorted(colors)}
    legend = "".join(f'<span><span style="color:{colors[c]}">■</span> Cluster {c} · {m}</span>'
                     for c, m in medians.items())
    alt = (f"3-D map of mainland Colombia with one column for each of the {len(rel)} clustered urban "
           f"zones in {year}, at its municipality's centroid, as tall as its head town's altitude and "
           f"coloured by cluster. Cluster {high}'s columns are the tallest (median {alt_med[high]:,.0f} m); "
           f"cluster {low}'s are the shortest ({alt_med[low]:,.0f} m). Labels name the ten most populous "
           "department capitals and Tunja.")
    region_top = {c: rel.loc[rel["cluster"] == c, "region"].value_counts(normalize=True) for c in (high, low)}
    return {"data": data, "alt": alt, "extra": f'<div class="legend">{legend}</div>{labels}',
            "fallback": f"Median head-town altitude, {year} urban zones: "
                        + "; ".join(f"cluster {c}: {m}" for c, m in medians.items()) + ".",
            "year": year, "n": len(rel), "filled": filled, "exag": exag, "alt_med": alt_med,
            "high": high, "low": low, "region_top": region_top,
            "cities": [city(c) for c in codes], "tunja_alt": col_of.loc["15001", "altitude_m"]}
