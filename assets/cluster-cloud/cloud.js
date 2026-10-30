// Cluster cloud for the workshop deck (slides/_water.qmd, #water-pca-3d): zone-years on the
// first three principal components. Each .cluster-cloud element carries its data as JSON;
// fragments on the same slide with data-cloud="turn" or "pc3" move the view, and the
// reader can drag to turn and scroll to zoom. Build: README.md in this folder.
// three.js manual: https://threejs.org/manual/ (checked 2026-10-30).
import {
  BufferAttribute, BufferGeometry, CanvasTexture, Color, Fog, Group, LinearFilter, LineBasicMaterial, LineSegments,
  PerspectiveCamera, Points, PointsMaterial, Scene, Vector3, WebGLRenderer,
} from "three";

const FOV = 30;
// rx tilts towards the reader, ry turns about PC2; zoom divides the fitted distance.
const VIEWS = {
  flat: { rx: 0, ry: 0, zoom: 1, spin: 0, focus: false },             // the 2-D picture
  turn: { rx: 0.35, ry: -0.85, zoom: 1.05, spin: 0.2, focus: false }, // PC3 comes forward
  pc3: { rx: -Math.PI / 2 + 0.15, ry: 0, zoom: 1.2, spin: 0, focus: true }, // PC3 up
};
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");

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
  else g.arc(c, c, r * 0.85, 0, 2 * Math.PI);
  g.fill();
  const texture = new CanvasTexture(canvas);
  texture.minFilter = LinearFilter; // no mipmaps: small markers keep their edges
  texture.generateMipmaps = false;
  return texture;
}

// Shortest equivalent of angle a near b, so a view change never unwinds earlier spins.
const near = (a, b) => b + Math.atan2(Math.sin(a - b), Math.cos(a - b));

