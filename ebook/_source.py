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


def epub_site_url() -> str:
    """The EPUB's copy on GitHub Pages, next to the website edition (make book-publish). Pages
    serves it as an e-book (application/epub+zip), where the release serves a generic file
    to save, so phones get this link (ebook.js): it is the one they may offer to open in a
    reader. Desktops keep EPUB_URL, whose downloads GitHub counts."""
    return BOOK_URL + EPUB_NAME
OG_IMAGE = "media/og-image.png"
OG_SIZE = (1200, 627)

# The Spanish page (ebook/es/index.qmd) calls use("es") first: it reads the Spanish edition's
# source (book-es/) and links to the Spanish book and EPUB. English is the default.
LANG = "en"
BOOK_DIR = "book"             # whose source the page reads
PAGE_DIR = "ebook"            # where the page and its own media live
SHARED = "media/"             # fonts, icons and clips, which both pages share
HEAD = "ebook/_head.html"
PAGES = {"en": SITE + "ebook/", "es": SITE + "ebook/es/"}

NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                "seventeen", "eighteen", "nineteen", "twenty"]
NUMBER_WORDS_ES = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
                   "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete",
                   "dieciocho", "diecinueve", "veinte"]
MONTHS_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
             "septiembre", "octubre", "noviembre", "diciembre"]


def use(lang: str) -> None:
    """Point the page at one edition: "en" (book/) or "es" (book-es/)."""
    global LANG, BOOK, BOOK_DIR, PAGE_DIR, SHARED, HEAD, PAGE_URL, EPUB_NAME, EPUB_URL, BOOK_URL, DECK_URL
    if lang != "es":
        return
    LANG, BOOK_DIR, BOOK = "es", "book-es", ROOT / "book-es"
    PAGE_DIR, SHARED, HEAD = "ebook/es", "../media/", "ebook/es/_head.html"
    PAGE_URL = PAGES["es"]
    EPUB_NAME = "prompt-check-publish-es.epub"
    EPUB_URL = f"{REPO}/releases/latest/download/{EPUB_NAME}"
    BOOK_URL, DECK_URL = "../../book/es/", "../../"


def words(n: int) -> str:
    table = NUMBER_WORDS_ES if LANG == "es" else NUMBER_WORDS
    return table[n] if 0 <= n < len(table) else f"{n:,}"


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
    return yaml.safe_load(read(f"{BOOK_DIR}/_quarto.yml"))


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
    d = datetime.date.fromisoformat(iso)
    return f"{MONTHS_ES[d.month - 1]} de {d.year}" if LANG == "es" else d.strftime("%B %Y")


def epub_size() -> str:
    """The published EPUB's size, from git's index (a full render empties docs/ meanwhile)."""
    folder = "docs/book/es" if LANG == "es" else "docs/book"
    out = subprocess.run(["git", "cat-file", "-s", f":{folder}/{EPUB_NAME}"], cwd=ROOT,
                         capture_output=True, text=True, check=True)
    return f"{int(out.stdout) / 1e6:.1f} MB"


# ---- the cover: palette and the fan of formats -----------------------------------------

@cache
def cover() -> dict:
    """The cover's colours and its fan of formats, parsed from book/media/cover.svg."""
    svg = read(f"{BOOK_DIR}/media/cover.svg")
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


def format_table() -> dict:
    """FORMAT_LINKS in the page's language, with this edition's EPUB and book."""
    if LANG != "es":
        return FORMAT_LINKS
    return {
        "html": ("Esta página", "HTML de Quarto, construido desde ebook/es/index.qmd", f"{REPO}/blob/main/ebook/es/index.qmd"),
        "pdf": ("El informe del agua", "{14-publish-many}, en Word y PDF", "chapters/14-publish-many.html#sec-water-report"),
        "docx": ("La guía de Londres", "{05-compute}, como archivo de Word", "chapters/05-compute.html#sec-formats"),
        "epub": ("Este libro", "el EPUB que puedes descargar", EPUB_URL),
        "slides": ("Las diapositivas del taller", "Reveal.js, en vivo (en inglés)", DECK_URL),
        "website": ("La edición web", "este libro, en vivo", BOOK_URL),
        "blog": ("El blog del agua", "{14-publish-many}, un sitio web con entradas", "chapters/14-publish-many.html#sec-water-website"),
        "dashboard": ("El dashboard del agua", "{14-publish-many}", "chapters/14-publish-many.html#sec-water-dashboard"),
    }


def format_links() -> list[dict]:
    fan = cover()["fan"]
    table = format_table()
    if [f["name"] for f in fan] != list(table):
        raise ValueError("the cover's formats changed: update FORMAT_LINKS in ebook/_source.py")
    out = []
    for f in fan:
        title, note, href = table[f["name"]]
        note = re.sub(r"\{([^}]+)\}", lambda m: chapter(m.group(1))["name"], note)
        if not href.startswith(("http", "../")):
            href = BOOK_URL + href
        out.append({**f, "title": title, "note": note, "href": href})
    return out


# ---- the table of contents -------------------------------------------------------------

def heading(rel: str) -> tuple[str, bool]:
    """A chapter file's title and whether Quarto numbers it, from its first level-1 heading."""
    fence = False
    for line in read(f"{BOOK_DIR}/{rel}").splitlines():
        if line.startswith(("```", "~~~")):
            fence = not fence
        elif not fence and line.startswith("# "):
            m = re.match(r"# (.+?)\s*(\{([^}]*)\})?\s*$", line)
            attrs = (m.group(3) or "").split()
            return m.group(1), ".unnumbered" not in attrs
    raise ValueError(f"{BOOK_DIR}/{rel} has no level-1 heading")


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
    word = "Capítulo" if LANG == "es" else "Chapter"
    return {**found[0], "name": f"{word} {found[0]['label']}"}


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
    return re.search(r"<desc[^>]*>(.+?)</desc>", read(f"{BOOK_DIR}/media/cover.svg"), re.S).group(1)


