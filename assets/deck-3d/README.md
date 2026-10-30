# Deck 3-D slides

The workshop deck's two three.js slides in Part 2:

- `cloud.js` turns the cluster cloud on `#water-pca-3d`: zone-years on the first three
  principal components.
- `relief.js` raises the clustered urban zones as columns at their head towns' altitude
  on `#water-relief`.

`stage.js` runs a 3-D slide. Fragments with `data-view` set the view, the reader can drag
to turn and scroll to zoom, rendering stops while the slide is not shown, and
`prefers-reduced-motion` turns animation off. Without WebGL the slide shows a short
note; a PDF export (`?print-pdf`) gets one still frame of the last view. `main.js` starts
a stage for each `.deck-3d` element by its `data-scene`. The deck cells compute every
point, number and border and write them into the slides as JSON. The scripts only draw.

The deck loads the prebuilt bundle `../deck-3d.min.js` once, from the cluster cloud's
cell. Quarto embeds it in `docs/index.html`, so rendering needs neither npm nor a
network. After editing a script here, rebuild the bundle and render the deck again:

```bash
cd assets/deck-3d
npm ci
npm run build
```

Versions are pinned in `package.json` and `package-lock.json` (three 0.187.0, esbuild
0.28.2; built 2026-10-30 with Node 23.11). three.js is MIT-licensed, and its notice is kept
at the end of the bundle. `node_modules/` is gitignored.
