// The e-book landing page's only script (ebook/index.qmd): drawing on scroll, the clips,
// the sticky bar on phones, copy-link, and phones' download hints. The page
// works without it: everything is drawn, the clips show their stills, the buttons are links.
// The page's words in its language (<html lang>): English, or the Spanish page's (ebook/es/).
const T = document.documentElement.lang.startsWith("es")
  ? { pause: "Pausa", play: "Reproducir", copied: "Enlace copiado", failed: "No se pudo copiar", copy: "Copiar enlace",
      copiedTo: "Copiado:", copyThis: "Copia esta dirección:" }
  : { pause: "Pause", play: "Play", copied: "Link copied", failed: "Copy failed", copy: "Copy link",
      copiedTo: "Copied", copyThis: "Copy this address:" };
(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const canWatch = "IntersectionObserver" in window;

  // Phones (iPads too): how to get the EPUB into a reading app, and the EPUB's copy on GitHub
  // Pages, which is served as an e-book; the release link (kept on desktops, where GitHub counts
  // it) is a generic file that phones save without offering a reader. In-app browsers (LinkedIn,
  // Instagram, Facebook, Android web views) often fail to download at all: say so first.
  const ua = navigator.userAgent;
  const inApp = /LinkedInApp|FBAN|FBAV|FB_IAB|Instagram| Line\/|MicroMessenger|Snapchat|musical_ly|BytedanceWebview|; wv\)/i.test(ua);
  const ios = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  const phone = inApp ? "inapp" : ios ? "ios" : /Android/i.test(ua) ? "android" : "";
  // Apple Books cannot deliver the book to an Android phone: show its button only elsewhere.
  if (/Android/i.test(ua)) {
    document.querySelectorAll('a[data-store="apple"]').forEach((a) => { a.hidden = true; });
  }
  if (phone) {
    document.querySelectorAll(`.howto[data-for="${phone}"]`).forEach((el) => { el.hidden = false; });
    // In-app web views may not handle a file served to display: they keep the release link.
    if (phone !== "inapp") {
      document.querySelectorAll("a[data-phone]").forEach((a) => { a.href = a.dataset.phone; });
    }
  }

  // Draw the loop and the fan of formats when they scroll into view (unless motion is off).
  const drawn = document.querySelectorAll("[data-draw]");
  if (canWatch && !reduce) {
    const watch = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add("drawn"); watch.unobserve(en.target); }
      });
    }, { threshold: 0.3 });
    drawn.forEach((el) => { el.classList.add("will-draw"); watch.observe(el); });
  }

  // Clips: load and play only while on screen, never with reduced motion; each can be paused.
  if (canWatch && !reduce) {
    const clips = document.querySelectorAll(".clip");
    const play = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        const clip = en.target;
        const video = clip.querySelector("video");
        if (en.isIntersecting && clip.dataset.paused !== "yes") {
          if (!video.src) { video.src = video.dataset.src; }
          video.play().catch(() => {});
        } else if (!en.isIntersecting && video.src) {
          video.pause();
        }
      });
    }, { threshold: 0.5 });
    clips.forEach((clip) => {
      const video = clip.querySelector("video");
      const button = clip.querySelector(".pause");
      video.addEventListener("playing", () => {
        clip.classList.add("playing");
        button.hidden = false;
      }, { once: true });
      button.addEventListener("click", () => {
        const paused = clip.dataset.paused === "yes";
        clip.dataset.paused = paused ? "no" : "yes";
        button.setAttribute("aria-pressed", String(!paused));
        button.textContent = paused ? T.pause : T.play;
        if (paused) { video.play().catch(() => {}); } else { video.pause(); }
      });
      play.observe(clip);
    });
  }

  // On phones, a slim download bar once the hero's buttons have scrolled away, hidden again
  // when the last call to action is on screen.
  const bar = document.querySelector(".sticky");
  const heroCtas = document.querySelector(".hero .ctas");
  const lastCtas = document.querySelector("#get .ctas");
  if (bar && heroCtas && canWatch) {
    bar.hidden = false;
    document.body.classList.add("has-sticky");
    let pastHero = false;
    let atEnd = false;
    const update = () => bar.classList.toggle("show", pastHero && !atEnd);
    new IntersectionObserver(([en]) => {
      pastHero = !en.isIntersecting && en.boundingClientRect.top < 0;
      update();
    }).observe(heroCtas);
    if (lastCtas) {
      new IntersectionObserver(([en]) => { atEnd = en.isIntersecting; update(); }).observe(lastCtas);
    }
  }

  // Copy the page's address (its canonical URL, without any tracking parameters).
  document.querySelectorAll("[data-copy]").forEach((button) => {
    const status = button.parentElement.querySelector(".copied");
    const label = button.querySelector("span");
    button.addEventListener("click", async () => {
      const url = button.dataset.copy;
      let ok = false;
      try {
        await navigator.clipboard.writeText(url);
        ok = true;
      } catch {
        const field = document.createElement("textarea");
        field.value = url;
        field.setAttribute("readonly", "");
        field.style.position = "absolute";
        field.style.left = "-9999px";
        document.body.appendChild(field);
        field.select();
        try { ok = document.execCommand("copy"); } catch { ok = false; }
        field.remove();
      }
      label.textContent = ok ? T.copied : T.failed;
      if (status) { status.textContent = ok ? `${T.copiedTo} ${url}` : `${T.copyThis} ${url}`; }
      setTimeout(() => { label.textContent = T.copy; }, 2500);
    });
  });
})();
