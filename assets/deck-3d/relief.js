// Relief view (slides/_water.qmd, #water-relief): one column per clustered urban zone, at
// its municipality's centroid, as tall as its head town's altitude (exaggerated) and
// coloured by cluster, standing on the national and department borders. The deck cell
// computes the columns, borders and city labels in km; this scene only draws them
// (stage.js). Altitude is the scene's y axis, so the stage turns the map about its
// vertical; north is -z.
import {
  BoxGeometry, BufferAttribute, BufferGeometry, DirectionalLight, HemisphereLight,
  InstancedMesh, LineBasicMaterial, LineSegments, MeshLambertMaterial, Object3D, Vector3,
} from "three";

// Lays out the city labels on screen for one frame (stage.js calls it with each label's
// point): above, beside or below the point (data-side, styled in theme.scss) so that no
// label covers another label or another labelled city. A search over the four sides keeps
// the cheapest layout. A label keeps its side if it can, so labels do not jump while the
// map turns; otherwise above is cheapest, then the side facing away from the cities'
// middle, the other side, and below. Where no side fits, a label hides, the last-listed
// city first (the deck cell lists them by priority).
function arrangeLabels(cities, spots, w, h) {
  const gap = parseFloat(getComputedStyle(cities[0].label).fontSize) * 0.25;
  cities.forEach((c) => { c.size ??= [c.label.offsetWidth, c.label.offsetHeight]; });
  const on = spots.map(([x, y]) => x >= 0 && x <= w && y >= 0 && y <= h);
  const midX = spots.reduce((sum, [x]) => sum + x, 0) / spots.length;
  const options = cities.map((c, i) => {
    if (!on[i]) return [[null, null, 0]]; // off the canvas: stage.js hides it anyway
    const [x, y] = spots[i];
    const [lw, lh] = c.size;
    const left = [x - gap - lw, x - gap, y - lh / 2, y + lh / 2];
    const right = [x + gap, x + gap + lw, y - lh / 2, y + lh / 2];
    const boxes = [
      ["above", [x - lw / 2, x + lw / 2, y - gap - lh, y - gap]],
      ...(x < midX ? [["left", left], ["right", right]] : [["right", right], ["left", left]]),
      ["below", [x - lw / 2, x + lw / 2, y + gap, y + gap + lh]],
    ];
    return boxes
      .map(([side, b], rank) => [side, b, side === c.side ? 0 : c.side ? 4 + rank : rank])
      .filter(([, b]) => !spots.some(([px, py], j) => j !== i && on[j]
        && px > b[0] && px < b[1] && py > b[2] && py < b[3]))
      .sort((a, b) => a[2] - b[2])
      .concat([[null, null, 100 + cities.length - i]]); // hidden
  });
  const overlap = (a, b) => a[0] < b[1] && b[0] < a[1] && a[2] < b[3] && b[2] < a[3];
  let best = null, bestCost = Infinity, budget = 20000; // a cap on the search per frame
  const chosen = [];
  (function search(i, cost) {
    if (cost >= bestCost || (best && --budget < 0)) return;
    if (i === cities.length) {
      best = chosen.map(([side]) => side);
      bestCost = cost;
      return;
    }
    for (const [side, b, price] of options[i]) {
      if (b && chosen.some(([, other]) => other && overlap(b, other))) continue;
      chosen.push([side, b]);
      search(i + 1, cost + price);
      chosen.pop();
    }
  })(0, 0);
  cities.forEach((c, i) => {
    if (!on[i]) return;
    c.hidden = !best[i];
    if (best[i]) c.side = c.label.dataset.side = best[i];
  });
}

export const relief = {
  views: (data) => ({
    flat: { rx: Math.PI / 2, ry: 0, zoom: 1, spin: 0, focus: false },     // the map from above
    tilt: { rx: Math.PI / 2 - 1.0, ry: 0, zoom: 1.4, spin: 0, focus: false }, // the columns rise
    // Into the highlands: turn about the highest cluster's middle column, closer and slowly.
    focus: { rx: 0.45, ry: 0.5, zoom: 2.2, spin: 0.06, focus: true,
             centre: [data.view[0], data.view[2], -data.view[1]] },
  }),

  build(group, data, el) {
    const [x0, x1, y0, y1] = data.extent;
    const half = Math.max(x1 - x0, y1 - y0) / 2;
    const width = half * 0.014; // column footprint, km
    const box = new BoxGeometry(1, 1, 1).translate(0, 0.5, 0); // stands on the map
    const top = (altitude) => Math.max((altitude / 1000) * data.exaggeration, width * 0.3);
    const place = new Object3D();
    const materials = data.clusters.map((c) => {
      const rows = [];
      for (let i = 0; i < data.cols.length; i += 4) if (data.cols[i + 3] === c.id) rows.push(i);
      const material = new MeshLambertMaterial({ color: c.color });
      material.userData.id = c.id;
      const mesh = new InstancedMesh(box, material, rows.length);
      rows.forEach((i, j) => {
        place.position.set(data.cols[i], 0, -data.cols[i + 1]);
        place.scale.set(width, top(data.cols[i + 2]), width);
        place.updateMatrix();
        mesh.setMatrixAt(j, place.matrix);
      });
      group.add(mesh);
      return material;
    });

    const lines = (flat, opacity) => {
      const pos = new Float32Array((flat.length / 2) * 3);
      for (let i = 0, j = 0; i < flat.length; i += 2, j += 3) {
        pos[j] = flat[i];
        pos[j + 2] = -flat[i + 1];
      }
      const geometry = new BufferGeometry();
      geometry.setAttribute("position", new BufferAttribute(pos, 3));
      group.add(new LineSegments(geometry,
        new LineBasicMaterial({ color: 0xb8c2cc, transparent: true, opacity })));
    };
    lines(data.outline, 0.8);
    lines(data.departments, 0.25);

    // Sky from above and sun from the north-west; both turn with the map.
    const sky = new HemisphereLight(0xffffff, 0x3a3a3a, 1.8);
    const sun = new DirectionalLight(0xffffff, 1.6);
    sun.position.set((x0 + x1) / 2 - half, half * 2, -(y1 + half));
    sun.target.position.set((x0 + x1) / 2, 0, -(y0 + y1) / 2);
    group.add(sky, sun, sun.target);

    // The .place-label elements, in data.cities order (x, y, altitude, cluster), each at the
    // top of its city's column; they dim with their cluster in the focus view.
    const cities = [...el.querySelectorAll(".place-label")].map((label, k) => {
      const [x, y, altitude, cluster] = data.cities.slice(k * 4, k * 4 + 4);
      return { label, to: new Vector3(x, top(altitude), -y), cluster, weight: 1 };
    });

    return {
      centre: [(x0 + x1) / 2, 0, -(y0 + y1) / 2],
      half,
      aspect: (x1 - x0) / (y1 - y0),
      labels: cities,
      arrange: (spots, w, h) => cities.length && arrangeLabels(cities, spots, w, h),
      focus(t) {
        // Names fade less than columns: they stay readable for orientation.
        cities.forEach((c) => { c.weight = data.focus.includes(c.cluster) ? 1 : 1 - 0.45 * t; });
        materials.forEach((m) => {
          m.opacity = data.focus.includes(m.userData.id) ? 1 : 1 - 0.8 * t;
          // Opaque columns draw in the opaque pass, so faded ones cannot cover them;
          // switching passes recompiles the shader (opaque ones force alpha to 1).
          if (m.transparent !== m.opacity < 1) {
            m.transparent = m.opacity < 1;
            m.depthWrite = !m.transparent;
            m.needsUpdate = true;
          }
        });
      },
    };
  },
};
