// The e-book landing page's only script (ebook/index.qmd): drawing on scroll, the clips,
// the sticky bar on phones, copy-link, and a hint for LinkedIn's in-app browser. The page
// works without it: everything is drawn, the clips show their stills, the buttons are links.
(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const canWatch = "IntersectionObserver" in window;

  // LinkedIn's in-app browser may not download files: say what to do instead.
  if (/LinkedInApp/i.test(navigator.userAgent)) {
    document.querySelectorAll(".inapp").forEach((el) => { el.hidden = false; });
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
        button.textContent = paused ? "Pause" : "Play";
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
      label.textContent = ok ? "Link copied" : "Copy failed";
      if (status) { status.textContent = ok ? `Copied ${url}` : `Copy this address: ${url}`; }
      setTimeout(() => { label.textContent = "Copy link"; }, 2500);
    });
  });
})();
