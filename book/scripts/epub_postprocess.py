"""Fix up the EPUB that Quarto 1.10.20 writes (book/PLAN.md §6.3). Standard library only.

1. Front matter order: title page, copyright, preface. Quarto needs index.qmd (the
   preface) first in the chapter list, so the copyright page moves in the spine and TOC.
2. Parts: Quarto drops `part:` entries from EPUB, so the part pages are ordinary chapters
   (h1 class "part"). Nest each part's chapters under it in nav.xhtml and toc.ncx, until
   the next part, the afterword (h1 class "backmatter") or the first appendix.
3. Landmarks: add the copyright page and the start of the body (the preface) to the cover and title page landmarks that Pandoc writes.
4. Validity: remove `alt` from the figure wrapper divs (not allowed on div in XHTML; the
   img inside keeps its alt text).
5. Re-zip with `mimetype` first and stored, as the OCF container spec requires.

Usage: python scripts/epub_postprocess.py path/to/book.epub   (rewrites it in place)
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

XHTML = "http://www.w3.org/1999/xhtml"
OPS = "http://www.idpf.org/2007/ops"
NCX = "http://www.daisy.org/z3986/2005/ncx/"
ET.register_namespace("", XHTML)
ET.register_namespace("epub", OPS)

H1 = re.compile(r"<h1([^>]*)>(.*?)</h1>", re.S)
DIV_ALT = re.compile(r'(<div\b[^>]*?)\s+alt="[^"]*"')


def classify(files: dict[str, str]) -> dict[str, str]:
    """Map each chapter file (EPUB/text/...) to part, end, copyright, preface or ''."""
    kinds = {}
    for name, text in files.items():
        m = H1.search(text)
        attrs, title = (m.group(1), re.sub(r"<[^>]+>", "", m.group(2))) if m else ("", "")
        cls = re.search(r'class="([^"]*)"', attrs)
        classes = cls.group(1).split() if cls else []
        if 'epub:type="copyright-page"' in text:
            kinds[name] = "copyright"
        elif 'epub:type="preface"' in text:
            kinds[name] = "preface"
        elif "part" in classes:
            kinds[name] = "part"
        elif "backmatter" in classes or title.startswith("Appendix"):
            kinds[name] = "end"
        else:
            kinds[name] = ""
    return kinds


def nest(container: ET.Element, item_tag: str, list_tag: str, target, kinds) -> None:
    """Regroup container's top-level items: copyright first, chapters under their part."""
    items = list(container.findall(item_tag))
    for item in items:
        container.remove(item)
    copyright_items = [i for i in items if kinds.get(target(i)) == "copyright"]
    items = copyright_items + [i for i in items if i not in copyright_items]
    keep_first = [i for i in items if target(i) == "text/title_page.xhtml"]
    items = keep_first + [i for i in items if i not in keep_first]
    inner = None
    for item in items:
        kind = kinds.get(target(item), "")
        if kind == "part":
            container.append(item)
            if list_tag == item_tag:  # NCX: navPoints nest directly
                inner = item
            else:                     # nav.xhtml: an <ol class="toc"> inside the <li>
                inner = item.find(list_tag)
                if inner is None:
                    inner = ET.SubElement(item, list_tag, {"class": "toc"})
            continue
        if kind in ("end", "copyright", "preface"):
            inner = None
        (inner if inner is not None else container).append(item)


