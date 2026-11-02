// Deforming meta-terrain (slides/_water.qmd, #water-meta-terrain): the surface over Saber 11
// (x) and infant mortality (z) rises to the school dropout of the cluster that owns each
// place, and glowing lines mark where one cluster hands over to the next. Each year reshapes
// it; a focused cluster keeps its colour and the rest fade. The deck cell computes the
// heights, the owner of each place and the border edges for every year.
import {
  AdditiveBlending, BufferAttribute, BufferGeometry, Color, LineBasicMaterial, LineSegments,
  Mesh, MeshLambertMaterial, PlaneGeometry,
} from "three";
import { chase, ease, frame, lights, palette, tone, world } from "./meta.js";

const WHITE = new Color(0xffffff);
const LIFT = 2.4; // dropout (0-1) to height: exaggerated, as the slide says

export const metaTerrain = {
  views: () => ({
    flat: { rx: 0.78, ry: -0.55, zoom: 1.05, spin: 0.04, focus: false },
  }),

  build(group, data, el) {
    const t = data.terrain, g = t.g, n = g * g, colors = palette(data);
    const geometry = new PlaneGeometry(2, 2, g - 1, g - 1);
    const position = new BufferAttribute(new Float32Array(n * 3), 3);
    for (let i = 0; i < g; i++) {
      for (let j = 0; j < g; j++) {
        position.setXYZ(i * g + j, -1 + (2 * j) / (g - 1), 0, -1 + (2 * i) / (g - 1));
      }
    }
    geometry.setAttribute("position", position);
    const color = new BufferAttribute(new Float32Array(n * 3), 3);
    geometry.setAttribute("color", color);
    group.add(
      new Mesh(geometry, new MeshLambertMaterial({ vertexColors: true })),
      new Mesh(geometry, new MeshLambertMaterial({
        color: 0xffffff, wireframe: true, transparent: true, opacity: 0.1, depthWrite: false })));

    // Two border sets cross-fade when the year changes: the one leaving, the one arriving.
    const maxEdges = Math.max(...t.edges.map((e) => e.length));
    const borders = [0, 1].map(() => {
      const geo = new BufferGeometry();
      geo.setAttribute("position", new BufferAttribute(new Float32Array(maxEdges * 3), 3));
      const material = new LineBasicMaterial({
        color: 0xffffff, transparent: true, blending: AdditiveBlending, depthWrite: false });
      const lines = new LineSegments(geo, material);
      lines.frustumCulled = false;
      group.add(lines);
      return { geo, material, ends: [] };
    });
    lights(group);

    const h = new Float32Array(n), hT = new Float32Array(n);
    const rgb = new Float32Array(n * 3), rgbT = new Float32Array(n * 3);
    const mix = [1];
    let state = 0, focus = 0;
    function update() {
      for (let v = 0; v < n; v++) position.setY(v, h[v] * LIFT);
      position.needsUpdate = true;
      color.array.set(rgb);
      color.needsUpdate = true;
      geometry.computeVertexNormals();
      borders.forEach(({ geo, ends }) => {
        const arr = geo.attributes.position.array;
        ends.forEach((v, e) => {
          arr[e * 3] = position.getX(v);
          arr[e * 3 + 1] = h[v] * LIFT + 0.03;
          arr[e * 3 + 2] = position.getZ(v);
        });
        geo.setDrawRange(0, ends.length);
        geo.attributes.position.needsUpdate = true;
      });
      borders[1].material.opacity = mix[0];
      borders[0].material.opacity = 1 - mix[0];
    }
    function retarget() {
      for (let v = 0; v < n; v++) {
        hT[v] = t.h[state][v] / data.scale;
        // Lighter on the heights so relief reads as relief.
        const lit = tone(colors, t.dom[state][v], focus).clone().lerp(WHITE, 0.3 * hT[v]);
        rgbT.set([lit.r, lit.g, lit.b], v * 3);
      }
    }

    return world({
      labels: frame(group, el),
      setState(i) {
        state = i;
        borders[0].ends = borders[1].ends;
        borders[1].ends = t.edges[i];
        mix[0] = 0;
        retarget();
      },
      setCluster(c) {
        focus = c;
        retarget();
      },
      animate(dt) {
        const k = ease(dt, 3.5);
        const moving = [chase(h, hT, k), chase(rgb, rgbT, k), chase(mix, [1], k)].some(Boolean);
        update();
        return moving;
      },
    });
  },
};
