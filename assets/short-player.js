// Opens a YouTube Short in a dialog over the deck (slides/_water.qmd, #water-kmeans) and asks
// the player for Spanish and 0.9x speed. The IFrame Player API (loaded only when the button
// is pressed, so rendering and the deck need no network) documents setPlaybackRate, which
// picks the nearest speed the video offers; it documents no audio-language setting, so the
// audio and caption language are requested with hl / cc_lang_pref and the dubbed audio track
// is switched with getAvailableAudioTracks / setAudioTrack where the player offers them.
// https://developers.google.com/youtube/iframe_api_reference (checked 2026-11-03)
(() => {
  const SPEED = 0.9, LANG = "es";
  let api = null;
  const loadApi = () => api ??= new Promise((resolve) => {
    if (window.YT?.Player) return resolve(window.YT);
    const previous = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => { previous?.(); resolve(window.YT); };
    const tag = document.createElement("script");
    tag.src = "https://www.youtube.com/iframe_api";
    document.head.append(tag);
  });

  function open(id) {
    const dialog = document.createElement("dialog");
    dialog.className = "short-dialog";
    dialog.innerHTML = '<div class="short-frame"><div id="short-player"></div></div>' +
      '<p class="short-info"></p><p class="short-links">' +
      `<a href="https://youtube.com/shorts/${id}" target="_blank" rel="noopener">↗ YouTube</a> · ` +
      '<button type="button" class="short-close">✕ close</button></p>';
    document.body.append(dialog);
    const info = dialog.querySelector(".short-info");
    let player;
    const close = () => { player?.destroy?.(); dialog.close(); dialog.remove(); };
    dialog.querySelector(".short-close").addEventListener("click", close);
    dialog.addEventListener("cancel", (e) => { e.preventDefault(); close(); });
    dialog.addEventListener("click", (e) => { if (e.target === dialog) close(); });
    dialog.showModal();
    info.textContent = "⏳ loading the player …";
    loadApi().then((YT) => {
      player = new YT.Player("short-player", {
        videoId: id, width: "100%", height: "100%",
        playerVars: { hl: LANG, cc_lang_pref: LANG, playsinline: 1, rel: 0, autoplay: 1 },
        events: {
          onReady: (e) => { e.target.setPlaybackRate(SPEED); e.target.playVideo(); },
          onStateChange: (e) => {
            if (e.data !== YT.PlayerState.PLAYING) return;
            const p = e.target, said = [];
            p.setPlaybackRate(SPEED);
            said.push(`speed ${p.getPlaybackRate()}×`);
            try {
              const tracks = p.getAvailableAudioTracks?.() ?? [];
              const spanish = tracks.find((t) => JSON.stringify(t).toLowerCase().includes("spanish") ||
                JSON.stringify(t).toLowerCase().includes('"es'));
              if (spanish) { p.setAudioTrack(spanish); said.push("audio: Spanish"); }
              else said.push(tracks.length ? "no Spanish audio track" : "audio language: use ⚙ → Audio track");
            } catch { said.push("audio language: use ⚙ → Audio track"); }
            info.textContent = said.join(" · ");
          },
        },
      });
    }).catch(() => { info.textContent = "⚠️ the player did not load: use the YouTube link"; });
  }

  document.addEventListener("click", (e) => {
    const button = e.target.closest?.("[data-video]");
    if (button) open(button.dataset.video);
  });
})();
