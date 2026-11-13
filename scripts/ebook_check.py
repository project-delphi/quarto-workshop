"""Check the e-book landing page as published: render it first (`make deck`), then

    make ebook-check            # or: uv run --with playwright python scripts/ebook_check.py OUT

It serves docs/ at /quarto-workshop/, as GitHub Pages does, and writes to OUT (default
_ebook-check/, ignored by git):

- screenshots at 375 x 812 and 1440 x 900, in light and dark OS settings, and with reduced
  motion; the phone's first screen, and the sticky bar after scrolling;
- whether the primary download button is on the phone's first screen (and above 640 px, the
  height left in LinkedIn's in-app browser);
- the bytes a phone downloads on first load, and any sideways scrolling;
- every link on the page, on the deck's title and Get the Book slides, and in the website
  edition's sidebar tools: local targets and #anchors must exist in docs/, external ones must
  answer (the EPUB's release link is reported as pending until the release exists);
- the contents' numbers against the website edition's sidebar;
- the share card, drawn as LinkedIn lays it out from the page's Open Graph tags, and the
  JSON-LD, parsed and checked for the fields a Book needs.

It exits non-zero if any check fails.
"""
from __future__ import annotations

import functools
import html
import http.server
import json
import re
import sys
import tempfile
import threading
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE_PATH = "/quarto-workshop/"
PUBLIC = "https://project-delphi.github.io/quarto-workshop/"
PAGE = "ebook/"
RELEASE = "https://github.com/project-delphi/quarto-workshop/releases/latest/download/"
REPO_FILES = ("https://github.com/project-delphi/quarto-workshop/blob/main/",
              "https://github.com/project-delphi/quarto-workshop/tree/main/")
# Sites that refuse automated requests (403 or LinkedIn's 999): reported, not failed.
NO_BOTS = ("https://github.com/signup", "https://www.linkedin.com/")
FAILS: list[str] = []


def fail(msg: str) -> None:
    FAILS.append(msg)
    print("FAIL", msg)


def serve() -> tuple[str, http.server.ThreadingHTTPServer]:
    """docs/ served at /quarto-workshop/ on a free local port."""
    tmp = Path(tempfile.mkdtemp())
    (tmp / SITE_PATH.strip("/")).symlink_to(DOCS)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Quiet, directory=str(tmp))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{srv.server_port}{SITE_PATH}", srv


# ---- links ------------------------------------------------------------------------------------

def ids_in(path: Path) -> set[str]:
    return set(re.findall(r'\sid="([^"]+)"', path.read_text(encoding="utf-8", errors="replace")))


def local_target(url: str) -> Path | None:
    """The file in docs/ that a URL under the published site points to."""
    rel = urlparse(url).path.removeprefix(SITE_PATH)
    p = DOCS / rel
    return p / "index.html" if (rel == "" or rel.endswith("/")) else p


@functools.cache
def external_status(url: str) -> int:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "link-check"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 429, 999):  # some sites refuse HEAD or robots: try GET
            try:
                get = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 link-check"})
                with urllib.request.urlopen(get, timeout=20) as r:
                    return r.status
            except urllib.error.HTTPError as e2:
                return e2.code
        return e.code
    except Exception:
        return 0


def check_links(where: str, base: str, hrefs: list[str]) -> None:
    seen = set()
    for h in hrefs:
        if h.startswith(("mailto:", "javascript:")) or h in seen:
            continue
        seen.add(h)
        url = urljoin(base, html.unescape(h))
        if url.startswith(RELEASE):
            code = external_status(url)
            print(f"  {'ok' if code == 200 else 'PENDING (no release yet)'} {code} {url}")
            continue
        if url.startswith(PUBLIC):
            target = local_target(url)
            frag = urlparse(url).fragment
            if not target.exists():
                fail(f"{where}: {h} -> missing {target.relative_to(ROOT)}")
            elif frag and target.suffix == ".html" and frag not in ids_in(target) \
                    and not frag.startswith("/"):
                fail(f"{where}: {h} -> no #{frag} in {target.relative_to(ROOT)}")
            continue
        if url.startswith(REPO_FILES):
            rel = url.split("/main/", 1)[1].split("#")[0]
            code = external_status(url)
            if code == 200:
                continue
            if (ROOT / rel).exists():  # in this branch, on GitHub once merged
                print(f"  pending merge: {url} (exists locally)")
            else:
                fail(f"{where}: {url} answered {code} and {rel} does not exist")
            continue
        if url.startswith("http"):
            code = external_status(url)
            if code != 200 and url.startswith(NO_BOTS) and code in (403, 999):
                print(f"  refuses automated checks ({code}): {url}")
            elif code != 200:
                fail(f"{where}: {url} answered {code}")


