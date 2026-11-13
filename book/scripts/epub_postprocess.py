"""Fix up the EPUB that Quarto 1.10.20 writes (book/PLAN.md §6.3). Needs Pillow (step 5).

1. Front matter order: title page, copyright, dedication, Contents, preface. Quarto needs
   index.qmd (the preface) first in the chapter list, so the copyright and dedication pages
   move in the spine and TOC.
2. Parts: Quarto drops `part:` entries from EPUB, so the part pages are ordinary chapters
   (h1 class "part"). Nest each part's chapters under it in nav.xhtml and toc.ncx, until
   the next part, the afterword (h1 class "backmatter") or the first appendix, and group
   the appendices under one "Appendices" entry.
3. Contents page: `toc: true` puts nav.xhtml in the spine, after the dedication. On that
   page show parts, chapters and appendices only (classes that styles/epub.css hides); the
   reader's own contents menu, which ignores the page's CSS, keeps every section.
4. Landmarks: add the copyright page and the start of the body (the preface) to the cover,
   title page and contents landmarks that Pandoc writes.
5. Validity: remove `alt` from the figure wrapper divs (not allowed on div in XHTML; the
   img inside keeps its alt text).
5a. Semantics: chapter headings read "Chapter 1" and appendix headings "Appendix A" above the
   title (the stylesheet sets the number on its own line, which split "Appendix A —" in
   three), and a part's heading "Part I: Foundations" becomes a "Part I" label and its name;
   appendices and the afterword get their epub:type and sit in backmatter, and front matter
   pages Pandoc marks bodymatter (About the Author) become frontmatter. The OPF gains the
   subtitle as a refined dc:title and title-page, copyright and text guide references; the
   NCX's cover meta names the cover image's real manifest id.
5b. Guard: the book uses no example lists, so an `<ol class="example">` means a line began
   with "@label." and Pandoc took a cross-reference for a list item: stop with an error.
5c. Typography: a caption's "Figure 1.1:" or "Table 1.1:" becomes a caption-label span; the
   no-break space Quarto puts in "Chapter 3" or "Figure 1.1" becomes a space; numbered
   chapters' and appendices' h1 get the class "chapter" and their first paragraph "hook";
   every other no-break space outside code becomes a space too; an identifier in a table cell
   may break after an underscore (<wbr/>);
   "Exercise II.1:" headings become an exercise-label span and the title; and on the
   Contents page an appendix reads by its letter, "A Windows: …", under "Appendices";
   a live-link card's QR code moves to the front of the card (styles/epub.css floats it); and
   the glossary's definition lists get epub:type glossary, glossterm and glossdef.
6. Light panels: figures drawn in dark ink on a transparent background sit on a light
   panel (class "on-light" on the img or an ancestor) that the stylesheet paints. A reader
   that drops CSS backgrounds, or Kindle, whose guidelines say it does not support
   "images with transparent areas" (https://kdp.amazon.com/en_US/help/topic/G75V4YX5X8GRGXWV,
   read 2026-11-12), would show dark ink on a night page, so those PNGs are flattened onto
   the panel's colour. Other images keep their transparency.
7. Re-zip with `mimetype` first and stored, as the OCF container spec requires.

Usage: python scripts/epub_postprocess.py path/to/book.epub   (rewrites it in place)
"""
from __future__ import annotations

import io
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

# Front matter that comes before the Contents page, in this order, after the title page.
FRONT = ("copyright", "dedication")
H1 = re.compile(r"<h1([^>]*)>(.*?)</h1>", re.S)
PANEL = (0xF1, 0xF0, 0xEB)  # styles/epub.css: img.on-light, .on-light img
DIV_ALT = re.compile(r'(<div\b[^>]*?)\s+alt="[^"]*"')


