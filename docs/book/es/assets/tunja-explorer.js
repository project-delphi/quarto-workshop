// Tunja explorer (slides/_water.qmd, #water-tunja): dropdowns choose a view (data table,
// summary, distribution, time series, scatter), the variables and the zone. The deck cell
// writes the 28 Tunja rows, every summary statistic, each variable's level, decimals and
// caveats into the page as JSON; this script only picks, bins and draws them as SVG.
// No libraries, no network. Numbers never get thousands separators ("2011", "172548").
(() => {
  const NS = "http://www.w3.org/2000/svg";
  const COLORS = { urban: "#86cce8", rural: "#e9b86e", municipality: "#b8c2cc" };
  const W = 900, H = 300, M = { l: 74, r: 20, t: 30, b: 44 };

  // Fixed decimals, never a thousands separator.
  const num = (v, dp) => (v === null || v === undefined || Number.isNaN(v) ? "·" : v.toFixed(dp));
  const el = (tag, attrs = {}, text) => {
    const e = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v));
    if (text !== undefined) e.textContent = text;
    return e;
  };

  const decimals = (step) => {
    for (let d = 0; d < 4; d++) if (Math.abs(step * 10 ** d - Math.round(step * 10 ** d)) < 1e-9) return d;
    return 3;
  };
  // A "nice" step (1, 2, 2.5, 5 x 10^n) giving about `count` intervals over [lo, hi].
  function niceStep(lo, hi, count) {
    const raw = (hi - lo || 1) / count, pow = 10 ** Math.floor(Math.log10(raw));
    return [1, 2, 2.5, 5, 10].map((m) => m * pow).find((s) => s >= raw * (1 - 1e-9));
  }
  // Tick positions covering [lo, hi] and how to print them.
  function ticks(lo, hi, count = 5) {
    const step = niceStep(lo, hi, count), vals = [], dp = decimals(step);
    for (let t = Math.ceil(lo / step - 1e-9) * step; t <= hi + step * 1e-9; t += step) vals.push(Math.round(t / step) * step);
    if (!vals.length) vals.push(lo);
    return { vals, f: (v) => v.toFixed(dp) };
  }

  function init(root) {
    const data = JSON.parse(root.querySelector("script[type='application/json']").textContent);
    const $ = (s) => root.querySelector(s);
    const [view, xvar, yvar, zone] = ["view", "x", "y", "zone"].map((n) => $(`[name=${n}]`));
    const out = $(".tj-out"), note = $(".tj-note");
    const info = Object.fromEntries(data.vars.map((v) => [v.key, v]));
    const statDp = (k) => (info[k].dp === 0 ? 0 : Math.min(info[k].dp + 1, 2));
    const years = data.years, y0 = years[0], y1 = years[years.length - 1];

    // Series (one per zone, or one for the municipality) for the chosen variables.
    function series(keys) {
      const municipal = keys.every((k) => info[k].level === "municipal");
      const zones = municipal ? ["urban"] : zone.value === "both" ? ["urban", "rural"] : [zone.value];
      return zones.map((z) => ({
        name: municipal ? "municipality" : z,
        text: municipal ? "whole municipality" : z,
        rows: data.rows.filter((r) => r.zone === z),
      }));
    }
    const colour = (s) => COLORS[s.name];
    const caveats = (keys) => [...new Set(keys.map((k) => info[k].note).filter(Boolean))].map((t) => ` · ⚠️ ${t}`).join("");
    const suspect = (k, r) => r[k] === 0 && info[k].suspect.includes(r.year);
    const fixedBar = (k) => info[k].level === "fixed";

    function scrollTable(html) {
      const t = document.createElement("table");
      t.className = "tj-table";
      t.innerHTML = html;
      const wrap = document.createElement("div");
      wrap.className = "tj-scroll";
      wrap.append(t);
      out.replaceChildren(wrap);
    }

    function table() {
      const rows = data.rows.filter((r) => zone.value === "both" || r.zone === zone.value);
      const head = ["year", "zone", ...data.vars.map((v) => v.key)];
      const cell = (r, h) => {
        if (h === "year") return `<td>${r.year}</td>`;
        if (h === "zone") return `<td>${r.zone}</td>`;
        const v = info[h];
        // Grey = a value repeated from another row (municipal: rural copies urban; fixed: every year after the first).
        const rep = (v.level === "municipal" && r.zone === "rural" && zone.value === "both") || (v.level === "fixed" && r.year !== y0);
        const warn = suspect(h, r) ? ' title="reported as 0, probably not reported"' : "";
        return `<td${rep ? ' class="rep"' : ""}${warn}>${num(r[h], v.dp)}${warn ? " ⚠️" : ""}</td>`;
      };
      scrollTable(`<thead><tr>${head.map((h) => `<th title="${info[h]?.label ?? ""}">${h}</th>`).join("")}</tr></thead>` +
        `<tbody>${rows.map((r) => `<tr>${head.map((h) => cell(r, h)).join("")}</tr>`).join("")}</tbody>`);
      note.textContent = `📋 ${rows.length} rows of water_municipal.csv: Tunja (DIVIPOLA 15001), ${y0}–${y1} · · = missing · grey = value repeated from another row · ⚠️ = reported as 0, probably not reported · hover a header for its meaning`;
    }

    function summary() {
      const z = zone.value, lines = [];
      data.vars.forEach((v) => {
        const sm = data.summary[v.key];
        const scopes = v.level === "municipal" ? ["municipal"] : z === "both" ? ["urban", "rural"] : [z];
        scopes.forEach((sc) => lines.push([v, sc, sm[sc]]));
      });
      scrollTable("<thead><tr><th>variable</th><th>zone</th><th>n</th><th>missing</th><th>mean</th><th>sd</th><th>min</th><th>median</th><th>max</th></tr></thead><tbody>" +
        lines.map(([v, sc, s]) => {
          const f = (x) => num(x, statDp(v.key));
          return `<tr><td title="${v.label}">${v.key}</td><td>${sc}</td><td>${s.n}</td><td>${s.missing}</td><td>${f(s.mean)}</td><td>${f(s.sd)}</td><td>${f(s.min)}</td><td>${f(s.median)}</td><td>${f(s.max)}</td></tr>`;
        }).join("") + "</tbody>");
      note.textContent = "🧮 n = years with a value · urban and rural are never pooled · a municipal variable has one value per year (one row) · IPM is one census value per zone (n = 1, no sd)";
    }

    function svg(label) {
      const s = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": label, class: "tj-svg" });
      out.replaceChildren(s);
      return s;
    }
    function message(s, lines, caption) {
      lines.forEach((t, i) => s.append(el("text", { x: W / 2, y: H / 2 - 12 + i * 24, "text-anchor": "middle" }, t)));
      note.textContent = caption || "";
    }
    // xt / yt: { vals, f }. Pass an empty yt.vals for no y gridlines.
    function axes(s, xs, ys, xlabel, ylabel, xt, yt) {
      s.append(el("line", { x1: M.l, y1: H - M.b, x2: W - M.r, y2: H - M.b, class: "ax" }),
        el("line", { x1: M.l, y1: M.t, x2: M.l, y2: H - M.b, class: "ax" }));
      xt.vals.forEach((t) => {
        s.append(el("line", { x1: xs(t), y1: H - M.b, x2: xs(t), y2: H - M.b + 5, class: "ax" }),
          el("text", { x: xs(t), y: H - M.b + 22, "text-anchor": "middle" }, xt.f(t)));
      });
      yt.vals.forEach((t) => {
        s.append(el("line", { x1: M.l - 5, y1: ys(t), x2: W - M.r, y2: ys(t), class: "grid" }),
          el("text", { x: M.l - 9, y: ys(t) + 5, "text-anchor": "end" }, yt.f(t)));
      });
      const mid = (M.t + H - M.b) / 2;
      s.append(el("text", { x: (M.l + W - M.r) / 2, y: H - 4, "text-anchor": "middle", class: "lab" }, xlabel),
        el("text", { x: 14, y: mid, "text-anchor": "middle", class: "lab", transform: `rotate(-90 14 ${mid})` }, ylabel));
    }
    // One row above the plot: a coloured dot and a name per series.
    function legend(s, list) {
      list.forEach((it, i) => {
        const x = M.l + i * 190;
        s.append(el("circle", { cx: x, cy: 11, r: 6, fill: colour(it) }), el("text", { x: x + 12, y: 16 }, it.text));
      });
    }
    const span = (vals) => {
      const lo = Math.min(...vals), hi = Math.max(...vals), pad = (hi - lo || 1) * 0.08;
      return [lo - pad, hi + pad];
    };

    // A variable with one value per zone has no trend or spread: draw the values themselves.
    function fixedBars(k) {
      const zs = zone.value === "both" ? ["urban", "rural"] : [zone.value];
      const vals = zs.map((z) => ({ z, v: data.summary[k][z].min })).filter((p) => p.v !== null);
      if (!vals.length) return message(svg(`${info[k].label}, Tunja`), ["no value"]);
      const s = svg(`${info[k].label}: ${vals.map((p) => `${p.z} ${num(p.v, info[k].dp)}`).join(", ")}, Tunja`);
      const dom = Math.max(...vals.map((p) => p.v)) * 1.12, xt = ticks(0, dom, 5);
      const xs = (v) => M.l + (v / dom) * (W - M.l - M.r);
      const rowH = 70, y = (i) => 50 + i * rowH;
      axes(s, xs, () => 0, info[k].short, "", xt, { vals: [], f: String });
      vals.forEach((p, i) => {
        s.append(el("rect", { x: M.l, y: y(i), width: Math.max(1, xs(p.v) - M.l), height: 42, fill: COLORS[p.z] }),
          el("text", { x: M.l + 8, y: y(i) + 27, class: "bar" }, p.z),
          el("text", { x: xs(p.v) + 8, y: y(i) + 27 }, num(p.v, info[k].dp)));
      });
      note.textContent = `💸 ${info[k].short} is one census value per zone, repeated in every year: no trend or spread to plot, so the chart shows the values${caveats([k])}`;
    }

    function distribution() {
      const k = xvar.value;
      if (fixedBar(k)) return fixedBars(k);
      const list = series([k]);
      const vals = list.flatMap((s) => s.rows.map((r) => r[k]).filter((v) => v !== null));
      const s = svg(`Histogram and dot plot of ${info[k].label}, Tunja`);
      if (!vals.length) return message(s, ["no values"]);
      // Bins start and end on tick values, so every bar edge is a labelled value.
      const step = niceStep(Math.min(...vals), Math.max(...vals), Math.min(10, Math.max(4, Math.ceil(Math.sqrt(vals.length)))));
      const lo = Math.floor(Math.min(...vals) / step + 1e-9) * step;
      const nb = Math.max(1, Math.round((Math.ceil(Math.max(...vals) / step - 1e-9) * step - lo) / step));
      const hi = lo + nb * step;
      const bins = list.map((ser) => {
        const c = Array(nb).fill(0);
        ser.rows.forEach((r) => { if (r[k] !== null) c[Math.min(nb - 1, Math.floor((r[k] - lo) / step + 1e-9))]++; });
        return c;
      });
      const ymax = Math.max(...bins.flat(), 2);
      const xs = (v) => M.l + ((v - lo) / (hi - lo)) * (W - M.l - M.r);
      const top = 28 + 24 * list.length, bot = H - M.b, ys = (v) => bot - (v / ymax) * (bot - top);
      const dp = decimals(step);
      const xt = { vals: Array.from({ length: nb + 1 }, (_, i) => lo + i * step), f: (v) => v.toFixed(dp) };
      const yt = ticks(0, ymax, 3);
      yt.vals = yt.vals.filter(Number.isInteger);
      axes(s, xs, ys, info[k].short, "years", xt, { vals: yt.vals, f: String });
      bins.forEach((c, j) => c.forEach((n, i) => {
        if (!n) return;
        const x0 = xs(lo + i * step), x1 = xs(lo + (i + 1) * step), bw = (x1 - x0) / list.length;
        s.append(el("rect", { x: x0 + j * bw + 1, y: ys(n), width: Math.max(1, bw - 2), height: bot - ys(n), fill: colour(list[j]), opacity: 0.85 }));
      }));
      // Above the bars, one row per series: every year as a dot; with 5 or more values also a box
      // (quartiles, white median line, whiskers = min and max; fewer values make quartiles meaningless).
      list.forEach((ser, j) => {
        const key = ser.name === "municipality" ? "municipal" : ser.name, st = data.summary[k][key];
        const y = M.t + 4 + j * 24;
        if (list.length > 1) s.append(el("text", { x: M.l - 9, y: y + 5, "text-anchor": "end", fill: colour(ser) }, ser.text));
        if (st.n >= 5) {
          s.append(el("line", { x1: xs(st.min), x2: xs(st.max), y1: y, y2: y, stroke: colour(ser), "stroke-width": 2 }),
            el("rect", { x: xs(st.q1), y: y - 8, width: Math.max(2, xs(st.q3) - xs(st.q1)), height: 16, fill: "none", stroke: colour(ser), "stroke-width": 2 }),
            el("line", { x1: xs(st.median), x2: xs(st.median), y1: y - 8, y2: y + 8, stroke: "#f0f0f0", "stroke-width": 3 }));
        }
        ser.rows.filter((r) => r[k] !== null).forEach((r) => {
          const c = el("circle", { cx: xs(r[k]), cy: y, r: 3.5, fill: colour(ser), stroke: "#191919" });
          c.append(el("title", {}, `${r.year}: ${num(r[k], info[k].dp)}`));
          s.append(c);
        });
      });
      note.textContent = `📊 ${vals.length} values · bars count years per value range${list.length > 1 ? " (urban | rural side by side)" : ""} · dots = years${vals.length >= 5 ? ", box = quartiles, white line = median, whiskers = min and max" : ""}${caveats([k])}`;
    }

    function timeSeries() {
      const k = xvar.value;
      if (fixedBar(k)) return fixedBars(k);
      const list = series([k]), v = info[k];
      const vals = list.flatMap((s) => s.rows.map((r) => r[k]).filter((x) => x !== null));
      const s = svg(`${v.label} by year, Tunja`);
      if (!vals.length) return message(s, ["no values"]);
      const xs = (x) => M.l + 12 + ((x - y0) / (y1 - y0)) * (W - M.l - M.r - 24);
      const [a, b] = span(vals);
      const ys = (x) => H - M.b - ((x - a) / (b - a)) * (H - M.b - M.t);
      axes(s, xs, ys, "year", v.short, { vals: years, f: String }, ticks(a, b));
      const breaks = v.breaks || [];
      breaks.forEach(([yr, label]) => {
        if (!label) return; // an unlabelled break only ends the line (2021 follows 2020's own regime)
        const x = xs(yr - 0.5);
        s.append(el("line", { x1: x, x2: x, y1: M.t, y2: H - M.b, class: "brk" }),
          el("text", { x: x + 5, y: M.t - 6, class: "brk-t" }, label));
      });
      list.forEach((ser) => {
        // Lines join consecutive years only: a missing year, a suspect 0 or a method change breaks the line.
        let run = [];
        const flush = () => {
          if (run.length > 1) s.append(el("polyline", { points: run.map((r) => `${xs(r.year)},${ys(r[k])}`).join(" "), fill: "none", stroke: colour(ser), "stroke-width": 3 }));
          run = [];
        };
        ser.rows.forEach((r) => {
          if (breaks.some(([yr]) => yr === r.year)) flush();
          if (r[k] === null || suspect(k, r)) flush(); else run.push(r);
        });
        flush();
        ser.rows.filter((r) => r[k] !== null).forEach((r) => {
          const hollow = suspect(k, r);
          const c = el("circle", { cx: xs(r.year), cy: ys(r[k]), r: 5, fill: hollow ? "#191919" : colour(ser), stroke: colour(ser), "stroke-width": hollow ? 2.5 : 0 });
          c.append(el("title", {}, `${r.year}: ${num(r[k], v.dp)}`));
          s.append(c);
        });
      });
      legend(s, list);
      note.textContent = `📈 one point per year · a gap is a missing year, not a zero${v.level === "municipal" ? " · municipality-wide: one value per year" : ""}${caveats([k])}`;
    }

    function scatter() {
      const kx = xvar.value, ky = yvar.value;
      const s = svg(`Scatter plot of ${info[ky].label} against ${info[kx].label}, Tunja`);
      if (kx === ky) return message(s, ["x and y are the same variable:", "every point would sit on a diagonal. Pick two different ones."]);
      const fixed = [kx, ky].find(fixedBar);
      if (fixed) return message(s, [`${info[fixed].short} has one value per zone, the same in every year,`, "so it cannot move with another variable. Pick one that changes by year."]);
      const list = series([kx, ky]);
      const pts = list.flatMap((ser) => ser.rows.filter((r) => r[kx] !== null && r[ky] !== null).map((r) => ({ ser, r })));
      if (!pts.length) return message(s, ["no year has both values"], "🔵 the two variables are never published in the same year");
      const [ax, bx] = span(pts.map((p) => p.r[kx])), [ay, by] = span(pts.map((p) => p.r[ky]));
      const xs = (v) => M.l + ((v - ax) / (bx - ax)) * (W - M.l - M.r);
      const ys = (v) => H - M.b - ((v - ay) / (by - ay)) * (H - M.b - M.t);
      axes(s, xs, ys, info[kx].short, info[ky].short, ticks(ax, bx), ticks(ay, by));
      pts.forEach(({ ser, r }) => {
        const hollow = suspect(kx, r) || suspect(ky, r);
        const c = el("circle", { cx: xs(r[kx]), cy: ys(r[ky]), r: 6, fill: hollow ? "#191919" : colour(ser), stroke: colour(ser), "stroke-width": hollow ? 2.5 : 0, opacity: 0.9 });
        c.append(el("title", {}, `${r.year}: ${num(r[kx], info[kx].dp)}, ${num(r[ky], info[ky].dp)}`));
        s.append(c, el("text", { x: xs(r[kx]) + 9, y: ys(r[ky]) - 7, class: "yr" }, `'${String(r.year).slice(2)}`));
      });
      legend(s, list);
      note.textContent = `🔵 ${pts.length} ${pts.length === 1 ? "year" : "years"} with both values · each point is one year ('15 = 2015) · a pattern across years is not a cause${caveats([kx, ky])}`;
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
