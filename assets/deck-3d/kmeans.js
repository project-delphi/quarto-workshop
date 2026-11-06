// k-means toy (slides/_water.qmd, #water-kmeans): synthetic points in 3-D, k centres that
// drop, grab their nearest points, move to the mean and repeat until nothing changes. The
// deck cell runs the algorithm (data.runs[r].states[i]: centres c, labels l or null, and the
// readout text) and this scene only draws it: points ease to their cluster's colour, lines
// join each point to its centre, centres glide, leaving a trail of where they have been, and,
// once stable, pulse. The stage's state is the step i; its "cluster" buttons pick the random
// start r (0 = the first).
import {
  BufferAttribute, BufferGeometry, CanvasTexture, Color, CylinderGeometry, LineBasicMaterial,
  LineSegments, LinearFilter, Mesh, MeshBasicMaterial, MeshLambertMaterial, AmbientLight,
  DirectionalLight, Points, PointsMaterial, SphereGeometry, Vector3,
} from "three";
import { chase, ease } from "./meta.js";

const GREY = new Color(0x8a8f96);
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");

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
    flat: { rx: 0.35, ry: -0.6, zoom: 1.12, spin: 0.08, focus: false },
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
      size: 0.055, sizeAttenuation: true, vertexColors: true, map: disc(), alphaTest: 0.05,
    }));
    points.frustumCulled = false;
    group.add(points);

    // The centres: glowing balls with a white halo, so they stay visible inside a cluster.
    const centres = colors.map((color) => {
      const ball = new Mesh(new SphereGeometry(0.05, 24, 16),
        new MeshLambertMaterial({ color, emissive: color, emissiveIntensity: 0.6 }));
      const halo = new Mesh(new SphereGeometry(0.07, 24, 16),
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

    // Each centre's trail: a tube per move and a dot at each place it stopped, from a pool as
    // long as the most moves in a run (every other state is a move). Tubes thicken towards the
    // latest position.
    const mostMoves = Math.ceil(Math.max(...data.runs.map((r) => r.states.length)) / 2);
    const tube = new CylinderGeometry(1, 1, 1, 10), dot = new SphereGeometry(0.018, 12, 8);
    const trails = colors.map((color) => {
      const material = new MeshBasicMaterial({ color });
      const make = (geometry) => {
        const mesh = new Mesh(geometry, material);
        mesh.visible = false;
        group.add(mesh);
        return mesh;
      };
      return { tubes: Array.from({ length: mostMoves }, () => make(tube)),
        dots: Array.from({ length: mostMoves }, () => make(dot)), way: [] };
    });
    const up = new Vector3(0, 1, 0), from = new Vector3(), to = new Vector3(), along = new Vector3();

    const cen = new Float32Array(k * 3), cenT = new Float32Array(k * 3);
    const lineA = [0];
    let dirty = true, run = 0, step = 0, lineOpacity = 0, clock = 0, first = true, stable = false, labels = null;
    const readout = el.closest("section")?.querySelector(".k-readout");

    function retarget() {
      const states = data.runs[run].states;
      const s = states[Math.min(step, states.length - 1)];
      cenT.set(s.c.map((v) => v / scale));
      labels = s.l;
      dirty = true;
      for (let i = 0; i < n; i++) {
        const c = labels ? colors[labels[i]] : GREY;
        colT.set([c.r, c.g, c.b], i * 3);
        if (labels) lineCol.set([c.r, c.g, c.b, c.r, c.g, c.b], i * 6);
      }
      lineGeometry.attributes.color.needsUpdate = true;
      lineA[0] = labels ? 0.16 : 0;
      // The places each centre has stopped at, up to this step.
      trails.forEach((trail, j) => {
        trail.way = [];
        for (const state of states.slice(0, step + 1)) {
          const p = state.c.slice(j * 3, j * 3 + 3).map((v) => v / scale);
          const last = trail.way[trail.way.length - 1];
          if (!last || p.some((v, a) => v !== last[a])) trail.way.push(p);
        }
      });
      stable = step >= states.length - 1 && states.length > 1;
      if (readout) readout.textContent = s.note;
      if (first) { cen.set(cenT); first = false; }
    }

    function draw() {
      for (let j = 0; j < k; j++) centres[j].position.set(cen[j * 3], cen[j * 3 + 1], cen[j * 3 + 2]);
      for (let i = 0; i < n; i++) {
        // Runs every frame of a glide, so it writes in place rather than making arrays.
        const a = i * 6, p = i * 3, c = (labels ? labels[i] : 0) * 3;
        linePos[a] = xyz[p]; linePos[a + 1] = xyz[p + 1]; linePos[a + 2] = xyz[p + 2];
        linePos[a + 3] = cen[c]; linePos[a + 4] = cen[c + 1]; linePos[a + 5] = cen[c + 2];
      }
      trails.forEach(({ tubes, dots, way }, j) => {
        const moves = way.length - 1;
        tubes.forEach((mesh, t) => {
          mesh.visible = t < moves;
          if (!mesh.visible) return;
          from.fromArray(way[t]);
          // The newest tube ends at the gliding centre, so the trail grows as it moves.
          if (t === moves - 1) to.set(cen[j * 3], cen[j * 3 + 1], cen[j * 3 + 2]);
          else to.fromArray(way[t + 1]);
          along.subVectors(to, from);
          const length = along.length();
          mesh.visible = length > 1e-4;
          if (!mesh.visible) return;
          const radius = 0.005 + (0.009 * (t + 1)) / moves;
          mesh.position.addVectors(from, to).multiplyScalar(0.5);
          mesh.scale.set(radius, length, radius);
          mesh.quaternion.setFromUnitVectors(up, along.divideScalar(length));
        });
        dots.forEach((mesh, t) => {
          mesh.visible = t < moves;
          if (mesh.visible) mesh.position.fromArray(way[t]);
        });
      });
      lineGeometry.attributes.position.needsUpdate = true;
      pointGeometry.attributes.color.needsUpdate = true;
    }

    return {
      centre: [0, 0, 0], half: 0.85, aspect: 1.7, labels: [], focus() {},
      // One step glides along the trail. A jump, or another start, lands at once: a straight glide
      // there would draw a path the algorithm did not take.
      setState(i) {
        const jump = Math.abs(i - step) > 1;
        step = i;
        retarget();
        if (jump) cen.set(cenT);
      },
      setCluster(c) { run = Math.min(c, data.runs.length - 1); retarget(); cen.set(cenT); },
      animate(dt) {
        const e = ease(dt, 3);
        // The centres glide slowly: their movement is the algorithm.
        let moving = chase(cen, cenT, ease(dt, 1.3)) | chase(col, colT, e);
        lineOpacity += (lineA[0] - lineOpacity) * e;
        if (Math.abs(lineA[0] - lineOpacity) > 0.005) moving = true;
        else lineOpacity = lineA[0];
        lineMaterial.opacity = lineOpacity;
        // Once nothing changes any more, the centres breathe (not with a still frame).
        const changed = Boolean(moving);
        let pulse = 1;
        if (stable && Number.isFinite(dt) && !reduceMotion.matches) {
          clock += dt;
          pulse = 1 + 0.18 * Math.sin(clock * 4);
          moving = true;
        }
        centres.forEach((c) => c.scale.setScalar(pulse));
        if (changed || dirty) draw(); // lines and colours only change while something moves
        dirty = false;
        return Boolean(moving);
      },
    };
  },
};
