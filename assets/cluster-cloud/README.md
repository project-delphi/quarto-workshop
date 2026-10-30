# Cluster cloud

`cloud.js` draws the turning 3-D cluster cloud on the workshop deck's `#water-pca-3d`
slide with [three.js](https://threejs.org/) (MIT licence; its notice is kept at the end of
the bundle). The deck cell computes the points and writes them into the slide as JSON. The
script only draws them: it computes no results.

The deck loads the prebuilt bundle `../cluster-cloud.min.js`, which Quarto embeds in
`docs/index.html`, so rendering needs neither npm nor a network. After editing `cloud.js`,
rebuild the bundle and render the deck again:

```bash
cd assets/cluster-cloud
npm ci
npm run build
```

Versions are pinned in `package.json` and `package-lock.json` (three 0.187.0, esbuild
0.28.2; built 2026-10-30 with Node 23.11). `node_modules/` is gitignored.

Behaviour: fragments with `data-cloud="turn"` or `data-cloud="pc3"` on the same slide set
the view. Drag turns the cloud and the scroll wheel zooms. With `prefers-reduced-motion`,
views change without animation and the cloud does not spin. Rendering stops while the slide
is not shown. Without WebGL, the slide shows a short note instead.
