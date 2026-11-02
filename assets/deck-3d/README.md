# Deck 3-D slides

The workshop deck's three three.js slides:

- `cloud.js` turns the cluster cloud on `#water-pca-3d` (Part 2): zone-years on the first
  three principal components.
- `relief.js` raises the clustered urban zones as columns at their head towns' altitude
  on `#water-relief` (Part 2), and names the cities the deck cell picks, each on the side
  of its column where it covers no other label. Part 1's `#london-map` reuses it in
  metres: the five sights as columns as tall as their visits, Visit London's churches as
  short markers, and the boroughs as muted fills on a blue water plane, so the Thames
  shows blue between them (`data.footprint` sets its wider columns; `data.areas` and
  `data.water` the fills).

- `meta.js` and `meta-*.js` draw Part 2's five optional slides (`#water-meta-terrain`, `-hulls`,
  `-stack`, `-orbits`, `-voronoi`): the outcomes the clustering never used (Saber 11, infant
  mortality, school dropout) per municipality and year, on the clusters the deck already chose
  (k fixed). A scene's state is a year (2017, 2019, 2022) and its focus a cluster (0 = all). All
  five read one shared JSON (`data-source`, embedded in the first of them, so keep it first).
  The stage owns the state: `.t-picker [data-state]` year buttons, a `.t-play` button (the
  years autoplay until fixed), `.c-picker [data-cluster]` buttons and fragments `data-step`
  (→ one year on) all go through it. A scene's `setState(i)` and `setCluster(c)` set targets
  and `animate(dt)` eases or springs towards them (`dt` = Infinity finishes at once, for
  reduced motion and PDF export). Hulls use three.js's `ConvexGeometry` (examples/jsm, bundled).

`stage.js` runs a 3-D slide. Fragments with `data-view` set the view, the reader can drag
to turn and scroll to zoom, rendering stops while the slide is not shown, and
`prefers-reduced-motion` turns animation off. Without WebGL the slide shows a short
note; a PDF export (`?print-pdf`) gets one still frame of the last view. `main.js` starts
a stage for each `.deck-3d` element by its `data-scene`. The deck cells compute every
point, number and border and write them into the slides as JSON. The scripts only draw.

The deck loads the prebuilt bundle `../deck-3d.min.js` once, from the London map's
cell (the first 3-D slide). Quarto embeds it in `docs/index.html`, so rendering needs neither npm nor a
network. After editing a script here, rebuild the bundle and render the deck again:

```bash
cd assets/deck-3d
npm ci
npm run build
```

Versions are pinned in `package.json` and `package-lock.json` (three 0.187.0, esbuild
0.28.2; built 2026-10-30 with Node 23.11). three.js is MIT-licensed, and its notice is kept
at the end of the bundle. `node_modules/` is gitignored.
