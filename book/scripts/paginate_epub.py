"""Lay the EPUB out page by page, as e-readers do, and report what does not fit a page
(PLAN-improvement.md §3.1; budgets and exceptions in pagefit.yml).

E-readers such as Apple Books and Readium-based apps (Thorium) paginate a chapter by setting it
in CSS columns one screen wide and one screen tall. This script does the same in Chrome, through
Playwright, with the book's own epub.css: it unzips the EPUB, opens each chapter at a reading
profile (screen size and text size), measures each *unit* (the smallest piece the stylesheet
keeps whole: a table, figure, image, quote, code block, aside, card, half of a Pause and think,
part of an agent box, item of an opener or key ideas) at its natural height, then sets the
chapter in columns and records which pages each unit's fragments fall on.

It reports, per profile:
- units split over two or more pages (a failure at a gating profile);
- units taller than their budget (pagefit.yml `budgets`; a failure);
- pages left more than a third blank because a unit was pushed whole to the next page, with
  the unit that pushed (headings travel with the unit after them);
- walls: three or more pages in a row with no figure, table, box, quote or code;
- images: their scale on the page, whether a height cap shrank them, and, for screenshots whose
  text size at capture pagefit.yml lists, the text size a reader sees.

    uv run --with playwright python scripts/paginate_epub.py _book/epub/prompt-check-publish.epub
    uv run --with playwright python scripts/paginate_epub.py EPUB --only chapters/slides.qmd ch019
    uv run --with playwright python scripts/paginate_epub.py EPUB --report-only --no-shots

It writes _book/pages/<edition>.json, a Markdown report beside it, and a picture of the page
where each failing unit starts (phone, 16 px) under _book/pages/<edition>-shots/. It exits
non-zero if any unit fails at a gating profile and is not listed under `exceptions`, unless
--report-only is given. The fonts are the ones epub.css names (Charter, Avenir Next), which macOS
has; elsewhere Chrome substitutes others and the pages differ, so CI runs it report-only.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright


@dataclass(frozen=True)
class Profile:
    width: int
    height: int
    font: int  # the reader's text size, in CSS px
    side: int  # left and right margin
    top: int  # top and bottom margin (readers keep room for a running head and page number)
    gate: bool  # a split here fails the check

    @property
    def page_height(self) -> int:
        return self.height - 2 * self.top


PROFILES = {
    "phone16": Profile(390, 844, 16, 20, 44, gate=True),
    # Spanish runs about 10% longer; English that fits at 19 px leaves Spanish room at 18 px.
    "phone19": Profile(390, 844, 19, 20, 44, gate=True),
    "tablet18": Profile(820, 1180, 18, 64, 56, gate=True),
    "phone18": Profile(390, 844, 18, 20, 44, gate=False),
    "phone20": Profile(390, 844, 20, 20, 44, gate=False),
}
BUDGET_PROFILE = "phone16"
TABLET_PROFILE = "tablet18"

# Units: the smallest pieces the stylesheet keeps whole. A unit inside another is not counted.
UNITS = ", ".join([
    "figure", "table", "img", "blockquote", "div.sourceCode", "pre", ".transcript",
    "div.callout", ".live-link", ".done", ".catchup",
    ".think > .think-question", ".think > .think-answer",
    ".opener > ul > li", ".opener > .opener-meta", ".keyideas > ul > li",
    ".cards > .card", ".story",
])
AGENT_BOX = {"parts": ".agent-box > div", "whole": ".agent-box"}
# Boxes that count as a break in the text even where their units are small.
VISUAL = "figure, table, img, blockquote, pre, .agent-box, div.callout, .think, .opener, " \
         ".keyideas, .live-link, .done, .catchup, .cards, .story"

READER_CSS = """
:root, body {{ font-size: {font}px !important; }}
html {{ margin: 0 !important; padding: 0 {side}px !important; }}
body {{ margin: 0 !important; max-width: none !important; }}
"""
COLUMNS_CSS = """
html {{ height: {height}px !important; box-sizing: border-box !important;
  padding: {top}px {side}px !important; column-width: {colwidth}px !important;
  column-gap: {gap}px !important; column-fill: auto !important; overflow: visible !important; }}