def page_links() -> None:
    s = (DOCS / "ebook/index.html").read_text()
    hrefs = re.findall(r'<a [^>]*href="([^"]+)"', s)
    print(f"landing page: {len(hrefs)} links")
    check_links("ebook/index.html", PUBLIC + PAGE, hrefs)
    srcs = re.findall(r'(?:src|data-src|srcset|href)="((?:media/|ebook\.)[^" ,]+)', s)
    srcs += re.findall(r'srcset="([^"]+)"', s) and re.findall(r'(media/[^ ,"]+) \d+w', s)
    for p in set(srcs):
        if not (DOCS / "ebook" / p).exists():
            fail(f"ebook/index.html: {p} is missing from docs/ebook/")
    for m in re.findall(r'<meta property="og:image" content="([^"]+)"', s):
        if not local_target(m).exists():
            fail(f"og:image {m} is missing")


def deck_links() -> None:
    s = (DOCS / "index.html").read_text()
    blocks = []
    for sid in ("title-slide", "get-the-book"):
        i = s.find(f'id="{sid}"')
        if i < 0:
            fail(f"the deck has no #{sid}")
            continue
        blocks.append(s[i:s.find("</section>", i)])
    hrefs = [h for b in blocks for h in re.findall(r'<a [^>]*href="([^"]+)"', b)]
    print(f"deck title and Get the Book slides: {len(hrefs)} links")
    check_links("index.html", PUBLIC, hrefs)
    if not re.search(r'<img [^>]*src="data:image/(webp|svg)', blocks[-1] if blocks else ""):
        print("  note: the Get the Book slide's images are not embedded")


def book_links() -> None:
    s = (DOCS / "book/index.html").read_text()
    i = s.find('class="sidebar-tools-main')
    tools = s[i:s.find("</div>", i)] if i >= 0 else ""
    hrefs = re.findall(r'href="([^"]+)"', tools)
    print(f"website edition sidebar tools: {hrefs}")
    if not any("ebook" in h for h in hrefs):
        fail("the website edition's sidebar has no link to the landing page")
    if not any(h.endswith(".epub") for h in hrefs):
        fail("the website edition's sidebar has no EPUB download")
    check_links("book/index.html", PUBLIC + "book/", hrefs)


def contents_numbers() -> None:
    """The page's chapter numbers must be the website edition's."""
    side = (DOCS / "book/index.html").read_text()
    book = dict(re.findall(r'<a href="\./(chapters/[^"]+|appendices/[^"]+)" class="sidebar-[^"]*">\s*'
                           r'<span class="menu-text"><span class="chapter-number">([^<]+)</span>', side))
    page = (DOCS / "ebook/index.html").read_text()
    mine = dict(re.findall(r'<a href="\.\./book/((?:chapters|appendices)/[^"]+)"><span class="n">([^<]*)</span>', page))
    diff = {k: (v, book.get(k, "")) for k, v in mine.items() if v != book.get(k, "")}
    if diff:
        fail(f"contents numbers differ from the website edition (page, book): {diff}")
    else:
        print(f"contents: {len(mine)} chapter and appendix numbers match the website edition")


# ---- share card and structured data --------------------------------------------------------------

