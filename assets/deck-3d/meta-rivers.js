// Cluster rivers (slides/_water.qmd, #water-meta-rivers): one tube from each cluster's mean in
// the first year to each cluster's mean in the picked year, as wide as the number of
// municipalities that made that move. When the year changes, the tubes' control points ease
// to their new places and the widths to their new flows; with a cluster in focus only the
// tubes into or out of it show. The deck cell computes the means and the counts.
import {
  BufferAttribute, CatmullRomCurve3, Color, Mesh, MeshLambertMaterial, TubeGeometry, Vector3,
} from "three";
import { chase, ease, frame, lights, palette, wx, wz, world } from "./meta.js";

const SEGMENTS = 40, SIDES = 8, MAX_RADIUS = 0.06, SPREAD = 3, LIFT = 2.4;

export const metaRivers = {
  views: () => ({
    flat: { rx: 0.62, ry: -0.5, zoom: 0.95, spin: 0.04, focus: false },
  }),

  build(group, data, el) {
    const colors = palette(data), from = data.states[0].centroids, k = colors.length;
    // Cluster means lie close together, so their places are spread SPREAD times about the
    // average of the first year's means (and their heights lifted); the slide says so.
    const mid = [from.reduce((a, c) => a + c.u, 0) / k, from.reduce((a, c) => a + c.v, 0) / k];
    const centre = (c) => [
      wx(mid[0] + (c.u - mid[0]) * SPREAD), c.w * LIFT, wz(mid[1] + (c.v - mid[1]) * SPREAD)];
    const total = data.u[0].length;
    // One tube per (cluster a in the first year, cluster b in the picked year); 5 control points.
    const tubes = [];
    for (let a = 0; a < k; a++) {
      for (let b = 0; b < k; b++) {
        const mesh = new Mesh(undefined, new MeshLambertMaterial({ vertexColors: true }));
        mesh.visible = false;
        group.add(mesh);
        // Colours run from the source cluster's to the target's: they never change.
        const colour = new Float32Array((SEGMENTS + 1) * (SIDES + 1) * 3), c = new Color();
        for (let i = 0; i < colour.length / 3; i++) {
          c.copy(colors[a]).lerp(colors[b], Math.floor(i / (SIDES + 1)) / SEGMENTS);
          colour.set([c.r, c.g, c.b], i * 3);
        }
        tubes.push({ a, b, mesh, colour, ctrl: new Float32Array(15), ctrlT: new Float32Array(15), r: [0], rT: [0], drawn: false });
      }
    }
    lights(group);

    function shape(tube) {
      const r = tube.r[0];
      tube.mesh.visible = r > 0.004;
      if (!tube.mesh.visible) return;
      const pts = [];
      for (let i = 0; i < 5; i++) pts.push(new Vector3(...tube.ctrl.slice(i * 3, i * 3 + 3)));
      tube.mesh.geometry?.dispose();
      const geometry = new TubeGeometry(new CatmullRomCurve3(pts), SEGMENTS, r, SIDES);
      geometry.setAttribute("color", new BufferAttribute(tube.colour, 3));
      tube.mesh.geometry = geometry;
    }

    let state = 0, focus = 0;
    function retarget() {
      const to = data.states[state].centroids;
      tubes.forEach((tube) => {
        const flow = state === 0 ? 0 : data.flows[state][tube.a][tube.b];
        const shown = !focus || tube.a + 1 === focus || tube.b + 1 === focus;
        const a = centre(from[tube.a]), b = to[tube.b].n ? centre(to[tube.b]) : a;
        // Winding: the middle control points swing to opposite sides of the straight line.
        const dx = b[0] - a[0], dz = b[2] - a[2], len = Math.hypot(dx, dz) || 1;
        const side = (tube.a % 2 ? 1 : -1) * 0.25 * Math.min(1, len), up = 0.15;
        [0, 0.25, 0.5, 0.75, 1].forEach((f, j) => {
          const bend = Math.sin(f * Math.PI) * (j === 2 ? -side : side);
          tube.ctrlT.set([
            a[0] + dx * f + (-dz / len) * bend,
            a[1] + (b[1] - a[1]) * f + Math.sin(f * Math.PI) * up,
            a[2] + dz * f + (dx / len) * bend,
          ], j * 3);
        });
        tube.rT[0] = flow && shown ? MAX_RADIUS * Math.sqrt(flow / total) * 1.4 : 0;
      });
    }

    return world({
      centre: [0, 0.8, 0],
      labels: frame(group, el),
      setState(i) { state = i; retarget(); },
      setCluster(c) { focus = c; retarget(); },
      animate(dt) {
        const ke = ease(dt, 3);
        let moving = false;
        tubes.forEach((tube) => {
          // A tube coming from nothing starts as a point on its source.
          if (tube.r[0] === 0 && tube.rT[0] > 0) {
            for (let j = 0; j < 5; j++) tube.ctrl.set(tube.ctrlT.slice(0, 3), j * 3);
          }
          const m = chase(tube.ctrl, tube.ctrlT, ke) | chase(tube.r, tube.rT, ke);
          // Tubes at rest keep the geometry they have; only moving ones (and the frame they
          // settle on) are rebuilt.
          if (m || tube.drawn) shape(tube);
          tube.drawn = Boolean(m);
          moving = moving || Boolean(m);
        });
        return moving;
      },
    });
  },
};
