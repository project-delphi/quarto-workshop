// Voronoi extrusion (slides/_water.qmd, #water-meta-voronoi): the Saber 11 x infant-mortality
// plane is split into the cells nearest each cluster's mean, and each cell is raised to its
// cluster's mean school dropout. A new clustering moves the borders and re-extrudes the
// cells. The deck cell computes which cluster owns each square of a 36 x 36 grid and the
// means; the squares ease in height and colour, so borders slide.
import {
  BoxGeometry, Color, InstancedMesh, Matrix4, Mesh, MeshLambertMaterial, SphereGeometry,
} from "three";
import { chase, ease, frame, lights, palette, wx, wz, world } from "./meta.js";

const LIFT = 2.4, BASE = 0.02; // dropout (0-1) to height, exaggerated as the slide says

export const metaVoronoi = {
  views: () => ({
    flat: { rx: 0.8, ry: -0.5, zoom: 1.05, spin: 0.04, focus: false },
  }),

  build(group, data, el) {
    const v = data.voronoi.g, n = v * v, colors = palette(data), size = 2 / v;
    const cells = new InstancedMesh(new BoxGeometry(1, 1, 1), new MeshLambertMaterial(), n);
    group.add(cells);
    const seeds = colors.map((color) => {
      const m = new Mesh(new SphereGeometry(0.045, 16, 12), new MeshLambertMaterial({
        color: 0xffffff, emissive: color, emissiveIntensity: 0.9 }));
      group.add(m);
      return m;
    });
    lights(group);
    const h = new Float32Array(n), hT = new Float32Array(n);
    const rgb = new Float32Array(n * 3), rgbT = new Float32Array(n * 3);
    const seedPos = new Float32Array(colors.length * 4), seedT = new Float32Array(seedPos.length);
    const m4 = new Matrix4(), tint = new Color();

    function update() {
      for (let i = 0; i < v; i++) {
        for (let j = 0; j < v; j++) {
          const idx = i * v + j, height = BASE + h[idx] * LIFT;
          m4.makeScale(size * 0.97, height, size * 0.97);
          m4.setPosition(-1 + size * (j + 0.5), height / 2, -1 + size * (i + 0.5));
          cells.setMatrixAt(idx, m4);
          cells.setColorAt(idx, tint.setRGB(rgb[idx * 3], rgb[idx * 3 + 1], rgb[idx * 3 + 2]));
        }
      }
      cells.instanceMatrix.needsUpdate = true;
      cells.instanceColor.needsUpdate = true;
      seeds.forEach((s, c) => {
        s.visible = seedPos[c * 4 + 3] > 0.5;
        s.position.set(seedPos[c * 4], seedPos[c * 4 + 1] + 0.06, seedPos[c * 4 + 2]);
      });
    }

    return world({
      labels: frame(group, el),
      setState(i) {
        const cs = data.states[i].centroids;
        for (let idx = 0; idx < n; idx++) {
          const c = data.voronoi.cell[i][idx];
          hT[idx] = cs[c - 1].w;
          const lit = tint.copy(colors[c - 1]);
          rgbT.set([lit.r, lit.g, lit.b], idx * 3);
        }
        colors.forEach((_, c) => {
          const m = cs[c];
          seedT.set(m ? [wx(m.u), BASE + m.w * LIFT, wz(m.v), 1] : [seedPos[c * 4], 0, seedPos[c * 4 + 2], 0], c * 4);
        });
      },
      animate(dt) {
        const k = ease(dt, 3.5);
        const moving = chase(h, hT, k) | chase(rgb, rgbT, k) | chase(seedPos, seedT, k);
        update();
        return Boolean(moving);
      },
    });
  },
};
