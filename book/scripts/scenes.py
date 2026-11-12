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