"""

MARK_UNITS = """(sel) => {
  const found = [...document.querySelectorAll(sel)];
  const set = new Set(found);
  const units = found.filter(e => { for (let p = e.parentElement; p; p = p.parentElement)
    if (set.has(p)) return false; return true; });
  return units.map((e, i) => { e.setAttribute('data-unit', i); return e.getBoundingClientRect().height; });
}"""

MEASURE = """([side, W, top, pageH, visualSel]) => {
  // A page is one column; text can start anywhere along a line, so take the column the
  // fragment's left edge lies in.
  const col = r => Math.floor((r.left - side + 2) / W);
  const rects = e => [...e.getClientRects()].filter(r => r.height > 1 && r.width > 1);
  const fill = {}, visual = new Set(); let last = 0;
  const grow = r => { const c = col(r); last = Math.max(last, c); fill[c] = Math.max(fill[c] || 0, r.bottom - top); };
  // Text, line by line, and replaced elements: what a reader sees on each page.
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const range = document.createRange();
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    if (!/\\S/.test(n.nodeValue)) continue;
    range.selectNodeContents(n);
    for (const r of range.getClientRects()) if (r.height > 1) grow(r);
  }
  for (const e of document.querySelectorAll('img, svg, math, hr')) rects(e).forEach(grow);
  for (const e of document.querySelectorAll(visualSel)) rects(e).forEach(r => visual.add(col(r)));

  const kind = e => {
    const tag = e.tagName.toLowerCase();  // XHTML keeps tag names in lower case
    if (e.matches('.agent-box > .prompt, .agent-box')) return 'prompt';
    if (tag === 'table' || (tag === 'figure' && e.querySelector('table'))) return 'table';
    if (tag === 'figure' || tag === 'img') return 'figure';
    if (e.matches('div.sourceCode, pre, .transcript')) return 'code';
    return 'text';
  };
  const name = e => {
    const float = e.closest('[id^="fig-"], [id^="tbl-"], [id^="lst-"]');
    const sec = e.closest('section[id]');
    const cap = e.querySelector('figcaption, caption, .callout-title, .box-label, .think-answer-label');
    const words = ((cap && cap.textContent.trim()) ? cap.textContent : e.textContent || e.getAttribute('alt') || '')
      .trim().replace(/\\s+/g, ' ').slice(0, 70);
    const cls = String(e.className || '').split(' ')[0];
    return {id: float ? float.id : (e.id || ''), section: sec ? sec.id : '',
            what: e.tagName.toLowerCase() + (cls ? '.' + cls : ''), words};
  };
  const units = [...document.querySelectorAll('[data-unit]')].map(e => {
    const rs = rects(e); rs.forEach(r => { const c = col(r); fill[c] = Math.max(fill[c] || 0, r.bottom - top); });
    const cols = [...new Set(rs.map(col))].sort((a, b) => a - b);
    return {i: +e.dataset.unit, kind: kind(e), ...name(e), pages: cols.length,
            start: cols.length ? cols[0] : -1, top: rs.length ? rs[0].top - top : 0};
  });

  // A page left blank at the bottom: who was pushed to the next page? Headings travel with the
  // unit after them (break-after: avoid), so name that unit.
  const heads = [...document.querySelectorAll('h1, h2, h3, h4')].map(h => {
    const r = rects(h)[0]; return r ? {c: col(r), top: r.top - top, words: h.textContent.trim().slice(0, 50)} : null;
  }).filter(Boolean);
  const gaps = [];
  for (let c = 0; c < last; c++) {
    const blank = 1 - Math.min(1, (fill[c] || 0) / pageH);
    if (blank <= 1 / 3) continue;
    const next = units.filter(u => u.start === c + 1).sort((a, b) => a.top - b.top);
    const head = heads.filter(h => h.c === c + 1).sort((a, b) => a.top - b.top)[0];
    let by = 'text (no unit at the top of the next page)';
    const near = 0.25 * pageH;
    if (next.length && next[0].top < near && (!head || next[0].top <= head.top)) by = next[0];
    else if (head && head.top < near) by = next.length ? {heading: head.words, ...next[0]} : {heading: head.words};
    gaps.push({page: c, blank: Math.round(blank * 100), by});
  }
  let run = 0; const walls = [];
  for (let c = 0; c <= last + 1; c++) {
    if (c <= last && !visual.has(c)) { run++; continue; }
    if (run >= 3) walls.push({from: c - run, pages: run}); run = 0;
  }
  const images = [...document.querySelectorAll('img')].map(img => {
    const r = img.getBoundingClientRect(), cs = getComputedStyle(img);
    const fig = img.closest('[id^="fig-"]');
    const cap = parseFloat(cs.maxHeight);
    return {id: fig ? fig.id : '', alt: (img.getAttribute('alt') || '').slice(0, 70),
            natural: [img.naturalWidth, img.naturalHeight], shown: [Math.round(r.width), Math.round(r.height)],
            capped: !isNaN(cap) && Math.abs(r.height - cap) < 1.5};
  });
  const words = (document.body.innerText.match(/\\S+/g) || []).length;
  return {pages: last + 1, units, gaps, walls, images, words};
}"""


def chapter_files(book: Path) -> list[str]:
    """The source file of each chNNN.xhtml, in order (the EPUB profile's chapter list)."""
    profile = yaml.safe_load((book / "_quarto-epub.yml").read_text(encoding="utf-8"))
    return [*profile["book"]["chapters"], *profile["book"].get("appendices", [])]


def epub_language(epub: Path) -> str:
    """The EPUB's dc:language ("en-GB", "es"), from its package file."""
    with zipfile.ZipFile(epub) as z:
        opf = next((n for n in z.namelist() if n.endswith(".opf")), None)
        text = z.read(opf).decode("utf-8") if opf else ""
    start = text.find("<dc:language")
    return text[text.find(">", start) + 1:text.find("</dc:language>", start)].strip() if start >= 0 else ""


def find_book(epub: Path, spanish: bool) -> Path:
    """The book project whose chapter list the EPUB follows: the first folder above the EPUB
    with a _quarto-epub.yml, or, for a Spanish EPUB found under book/ (a store edition is
    made there), its sibling book-es/."""
    for parent in epub.resolve().parents:
        if (parent / "_quarto-epub.yml").exists():
            sibling = parent.with_name(parent.name + "-es")
            return sibling if spanish and not parent.name.endswith("-es") and sibling.exists() else parent
    sys.exit(f"paginate_epub: no _quarto-epub.yml above {epub}; pass --book")


def matches(rule: dict, source: str, unit: dict) -> bool:
    if rule.get("file") not in (source, "*") or rule.get("kind", unit["kind"]) != unit["kind"]:
        return False
    want = str(rule.get("unit", "*"))
    return want == "*" or want in (unit["id"], unit["section"]) or unit["words"].startswith(want)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("epub", type=Path)
    ap.add_argument("--book", type=Path, help="the book project (default: found above the EPUB)")
    ap.add_argument("--only", nargs="*", default=[], help="chNNN names or source files")
    ap.add_argument("--profiles", nargs="*", default=list(PROFILES))
    ap.add_argument("--config", type=Path, help="default: pagefit.yml in book/")
    ap.add_argument("--out", type=Path, help="default: _book/pages in the book project")
    ap.add_argument("--agent-box", choices=list(AGENT_BOX), help="override pagefit.yml")
    ap.add_argument("--extra-css", type=Path, help="a stylesheet added after the book's, to try a change "
                    "before rebuilding (the result is then not the EPUB's)")
    ap.add_argument("--report-only", action="store_true", help="exit 0 whatever is found")
    ap.add_argument("--no-shots", action="store_true", help="skip the pictures of failing pages")
    if "--self-test" in sys.argv:
        self_test()
        return
    args = ap.parse_args()

    spanish = epub_language(args.epub).startswith("es")
    book = (args.book or find_book(args.epub, spanish)).resolve()
    here = Path(__file__).resolve().parents[1]  # book/, where pagefit.yml lives
    config = yaml.safe_load((args.config or here / "pagefit.yml").read_text(encoding="utf-8"))
    budgets = config["budgets"]
    agent_box = args.agent_box or config.get("agent_box", "parts")
    units_sel = f"{UNITS}, {AGENT_BOX[agent_box]}"
    extra = args.extra_css.read_text(encoding="utf-8") if args.extra_css else ""
    sources = chapter_files(book)
    edition = ("es" if spanish else "en") + ("-store" if "store" in args.epub.parts else "")
    out = (args.out or book / "_book" / "pages").resolve()
    shots = out / f"{edition}-shots"
    out.mkdir(parents=True, exist_ok=True)
    if not args.no_shots:
        shots.mkdir(exist_ok=True)
        for old in shots.glob("*.png"):
            old.unlink()

    results: dict = {"edition": edition, "agent_box": agent_box, "chapters": {},
                     **({"extra_css": str(args.extra_css)} if args.extra_css else {})}
    with tempfile.TemporaryDirectory() as tmp:
        zipfile.ZipFile(args.epub).extractall(tmp)
        files = sorted(Path(tmp, "EPUB", "text").glob("ch*.xhtml"))
        if len(files) != len(sources):
            sys.exit(f"paginate_epub: {len(files)} chapter files but {len(sources)} sources in "
                     f"{book / '_quarto-epub.yml'}; rebuild the EPUB")
        pairs = list(zip(files, sources))
        if args.only:
            pairs = [(f, s) for f, s in pairs if any(o in (f.stem, s) or s.endswith(o) for o in args.only)]
            if not pairs:
                sys.exit(f"paginate_epub: nothing matches {args.only}")
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel="chrome")
            for f, source in pairs:
                chapter = results["chapters"].setdefault(f.stem, {"source": source, "profiles": {}})
                for pname in args.profiles:
                    p = PROFILES[pname]
                    page = browser.new_page(viewport={"width": p.width, "height": p.height})
                    page.goto(f.as_uri())
                    page.add_style_tag(content=READER_CSS.format(font=p.font, side=p.side) + extra)
                    page.wait_for_timeout(100)
                    natural = page.evaluate(MARK_UNITS, units_sel)
                    page.add_style_tag(content=COLUMNS_CSS.format(
                        height=p.height, top=p.top, side=p.side, colwidth=p.width - 2 * p.side, gap=2 * p.side))
                    page.wait_for_timeout(100)
                    m = page.evaluate(MEASURE, [p.side, p.width, p.top, p.page_height, VISUAL])
                    for u in m["units"]:
                        u["height"] = round(natural[u["i"]] / p.page_height, 2)
                    chapter["profiles"][pname] = m
                    if pname == BUDGET_PROFILE and not args.no_shots:
                        chapter["_page"] = page  # kept open for the pictures below
                    else:
                        page.close()
                judge(chapter, source, budgets, config)
                page = chapter.pop("_page", None)
                if page:
                    p = PROFILES[BUDGET_PROFILE]
                    for start in sorted({u["start"] for u in chapter["failures"] if u["profile"] == BUDGET_PROFILE
                                         and not u.get("excepted") and u["start"] >= 0}):
                        page.evaluate(f"window.scrollTo({start * p.width}, 0)")
                        page.screenshot(path=str(shots / f"{f.stem}-p{start + 1:02d}.png"))
                    page.close()
            browser.close()

    (out / f"{edition}.json").write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
    report = summarise(results, config, args.profiles)
    (out / f"{edition}.md").write_text(report, encoding="utf-8")
    failures = [u for c in results["chapters"].values() for u in c["failures"] if not u.get("excepted")]
    print(report.split("\n## ")[0])
    print(f"report: {out / f'{edition}.md'}")
    if failures and not args.report_only:
        sys.exit(f"paginate_epub: {len(failures)} unit(s) split or over budget (see the report)")


