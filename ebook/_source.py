"""What the e-book landing page (ebook/index.qmd) reads from the book's source.

Every title, number, chapter and quotation on the page comes from here, read from book/ and
examples/ when the page renders, so the page cannot drift from the book. Wording the page
quotes is found in the book's text, and the render stops if it is no longer there (`quote`),
as the book's own `text_holds` does. scripts/ebook_media.py imports this module too, for the
page's <head> (`head_html`), so the share card and the page say the same thing.

Quarto runs the page's cells from ebook/; ROOT is the repository root either way.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
from functools import cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"

SITE = "https://project-delphi.github.io/quarto-workshop/"
PAGE_URL = SITE + "ebook/"
REPO = "https://github.com/project-delphi/quarto-workshop"
EPUB_NAME = "prompt-check-publish.epub"
# A GitHub release carries the EPUB; GitHub counts its downloads. The release is made by hand
# (README.md, "The e-book landing page"), so this URL answers 404 until it exists.
EPUB_URL = f"{REPO}/releases/latest/download/{EPUB_NAME}"
# Links inside the site are relative to docs/ebook/, so they work locally and when published.
BOOK_URL = "../book/"
DECK_URL = "../"
OG_IMAGE = "media/og-image.png"
OG_SIZE = (1200, 627)

NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                "seventeen", "eighteen", "nineteen", "twenty"]


def words(n: int) -> str:
    return NUMBER_WORDS[n] if 0 <= n < len(NUMBER_WORDS) else f"{n:,}"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def quote(rel: str, *phrases: str) -> None:
    """Stop the render unless each phrase still appears in the file (whitespace-insensitive)."""
    text = " ".join(read(rel).split())
    for p in phrases:
        if " ".join(p.split()) not in text:
            raise ValueError(f"{rel} no longer says {p!r}: update the landing page's wording")


# ---- the book's metadata ---------------------------------------------------------------

@cache
def config() -> dict:
    return yaml.safe_load(read("book/_quarto.yml"))


def meta() -> dict:
    c = config()
    b = c["book"]
    return {
        "title": b["title"],
        "subtitle": b["subtitle"],
        "author": b["author"],
        "date": b["date"],
        "description": " ".join(c["description"].split()),
        "rights": c["rights"],
        "lang": c["lang"],
        "keywords": c["keywords"],
        "site_url": b["site-url"],
    }


def first_sentence(text: str) -> str:
    return re.split(r"(?<=\.)\s", text, maxsplit=1)[0]


def month_year(iso: str) -> str:
    import datetime
    return datetime.date.fromisoformat(iso).strftime("%B %Y")


def epub_size() -> str:
    """The published EPUB's size, from git's index (a full render empties docs/ meanwhile)."""
    out = subprocess.run(["git", "cat-file", "-s", f":docs/book/{EPUB_NAME}"], cwd=ROOT,
                         capture_output=True, text=True, check=True)
    return f"{int(out.stdout) / 1e6:.1f} MB"


# ---- the cover: palette and the fan of formats -----------------------------------------

@cache
def cover() -> dict:
    """The cover's colours and its fan of formats, parsed from book/media/cover.svg."""
    svg = read("book/media/cover.svg")
    paths = re.findall(r'<path d="(M[^"]+)" stroke="(#[0-9a-f]{6})"', svg)
    dots = re.findall(r'<circle cx="(\d+)" cy="(\d+)" r="(\d+)" fill="(#[0-9a-f]{6})"', svg)
    labels = re.findall(r'<text x="(\d+)" y="(\d+)" fill="(#[0-9a-f]{6})">([a-z]+)</text>', svg)
    box = re.search(r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" rx="(\d+)"', svg)
    src = re.search(r'<text x="(\d+)" y="(\d+)"[^>]*>\.qmd</text>', svg)
    if not (len(paths) == len(dots) == len(labels) > 0 and box and src):
        raise ValueError("book/media/cover.svg changed shape: update ebook/_source.py's parser")
    fan = []
    for (d, colour), (cx, cy, r, _), (lx, ly, _, name) in zip(paths, dots, labels):
        fan.append({"name": name, "colour": colour, "d": d, "dot": (int(cx), int(cy), int(r)),
                    "label": (int(lx), int(ly))})
    fill = lambda pattern: re.search(pattern, svg).group(1)  # noqa: E731
    return {
        "navy": fill(r'<rect width="1600" height="2560" fill="(#[0-9a-f]{6})"'),
        "cream": fill(r'fill="(#[0-9a-f]{6})" font-size="184"'),
        "subtitle": fill(r'fill="(#[0-9a-f]{6})" font-size="60"'),
        "label": fill(r'letter-spacing="10" fill="(#[0-9a-f]{6})"'),
        "fan": fan,
        "box": tuple(int(v) for v in box.groups()),
        "src": (int(src.group(1)), int(src.group(2))),
    }


# Where each format can be seen: a live example where one exists, else the book's section
# that shows it. Keys are the cover's labels; the page stops if the cover's formats change.
# {stem} in a note becomes that chapter's "Chapter N", numbered from _chapters.yml.
FORMAT_LINKS = {
    "html": ("This page", "Quarto HTML, built from ebook/index.qmd", f"{REPO}/blob/main/ebook/index.qmd"),
    "pdf": ("The water report", "{14-publish-many}, in Word and PDF", "chapters/14-publish-many.html#sec-water-report"),
    "docx": ("The London guide", "{05-compute}, as a Word file", "chapters/05-compute.html#sec-formats"),
    "epub": ("This book", "the EPUB you can download", EPUB_URL),
    "slides": ("The workshop slides", "Reveal.js, live", DECK_URL),
    "website": ("The website edition", "this book, live", BOOK_URL),
    "blog": ("The water blog", "{14-publish-many}, a website with posts", "chapters/14-publish-many.html#sec-water-website"),
    "dashboard": ("The water dashboard", "{14-publish-many}", "chapters/14-publish-many.html#sec-water-dashboard"),
}


def format_links() -> list[dict]:
    fan = cover()["fan"]
    if [f["name"] for f in fan] != list(FORMAT_LINKS):
        raise ValueError("the cover's formats changed: update FORMAT_LINKS in ebook/_source.py")
    out = []
    for f in fan:
        title, note, href = FORMAT_LINKS[f["name"]]
        note = re.sub(r"\{([^}]+)\}", lambda m: chapter(m.group(1))["name"], note)
        if not href.startswith(("http", "../")):
            href = BOOK_URL + href
        out.append({**f, "title": title, "note": note, "href": href})
    return out


# ---- the table of contents -------------------------------------------------------------

def heading(rel: str) -> tuple[str, bool]:
    """A chapter file's title and whether Quarto numbers it, from its first level-1 heading."""
    fence = False
    for line in read(f"book/{rel}").splitlines():
        if line.startswith(("```", "~~~")):
            fence = not fence
        elif not fence and line.startswith("# "):
            m = re.match(r"# (.+?)\s*(\{([^}]*)\})?\s*$", line)
            attrs = (m.group(3) or "").split()
            return m.group(1), ".unnumbered" not in attrs
    raise ValueError(f"book/{rel} has no level-1 heading")


def href(rel: str) -> str:
    return BOOK_URL + rel.removesuffix(".qmd") + ".html"


def contents() -> dict:
    """Parts, chapters and appendices, numbered as Quarto numbers them, from _chapters.yml."""
    ch = yaml.safe_load(read("book/_chapters.yml"))
    n = 0

    def entry(rel: str) -> dict:
        nonlocal n
        title, numbered = heading(rel)
        if numbered:
            n += 1
        return {"label": str(n) if numbered else "", "title": title, "href": href(rel),
                "file": rel}

    front = [entry(r) for r in ch["front"]]
    parts = []
    for p in ch["parts"]:
        title, _ = heading(p["file"])
        label, name = title.split(": ", 1)
        parts.append({"label": label, "title": name, "href": href(p["file"]),
                      "chapters": [entry(r) for r in p["chapters"]]})
    back = [entry(r) for r in ch["back"]]
    appendices = []
    for i, rel in enumerate(ch["appendices"]):
        title, _ = heading(rel)
        appendices.append({"label": chr(ord("A") + i), "title": title, "href": href(rel)})
    return {"front": front, "parts": parts, "back": back, "appendices": appendices,
            "chapters": n}


def chapter(stem: str) -> dict:
    """A numbered chapter found by its file name (such as 05-compute), with "name": "Chapter N"."""
    toc = contents()
    found = [c for p in toc["parts"] for c in p["chapters"]
             if Path(c["file"]).stem == stem and c["label"]]
    if len(found) != 1:
        raise ValueError(f"book/_chapters.yml has no numbered chapter {stem}")
    return {**found[0], "name": f"Chapter {found[0]['label']}"}


# ---- the two projects --------------------------------------------------------------------

def london_top() -> dict:
    """London's most visited ALVA member attraction, as the book's preface computes it."""
    import pandas as pd

    att = pd.read_csv(ROOT / "examples/london/data/attractions.csv")
    visits_col = next(c for c in att.columns if c.startswith("visits_"))
    top = att.loc[att[visits_col].idxmax()]
    return {"name": top["attraction"], "visits": int(top[visits_col]),
            "year": visits_col.removeprefix("visits_"), "n": len(att)}


def water_span() -> dict:
    """The water table's coverage, as Chapter 8 computes it, through the project's analysis.py."""
    import sys

    scripts = str(ROOT / "examples/water/scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import analysis

    raw = analysis.load()
    kinds = raw.drop_duplicates("divipola")["entity_type"].value_counts()
    return {"codes": int(raw["divipola"].nunique()), "first": int(raw["year"].min()),
            "last": int(raw["year"].max()), "municipalities": int(kinds.get("municipality", 0)),
            "zones": sorted(raw["zone"].unique())}


# ---- figures: captions and alt texts as the book gives them --------------------------------

def gif_figure(gif: str) -> dict:
    """A GIF's caption and alt text, from the chapter that shows it (its EPUB stand-in)."""
    for qmd in sorted((BOOK / "chapters").glob("*.qmd")):
        m = re.search(r"!\[(.+?)\]\(\.\./media/gifs/" + re.escape(gif)
                      + r'\.gif\)\{[^}]*fig-alt="([^"]+)"', qmd.read_text(encoding="utf-8"))
        if m:
            return {"caption": m.group(1), "alt": m.group(2)}
    raise ValueError(f"no chapter shows media/gifs/{gif}.gif with alt text")


def cell_figure(rel: str, label: str) -> dict:
    """A code cell's figure caption and alt text, from its #| options."""
    text = read(rel)
    i = text.index(f"#| label: {label}")
    opts = dict(re.findall(r'#\| (fig-cap|fig-alt): "(.+)"', text[i:i + 2000]))
    return {"caption": opts["fig-cap"], "alt": opts["fig-alt"]}


def cover_desc() -> str:
    """The cover's own description (its SVG <desc>), used as its alt text."""
    return re.search(r"<desc[^>]*>(.+?)</desc>", read("book/media/cover.svg"), re.S).group(1)


def audiences() -> list[str]:
    """Who the preface says the book is for."""
    m = re.search(r"I wrote this book for (.+?): anyone", " ".join(read("book/index.qmd").split()))
    return re.split(r", | and ", m.group(1))


# ---- text the page quotes ------------------------------------------------------------------

def paragraph_after(rel: str, marker: str) -> str:
    """The paragraph that starts with marker, without it, joined onto one line."""
    text = read(rel)
    i = text.index(marker) + len(marker)
    return " ".join(text[i:].split("\n\n", 1)[0].split())


def author_linkedin() -> str:
    """The author's LinkedIn profile, from the workshop deck's header (index.qmd)."""
    return re.search(r'^author-linkedin: "([^"]+)"$', read("index.qmd"), re.M).group(1)


def about_author() -> str:
    """The About the Author page's paragraphs, as Markdown."""
    body = read("book/about-author.qmd").split("\n", 1)[1].strip()
    return body


def ai_statement() -> str:
    return paragraph_after("book/copyright.qmd", "**AI usage statement.**")


def checked_with() -> str:
    """The Quarto version the copyright page says the book was checked with."""
    return re.search(r"Checked with Quarto ([\d.]+)", read("book/copyright.qmd")).group(1)


def assistant_cost() -> tuple[str, str]:
    """The preface's sentence on what Claude Code needs, and the date it was checked."""
    m = re.search(r"(Claude Code, for one, needs [^(]+?)\s*\(checked (\d{4}-\d{2}-\d{2})",
                  " ".join(read("book/index.qmd").split()))
    return m.group(1), m.group(2)


def assistant_accounts() -> tuple[str, str]:
    """Chapter 3's list of what each assistant's account needs, and its checked date."""
    text = " ".join(read("book/chapters/03-setup.qmd").split())
    m = re.search(r"(Claude Code needs a [^;]+); (Codex a [^(]+?) \(for pay-per-use billing, "
                  r"@sec-choose\); (Antigravity a Google account) \(checked (\d{4}-\d{2}-\d{2})\)",
                  text)
    return f"{m.group(1)}; {m.group(2)}; {m.group(3)}", m.group(4)


# ---- the page's <head>: share card, icons, structured data ---------------------------------

def share_text() -> tuple[str, str]:
    """The page's title and description, for its <title>, search results and share cards."""
    m = meta()
    return (f"{m['title']}: a free e-book by {m['author']}",
            "Free e-book. " + first_sentence(m["description"]))


def head_html() -> str:
    """The page's <head> additions. scripts/ebook_media.py writes them to ebook/_head.html,
    and the page stops if that file differs from what this returns (it is stale). Quarto writes
    <meta name="description"> itself, and fills the description tags below, from the page's
    `description`, which the page checks against share_text()."""
    m = meta()
    title, desc = share_text()
    image = PAGE_URL + OG_IMAGE
    alt = (f"The cover of {m['title']}, beside its title, subtitle and author, and the words "
           "Free e-book, EPUB and website edition.")
    ld = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": m["title"],
        "alternativeHeadline": m["subtitle"],
        "author": {"@type": "Person", "name": m["author"]},
        "datePublished": m["date"],
        "inLanguage": m["lang"],
        "isAccessibleForFree": True,
        "bookFormat": "https://schema.org/EBook",
        "url": PAGE_URL,
        "image": PAGE_URL + "media/cover-720.webp",
        "description": m["description"],
        "keywords": ", ".join(m["keywords"]),
        "workExample": [
            {"@type": "Book", "bookFormat": "https://schema.org/EBook",
             "encodingFormat": "application/epub+zip", "url": EPUB_URL},
            {"@type": "Book", "bookFormat": "https://schema.org/EBook",
             "encodingFormat": "text/html", "url": m["site_url"]},
        ],
    }
    e = lambda s: html.escape(s, quote=True)  # noqa: E731
    w, h = OG_SIZE
    lines = [
        "<!-- Generated by scripts/ebook_media.py from book/_quarto.yml (ebook/_source.py); do not edit. -->",
        f'<meta name="author" content="{e(m["author"])}">',
        f'<link rel="canonical" href="{PAGE_URL}">',
        '<meta name="theme-color" content="#13202e">',
        '<meta name="color-scheme" content="dark">',
        '<meta property="og:type" content="book">',
        f'<meta property="og:title" content="{e(title)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{PAGE_URL}">',
        f'<meta property="og:image" content="{image}">',
        '<meta property="og:image:type" content="image/png">',
        f'<meta property="og:image:width" content="{w}">',
        f'<meta property="og:image:height" content="{h}">',
        f'<meta property="og:image:alt" content="{e(alt)}">',
        f'<meta property="og:locale" content="{m["lang"].replace("-", "_")}">',
        f'<meta property="book:author" content="{e(m["author"])}">',
        f'<meta property="book:release_date" content="{m["date"]}">',
        *[f'<meta property="book:tag" content="{e(k)}">' for k in m["keywords"]],
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(title)}">',
        f'<meta name="twitter:description" content="{e(desc)}">',
        f'<meta name="twitter:image" content="{image}">',
        f'<meta name="twitter:image:alt" content="{e(alt)}">',
        '<link rel="icon" href="media/favicon.svg" type="image/svg+xml">',
        '<link rel="icon" href="media/favicon-32.png" type="image/png" sizes="32x32">',
        '<link rel="apple-touch-icon" href="media/apple-touch-icon.png">',
        '<link rel="preload" href="media/fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin>',
        '<link rel="preload" href="media/fonts/nunito-sans.woff2" as="font" type="font/woff2" crossorigin>',
        '<script type="application/ld+json">',
        json.dumps(ld, indent=1, ensure_ascii=False),
        "</script>",
    ]
    return "\n".join(lines) + "\n"


def check_head() -> None:
    if read("ebook/_head.html") != head_html():
        raise ValueError("ebook/_head.html is stale: run `make ebook-media STEPS=head`")
