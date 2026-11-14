"""Find English sentences left in the built Spanish edition (translation/PLAN.md, section 4).

Reads the Spanish website edition (book-es/_book/html) and EPUB, skips code (`code`, `pre`,
`script`, `style`, `svg`) and anything marked translate="no", and reports each sentence or alt
text whose words are mostly English function words and hardly any Spanish ones. Quotations the
book keeps in English on purpose (screen text, the London guide's own words, paper titles) are
listed in KEPT so that the report shows only what still needs a look.

    python3 translation/english_scan.py           # exit status 1 if anything is left
"""
from __future__ import annotations

import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "book-es" / "_book" / "html"
EPUB = ROOT / "book-es" / "_book" / "epub" / "prompt-check-publish-es.epub"

EN = set("the and of to is are was were with that this for from by on in it its be been has have "
         "you your which what when where how why not can will would should into than then they "
         "their there these those an as at or if but so do does did each every one".split())
ES = set("el la los las de del y que en un una es son con por para se su sus al lo como más "
         "pero ya o si no le les este esta esto estos estas cada sin sobre entre cuando donde "
         "hay está están fue ser muy también tu tus te".split())
SKIP = {"code", "pre", "script", "style", "svg", "math", "kbd", "samp"}
# English kept on purpose, matched as substrings of a flagged sentence.
KEPT = [
    "Generate an SVG of a pelican riding a bicycle", "Claude Code'll be able to read",
    "subject to your permission settings", "Catch me up: follow", "Most visited in 2025",
    "ten most visited ALVA member attractions", "ALVA member attractions",
    "every number comes from a cited file", "call ALVA counts", "Do not do it silently",
    "Changes will not be effective", "the remote origin does not have a branch",
    "Please tell me who you are", "There is an unactivated Python environment",
    "Kernel is running over TCP", "the next cluster cuts inertia", "Visits made in",
    "Least squares quantization", "Silhouettes: a graphical aid", "Clustering in an object",
    "k-means++: the advantages", "The proof and measurement of association",
    "Ecological correlations and the behavior", "Causal Inference: What If",
    "Learn Markdown in Y minutes", "Cathedrals and churches in London", "Publish site",
    "Sign in with", "Select login method", "Yes, I trust this folder", "No, exit",
    "Prompt, Check, Publish", "virtualization is not enabled", "Sorry, try again", "Access denied",
    "already exists", "Setup notes", "command line developer tools", "RPC failed",
    "the remote end hung up", "Allow this command", "Output created", "London's most visited",
    "Committed the dashboard changes", "Top 10 with free entry", "More # signs",
    "A blank line starts", "Leave a blank line", "a quotation", "a line across", "Click it to open",
    "Click the picture", "A picture, with its caption", "Five sights", "Getting around",
    "Plan your visit", "Before you go", "Sights at a glance", "Read more", "Tip from a local",
    "Visit London", "Four kinds of municipal zone", "Kinds of municipal zone in Colombia",
    "Drinking-water quality and infant mortality", "Visits to London's leading", "How the kinds differ",
    "Pandemic loss and recovery", "A descriptive cluster analysis", "Water quality, services",
    "Known gaps and caveats", "User's Guide", "cannot parse length", "unexpected argument",
    "LLMflation", "book a free timed ticket", "with 7,116,929 visits", "a graphical aid",
    "Reproducible Data Publishing with Quarto and AI Coding Assistants",
]


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth, self.parts = 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP or a.get("translate") == "no" or self.depth:
            if tag not in ("br", "img", "meta", "link", "input", "hr", "wbr"):
                self.depth += 1
            return
        if a.get("alt"):
            self.parts.append("\n" + a["alt"] + "\n")
        if a.get("aria-label") and len(a["aria-label"]) > 40:
            self.parts.append("\n" + a["aria-label"] + "\n")
        if tag in ("p", "li", "td", "th", "h1", "h2", "h3", "h4", "figcaption", "div", "dt", "dd", "title"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if self.depth and tag not in ("br", "img", "meta", "link", "input", "hr", "wbr"):
            self.depth -= 1

    def handle_data(self, data):
        if not self.depth:
            self.parts.append(data)


def sentences(html: str):
    p = Text()
    p.feed(html)
    for block in "".join(p.parts).split("\n"):
        for s in re.split(r"(?<=[.!?:;])\s+", block):
            s = " ".join(s.split())
            if len(s.split()) >= 5:
                yield s


def english(s: str) -> bool:
    words = re.findall(r"[a-záéíóúñü']+", s.lower())
    if len(words) < 5:
        return False
    en = sum(w in EN for w in words) / len(words)
    es = sum(w in ES for w in words) / len(words)
    return en >= 0.2 and es < 0.08


def scan() -> list[tuple[str, str]]:
    hits = []
    for page in sorted(HTML.rglob("*.html")):
        if "site_libs" in page.parts:
            continue
        for s in sentences(page.read_text(encoding="utf-8")):
            if english(s) and not any(k in s for k in KEPT):
                hits.append((str(page.relative_to(HTML)), s))
    if EPUB.exists():
        with zipfile.ZipFile(EPUB) as z:
            for name in sorted(n for n in z.namelist() if n.endswith(".xhtml")):
                for s in sentences(z.read(name).decode("utf-8")):
                    if english(s) and not any(k in s for k in KEPT):
                        hits.append(("epub:" + name, s))
    return hits


def main() -> int:
    hits = scan()
    seen = set()
    for where, s in hits:
        if s in seen:
            continue
        seen.add(s)
        print(f"{where}: {s[:200]}")
    print(f"{len(seen)} English sentences left in the Spanish edition")
    return 1 if seen else 0


if __name__ == "__main__":
    sys.exit(main())
