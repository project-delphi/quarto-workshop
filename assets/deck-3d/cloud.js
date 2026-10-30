// Cluster cloud (slides/_water.qmd, #water-pca-3d): zone-years on the first three principal
// components, coloured and shaped by cluster as in the 2-D figure. The deck cell computes
// the points; this scene only draws them (stage.js runs the slide).
import {
  BufferAttribute, BufferGeometry, CanvasTexture, LinearFilter, LineBasicMaterial,
  LineSegments, Points, PointsMaterial, Vector3,
} from "three";

// White marker shapes, tinted by each cluster's material; they match the 2-D figure's
// matplotlib markers (analysis.CLUSTER_MARKERS).
function marker(shape) {
  const size = 64, c = size / 2, r = size * 0.42;
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = size;
  const g = canvas.getContext("2d");
  g.fillStyle = "#fff";
  g.beginPath();
  const poly = (points) => points.forEach(([x, y], i) => (i ? g.lineTo(x, y) : g.moveTo(x, y)));
  if (shape === "s") g.rect(c - r * 0.8, c - r * 0.8, r * 1.6, r * 1.6);
  else if (shape === "^") poly([[c, c - r], [c + r, c + r * 0.8], [c - r, c + r * 0.8]]);
  else if (shape === "v") poly([[c, c + r], [c + r, c - r * 0.8], [c - r, c - r * 0.8]]);
  else if (shape === "D") poly([[c, c - r], [c + r * 0.75, c], [c, c + r], [c - r * 0.75, c]]);
  else if (shape === "P" || shape === "X") {
    const t = r * 0.3;
    g.translate(c, c);
    if (shape === "X") g.rotate(Math.PI / 4);
    g.rect(-t, -r, 2 * t, 2 * r);
    g.rect(-r, -t, 2 * r, 2 * t);
  } else if (shape === "*") {
    poly(Array.from({ length: 10 }, (_, i) => {
      const a = -Math.PI / 2 + (i * Math.PI) / 5, q = i % 2 ? r * 0.45 : r;
      return [c + q * Math.cos(a), c + q * Math.sin(a)];
    }));
  } else g.arc(c, c, r * 0.85, 0, 2 * Math.PI);
  g.fill();
  const texture = new CanvasTexture(canvas);
  texture.minFilter = LinearFilter; // no mipmaps: small markers keep their edges
  texture.generateMipmaps = false;
  return texture;
}

export const cloud = {
  views: () => ({
    flat: { rx: 0, ry: 0, zoom: 1, spin: 0, focus: false },              // the 2-D picture
    turn: { rx: 0.35, ry: -0.85, zoom: 1.05, spin: 0.2, focus: false },  // PC3 comes forward
    pc3: { rx: -Math.PI / 2 + 0.15, ry: 0, zoom: 1.2, spin: 0, focus: true }, // PC3 up
  }),

  build(group, data, el) {
    const { lo, hi } = data; // 1st-99th percentiles: fit the bulk, not the outliers
    const half = Math.max(...hi.map((v, a) => (v - lo[a]) / 2));
    const materials = data.clusters.map((c) => {
      const idx = [];
      for (let i = 0; i < data.cluster.length; i++) if (data.cluster[i] === c.id) idx.push(i);
      const pos = new Float32Array(idx.length * 3);
      idx.forEach((p, j) => {
        for (let a = 0; a < 3; a++) pos[j * 3 + a] = data.xyz[p * 3 + a] / data.scale;
      });
      const geometry = new BufferGeometry();
      geometry.setAttribute("position", new BufferAttribute(pos, 3));
      const material = new PointsMaterial({
        color: c.color, map: marker(c.marker), size: half * 0.075, sizeAttenuation: true,
        transparent: true, alphaTest: 0.05,
      });
      material.userData.id = c.id;
      group.add(new Points(geometry, material));
      return material;
    });

    // Axes through the PCA origin (the mean zone-year), spanning the data.
    const axes = new Float32Array(18);
    [0, 1, 2].forEach((a) => {
      axes[a * 6 + a] = lo[a] * 1.15;
      axes[a * 6 + 3 + a] = hi[a] * 1.15;
    });
    const axisGeometry = new BufferGeometry();
    axisGeometry.setAttribute("position", new BufferAttribute(axes, 3));
    group.add(new LineSegments(axisGeometry,
      new LineBasicMaterial({ color: 0xb8c2cc, transparent: true, opacity: 0.55 })));

    return {
      centre: lo.map((v, a) => (v + hi[a]) / 2),
      half,
      aspect: (hi[0] - lo[0]) / (hi[1] - lo[1]),
      // The .axis-label elements, in PC order, at the positive end of each axis.
      labels: [...el.querySelectorAll(".axis-label")].map((label, a) => {
        const to = new Vector3();
        to.setComponent(a, hi[a] * 1.22);
        return { label, from: new Vector3(), to };
      }),
      focus(t) {
        materials.forEach((m) => {
          m.opacity = m.userData.id === data.focus ? 1 : 1 - 0.8 * t;
          m.depthWrite = m.opacity > 0.99;
        });
      },
    };
  },
};
