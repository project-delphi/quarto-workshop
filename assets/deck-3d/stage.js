// A 3-D slide stage shared by the deck's scenes (main.js). A .deck-3d element carries its
// scene's data as JSON. Fragments on the same slide with data-view="<name>" move between
// the scene's views; the reader can drag to turn and scroll to zoom. Rendering runs only
// while the slide is shown, a PDF export gets one still frame of the last view, and
// without WebGL the element's .fallback note shows instead.
// three.js manual: https://threejs.org/manual/ (checked 2026-10-30).
import { Color, Fog, Group, PerspectiveCamera, Scene, Vector3, WebGLRenderer } from "three";

const FOV = 30;
const KEYS = ["rx", "ry", "dist", "focus", "cx", "cy", "cz"];
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");

// Shortest equivalent of angle a near b, so a view change never unwinds earlier turns.
const near = (a, b) => b + Math.atan2(Math.sin(a - b), Math.cos(a - b));

// scene.views(data) names the views: rx tilts towards the reader, ry turns about the
// vertical axis, zoom divides the fitted distance, spin turns ry (rad/s), focus fades the
// other groups, and centre (optional) is the point the view turns about.
// scene.build(group, data, el) adds its objects to group and returns { centre, half, aspect,
// labels: [{ label, from, to }], focus(t) }: the data's centre and largest half-range, its
// face-on width/height, HTML labels drawn at a line's end (they fade as the line turns
// towards the reader), and a callback that fades the unfocused groups by t (0 to 1).
export function stage(el, deck, sceneType) {
  const data = JSON.parse(el.querySelector("script[type='application/json']").textContent);
  const slide = el.closest("section");
  const views = sceneType.views(data);
  const printing = deck.isPrintView?.() ?? document.documentElement.classList.contains("reveal-print");
  let renderer, scene, camera, outer, inner, world, raf = 0, last = 0, userUntil = 0;
  let view = views.flat;
  let zoom = 1; // the reader's wheel zoom within the current view
  const cur = Object.fromEntries(KEYS.map((key) => [key, 0]));
  const target = { ...cur };

  function build() {
    try {
      renderer = new WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: printing });
    } catch {
      el.querySelector(".fallback").hidden = false;
      return false;
    }
    const canvas = renderer.domElement;
    canvas.setAttribute("aria-hidden", "true");
    canvas.setAttribute("data-prevent-swipe", "");
    el.prepend(canvas);
    el.classList.add("is-drawn"); // shows the labels and legend (theme.scss)
    scene = new Scene();
    outer = new Group();
    inner = new Group();
    outer.add(inner);
    scene.add(outer);
    world = sceneType.build(inner, data, el);
    camera = new PerspectiveCamera(FOV, 1, world.half * 0.01, world.half * 40);
    // Far objects fade into the slide background, a depth cue when the scene turns.
    let background = "rgba(0, 0, 0, 0)";
    for (let e = el; e && background === "rgba(0, 0, 0, 0)"; e = e.parentElement) {
      background = getComputedStyle(e).backgroundColor;
    }
    scene.fog = new Fog(new Color(background === "rgba(0, 0, 0, 0)" ? "#222222" : background), 1, 2);

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
      const ends = ["pointerup", "pointercancel", "lostpointercapture"];
      const end = () => {
        canvas.removeEventListener("pointermove", move);
        ends.forEach((type) => canvas.removeEventListener(type, end));
      };
      canvas.addEventListener("pointermove", move);
      ends.forEach((type) => canvas.addEventListener(type, end));
    });
    canvas.addEventListener("wheel", (e) => {
      e.preventDefault();
      zoom = Math.min(2, Math.max(0.25, zoom * Math.exp(e.deltaY * 0.001)));
      target.dist = aim();
      start();
    }, { passive: false });
    setView(view);
    resize();
    Object.assign(cur, target);
    return true;
  }

  // Camera distance at which the data's largest half-range fits the canvas height, and the
  // distance for the current view and wheel zoom.
  const fit = () => (world.half * 1.1) / Math.tan((FOV * Math.PI) / 360) /
    Math.min(1, camera.aspect / world.aspect);
  const aim = () => (fit() / view.zoom) * zoom;

  function resize() {
    if (!renderer) return;
    const w = el.clientWidth, h = el.clientHeight;
    renderer.setPixelRatio(Math.min(3, devicePixelRatio * deck.getScale()));
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    target.dist = aim();
    draw();
    start();
  }

  function setView(next) {
    view = next;
    target.rx = view.rx;
    target.ry = view.ry;
    cur.rx = near(cur.rx, target.rx);
    cur.ry = near(cur.ry, target.ry);
    target.focus = view.focus ? 1 : 0;
    zoom = 1;
    if (world) {
      [target.cx, target.cy, target.cz] = view.centre ?? world.centre;
      target.dist = aim();
    }
  }

  function draw() {
    outer.rotation.set(cur.rx, cur.ry, 0, "XYZ");
    inner.position.set(-cur.cx, -cur.cy, -cur.cz);
    camera.position.set(0, 0, cur.dist);
    camera.lookAt(0, 0, 0);
    scene.fog.near = cur.dist - world.half * 0.5;
    scene.fog.far = cur.dist + world.half * 3;
    world.focus(cur.focus);
    renderer.render(scene, camera);
    const w = el.clientWidth, h = el.clientHeight;
    const screen = (v) => {
      const p = inner.localToWorld(v.clone()).project(camera);
      return [((p.x + 1) / 2) * w, ((1 - p.y) / 2) * h];
    };
    scene.updateMatrixWorld();
    world.labels.forEach(({ label, from, to }) => {
      const [x, y] = screen(to);
      const [fx, fy] = screen(from);
      label.style.left = `${x}px`;
      label.style.top = `${y}px`;
      label.style.opacity = Math.min(1, Math.max(0, (Math.hypot(x - fx, y - fy) - 40) / 60));
    });
  }

  function frame(t) {
    const dt = Math.min(0.05, (t - (last || t)) / 1000);
    last = t;
    const still = reduceMotion.matches;
    if (view.spin && !still && t > userUntil) target.ry += view.spin * dt;
    const k = still ? 1 : 1 - Math.exp(-dt * 2.5);
    for (const key of KEYS) cur[key] += (target[key] - cur[key]) * k;
    draw();
    const settled = KEYS.every((key) => Math.abs(target[key] - cur[key]) < 1e-3 * (key === "dist" || key[0] === "c" ? world.half : 1));
    raf = settled && !(view.spin && !still) ? 0 : requestAnimationFrame(frame);
  }

  function start() {
    if (!raf && renderer && deck.getCurrentSlide() === slide && !document.hidden) {
      last = 0;
      raf = requestAnimationFrame(frame);
    }
  }

  function update() {
    const shown = [...slide.querySelectorAll("[data-view].visible")].pop();
    setView(views[shown?.dataset.view] ?? views.flat);
    if (printing) {
      if (renderer || build()) {
        resize();
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
  deck.on("pdf-ready", update); // the print layout is done: draw at its final size
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) return start();
    cancelAnimationFrame(raf);
    raf = 0;
  });
  update();
}