def share_card(out: Path, browser) -> None:
    s = (DOCS / "ebook/index.html").read_text()
    og = {k: html.unescape(v) for k, v in re.findall(r'<meta property="(og:[^"]+)" content="([^"]*)"', s)}
    need = ["og:title", "og:description", "og:url", "og:type", "og:image", "og:image:width",
            "og:image:height"]
    for k in need:
        if not og.get(k):
            fail(f"missing {k}")
    if og.get("og:type") != "book":
        fail(f"og:type is {og.get('og:type')}")
    if not og.get("og:url", "").startswith("https://") or not og.get("og:image", "").startswith("https://"):
        fail("og:url and og:image must be absolute https URLs")
    img = local_target(og["og:image"])
    from PIL import Image
    with Image.open(img) as im:
        if im.size != (1200, 627):
            fail(f"og:image is {im.size}")
    if img.stat().st_size > 1_000_000:
        fail(f"og:image is {img.stat().st_size} bytes")
    print(f"og:image {img.relative_to(ROOT)}: 1200 x 627, {img.stat().st_size / 1000:.0f} KB")
    host = urlparse(og["og:url"]).hostname
    card = f"""<!doctype html><meta charset="utf-8"><style>
body {{ margin: 0; background: #f4f2ee; font: 14px/1.4 -apple-system, "Segoe UI", Roboto, sans-serif; }}
.post {{ width: 552px; margin: 24px auto; background: #fff; border-radius: 8px; box-shadow: 0 0 0 1px #e0dfdc; overflow: hidden; }}
.who {{ padding: 12px 16px; color: #666; }} .txt {{ padding: 0 16px 12px; color: #191919; }}
img {{ display: block; width: 552px; aspect-ratio: 1200/627; object-fit: cover; }}
.meta {{ padding: 8px 12px 12px; background: #eef3f8; }}
.t {{ font-weight: 600; color: #191919; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
.h {{ color: #666; font-size: 12px; }}
</style><div class="post"><div class="who">Preview of a LinkedIn post sharing the page (drawn from its Open Graph tags)</div>
<div class="txt">My free e-book is out.</div>
<img src="{img.as_uri()}" alt=""><div class="meta"><div class="t">{html.escape(og["og:title"])}</div>
<div class="h">{host}</div></div></div>"""
    f = out / "share-card.html"
    f.write_text(card)
    page = browser.new_page(viewport={"width": 600, "height": 520}, device_scale_factor=2)
    page.goto(f.as_uri())
    page.wait_for_timeout(300)
    page.locator(".post").screenshot(path=str(out / "share-card.png"))
    page.close()
    print(f"share card: {out / 'share-card.png'}")


def json_ld() -> None:
    s = (DOCS / "ebook/index.html").read_text()
    m = re.search(r'<script type="application/ld\+json">(.+?)</script>', s, re.S)
    if not m:
        return fail("no JSON-LD")
    try:
        ld = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        return fail(f"JSON-LD does not parse: {e}")
    want = {"@context": "https://schema.org", "@type": "Book", "isAccessibleForFree": True,
            "bookFormat": "https://schema.org/EBook"}
    for k, v in want.items():
        if ld.get(k) != v:
            fail(f"JSON-LD {k} is {ld.get(k)!r}, not {v!r}")
    for k in ("name", "author", "datePublished", "url", "image"):
        if not ld.get(k):
            fail(f"JSON-LD has no {k}")
    if ld.get("author", {}).get("@type") != "Person":
        fail("JSON-LD author is not a Person")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", ld.get("datePublished", "")):
        fail("JSON-LD datePublished is not an ISO date")
    if not local_target(ld["image"]).exists():
        fail(f"JSON-LD image {ld['image']} is missing")
    print(f"JSON-LD: a schema.org Book, {len(ld)} properties, parses and has the required fields")


# ---- in a browser ------------------------------------------------------------------------------------

def scroll_through(page) -> None:
    """Scroll to the bottom and back, so every drawing and lazy image has been triggered."""
    h = page.evaluate("document.documentElement.scrollHeight")
    for y in range(0, h, 500):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(120)
    page.wait_for_timeout(1800)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)