def classify(files: dict[str, str]) -> dict[str, str]:
    """Map each chapter file (EPUB/text/...) to part, end, appendix, copyright, dedication,
    preface or ''."""
    kinds = {}
    for name, text in files.items():
        m = H1.search(text)
        attrs, title = (m.group(1), re.sub(r"<[^>]+>", "", m.group(2))) if m else ("", "")
        cls = re.search(r'class="([^"]*)"', attrs)
        classes = cls.group(1).split() if cls else []
        if 'epub:type="copyright-page"' in text:
            kinds[name] = "copyright"
        elif 'epub:type="dedication"' in text:
            kinds[name] = "dedication"
        elif 'epub:type="preface"' in text:
            kinds[name] = "preface"
        elif "part" in classes:
            kinds[name] = "part"
        elif title.startswith("Appendix"):
            kinds[name] = "appendix"
        elif "backmatter" in classes:
            kinds[name] = "end"
        else:
            kinds[name] = ""
    return kinds


def nest(container: ET.Element, item_tag: str, list_tag: str, target, kinds,
         group) -> None:
    """Regroup container's top-level items: title page, copyright and dedication first,
    chapters under their part, appendices under one entry that group(first_appendix_item)
    makes."""
    items = list(container.findall(item_tag))
    for item in items:
        container.remove(item)
    front = [i for kind in FRONT for i in items if kinds.get(target(i)) == kind]
    items = front + [i for i in items if i not in front]
    keep_first = [i for i in items if target(i) == "EPUB/text/title_page.xhtml"]
    items = keep_first + [i for i in items if i not in keep_first]
    inner = None
    appendices = None
    for item in items:
        kind = kinds.get(target(item), "")
        if kind == "appendix":
            if appendices is None:
                head, appendices = group(item)
                container.append(head)
            appendices.append(item)
            continue
        if kind == "part":
            container.append(item)
            if list_tag == item_tag:  # NCX: navPoints nest directly
                inner = item
            else:                     # nav.xhtml: an <ol class="toc"> inside the <li>
                inner = item.find(list_tag)
                if inner is None:
                    inner = ET.SubElement(item, list_tag, {"class": "toc"})
            continue
        if kind in ("end", "preface", *FRONT):
            inner = None
        (inner if inner is not None else container).append(item)


def mark_page(ol: ET.Element, target, kinds: dict[str, str]) -> None:
    """Classes for the Contents page: the entries before it (copyright, dedication) and each
    chapter's list of sections are hidden there by styles/epub.css; parts and the
    appendices group are styled as headings."""
    for li in ol.iter(f"{{{XHTML}}}li"):
        kind = kinds.get(target(li), "")
        if li.get("class") == "toc-group":
            continue
        if kind in FRONT:
            li.set("class", "toc-before")
        elif kind == "part":
            li.set("class", "toc-part")
        else:
            sub = li.find(f"{{{XHTML}}}ol")
            if sub is not None:
                sub.set("class", "toc toc-sections")


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

    def group(first):
        li = ET.Element(f"{{{XHTML}}}li", {"class": "toc-group"})
        ET.SubElement(li, f"{{{XHTML}}}span").text = "Appendices"
        return li, ET.SubElement(li, f"{{{XHTML}}}ol", {"class": "toc"})

    nest(ol, f"{{{XHTML}}}li", f"{{{XHTML}}}ol", target, kinds, group)
    mark_page(ol, target, kinds)
    lm = landmarks.find(f"{{{XHTML}}}ol")
    have = {a.get(f"{{{OPS}}}type") for a in lm.iter(f"{{{XHTML}}}a")}
    by_kind = {k: f[len("EPUB/"):] for f, k in kinds.items() if k in ("copyright", "preface")}
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

    def group(first):
        point = ET.Element(f"{{{NCX}}}navPoint", {"id": "navPoint-appendices"})
        ET.SubElement(ET.SubElement(point, f"{{{NCX}}}navLabel"), f"{{{NCX}}}text").text = \
            "Appendices"
        src = first.find(f"{{{NCX}}}content").get("src")
        ET.SubElement(point, f"{{{NCX}}}content", {"src": src})
        return point, point

    nest(nav_map, f"{{{NCX}}}navPoint", f"{{{NCX}}}navPoint", target, kinds, group)

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
    """Move the copyright and dedication pages' itemrefs to just after the title page."""
    after = re.search(r'<itemref idref="title_page_xhtml"[^>]*/>', text).end()
    for kind in FRONT:
        for name in (n for n, k in kinds.items() if k == kind):
            idref = Path(name).name.replace(".", "_")
            m = re.search(rf'\s*<itemref idref="{re.escape(idref)}"[^>]*/>', text)
            if not m:
                continue
            ref = m.group(0)
            text = text[:m.start()] + text[m.end():]
            if m.start() < after:
                after -= len(ref)
            text = text[:after] + ref + text[after:]
            after += len(ref)
    return text