def judge(chapter: dict, source: str, budgets: dict, config: dict) -> None:
    """Mark each unit that splits at a gating profile, or is over its budget."""
    failures = []
    for pname, m in chapter["profiles"].items():
        p = PROFILES[pname]
        for u in m["units"]:
            why = []
            if p.gate and u["pages"] > 1:
                why.append(f"split over {u['pages']} pages")
            if pname == BUDGET_PROFILE and u["height"] > budgets[u["kind"]]:
                why.append(f"{u['height']:.2f} page, budget {budgets[u['kind']]}")
            if pname == TABLET_PROFILE and u["kind"] == "figure" and u["height"] > budgets["figure_tablet"]:
                why.append(f"{u['height']:.2f} page on a tablet, budget {budgets['figure_tablet']}")
            if why:
                rule = next((r for r in config.get("exceptions") or [] if matches(r, source, u)), None)
                failures.append({**u, "profile": pname, "why": "; ".join(why),
                                 **({"excepted": rule["reason"]} if rule else {})})
    chapter["failures"] = failures


def summarise(results: dict, config: dict, profiles: list[str]) -> str:
    chapters = results["chapters"]
    walls_exempt = set(config.get("walls_exempt") or [])
    shots = config.get("screenshots") or {}
    min_px = config.get("min_text_px", 9)
    lines = [f"# Page fit: {results['edition']} edition", "",
             f"Agent boxes measured as {results['agent_box']}; budgets at {BUDGET_PROFILE}: "
             + ", ".join(f"{k} {v}" for k, v in config["budgets"].items()) + ".", "",
             "Split and Over budget leave out units excepted in pagefit.yml.", "",
             "| Profile | Pages | Units | Split | Over budget | Pages > ⅓ blank | ≥ ½ blank | Walls | Words |",
             "|---|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for pname in profiles:
        ms = [(c, c["profiles"][pname]) for c in chapters.values() if pname in c["profiles"]]
        units = [u for _, m in ms for u in m["units"]]
        rules = config.get("exceptions") or []
        split = sum(u["pages"] > 1 and not any(matches(r, c["source"], u) for r in rules)
                    for c, m in ms for u in m["units"])
        over = [u for c in chapters.values() for u in c["failures"]
                if u["profile"] == pname and "budget" in u["why"] and not u.get("excepted")]
        gaps = [g for _, m in ms for g in m["gaps"]]
        walls = [w for c, m in ms if c["source"] not in walls_exempt for w in m["walls"]]
        lines.append(f"| {pname}{' (gate)' if PROFILES[pname].gate else ''} | {sum(m['pages'] for _, m in ms)} "
                     f"| {len(units)} | {split} | {len(over)} | {len(gaps)} "
                     f"| {sum(g['blank'] >= 50 for g in gaps)} | {len(walls)} | {sum(m['words'] for _, m in ms)} |")
    open_ = [(k, c, u) for k, c in chapters.items() for u in c["failures"] if not u.get("excepted")]
    excepted = [(k, c, u) for k, c in chapters.items() for u in c["failures"] if u.get("excepted")]
    lines += ["", f"Failing units: {len(open_)} (excepted: {len(excepted)}).", ""]

    lines += ["## Failing units", "", "| File | Profile | Unit | Kind | Height | Pages | Why |", "|---|---|---|---|--:|--:|---|"]
    for k, c, u in sorted(open_, key=lambda t: (-t[2]["height"], t[0])):
        lines.append(f"| {c['source']} ({k}) | {u['profile']} | {u['id'] or '#' + u['section']} {u['what']}: "
                     f"{u['words'][:50]} | {u['kind']} | {u['height']:.2f} | {u['pages']} | {u['why']} |")
    if excepted:
        lines += ["", "## Excepted (pagefit.yml)", ""]
        lines += [f"- {c['source']}: {u['words'][:50]} ({u['why']}): {u['excepted']}" for k, c, u in excepted]

    lines += ["", f"## Pages more than a third blank ({BUDGET_PROFILE})", "",
              "| File | Page | Blank | Pushed by |", "|---|--:|--:|---|"]
    for k, c in chapters.items():
        for g in c["profiles"].get(BUDGET_PROFILE, {}).get("gaps", []):
            by = g["by"]
            if isinstance(by, dict):
                by = ((f"heading “{by['heading']}” with " if "heading" in by else "")
                      + (f"{by.get('id') or '#' + by.get('section', '')} {by.get('what', '')} {by.get('height', '')}"
                         if "what" in by else "")).strip()
            lines.append(f"| {c['source']} | {g['page'] + 1} | {g['blank']}% | {by} |")

    lines += ["", f"## Walls: three or more pages with no visual unit ({BUDGET_PROFILE})", ""]
    for k, c in chapters.items():
        for w in c["profiles"].get(BUDGET_PROFILE, {}).get("walls", []):
            note = " (exempt)" if c["source"] in walls_exempt else ""
            lines.append(f"- {c['source']}: pages {w['from'] + 1}–{w['from'] + w['pages']}{note}")

    lines += ["", f"## Images ({BUDGET_PROFILE})", "",
              "Scale is the shown width over the file's width. Text size is listed only for screenshots "
              "whose capture text size pagefit.yml gives.", "",
              "| File | Image | Natural | Shown | Scale | Text on screen | Note |", "|---|---|---|---|--:|--:|---|"]
    for k, c in chapters.items():
        for img in c["profiles"].get(BUDGET_PROFILE, {}).get("images", []):
            if not img["natural"][0]:
                continue
            scale = img["shown"][0] / img["natural"][0]
            key = next((s for s in shots if s in (img["id"],) or img["alt"].startswith(s)), None)
            text = f"{shots[key] * scale:.1f} px" if key else ""
            notes = ["capped by max-height"] if img["capped"] else []
            if key and shots[key] * scale < min_px:
                notes.append(f"text under {min_px} px")
            if notes or key:
                lines.append(f"| {c['source']} | {img['id'] or img['alt'][:40]} | {img['natural'][0]}×{img['natural'][1]} "
                             f"| {img['shown'][0]}×{img['shown'][1]} | {scale:.2f} | {text} | {'; '.join(notes)} |")
    return "\n".join(lines) + "\n"


FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"><head><meta charset="utf-8" />
<title>{name}</title><link rel="stylesheet" type="text/css" href="../styles/stylesheet1.css" /></head>
<body><section class="level1"><h1>Fixture</h1>{body}</section></body></html>"""


def self_test() -> None:
    """Build a two-chapter EPUB: one that fits and one with a table taller than a page and a
    prompt over budget. This script must pass the first and fail the second, naming both."""
    import subprocess

    para = "<p>" + "A sentence of ordinary length for a paragraph of text. " * 6 + "</p>"
    rows = "".join(f"<tr><td>row {i}</td><td>a cell with a few words in it</td></tr>" for i in range(40))
    good = para * 3 + "<figure><table><tr><td>one</td><td>two</td></tr></table></figure>" + para
    bad = (para + '<div id="tbl-tall"><figure><figcaption>Table 1</figcaption><table>' + rows
           + "</table></figure></div>" + para
           + '<div class="agent-box"><div class="prompt"><div class="box-label">Ask</div><pre>'
           + "Do one long thing, then another, and check each. " * 30 + "</pre></div></div>" + para)
    css = Path(__file__).resolve().parents[1] / "styles" / "epub.css"
    with tempfile.TemporaryDirectory() as tmp:
        book = Path(tmp)
        (book / "_quarto-epub.yml").write_text("book:\n  chapters: [good.qmd, bad.qmd]\n")
        epub = book / "fixture.epub"
        with zipfile.ZipFile(epub, "w") as z:
            z.writestr("EPUB/styles/stylesheet1.css", css.read_text(encoding="utf-8"))
            z.writestr("EPUB/text/ch001.xhtml", FIXTURE.format(name="ch001", body=good))
            z.writestr("EPUB/text/ch002.xhtml", FIXTURE.format(name="ch002", body=bad))
        run = [sys.executable, __file__, str(epub), "--book", str(book), "--no-shots", "--out", str(book / "out")]
        ok = subprocess.run([*run, "--only", "good.qmd"], capture_output=True, text=True)
        ko = subprocess.run([*run, "--only", "bad.qmd"], capture_output=True, text=True)
        failed = [u for c in json.loads((book / "out" / "en.json").read_text(encoding="utf-8"))["chapters"].values()
                  for u in c["failures"]]
    problems = []
    if ok.returncode != 0:
        problems.append(f"a chapter that fits failed:\n{ok.stdout}{ok.stderr}")
    if ko.returncode == 0:
        problems.append("a chapter with a table taller than a page passed")
    if not any(u["id"] == "tbl-tall" and "split over" in u["why"] for u in failed):
        problems.append("the table taller than a page was not reported as split")
    if not any(u["kind"] == "prompt" and "budget" in u["why"] for u in failed):
        problems.append("the long prompt was not reported as over its budget")
    if problems:
        sys.exit("paginate_epub self-test failed:\n- " + "\n- ".join(problems))
    print("paginate_epub self-test: a fitting chapter passes; a too-tall table and a long prompt fail")


if __name__ == "__main__":
    main()
