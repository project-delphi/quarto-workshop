// k-means toy (slides/_water.qmd, #water-kmeans): synthetic points in 3-D, k centres that
// drop, grab their nearest points, move to the mean and repeat until nothing changes. The
// deck cell runs the algorithm (data.runs[r].states[i]: centres c, labels l or null, and the
// readout text) and this scene only draws it: points ease to their cluster's colour, lines
// join each point to its centre, centres glide and, once stable, pulse. The stage's state is
// the step i; its "cluster" buttons pick the random start r (0 = the first).
import {
  BufferAttribute, BufferGeometry, CanvasTexture, Color, LineBasicMaterial, LineSegments,
  LinearFilter, Mesh, MeshBasicMaterial, MeshLambertMaterial, AmbientLight, DirectionalLight,
  Points, PointsMaterial, SphereGeometry,
} from "three";
import { chase, ease } from "./meta.js";

const GREY = new Color(0x8a8f96);

function disc() {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 64;
  const g = canvas.getContext("2d");
  g.fillStyle = "#fff";
  g.beginPath();
  g.arc(32, 32, 28, 0, 2 * Math.PI);
  g.fill();
  const texture = new CanvasTexture(canvas);
  texture.minFilter = LinearFilter;
  texture.generateMipmaps = false;
  return texture;
}

export const kmeans = {
  views: () => ({
    flat: { rx: 0.35, ry: -0.6, zoom: 1.05, spin: 0.15, focus: false },
  }),

  build(group, data, el) {
    const { k, scale } = data;
    const n = data.pts.length / 3;
    const colors = data.colors.map((c) => new Color(c));
    const xyz = Float32Array.from(data.pts, (v) => v / scale);

    // The points: one geometry, colours eased frame by frame.
    const col = new Float32Array(n * 3), colT = new Float32Array(n * 3);
    const pointGeometry = new BufferGeometry();
    pointGeometry.setAttribute("position", new BufferAttribute(xyz, 3));
    pointGeometry.setAttribute("color", new BufferAttribute(col, 3));
    const points = new Points(pointGeometry, new PointsMaterial({
      size: 0.1, sizeAttenuation: true, vertexColors: true, map: disc(), alphaTest: 0.05,
    }));
    points.frustumCulled = false;
    group.add(points);

    // The centres: glowing balls with a white halo, so they stay visible inside a cluster.
    const centres = colors.map((color) => {
      const ball = new Mesh(new SphereGeometry(0.085, 24, 16),
        new MeshLambertMaterial({ color, emissive: color, emissiveIntensity: 0.6 }));
      const halo = new Mesh(new SphereGeometry(0.12, 24, 16),
        new MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.3, depthWrite: false }));
      ball.add(halo);
      group.add(ball);
      return ball;
    });
    group.add(new AmbientLight(0xffffff, 1.6));
    const sun = new DirectionalLight(0xffffff, 2.2);
    sun.position.set(1.2, 2.5, 1.8);
    group.add(sun);

    // Lines from each point to its centre (their length is the distance k-means minimises).
    const linePos = new Float32Array(n * 6), lineCol = new Float32Array(n * 6);
    const lineGeometry = new BufferGeometry();
    lineGeometry.setAttribute("position", new BufferAttribute(linePos, 3));
    lineGeometry.setAttribute("color", new BufferAttribute(lineCol, 3));
    const lineMaterial = new LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0 });
    const lines = new LineSegments(lineGeometry, lineMaterial);
    lines.frustumCulled = false;
    group.add(lines);

    const cen = new Float32Array(k * 3), cenT = new Float32Array(k * 3);
    const lineA = [0];
    let run = 0, step = 0, lineOpacity = 0, clock = 0, first = true, stable = false, labels = null;
    const readout = el.closest("section")?.querySelector(".k-readout");

    function retarget() {
      const states = data.runs[run].states;
      const s = states[Math.min(step, states.length - 1)];
      cenT.set(s.c.map((v) => v / scale));
      labels = s.l;
      for (let i = 0; i < n; i++) {
        const c = labels ? colors[labels[i]] : GREY;
        colT.set([c.r, c.g, c.b], i * 3);
      }
      lineA[0] = labels ? 0.4 : 0;
      stable = step >= states.length - 1 && states.length > 1;
      if (readout) readout.textContent = s.note;
      if (first) { cen.set(cenT); first = false; }
    }

    function draw() {
      for (let j = 0; j < k; j++) centres[j].position.set(cen[j * 3], cen[j * 3 + 1], cen[j * 3 + 2]);
      for (let i = 0; i < n; i++) {
        const j = labels ? labels[i] : 0;
        linePos.set([xyz[i * 3], xyz[i * 3 + 1], xyz[i * 3 + 2],
          cen[j * 3], cen[j * 3 + 1], cen[j * 3 + 2]], i * 6);
        const c = colors[j];
        lineCol.set([c.r, c.g, c.b, c.r, c.g, c.b], i * 6);
      }
      lineGeometry.attributes.position.needsUpdate = true;
      lineGeometry.attributes.color.needsUpdate = true;
      pointGeometry.attributes.color.needsUpdate = true;
    }

    return {
      centre: [0, 0, 0], half: 0.85, aspect: 1.7, labels: [], focus() {},
      setState(i) { step = i; retarget(); },
      setCluster(c) { run = Math.min(c, data.runs.length - 1); retarget(); },
      animate(dt) {
        const e = ease(dt, 3);
        let moving = chase(cen, cenT, e) | chase(col, colT, e);
        lineOpacity += (lineA[0] - lineOpacity) * e;
        if (Math.abs(lineA[0] - lineOpacity) > 0.005) moving = true;
        else lineOpacity = lineA[0];
        lineMaterial.opacity = lineOpacity;
        // Once nothing changes any more, the centres breathe (not with a still frame).
        let pulse = 1;
        if (stable && Number.isFinite(dt)) {
          clock += dt;
          pulse = 1 + 0.18 * Math.sin(clock * 4);
          moving = true;
        }
        centres.forEach((c) => c.scale.setScalar(pulse));
        draw();
        return Boolean(moving);
      },
    };
  },
};