APPENDIX_H1 = re.compile(r'<h1([^>]*)>Appendix <span class="header-section-number">([^<]+)</span>\s*—\s*')
CHAPTER_H1 = re.compile(r'<h1([^>]*)><span class="header-section-number">(\d+)</span>')
PART_H1 = re.compile(r'<h1([^>]*\bpart\b[^>]*)>(Part [IVX]+):\s*')
CAPTION = re.compile(r'(<figcaption\b[^>]*>\s*)((?:Figure|Table) [A-Z0-9]+(?:\.\d+)?):\s*')
# Quarto joins "Chapter", "Figure" and the like to their number with a no-break space, which
# macOS's Charter (a reading font in Apple Books) draws twice as wide as a space.
NBSP_REF = re.compile("(Chapter|Section|Figure|Table|Appendix|Part|Equation)\u00a0")
HOOK = re.compile(r'(<h1 class="chapter"[^>]*>.*?</h1>\s*)<p>', re.S)
EXERCISE_H2 = re.compile(r'<h2 class="unnumbered"([^>]*)>(Exercise [IVX]+\.\d+):\s*')
NAV_APPENDIX = re.compile(r'Appendix (<span class="header-section-number">[A-Z]</span>) — ')


LIVE_LINK = re.compile(r'<div class="live-link">\s*<p>(.*?)</p>\s*</div>', re.S)
QR_IMG = re.compile(r'<img [^>]*class="qr"[^>]*/>')


def live_links(text: str) -> str:
    """A live-link card ("Turn the map yourself in the website edition, or scan: [QR]") gets
    its QR code first, in a paragraph of its own that the stylesheet floats right, and the
    sentence ends "or scan the code." instead of running into the image."""
    def card(m: re.Match) -> str:
        body = m.group(1)
        img = QR_IMG.search(body)
        if not img:
            return m.group(0)
        body = re.sub(r",?\s*or scan:\s*$", ", or scan the code.", body.replace(img.group(0), "").strip())
        return f'<div class="live-link"><p class="qr">{img.group(0)}</p><p>{body}</p></div>'
    return LIVE_LINK.sub(card, text)


PRE = re.compile(r"<pre\b.*?</pre>", re.S)
TD_CODE = re.compile(r"(<td\b[^>]*>)(.*?)(</td>)", re.S)


def plain_spaces(text: str) -> str:
    """"Chapter 3" and "Figure 1.1" with an ordinary space (the stylesheet keeps them on one
    line), and so every other no-break space outside code blocks (Pandoc adds them after
    abbreviations such as "No." and "et al."): macOS's Charter draws them twice as wide."""
    text = NBSP_REF.sub(r"\1 ", text)
    parts, last = [], 0
    for m in PRE.finditer(text):
        parts += [text[last:m.start()].replace("\u00a0", " "), m.group(0)]
        last = m.end()
    return "".join(parts + [text[last:].replace("\u00a0", " ")])


