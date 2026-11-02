// Morphing scatter with convex hulls (slides/_water.qmd, #water-meta-hulls): municipalities
// on Saber 11 (x), dropout (y) and infant mortality (z). Under each clustering the points
// ease towards their cluster's mean and take its colour, and a glowing hull wraps each
// cluster's core (the 85 % nearest its mean) and reshapes with the points.
import { DoubleSide, EdgesGeometry, LineBasicMaterial, LineSegments, Mesh, MeshBasicMaterial, Vector3 } from "three";
import { ConvexGeometry } from "three/examples/jsm/geometries/ConvexGeometry.js";
import { ease, frame, lights, morphPoints, palette, pulled, world } from "./meta.js";

export const metaHulls = {
  views: () => ({
    flat: { rx: 0.5, ry: -0.7, zoom: 1.45, spin: 0.05, focus: false },
  }),

  build(group, data, el) {
    const colors = palette(data), n = data.u.length;
    const cloud = morphPoints(group, data, (s, i) => pulled(data, s, i, data.pull), { size: 0.045 });
    const hulls = colors.map((color) => {
      const fill = new Mesh(undefined, new MeshBasicMaterial({
        color, transparent: true, opacity: 0.16, side: DoubleSide, depthWrite: false }));
      const edge = new LineSegments(undefined, new LineBasicMaterial({
        color, transparent: true, opacity: 0.55 }));
      fill.visible = edge.visible = false;
      group.add(fill, edge);
      return { fill, edge };
    });
    let state = 0, grow = 1;

    function rebuild() {
      const lab = data.labels[state], core = data.states[state].core, p = cloud.pos;
      hulls.forEach(({ fill, edge }, c) => {
        const pts = [];
        for (let i = 0; i < n; i++) {
          if (lab[i] === c + 1 && core[i]) pts.push(new Vector3(p[i * 3], p[i * 3 + 1], p[i * 3 + 2]));
        }
        fill.geometry?.dispose();
        edge.geometry?.dispose();
        fill.visible = edge.visible = pts.length >= 4;
        if (!fill.visible) return;
        fill.geometry = new ConvexGeometry(pts);
        edge.geometry = new EdgesGeometry(fill.geometry, 20);
        fill.material.opacity = 0.16 * grow;
        edge.material.opacity = 0.55 * grow;
      });
    }
    lights(group);

    return world({
      labels: frame(group, el),
      setState(i) {
        state = i;
        grow = 0;
        cloud.set(i);
      },
      animate(dt) {
        const k = ease(dt, 3);
        grow += (1 - grow) * k;
        const moving = cloud.step(k) || grow < 0.999;
        if (!moving) grow = 1;
        rebuild();
        return moving;
      },
    });
  },
};