function cloud(el, deck) {
  const data = JSON.parse(el.querySelector("script[type='application/json']").textContent);
  const slide = el.closest("section");
  const n = data.cluster.length;
  const { lo, hi } = data;
  const mid = lo.map((v, a) => (v + hi[a]) / 2);
  const half = Math.max(...hi.map((v, a) => (v - lo[a]) / 2));
  const centre = new Vector3(...mid);

  let renderer, scene, camera, outer, materials, labels, raf = 0, last = 0, userUntil = 0;
  let view = VIEWS.flat;
  const cur = { rx: 0, ry: 0, dist: 0, focus: 0 };
  const target = { ...cur };

  function build() {
    try {
      renderer = new WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
    } catch {
      el.querySelector(".cloud-fallback").hidden = false;
      return false;
    }
    const canvas = renderer.domElement;
    canvas.setAttribute("aria-hidden", "true");
    canvas.setAttribute("data-prevent-swipe", "");
    el.prepend(canvas);
    scene = new Scene();
    // Far points fade into the slide background, a depth cue when the cloud turns.
    let background = "rgba(0, 0, 0, 0)";
    for (let e = el; e && background === "rgba(0, 0, 0, 0)"; e = e.parentElement) {
      background = getComputedStyle(e).backgroundColor;
    }
    scene.fog = new Fog(new Color(background === "rgba(0, 0, 0, 0)" ? "#222222" : background), 1, 2);
    camera = new PerspectiveCamera(FOV, 1, 0.1, 200);
    outer = new Group();
    const inner = new Group();
    inner.position.set(-mid[0], -mid[1], -mid[2]);
    outer.add(inner);
    scene.add(outer);

    materials = data.clusters.map((c) => {
      const idx = [];
      for (let i = 0; i < n; i++) if (data.cluster[i] === c.id) idx.push(i);
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
      inner.add(new Points(geometry, material));
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
    inner.add(new LineSegments(axisGeometry,
      new LineBasicMaterial({ color: 0xb8c2cc, transparent: true, opacity: 0.55 })));
    labels = [...el.querySelectorAll(".cloud-axis")].map((label, a) => {
      const end = new Vector3();
      end.setComponent(a, hi[a] * 1.22);
      return { label, end };
    });

    canvas.addEventListener("pointerdown", (down) => {
      canvas.setPointerCapture(down.pointerId);
      let x = down.clientX, y = down.clientY;
      const move = (e) => {
        const s = deck.getScale();
        target.ry += ((e.clientX - x) / s) * 0.008;
        target.rx += ((e.clientY - y) / s) * 0.008;
        cur.ry = target.ry;
        cur.rx = target.rx;
        x = e.clientX;
        y = e.clientY;
        userUntil = performance.now() + 4000;
        start();
      };
      canvas.addEventListener("pointermove", move);
      canvas.addEventListener("pointerup", () => canvas.removeEventListener("pointermove", move), { once: true });
    });
    canvas.addEventListener("wheel", (e) => {
      e.preventDefault();
      target.dist = Math.min(fit() * 2, Math.max(fit() * 0.35, target.dist * Math.exp(e.deltaY * 0.001)));
      start();
    }, { passive: false });
    resize();
    cur.dist = target.dist;
    return true;
  }

  // Camera distance at which the data's largest half-range fits the canvas height.
  const fit = () => (half * 1.1) / Math.tan((FOV * Math.PI) / 360) /
    Math.min(1, camera.aspect / ((hi[0] - lo[0]) / (hi[1] - lo[1])));

  function resize() {
    if (!renderer) return;
    const w = el.clientWidth, h = el.clientHeight;
    renderer.setPixelRatio(Math.min(3, devicePixelRatio * deck.getScale()));
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    target.dist = fit() / view.zoom;
    draw();
  }

  function setView(name) {
    view = VIEWS[name] ?? VIEWS.flat;
    target.rx = view.rx;
    target.ry = view.ry;
    cur.ry = near(cur.ry, target.ry);
    target.focus = view.focus ? 1 : 0;
    if (camera) target.dist = fit() / view.zoom;
  }

  function draw() {
    outer.rotation.set(cur.rx, cur.ry, 0, "XYZ");
    camera.position.set(0, 0, cur.dist);
    scene.fog.near = cur.dist - half * 0.5;
    scene.fog.far = cur.dist + half * 3;
    camera.lookAt(0, 0, 0);
    materials.forEach((m) => {
      m.opacity = m.userData.id === data.focus ? 1 : 1 - 0.8 * cur.focus;
      m.depthWrite = m.opacity > 0.99;
    });
    renderer.render(scene, camera);
    // An axis label fades out as its axis turns towards the reader.
    const w = el.clientWidth, h = el.clientHeight;
    const screen = (v) => {
      const p = v.clone().sub(centre).applyEuler(outer.rotation).project(camera);
      return [((p.x + 1) / 2) * w, ((1 - p.y) / 2) * h];
    };
    const [ox, oy] = screen(new Vector3());
    labels.forEach(({ label, end }) => {
      const [x, y] = screen(end);
      label.style.left = `${x}px`;
      label.style.top = `${y}px`;
      label.style.opacity = Math.min(1, Math.max(0, (Math.hypot(x - ox, y - oy) - 40) / 60));
    });
  }

  function frame(t) {
    const dt = Math.min(0.05, (t - (last || t)) / 1000);
    last = t;
    const still = reduceMotion.matches;
    if (view.spin && !still && t > userUntil) target.ry += view.spin * dt;
    const k = still ? 1 : 1 - Math.exp(-dt * 2.5);
    for (const key of ["rx", "ry", "dist", "focus"]) cur[key] += (target[key] - cur[key]) * k;
    draw();
    const settled = ["rx", "ry", "dist", "focus"].every((key) => Math.abs(target[key] - cur[key]) < 1e-3);
    raf = settled && !(view.spin && !still) ? 0 : requestAnimationFrame(frame);
  }

  function start() {
    if (!raf && renderer && deck.getCurrentSlide() === slide && !document.hidden) {
      last = 0;
      raf = requestAnimationFrame(frame);
    }
  }

  function update() {
    const shown = [...slide.querySelectorAll("[data-cloud].visible")].pop();
    setView(shown ? shown.dataset.cloud : "flat");
    // A PDF export shows every slide at once with its fragments visible: draw the last view.
    if (document.documentElement.classList.contains("reveal-print")) {
      if (renderer || build()) {
        Object.assign(cur, target);
        draw();
      }
      return;
    }
    if (deck.getCurrentSlide() !== slide) {
      cancelAnimationFrame(raf);
      raf = 0;
      return;
    }
    if (!renderer && !build()) return;
    start();
  }

  deck.on("slidechanged", update);
  deck.on("fragmentshown", update);
  deck.on("fragmenthidden", update);
  deck.on("resize", resize);
  document.addEventListener("visibilitychange", () => (document.hidden ? cancelAnimationFrame(raf) || (raf = 0) : start()));
  update();
}

function initialize() {
  const deck = window.Reveal;
  if (!deck) return;
  const run = () => document.querySelectorAll(".cluster-cloud").forEach((el) => cloud(el, deck));
  if (deck.isReady()) run();
  else deck.on("ready", run);
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize);
else initialize();