def code_breaks(text: str) -> str:
    """A long identifier in a table cell (`sewer_coverage_total`) may break after an underscore
    (<wbr/>, which copying leaves out), not at an arbitrary letter."""
    def cell(m: re.Match) -> str:
        body = re.sub(r"(<code>)(.*?)(</code>)",
                      lambda c: c.group(1) + c.group(2).replace("_", "_<wbr/>") + c.group(3), m.group(2))
        return m.group(1) + body + m.group(3)
    return TD_CODE.sub(cell, text)


def label_captions(text: str) -> str:
    """"Figure 1.1: What…" becomes a caption-label span and the caption, so the stylesheet
    can set the label apart; without CSS it still reads "Figure 1.1 What…"."""
    return CAPTION.sub(r'\1<span class="caption-label">\2</span> ', text)


def fix_chapter(text: str, kind: str, front: bool) -> str:
    """Chapter, part and appendix headings, and epub:type for appendices, the afterword and
    front matter."""
    if kind == "":
        text = CHAPTER_H1.sub(r'<h1 class="chapter"\1><span class="header-section-number">Chapter \2</span>',
                              text, 1)
        text = HOOK.sub(r'\1<p class="hook">', text, 1)
        text = EXERCISE_H2.sub(r'<h2 class="unnumbered exercise"\1><span class="exercise-label">\2</span> ', text)
    elif kind == "part":
        text = PART_H1.sub(r'<h1\1><span class="part-label">\2</span> ', text, 1)
    if kind == "appendix" and 'id="sec-glossary"' in text:
        # EPUB 3 structural semantics for the glossary, so reading systems can find its terms.
        text = (text.replace("<dl>", '<dl epub:type="glossary">').replace("<dt>", '<dt epub:type="glossterm">')
                .replace("<dd>", '<dd epub:type="glossdef">'))
    if kind == "appendix":
        text = APPENDIX_H1.sub(r'<h1 class="chapter"\1><span class="header-section-number">Appendix \2</span> ',
                               text, 1)
        text = text.replace('<body epub:type="bodymatter">', '<body epub:type="backmatter">', 1)
        text = re.sub(r'<section ([^>]*class="level1[^"]*")>', r'<section \1 epub:type="appendix">', text, 1)
    elif kind == "end":
        text = text.replace('<body epub:type="bodymatter">', '<body epub:type="backmatter">', 1)
        text = re.sub(r'<section ([^>]*class="level1[^"]*")>', r'<section \1 epub:type="afterword">', text, 1)
    elif front:
        text = text.replace('<body epub:type="bodymatter">', '<body epub:type="frontmatter">', 1)
    return text


def fix_opf(text: str, kinds: dict[str, str], subtitle: str) -> str:
    """The spine order, the subtitle as a refined dc:title, and fuller guide references."""
    text = fix_spine(text, kinds)
    if subtitle and "title-type" not in text:
        m = re.search(r'(<dc:title id="([^"]+)">[^<]*</dc:title>)', text)
        title, tid = m.group(1), m.group(2)
        text = text.replace(title, title
            + f'\n    <meta refines="#{tid}" property="title-type">main</meta>'
            + f'\n    <dc:title id="epub-subtitle">{subtitle}</dc:title>'
            + '\n    <meta refines="#epub-subtitle" property="title-type">subtitle</meta>', 1)
    refs = {"title-page": ("Title Page", "text/title_page.xhtml")}
    for name, kind in kinds.items():
        if kind == "copyright":
            refs["copyright-page"] = ("Copyright", name[len("EPUB/"):])
        if kind == "preface":
            refs["text"] = ("Start of Content", name[len("EPUB/"):])
    extra = "".join(f'\n    <reference type="{k}" title="{v[0]}" href="{v[1]}" />'
                    for k, v in refs.items() if f'type="{k}"' not in text)
    return text.replace("<guide>", "<guide>" + extra, 1)


