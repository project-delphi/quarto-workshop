// Tunja explorer (slides/_water.qmd, #water-tunja): dropdowns choose a view (data table,
// summary, distribution, time series, scatter), the variables and the zone. The deck cell
// writes the 28 Tunja rows and every summary statistic into the page as JSON; this script
// only picks, bins and draws them as SVG. No libraries, no network.
(() => {
  const NS = "http://www.w3.org/2000/svg";
  const COLORS = { urban: "#86cce8", rural: "#e9b86e", municipality: "#b8c2cc" };
  const W = 900, H = 300, M = { l: 70, r: 20, t: 14, b: 44 };

  const fmt = (v) => {
    if (v === null || v === undefined || Number.isNaN(v)) return "·";
    const a = Math.abs(v);
    return a >= 1000 ? Math.round(v).toLocaleString("en-US") : String(Math.round(v * 100) / 100);
  };
  const el = (tag, attrs = {}, text) => {
    const e = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v));
    if (text !== undefined) e.textContent = text;
    return e;
  };

  // "Nice" tick positions covering [lo, hi].
  function ticks(lo, hi, count = 5) {
    if (lo === hi) { lo -= 1; hi += 1; }
    const raw = (hi - lo) / count, pow = 10 ** Math.floor(Math.log10(raw));
    const step = [1, 2, 2.5, 5, 10].map((m) => m * pow).find((s) => s >= raw);
    const out = [];
    for (let t = Math.ceil(lo / step) * step; t <= hi + step * 1e-9; t += step) out.push(Math.round(t / step) * step);
    return out;
  }

  function init(root) {
    const data = JSON.parse(root.querySelector("script[type='application/json']").textContent);
    const $ = (s) => root.querySelector(s);
    const [view, xvar, yvar, zone] = ["view", "x", "y", "zone"].map((n) => $(`[name=${n}]`));
    const out = $(".tj-out"), note = $(".tj-note");
    const info = Object.fromEntries(data.vars.map((v) => [v.key, v]));

    // Series (one per zone, or one for the municipality) for the chosen variables.
    function series(keys) {
      const municipal = keys.every((k) => info[k].level === "municipal");
      const zones = municipal ? ["urban"] : zone.value === "both" ? ["urban", "rural"] : [zone.value];
      return zones.map((z) => ({
        name: municipal ? "municipality" : z,
        rows: data.rows.filter((r) => r.zone === z),
      }));
    }
    const colour = (s) => COLORS[s.name];

    function table() {
      const rows = data.rows.filter((r) => zone.value === "both" || r.zone === zone.value);
      const head = ["year", "zone", ...data.vars.map((v) => v.key)];
      const t = document.createElement("table");
      t.className = "tj-table";
      t.innerHTML = `<thead><tr>${head.map((h) => `<th title="${info[h]?.label ?? ""}">${h}</th>`).join("")}</tr></thead>` +
        `<tbody>${rows.map((r) => `<tr>${head.map((h) => `<td>${h === "zone" ? r.zone : fmt(r[h])}</td>`).join("")}</tr>`).join("")}</tbody>`;
      const wrap = document.createElement("div");
      wrap.className = "tj-scroll";
      wrap.append(t);
      out.replaceChildren(wrap);
      note.textContent = `📋 ${rows.length} rows of water_municipal.csv: Tunja (DIVIPOLA 15001), 2010–2023 · · = missing · hover a header for its meaning`;
    }

    function summary() {
      const keys = data.vars.map((v) => v.key);
      const z = zone.value;
      const t = document.createElement("table");
      t.className = "tj-table";
      t.innerHTML = "<thead><tr><th>variable</th><th>n</th><th>missing</th><th>mean</th><th>sd</th><th>min</th><th>median</th><th>max</th></tr></thead><tbody>" +
        keys.map((k) => {
          const s = data.summary[k][z];
          return `<tr><td title="${info[k].label}">${k}</td><td>${s.n}</td><td>${s.missing}</td><td>${fmt(s.mean)}</td><td>${fmt(s.sd)}</td><td>${fmt(s.min)}</td><td>${fmt(s.median)}</td><td>${fmt(s.max)}</td></tr>`;
        }).join("") + "</tbody>";
      const wrap = document.createElement("div");
      wrap.className = "tj-scroll";
      wrap.append(t);
      out.replaceChildren(wrap);
      note.textContent = `🧮 ${z === "both" ? "urban and rural rows pooled (28 rows)" : `${z} rows (14 years)`} · a municipality-level variable repeats in both zones, so it is counted once (14 years)`;
    }

    function svg(label) {
      const s = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": label, class: "tj-svg" });
      out.replaceChildren(s);
      return s;
    }
    function axes(s, xs, ys, xlabel, ylabel, xticks, yticks, fx = fmt) {
      s.append(el("line", { x1: M.l, y1: H - M.b, x2: W - M.r, y2: H - M.b, class: "ax" }),
        el("line", { x1: M.l, y1: M.t, x2: M.l, y2: H - M.b, class: "ax" }));
      xticks.forEach((t) => {
        s.append(el("line", { x1: xs(t), y1: H - M.b, x2: xs(t), y2: H - M.b + 5, class: "ax" }),
          el("text", { x: xs(t), y: H - M.b + 22, "text-anchor": "middle" }, fx(t)));
      });
      yticks.forEach((t) => {
        s.append(el("line", { x1: M.l - 5, y1: ys(t), x2: W - M.r, y2: ys(t), class: "grid" }),
          el("text", { x: M.l - 9, y: ys(t) + 5, "text-anchor": "end" }, fmt(t)));
      });
      s.append(el("text", { x: (M.l + W - M.r) / 2, y: H - 4, "text-anchor": "middle", class: "lab" }, xlabel),
        el("text", { x: 14, y: (M.t + H - M.b) / 2, "text-anchor": "middle", class: "lab", transform: `rotate(-90 14 ${(M.t + H - M.b) / 2})` }, ylabel));
    }
    function legend(s, list) {
      list.forEach((it, i) => {
        s.append(el("circle", { cx: W - M.r - 90, cy: M.t + 8 + i * 20, r: 6, fill: colour(it) }),
          el("text", { x: W - M.r - 78, y: M.t + 13 + i * 20 }, it.name));
      });
    }
    const span = (vals) => {
      const lo = Math.min(...vals), hi = Math.max(...vals), pad = (hi - lo || 1) * 0.08;
      return [lo - pad, hi + pad];
    };

    function distribution() {
      const k = xvar.value, list = series([k]);
      const vals = list.flatMap((s) => s.rows.map((r) => r[k]).filter((v) => v !== null));
      const s = svg(`Histogram and box plot of ${info[k].label}, Tunja`);
      if (!vals.length) { s.append(el("text", { x: W / 2, y: H / 2, "text-anchor": "middle" }, "no values")); note.textContent = ""; return; }
      const lo = Math.min(...vals), hi = Math.max(...vals);
      const nb = Math.min(10, Math.max(4, Math.ceil(Math.sqrt(vals.length))));
      const w = (hi - lo || 1) / nb;
      const bins = list.map((ser) => {
        const c = Array(nb).fill(0);
        ser.rows.forEach((r) => { if (r[k] !== null) c[Math.min(nb - 1, Math.floor((r[k] - lo) / w))]++; });
        return c;
      });
      const ymax = Math.max(...bins.flat(), 1);
      const [a, b] = span([lo, hi]);
      const xs = (v) => M.l + ((v - a) / (b - a)) * (W - M.l - M.r);
      const top = M.t, bot = 168, ys = (v) => bot - (v / ymax) * (bot - top);
      axes(s, xs, ys, info[k].label, "years", ticks(lo, hi), ticks(0, ymax, 3).filter(Number.isInteger));
      bins.forEach((c, j) => c.forEach((n, i) => {
        if (!n) return;
        const x0 = xs(lo + i * w), x1 = xs(lo + (i + 1) * w), bw = (x1 - x0) / list.length;
        s.append(el("rect", { x: x0 + j * bw + 1, y: ys(n), width: Math.max(1, bw - 2), height: bot - ys(n), fill: colour(list[j]), opacity: 0.85 }));
      }));
      // Box plots (whiskers = min and max, the data are only 14 years): median line, box = quartiles.
      list.forEach((ser, j) => {
        const st = data.summary[k][ser.name === "municipality" ? "both" : ser.name];
        if (st.n === 0) return;
        const y = 200 + j * 26;
        s.append(el("line", { x1: xs(st.min), x2: xs(st.max), y1: y, y2: y, stroke: colour(ser), "stroke-width": 2 }),
          el("rect", { x: xs(st.q1), y: y - 8, width: Math.max(2, xs(st.q3) - xs(st.q1)), height: 16, fill: "none", stroke: colour(ser), "stroke-width": 2 }),
          el("line", { x1: xs(st.median), x2: xs(st.median), y1: y - 8, y2: y + 8, stroke: "#f0f0f0", "stroke-width": 3 }));
      });
      legend(s, list);
      note.textContent = `📊 ${vals.length} values · bars count years · box = quartiles, white line = median, whiskers = min and max`;
    }

    function timeSeries() {
      const k = xvar.value, list = series([k]);
      const vals = list.flatMap((s) => s.rows.map((r) => r[k]).filter((v) => v !== null));
      const s = svg(`${info[k].label} by year, Tunja`);
      if (!vals.length) { s.append(el("text", { x: W / 2, y: H / 2, "text-anchor": "middle" }, "no values")); note.textContent = ""; return; }
      const y0 = data.years[0], y1 = data.years[data.years.length - 1];
      const xs = (v) => M.l + 12 + ((v - y0) / (y1 - y0)) * (W - M.l - M.r - 24);
      const [a, b] = span(vals);
      const ys = (v) => H - M.b - ((v - a) / (b - a)) * (H - M.b - M.t);
      axes(s, xs, ys, "year", info[k].label, data.years.filter((y) => (y - y0) % 2 === 0), ticks(a, b), String);
      list.forEach((ser) => {
        // Draw runs of consecutive years; a missing year breaks the line.
        let run = [];
        const flush = () => {
          if (run.length > 1) s.append(el("polyline", { points: run.map((r) => `${xs(r.year)},${ys(r[k])}`).join(" "), fill: "none", stroke: colour(ser), "stroke-width": 3 }));
          run = [];
        };
        ser.rows.forEach((r) => { if (r[k] === null) flush(); else run.push(r); });
        flush();
        ser.rows.filter((r) => r[k] !== null).forEach((r) => {
          const c = el("circle", { cx: xs(r.year), cy: ys(r[k]), r: 5, fill: colour(ser) });
          c.append(el("title", {}, `${r.year}: ${fmt(r[k])}`));
          s.append(c);
        });
      });
      legend(s, list);
      note.textContent = `📈 one point per year · a gap is a missing year, not a zero ${info[k].level === "municipal" ? "· municipality-level: one value per year" : ""}`;
    }

    function scatter() {
      const kx = xvar.value, ky = yvar.value, list = series([kx, ky]);
      const s = svg(`Scatter plot of ${info[ky].label} against ${info[kx].label}, Tunja`);
      const pts = list.flatMap((ser) => ser.rows.filter((r) => r[kx] !== null && r[ky] !== null).map((r) => ({ ser, r })));
      if (!pts.length) { s.append(el("text", { x: W / 2, y: H / 2, "text-anchor": "middle" }, "no years with both values")); note.textContent = ""; return; }
      const [ax, bx] = span(pts.map((p) => p.r[kx])), [ay, by] = span(pts.map((p) => p.r[ky]));
      const xs = (v) => M.l + ((v - ax) / (bx - ax)) * (W - M.l - M.r);
      const ys = (v) => H - M.b - ((v - ay) / (by - ay)) * (H - M.b - M.t);
      axes(s, xs, ys, info[kx].label, info[ky].label, ticks(ax, bx), ticks(ay, by));
      pts.forEach(({ ser, r }) => {
        const c = el("circle", { cx: xs(r[kx]), cy: ys(r[ky]), r: 6, fill: colour(ser), opacity: 0.9 });
        c.append(el("title", {}, `${r.year}: ${fmt(r[kx])}, ${fmt(r[ky])}`));
        s.append(c, el("text", { x: xs(r[kx]) + 9, y: ys(r[ky]) - 7, class: "yr" }, `'${String(r.year).slice(2)}`));
      });
      legend(s, list);
      note.textContent = `🔵 ${pts.length} years with both values · each point is one year ('15 = 2015) · a pattern across years is not a cause`;
    }

    function draw() {
      yvar.disabled = view.value !== "scatter";
      $(".tj-y").hidden = view.value !== "scatter";
      $(".tj-x").hidden = ["table", "summary"].includes(view.value);
      $(".tj-xl").textContent = view.value === "scatter" ? "x" : "variable";
      ({ table, summary, distribution, series: timeSeries, scatter })[view.value]();
    }
    yvar.value = "infant_mortality";
    [view, xvar, yvar, zone].forEach((c) => c.addEventListener("change", draw));
    draw();
  }
  document.querySelectorAll(".tunja").forEach(init);
})();