def fix_nav(text: str, kinds: dict[str, str]) -> str:
    root = ET.fromstring(text)
    navs = root.iter(f"{{{XHTML}}}nav")
    toc = landmarks = None
    for nav in navs:
        kind = nav.get(f"{{{OPS}}}type")
        toc = nav if kind == "toc" else toc
        landmarks = nav if kind == "landmarks" else landmarks
    ol = toc.find(f"{{{XHTML}}}ol")

    def target(li):
        a = li.find(f"{{{XHTML}}}a")
        return "EPUB/" + a.get("href").split("#")[0] if a is not None else ""

    nest(ol, f"{{{XHTML}}}li", f"{{{XHTML}}}ol", target, kinds)
    lm = landmarks.find(f"{{{XHTML}}}ol")
    have = {a.get(f"{{{OPS}}}type") for a in lm.iter(f"{{{XHTML}}}a")}
    by_kind = {k: f[len("EPUB/"):] for f, k in kinds.items() if k in ("copyright", "preface")}
    # No "toc" landmark: Pandoc leaves nav.xhtml out of the spine, and a landmark must
    # point at a spine item (epubcheck RSC-011).
    extra = []
    if "copyright" in by_kind:
        extra.append(("copyright-page", by_kind["copyright"], "Copyright"))
    if "preface" in by_kind:
        extra.append(("bodymatter", by_kind["preface"], "Start of Content"))
    for etype, href, label in extra:
        if etype in have:
            continue
        li = ET.SubElement(lm, f"{{{XHTML}}}li")
        a = ET.SubElement(li, f"{{{XHTML}}}a", {"href": href, f"{{{OPS}}}type": etype})
        a.text = label
    body = ET.tostring(root, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n' + body + "\n"


def fix_ncx(text: str, kinds: dict[str, str]) -> str:
    ET.register_namespace("", NCX)
    root = ET.fromstring(text)
    ET.register_namespace("", XHTML)
    nav_map = root.find(f"{{{NCX}}}navMap")

    def target(point):
        content = point.find(f"{{{NCX}}}content")
        return "EPUB/" + content.get("src").split("#")[0] if content is not None else ""

    nest(nav_map, f"{{{NCX}}}navPoint", f"{{{NCX}}}navPoint", target, kinds)

    def depth(el, d=0):
        kids = el.findall(f"{{{NCX}}}navPoint")
        return max([depth(k, d + 1) for k in kids], default=d)

    for meta in root.iter(f"{{{NCX}}}meta"):
        if meta.get("name") == "dtb:depth":
            meta.set("content", str(depth(nav_map)))
    ET.register_namespace("", NCX)
    out = ET.tostring(root, encoding="unicode")
    ET.register_namespace("", XHTML)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + out + "\n"


def fix_spine(text: str, kinds: dict[str, str]) -> str:
    """Move the copyright page's itemref to just after the title page."""
    for name, kind in kinds.items():
        if kind != "copyright":
            continue
        idref = Path(name).name.replace(".", "_")
        m = re.search(rf'\s*<itemref idref="{re.escape(idref)}"[^>]*/>', text)
        if not m:
            continue
        ref = m.group(0)
        text = text.replace(ref, "", 1)
        t = re.search(r'<itemref idref="title_page_xhtml"[^>]*/>', text)
        text = text[:t.end()] + ref + text[t.end():]
    return text


def main(path: str) -> None:
    epub = Path(path)
    with zipfile.ZipFile(epub) as z:
        entries = [(i, z.read(i.filename)) for i in z.infolist()]
    chapters = {i.filename: d.decode("utf-8") for i, d in entries
                if i.filename.startswith("EPUB/text/ch") and i.filename.endswith(".xhtml")}
    kinds = classify(chapters)
    fixed = []
    for info, data in entries:
        name = info.filename
        if name.endswith(".xhtml") and name.startswith("EPUB/text/"):
            data = DIV_ALT.sub(r"\1", data.decode("utf-8")).encode("utf-8")
        elif name == "EPUB/nav.xhtml":
            data = fix_nav(data.decode("utf-8"), kinds).encode("utf-8")
        elif name == "EPUB/toc.ncx":
            data = fix_ncx(data.decode("utf-8"), kinds).encode("utf-8")
        elif name == "EPUB/content.opf":
            data = fix_spine(data.decode("utf-8"), kinds).encode("utf-8")
        fixed.append((name, data))
    tmp = epub.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w") as z:
        mimetype = [d for n, d in fixed if n == "mimetype"]
        z.writestr(zipfile.ZipInfo("mimetype"), mimetype[0], compress_type=zipfile.ZIP_STORED)
        for name, data in fixed:
            if name != "mimetype":
                z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
    tmp.replace(epub)
    parts = sum(1 for k in kinds.values() if k == "part")
    print(f"post-processed {epub.name}: {parts} parts nested, copyright moved, landmarks added")


if __name__ == "__main__":
    main(sys.argv[1])