def panel_images(text: str) -> set[str]:
    """Media paths (EPUB/media/...) of the imgs in a chapter shown on a light panel."""
    found: set[str] = set()

    def walk(e: ET.Element, lit: bool) -> None:
        lit = lit or "on-light" in (e.get("class") or "").split()
        if e.tag == f"{{{XHTML}}}img" and lit and e.get("src", "").startswith("../media/"):
            found.add("EPUB/" + e.get("src")[3:])
        for child in e:
            walk(child, lit)

    walk(ET.fromstring(text), False)
    return found


def flatten(data: bytes) -> bytes:
    """A PNG with transparent pixels, composited onto the panel colour; others unchanged."""
    from PIL import Image
    im = Image.open(io.BytesIO(data))
    if "A" not in im.getbands() or im.getchannel("A").getextrema()[0] == 255:
        return data
    flat = Image.new("RGB", im.size, PANEL)
    flat.paste(im, mask=im.getchannel("A"))
    out = io.BytesIO()
    flat.save(out, "PNG", optimize=True)
    return out.getvalue()


def main(path: str) -> None:
    epub = Path(path)
    with zipfile.ZipFile(epub) as z:
        entries = [(i, z.read(i.filename)) for i in z.infolist()]
    chapters = {i.filename: d.decode("utf-8") for i, d in entries
                if i.filename.startswith("EPUB/text/ch") and i.filename.endswith(".xhtml")}
    kinds = classify(chapters)
    examples = [n for n, c in chapters.items() if '<ol class="example"' in c]
    if examples:
        sys.exit("epub_postprocess: an example list in " + ", ".join(examples) + ": a line "
                 "starts with '@label.', which Pandoc reads as a list item; rewrap it")
    first_part = min((n for n, k in kinds.items() if k == "part"), default="")
    titles = [d.decode("utf-8") for i, d in entries if i.filename == "EPUB/text/title_page.xhtml"]
    sub = re.search(r'<p class="subtitle">(.*?)</p>', titles[0] if titles else "")
    subtitle = sub.group(1) if sub else ""
    opf = next(d.decode("utf-8") for i, d in entries if i.filename == "EPUB/content.opf")
    cover = re.search(r'<item [^>]*properties="cover-image"[^>]*id="([^"]+)"', opf)
    panels = set().union(*(panel_images(t) for t in chapters.values()))
    flattened = 0
    fixed = []
    for info, data in entries:
        name = info.filename
        if name.endswith(".xhtml") and name.startswith("EPUB/text/"):
            text = code_breaks(live_links(label_captions(plain_spaces(DIV_ALT.sub(r"\1", data.decode("utf-8"))))))
            if name in kinds:
                text = fix_chapter(text, kinds[name], bool(first_part) and name < first_part)
            data = text.encode("utf-8")
        elif name == "EPUB/nav.xhtml":
            nav = NAV_APPENDIX.sub(r"\1 ", plain_spaces(data.decode("utf-8")))
            data = fix_nav(nav, kinds).encode("utf-8")
        elif name == "EPUB/toc.ncx":
            text = fix_ncx(data.decode("utf-8"), kinds)
            if cover:
                text = re.sub(r'(<meta name="cover" content=")[^"]*(")', rf'\g<1>{cover.group(1)}\2', text)
            data = text.encode("utf-8")
        elif name == "EPUB/content.opf":
            data = fix_opf(data.decode("utf-8"), kinds, subtitle).encode("utf-8")
        elif name in panels and name.endswith(".png"):
            new = flatten(data)
            flattened += new is not data
            data = new
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
    appendices = sum(1 for k in kinds.values() if k == "appendix")
    print(f"post-processed {epub.name}: {parts} parts nested, {appendices} appendices grouped, "
          f"front matter moved, landmarks added, {flattened} panel figures flattened")


if __name__ == "__main__":
    main(sys.argv[1])