def audiences() -> list[str]:
    """Who the preface says the book is for."""
    pattern = r"Escribí este libro para (.+?): cualquiera" if LANG == "es" else r"I wrote this book for (.+?): anyone"
    m = re.search(pattern, " ".join(read(f"{BOOK_DIR}/index.qmd").split()))
    return re.split(r", | y " if LANG == "es" else r", | and ", m.group(1))


# ---- text the page quotes ------------------------------------------------------------------

def paragraph_after(rel: str, marker: str) -> str:
    """The paragraph that starts with marker, without it, joined onto one line."""
    text = read(rel)
    i = text.index(marker) + len(marker)
    return " ".join(text[i:].split("\n\n", 1)[0].split())


def author_linkedin() -> str:
    """The author's LinkedIn profile, from the workshop deck's header (index.qmd)."""
    m = re.search(r'^author-linkedin: "([^"]+)"$', read("index.qmd"), re.M)
    if not m:
        raise ValueError('index.qmd needs author-linkedin: "https://…" (double-quoted, alone on its line)')
    return m.group(1)


def about_author() -> str:
    """The About the Author page's paragraphs, as Markdown."""
    body = read(f"{BOOK_DIR}/about-author.qmd").split("\n", 1)[1].strip()
    return body


def ai_statement() -> str:
    marker = "**Declaración de uso de IA.**" if LANG == "es" else "**AI usage statement.**"
    return paragraph_after(f"{BOOK_DIR}/copyright.qmd", marker)


def checked_with() -> str:
    """The Quarto version the copyright page says the book was checked with."""
    return re.search(r"(?:Checked with|Revisado con) Quarto ([\d.]+)", read(f"{BOOK_DIR}/copyright.qmd")).group(1)


def assistant_cost() -> tuple[str, str]:
    """The preface's sentence on what Claude Code needs, and the date it was checked."""
    pattern = (r"(Claude Code, por ejemplo, necesita [^(]+?)\s*\(consultado el (\d{4}-\d{2}-\d{2})"
               if LANG == "es" else r"(Claude Code, for one, needs [^(]+?)\s*\(checked (\d{4}-\d{2}-\d{2})")
    m = re.search(pattern, " ".join(read(f"{BOOK_DIR}/index.qmd").split()))
    return m.group(1), m.group(2)


def assistant_accounts() -> tuple[str, str]:
    """Chapter 3's list of what each agent's account needs, and its checked date."""
    text = " ".join(read(f"{BOOK_DIR}/chapters/03-setup.qmd").split())
    if LANG == "es":
        m = re.search(r"(Claude Code necesita una [^;]+); (Codex, [^(]+?) \(para facturación por uso, "
                      r"@sec-choose\); (Antigravity, una cuenta de Google) \(consultado el (\d{4}-\d{2}-\d{2})\)",
                      text)
    else:
        m = re.search(r"(Claude Code needs a [^;]+); (Codex a [^(]+?) \(for pay-per-use billing, "
                      r"@sec-choose\); (Antigravity a Google account) \(checked (\d{4}-\d{2}-\d{2})\)",
                      text)
    return f"{m.group(1)}; {m.group(2)}; {m.group(3)}", m.group(4)


# ---- the page's <head>: share card, icons, structured data ---------------------------------

def share_text() -> tuple[str, str]:
    """The page's title and description, for its <title>, search results and share cards."""
    m = meta()
    if LANG == "es":
        return (f"{m['title']}: un libro electrónico gratuito de {m['author']}",
                "Libro electrónico gratuito. " + first_sentence(m["description"]))
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
    alt = (f"La cubierta de {m['title']}, al lado de su título, su subtítulo y su autoría, y las palabras "
           "Libro electrónico gratuito, EPUB y edición web." if LANG == "es" else
           f"The cover of {m['title']}, beside its title, subtitle and author, and the words "
           "Free e-book, EPUB and website edition.")
    ld = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": m["title"],
        "alternativeHeadline": m["subtitle"],
        "author": {"@type": "Person", "name": m["author"], "sameAs": [author_linkedin()]},
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
        f"<!-- Generated by scripts/ebook_media.py from {BOOK_DIR}/_quarto.yml (ebook/_source.py); do not edit. -->",
        f'<meta name="author" content="{e(m["author"])}">',
        f'<link rel="canonical" href="{PAGE_URL}">',
        *[f'<link rel="alternate" hreflang="{lang}" href="{url}">' for lang, url in PAGES.items()],
        f'<link rel="alternate" hreflang="x-default" href="{PAGES["en"]}">',
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
        f'<link rel="icon" href="{SHARED}favicon.svg" type="image/svg+xml">',
        f'<link rel="icon" href="{SHARED}favicon-32.png" type="image/png" sizes="32x32">',
        f'<link rel="apple-touch-icon" href="{SHARED}apple-touch-icon.png">',
        f'<link rel="preload" href="{SHARED}fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin>',
        f'<link rel="preload" href="{SHARED}fonts/nunito-sans.woff2" as="font" type="font/woff2" crossorigin>',
        '<script type="application/ld+json">',
        json.dumps(ld, indent=1, ensure_ascii=False),
        "</script>",
    ]
    return "\n".join(lines) + "\n"


def check_head() -> None:
    if read(HEAD) != head_html():
        raise ValueError(f"{HEAD} is stale: run `make ebook-media STEPS=head`"
                         + (" EDITION=es" if LANG == "es" else ""))
