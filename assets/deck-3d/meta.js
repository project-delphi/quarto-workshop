// Shared by the optional meta-feature slides (slides/_water.qmd, #water-meta-*): the three
// outcomes the clustering never saw, for each municipality, under clusterings with k = 2 to 5.
// The deck cell computes every position, label, centroid, count and border (data.*); these
// helpers and the six scenes only draw them and ease between states.
//
// World frame: x = Saber 11, z = infant mortality (depth), y = school dropout (height), each
// scaled from its 2nd-98th percentile to [0, 1] and drawn on x, z in [-1, 1], y in [0, 1].
import {
  AmbientLight, BufferAttribute, BufferGeometry, Color, DirectionalLight, GridHelper,
  LineBasicMaterial, LineSegments, Points, PointsMaterial, Vector3,
} from "three";

export const HALF = 1.3;
export const wx = (u) => (u - 0.5) * 2;
export const wz = (v) => (v - 0.5) * 2;

export const palette = (data) => data.colors.map((c) => new Color(c));

// Eases the numbers in cur towards tgt by the share k; true while any is still moving.
export function chase(cur, tgt, k) {
  let moving = false;
  for (let i = 0; i < cur.length; i++) {
    const d = tgt[i] - cur[i];
    if (Math.abs(d) > 2e-4) {
      cur[i] += d * k;
      moving = true;
    } else cur[i] = tgt[i];
  }
  return moving;
}

// Share of the remaining distance to cover this frame (dt = Infinity finishes at once).
export const ease = (dt, speed = 4) => 1 - Math.exp(-dt * speed);

export function lights(group) {
  group.add(new AmbientLight(0xffffff, 1.6));
  const sun = new DirectionalLight(0xffffff, 2.2);
  sun.position.set(1.2, 2.5, 1.8);
  group.add(sun);
}

// Floor grid, the three axes and their HTML labels (the .axis-label spans, in x, z, y order).
export function frame(group, el, { floor = true } = {}) {
  if (floor) {
    const grid = new GridHelper(2, 8, 0x6b7480, 0x3a4048);
    grid.material.transparent = true;
    grid.material.opacity = 0.55;
    group.add(grid);
  }
  const seg = [-1, 0, 1, 1, 0, 1, 1, 0, -1, 1, 0, 1, -1, 0, -1, -1, 1.05, -1];
  const geometry = new BufferGeometry();
  geometry.setAttribute("position", new BufferAttribute(new Float32Array(seg), 3));
  group.add(new LineSegments(geometry,
    new LineBasicMaterial({ color: 0xb8c2cc, transparent: true, opacity: 0.7 })));
  const ends = [[0, 0, 1.3], [1.32, 0, 0], [-1, 1.2, -1]];
  return [...el.querySelectorAll(".axis-label")].map((label, i) => (
    { label, to: new Vector3(...ends[i]) }));
}

// What every scene returns besides its own parts.
export function world(extra) {
  return { centre: [0, 0.35, 0], half: HALF, aspect: 1.7, labels: [], focus() {}, ...extra };
}

// World position of municipality i pulled `pull` of the way to its cluster's centroid.
export function pulled(data, state, i, pull) {
  const s = data.scale, c = data.states[state].centroids[data.labels[state][i] - 1];
  const x = wx(data.u[i] / s), z = wz(data.v[i] / s), y = data.w[i] / s;
  return [x + (wx(c.u) - x) * pull, y + (c.w - y) * pull, z + (wz(c.v) - z) * pull];
}

// A cloud of the municipalities as points: each eases to where(state, i) -> [x, y, z] and to
// its cluster's colour under the picked state.
export function morphPoints(group, data, where, { size = 0.05, opacity = 1 } = {}) {
  const n = data.u.length, colors = palette(data);
  const pos = new Float32Array(n * 3), col = new Float32Array(n * 3);
  const tgt = new Float32Array(n * 3), tcol = new Float32Array(n * 3);
  const geometry = new BufferGeometry();
  geometry.setAttribute("position", new BufferAttribute(pos, 3));
  geometry.setAttribute("color", new BufferAttribute(col, 3));
  const material = new PointsMaterial({
    size, sizeAttenuation: true, vertexColors: true, transparent: opacity < 1, opacity,
    depthWrite: opacity >= 1,
  });
  const points = new Points(geometry, material);
  points.frustumCulled = false;
  group.add(points);
  return {
    points, pos,
    set(state) {
      for (let i = 0; i < n; i++) {
        tgt.set(where(state, i), i * 3);
        const c = colors[data.labels[state][i] - 1];
        tcol.set([c.r, c.g, c.b], i * 3);
      }
    },
    step(k) {
      const a = chase(pos, tgt, k), b = chase(col, tcol, k);
      geometry.attributes.position.needsUpdate = true;
      geometry.attributes.color.needsUpdate = true;
      return a || b;
    },
  };
}
