// Cluster rivers (slides/_water.qmd, #water-meta-rivers): one tube from each of the two k = 2
// clusters' means to each cluster mean of the picked clustering, as wide as the number of
// municipalities that make the trip. When the picked k changes, the tubes' control points
// ease to their new places and the widths to their new flows. The deck cell computes the
// means and the counts.
import {
  BufferAttribute, CatmullRomCurve3, Color, Mesh, MeshLambertMaterial, TubeGeometry, Vector3,
} from "three";
import { chase, ease, frame, lights, palette, wx, wz, world } from "./meta.js";

const SEGMENTS = 40, SIDES = 8, MAX_RADIUS = 0.06, SPREAD = 3, LIFT = 2.4;
// Cluster means lie close together, so their places are spread SPREAD times about the average
// of the k = 2 means (and their heights lifted); the slide says so.

export const metaRivers = {
  views: () => ({
    flat: { rx: 0.62, ry: -0.5, zoom: 0.95, spin: 0.04, focus: false },
  }),

  build(group, data, el) {
    const colors = palette(data), from = data.states[0].centroids;
    const mid = [from.reduce((a, c) => a + c.u, 0) / from.length, from.reduce((a, c) => a + c.v, 0) / from.length];
    const centre = (c) => [
      wx(mid[0] + (c.u - mid[0]) * SPREAD), c.w * LIFT, wz(mid[1] + (c.v - mid[1]) * SPREAD)];
    const total = data.u.length;
    // One tube per (source cluster a, target cluster b); 5 control points each.
    const tubes = [];
    from.forEach((_, a) => colors.forEach((_, b) => {
      const mesh = new Mesh(undefined, new MeshLambertMaterial({ vertexColors: true }));
      mesh.visible = false;
      group.add(mesh);
      tubes.push({ a, b, mesh, ctrl: new Float32Array(15), ctrlT: new Float32Array(15), r: [0], rT: [0] });
    }));
    lights(group);

    function shape(tube) {
      const pts = [];
      for (let i = 0; i < 5; i++) pts.push(new Vector3(...tube.ctrl.slice(i * 3, i * 3 + 3)));
      const r = tube.r[0];
      tube.mesh.visible = r > 0.004;
      if (!tube.mesh.visible) return;
      tube.mesh.geometry?.dispose();
      const geometry = new TubeGeometry(new CatmullRomCurve3(pts), SEGMENTS, r, SIDES);
      // From the source cluster's colour to the target's along the tube.
      const col = new Float32Array(geometry.attributes.position.count * 3);
      const c0 = colors[tube.a], c1 = colors[tube.b], c = new Color();
      for (let i = 0; i < col.length / 3; i++) {
        c.copy(c0).lerp(c1, Math.floor(i / (SIDES + 1)) / SEGMENTS);
        col.set([c.r, c.g, c.b], i * 3);
      }
      geometry.setAttribute("color", new BufferAttribute(col, 3));
      tube.mesh.geometry = geometry;
    }

    return world({
      centre: [0, 0.8, 0],
      labels: frame(group, el),
      setState(i) {
        const to = data.states[i].centroids;
        tubes.forEach((tube) => {
          const flow = i === 0 ? 0 : (data.flows[i][tube.a]?.[tube.b] ?? 0);
          const a = centre(from[tube.a]), b = to[tube.b] ? centre(to[tube.b]) : a;
          // Winding: the middle control points swing to opposite sides of the straight line.
          const dx = b[0] - a[0], dz = b[2] - a[2], len = Math.hypot(dx, dz) || 1;
          const side = (tube.a ? 1 : -1) * 0.25 * Math.min(1, len), up = 0.15;
          [0, 0.25, 0.5, 0.75, 1].forEach((f, j) => {
            const bend = Math.sin(f * Math.PI) * (j === 2 ? -side : side);
            tube.ctrlT.set([
              a[0] + dx * f + (-dz / len) * bend,
              a[1] + (b[1] - a[1]) * f + Math.sin(f * Math.PI) * up,
              a[2] + dz * f + (dx / len) * bend,
            ], j * 3);
          });
          tube.rT[0] = flow ? MAX_RADIUS * Math.sqrt(flow / total) * 1.4 : 0;
        });
        if (i === 0) tubes.forEach((tube) => { tube.rT[0] = 0; });
      },
      animate(dt) {
        const k = ease(dt, 3);
        let moving = false;
        tubes.forEach((tube) => {
          // A tube coming from nothing starts as a point on its source.
          if (tube.r[0] === 0 && tube.rT[0] > 0) {
            for (let j = 0; j < 5; j++) tube.ctrl.set(tube.ctrlT.slice(0, 3), j * 3);
          }
          moving = chase(tube.ctrl, tube.ctrlT, k) | chase(tube.r, tube.rT, k) | moving;
          shape(tube);
        });
        return Boolean(moving);
      },
    });
  },
};
