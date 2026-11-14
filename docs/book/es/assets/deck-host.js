// A Reveal-like host so the deck's 3-D bundle (assets/deck-3d.min.js, built from
// assets/deck-3d/) runs in the book's HTML edition, unchanged. Load it before the bundle.
//
// The bundle's stage (assets/deck-3d/stage.js) asks Reveal for the current slide, its scale,
// and events (ready, slidechanged, fragmentshown, resize), and reads which fragments with
// data-view are .visible. Here a "slide" is the book section that holds the scene: it is
// current while the scene is on screen, so only visible scenes render. The view buttons that
// scripts/scenes.py writes beside each scene stand in for fragments: pressing one marks it
// .visible, as Reveal marks a shown fragment, and the stage moves to that view.
(() => {
  if (window.Reveal) return;
  const handlers = {};
  let current = null;
  const emit = (type) => (handlers[type] ?? []).forEach((fn) => fn({}));
  window.Reveal = {
    isReady: () => true,
    on: (type, fn) => (handlers[type] ??= []).push(fn),
    getScale: () => 1,
    isPrintView: () => false,
    getCurrentSlide: () => current,
  };

  function wire() {
    const shown = new Map();
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((e) => shown.set(e.target, e.isIntersecting ? e.intersectionRatio : 0));
      // The most visible scene's section is the current slide.
      let best = null, ratio = 0;
      shown.forEach((r, scene) => { if (r > ratio) { ratio = r; best = scene; } });
      const next = best ? best.closest("section") : null;
      if (next !== current) {
        current = next;
        emit("slidechanged");
      }
    }, { threshold: [0, 0.25, 0.5, 0.75, 1] });
    document.querySelectorAll(".deck-3d").forEach((el) => observer.observe(el));

    document.addEventListener("click", (event) => {
      const button = event.target.closest(".view-buttons button[data-view]");
      if (!button) return;
      button.parentElement.querySelectorAll("button").forEach((b) => {
        b.classList.toggle("visible", b === button);
        b.setAttribute("aria-pressed", String(b === button));
      });
      emit("fragmentshown");
    });
    addEventListener("resize", () => emit("resize"));
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", wire);
  else wire();
})();