def browse(base: str, out: Path) -> None:
    url = base + PAGE
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        # First load on a phone: what is downloaded before any scrolling.
        ctx = browser.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2,
                                  is_mobile=True, has_touch=True)
        page = ctx.new_page()
        sizes: dict[str, int] = {}

        def record(resp):
            try:
                sizes[resp.url] = len(resp.body())
            except Exception:
                pass
        page.on("response", record)
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(800)
        total = sum(sizes.values())
        print(f"first load on a phone: {len(sizes)} files, {total / 1000:.0f} KB")
        for u, n in sorted(sizes.items(), key=lambda kv: -kv[1])[:6]:
            print(f"  {n / 1000:6.0f} KB  {u.removeprefix(base)}")
        if total > 1_500_000:
            fail(f"first load is {total} bytes, over 1.5 MB")
        r = page.locator(".hero .btn.primary").bounding_box()
        print(f"primary download button at 375 x 812: top {r['y']:.0f}, bottom {r['y'] + r['height']:.0f} px")
        if r["y"] + r["height"] > 812:
            fail("the download button is below the phone's first screen")
        elif r["y"] + r["height"] > 640:
            print("  note: below 640 px, so LinkedIn's in-app browser may hide it")
        page.screenshot(path=str(out / "phone-first-screen.png"))
        ctx.close()

        for scheme in ("dark", "light"):
            for name, (w, h) in {"phone": (375, 812), "desktop": (1440, 900)}.items():
                # Scale 1: a full-page shot taller than Chrome's 16,384 px texture repeats itself.
                ctx = browser.new_context(viewport={"width": w, "height": h}, color_scheme=scheme,
                                          device_scale_factor=1,
                                          is_mobile=name == "phone", has_touch=name == "phone")
                page = ctx.new_page()
                errors: list[str] = []
                page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto(url, wait_until="networkidle")
                scroll_through(page)
                over = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                if over > 0:
                    fail(f"{name} {scheme}: the page scrolls sideways by {over} px")
                if errors:
                    fail(f"{name} {scheme}: console errors {errors}")
                page.screenshot(path=str(out / f"{name}-{scheme}-full.png"), full_page=True)
                if name == "phone" and scheme == "dark":
                    page.evaluate("window.scrollTo(0, 2200)")
                    page.wait_for_timeout(700)
                    shown = page.evaluate("document.querySelector('.sticky').classList.contains('show')")
                    print(f"sticky bar after scrolling on a phone: {'shown' if shown else 'NOT shown'}")
                    if not shown:
                        fail("the sticky bar does not appear after the hero")
                    page.screenshot(path=str(out / "phone-sticky.png"))
                ctx.close()

        ctx = browser.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=1,
                                  reduced_motion="reduce", is_mobile=True, has_touch=True)
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(500)
        state = page.evaluate("""({
          willDraw: document.querySelectorAll('.will-draw').length,
          videos: [...document.querySelectorAll('video')].filter(v => v.src).length })""")
        print(f"reduced motion: {state['willDraw']} hidden drawings, {state['videos']} videos loaded")
        if state["willDraw"] or state["videos"]:
            fail("reduced motion still animates or loads video")
        page.screenshot(path=str(out / "phone-reduced-motion-full.png"), full_page=True)
        ctx.close()
        share_card(out, browser)
        browser.close()


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "_ebook-check").resolve()
    out.mkdir(parents=True, exist_ok=True)
    if not (DOCS / "ebook/index.html").exists():
        raise SystemExit("render the site first: make deck")
    base, srv = serve()
    print(f"serving docs/ at {base}")
    page_links()
    deck_links()
    book_links()
    contents_numbers()
    json_ld()
    browse(base, out)
    srv.shutdown()
    print(f"\nscreenshots in {out}")
    if FAILS:
        raise SystemExit(f"{len(FAILS)} check(s) failed")
    print("all checks passed")


if __name__ == "__main__":
    main()
