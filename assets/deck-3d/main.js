// The deck's 3-D slides: each .deck-3d element names its scene in data-scene. The deck
// loads this bundle once (deck-3d.min.js, from the first 3-D slide's cell).
import { cloud } from "./cloud.js";
import { relief } from "./relief.js";
import { stage } from "./stage.js";

const scenes = { cloud, relief };

function initialize() {
  const deck = window.Reveal;
  if (!deck) return;
  const run = () => document.querySelectorAll(".deck-3d").forEach((el) => {
    if (el.dataset.ready || !scenes[el.dataset.scene]) return;
    el.dataset.ready = "true";
    stage(el, deck, scenes[el.dataset.scene]);
  });
  if (deck.isReady()) run();
  else deck.on("ready", run);
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize);
else initialize();
