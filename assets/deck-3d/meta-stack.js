// Meta-feature stack (slides/_water.qmd, #water-meta-stack): one Saber 11 x infant-mortality
// plane per clustering (k = 2 to 5), stacked upward. Picking a larger k lifts the next plane
// into place; lines join the same municipality on adjacent planes, bright where its cluster
// changed. Municipalities sit pulled towards their cluster's mean on each plane. The deck
// cell computes the sample of municipalities and every label.
import {
  BufferAttribute, BufferGeometry, DoubleSide, Group, LineBasicMaterial, LineLoop, LineSegments,
  Mesh, MeshBasicMaterial, PlaneGeometry, Points, PointsMaterial, Vector3,
} from "three";
import { chase, ease, palette, wx, wz, world } from "./meta.js";

const GAP = 0.5;

export const metaStack = {
  views: () => ({
    flat: { rx: 0.42, ry: -0.6, zoom: 1.0, spin: 0.04, focus: false },
  }),

  build(group, data, el) {
    const colors = palette(data), n = data.u.length, layers = data.states.length;
    const planes = data.states.map((state, s) => {
      const pos = new Float32Array(n * 3), col = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) {
        const c = state.centroids[data.labels[s][i] - 1], col3 = colors[data.labels[s][i] - 1];
        const x = wx(data.u[i] / data.scale), z = wz(data.v[i] / data.scale);
        pos.set([x + (wx(c.u) - x) * data.pull, 0, z + (wz(c.v) - z) * data.pull], i * 3);
        col.set([col3.r, col3.g, col3.b], i * 3);
      }
      const geometry = new BufferGeometry();
      geometry.setAttribute("position", new BufferAttribute(pos, 3));
      geometry.setAttribute("color", new BufferAttribute(col, 3));
      const dots = new Points(geometry, new PointsMaterial({
        size: 0.06, vertexColors: true, transparent: true, depthWrite: false }));
      const sheet = new Mesh(new PlaneGeometry(2, 2).rotateX(-Math.PI / 2), new MeshBasicMaterial({
        color: 0x2b3038, transparent: true, opacity: 0.35, side: DoubleSide, depthWrite: false }));
      const edge = new LineLoop(
        new BufferGeometry().setFromPoints([[-1, 0, -1], [1, 0, -1], [1, 0, 1], [-1, 0, 1]]
          .map((p) => new Vector3(...p))),
        new LineBasicMaterial({ color: 0xb8c2cc, transparent: true }));
      const holder = new Group();
      holder.add(sheet, edge, dots);
      group.add(holder);
      return { holder, sheet, edge, dots, pos };
    });

    // Links between adjacent planes for the sampled municipalities.
    const links = [];
    for (let s = 0; s + 1 < layers; s++) {
      const changed = [], same = [];
      data.sample.forEach((i) => {
        (data.labels[s][i] === data.labels[s + 1][i] ? same : changed).push(i);
      });
      [[same, 0x8a929c, 0.28], [changed, 0xfff2b0, 0.95]].forEach(([ids, color, opacity]) => {
        const geometry = new BufferGeometry();
        geometry.setAttribute("position", new BufferAttribute(new Float32Array(ids.length * 6), 3));
        const material = new LineBasicMaterial({ color, transparent: true, opacity, depthWrite: false });
        const lines = new LineSegments(geometry, material);
        lines.frustumCulled = false;
        group.add(lines);
        links.push({ s, ids, geometry, material, opacity, lines });
      });
    }

    const y = new Float32Array(layers), yT = new Float32Array(layers);
    const alpha = new Float32Array(layers), alphaT = new Float32Array(layers);
    function update() {
      planes.forEach((p, s) => {
        p.holder.position.y = y[s];
        p.dots.material.opacity = alpha[s];
        p.sheet.material.opacity = 0.35 * alpha[s];
        p.edge.material.opacity = alpha[s];
        p.holder.visible = alpha[s] > 0.01;
      });
      links.forEach((l) => {
        const a = planes[l.s], b = planes[l.s + 1], arr = l.geometry.attributes.position.array;
        l.ids.forEach((i, j) => {
          arr.set([a.pos[i * 3], y[l.s], a.pos[i * 3 + 2], b.pos[i * 3], y[l.s + 1], b.pos[i * 3 + 2]], j * 6);
        });
        l.geometry.attributes.position.needsUpdate = true;
        l.material.opacity = l.opacity * Math.min(alpha[l.s], alpha[l.s + 1]);
        l.lines.visible = l.material.opacity > 0.01;
      });
    }

    // Axis labels beside the bottom plane: x and z as on the other slides, and the stack.
    const labels = [...el.querySelectorAll(".axis-label")].map((label, i) => ({
      label, to: new Vector3(...[[0, 0, 1.3], [1.32, 0, 0], [-1, layers * GAP - GAP + 0.25, -1]][i]) }));

    return world({
      centre: [0, (GAP * (layers - 1)) / 2, 0],
      labels,
      setState(i) {
        for (let s = 0; s < layers; s++) {
          // Planes above the picked one wait stacked on the first, hidden.
          yT[s] = s <= i ? s * GAP : 0;
          alphaT[s] = s <= i ? 1 : 0;
        }
      },
      animate(dt) {
        const k = ease(dt, 3.5);
        const moving = chase(y, yT, k) | chase(alpha, alphaT, k);
        update();
        return Boolean(moving);
      },
    });
  },
};
