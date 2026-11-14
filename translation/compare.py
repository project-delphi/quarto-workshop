"""Compare each English chapter in book/ with its Spanish translation in book-es/.

For every pair (same relative path) it checks what must not change in a translation
(translation/PLAN.md, section 4), and exits with status 1 on any error:

- executable cells: the same number, the same cell options apart from captions and alt
  text, and the same Python: every token identical except string literals that reach the page
  (decision D3), which are listed in translation/code-strings.md for review;
- display-only fences outside prompt boxes: byte-for-byte identical; fences in a
  `.prompt` box (decision D4) are translated, but every backticked literal and file path in
  the English prompt must appear in the Spanish one;
- headings: the same levels in the same order, with the same IDs and classes;
- the same set of IDs ({#...}, #| label), cross-references (@sec-..., any case), URLs
  (a link to the English website edition may become one to the Spanish edition), image paths,
  shortcodes and inline `{python}` expressions; other inline code is compared as a multiset
  and reported as a warning.

Run from the repository root:  python3 translation/compare.py [files...]
With no arguments it compares every Spanish file that exists.
"""
from __future__ import annotations

import io
import re
import sys
import tokenize
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN, ES = ROOT / "book", ROOT / "book-es"
REPORT = ROOT / "translation" / "code-strings.md"
CAPTION_OPTIONS = {"fig-cap", "fig-alt", "tbl-cap", "fig-subcap", "lst-cap", "tbl-subcap"}
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*(\{[^}]*\})?\s*$")
ID = re.compile(r"(?<![\w&])#([A-Za-z][\w:.-]*[\w-])")
REF = re.compile(r"(?<![\w@`])@([A-Za-z]+-[\w-]*\w)")
URL = re.compile(r"https?://[^\s)\"'>\]]+")
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
SHORTCODE = re.compile(r"\{\{<.*?>\}\}")
INLINE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
PROMPT_DIV = re.compile(r"^:{3,}\s*\{?[^}\n]*\bprompt\b")
LITERAL_PATH = re.compile(r"[\w.~-]*[/.][\w./~*-]*\w")


def blocks(text: str):
    """Split a .qmd into ('prose', text) and ('fence', info, body, in_prompt) items."""
    out, prose, lines, i = [], [], text.split("\n"), 0
    prompt_pending = False
    while i < len(lines):
        line = lines[i]
        m = FENCE.match(line)
        if m:
            marker, info = m.group(2), m.group(3).strip()
            body, j = [], i + 1
            while j < len(lines) and not re.match(rf"^\s*{re.escape(marker[0])}{{{len(marker)},}}\s*$", lines[j]):
                body.append(lines[j])
                j += 1
            out.append(("prose", "\n".join(prose)))
            prose = []
            out.append(("fence", info, "\n".join(body), prompt_pending))
            prompt_pending = False
            i = j + 1
            continue
        if PROMPT_DIV.match(line):
            prompt_pending = True
        elif line.startswith(":::") and not line.strip(": ") == "":
            prompt_pending = False
        prose.append(line)
        i += 1
    out.append(("prose", "\n".join(prose)))
    return out


def split_cell(body: str):
    opts, code = [], []
    for line in body.split("\n"):
        (opts if line.startswith("#|") and not code else code).append(line)
    return opts, "\n".join(code)


def option_key(line: str) -> str:
    return line[2:].split(":", 1)[0].strip()


def tokens(code: str):
    """(kind, text) per token; kind 'str' for string literals and f-string text."""
    out = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(code + "\n").readline):
            if tok.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
                            tokenize.ENDMARKER):
                continue
            if tok.type == getattr(tokenize, "FSTRING_MIDDLE", -1):
                # An f-string's text may gain or lose a segment in translation ("its own {n}" ->
                # "sus {n} propias"); its expressions and delimiters still have to match.
                out.append(("fstr", tok.string))
                continue
            kind = "str" if tok.type == tokenize.STRING else "tok"
            out.append((kind, tok.string))
    except (tokenize.TokenError, IndentationError, SyntaxError) as e:
        out.append(("error", str(e)))
    return out


QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")


def mask(expr: str) -> str:
    """An inline expression with its string literals blanked: they may be translated
    (`.replace(' and ', ' or ')` -> `.replace(' y ', ' o ')`), the rest may not."""
    return QUOTED.sub('""', expr) if "replace(" in expr or "join(" in expr else expr


def norm_url(u: str) -> str:
    u = u.rstrip(".,:;")
    return u.replace("quarto-workshop/book/es/", "quarto-workshop/book/").replace(
        "quarto-workshop/ebook/es/", "quarto-workshop/ebook/").replace(
        "prompt-check-publish-es.epub", "prompt-check-publish.epub")


def auto_id(text: str) -> str:
    """Pandoc's auto_identifiers, for a heading with no explicit ID (heading_ids.py has the same)."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_]", "", text) if "`" in text or "*" in text else text
    text = "".join(ch for ch in text.lower() if ch.isalnum() or ch in " _-.")
    text = re.sub(r"^[^a-z]+", "", re.sub(r"\s+", "-", text.strip()))
    return text or "section"


def repeated_auto_ids() -> set[str]:
    """English headings without an explicit ID whose automatic ID recurs across the book (such
    as #summary). A single-document EPUB numbers repeats (summary-1, ...), which an explicit ID
    cannot do, so their Spanish twins keep Pandoc's automatic IDs, and any ID is accepted."""
    from collections import Counter
    seen, explicit = Counter(), set()
    for pattern in ("*.qmd", "chapters/*.qmd", "appendices/*.qmd"):
        for path in EN.glob(pattern):
            blocks_ = [b[1] for b in blocks(path.read_text()) if b[0] == "prose"]
            for text in blocks_:
                explicit |= set(ID.findall(" ".join(re.findall(r"\{[^{}\n]*\}", text))))
                for line in text.split("\n"):
                    m = HEADING.match(line)
                    if m and not any(a.startswith("#") for a in (m.group(3) or "{}")[1:-1].split()):
                        seen[auto_id(m.group(2))] += 1
    # Repeated, or taken by an explicit ID elsewhere (Pandoc then numbers the automatic one).
    return {k for k, v in seen.items() if v > 1 or k in explicit}


REPEATED: set[str] = set()


def headings(prose_parts):
    """(level, effective ID, other attributes) per heading: an explicit #id, else Pandoc's."""
    hs = []
    for text in prose_parts:
        for line in text.split("\n"):
            m = HEADING.match(line)
            if m:
                attrs = (m.group(3) or "{}")[1:-1].split()
                ids = [a[1:] for a in attrs if a.startswith("#")]
                rest = tuple(a for a in attrs if not a.startswith("#"))
                hs.append((len(m.group(1)), ids[0] if ids else auto_id(m.group(2)), rest, bool(ids)))
    return hs


# Differences a translation needs and the checks would otherwise reject, each with its reason.
# Keyed by file, then by check, then by the exact item; reported as accepted, not as errors.
EXCEPTIONS = {
    "appendices/f-translation.qmd": {
        "URLs": {
            "https://project-delphi.github.io/quarto-workshop/book/": "the brief asked appendix F to "
            "say that this Spanish edition exists; the note links its website edition",
        },
    },
    "chapters/09-explore.qmd": {
        "inline {python}": {
            "{python} rural_med_band": "an English band name (\"low\") inside a sentence; the "
            "Spanish types \"bajo\", which the cell's own guard on fig-wat-years keeps true",
        },
    },
}


def compare(rel: str, strings: list) -> tuple[list[str], list[str]]:
    en, es = (EN / rel).read_text(), (ES / rel).read_text()
    be, bs = blocks(en), blocks(es)
    errors, warnings = [], []
    fe = [b for b in be if b[0] == "fence"]
    fs = [b for b in bs if b[0] == "fence"]
    pe = [b[1] for b in be if b[0] == "prose"]
    ps = [b[1] for b in bs if b[0] == "prose"]
    if len(fe) != len(fs):
        errors.append(f"{len(fe)} fences in English, {len(fs)} in Spanish")
    for n, (a, b) in enumerate(zip(fe, fs), 1):
        if a[1] != b[1]:
            errors.append(f"fence {n}: info {a[1]!r} became {b[1]!r}")
            continue
        if a[1].startswith("{python"):
            oa, ca = split_cell(a[2])
            ob, cb = split_cell(b[2])
            ka = [l for l in oa if option_key(l) not in CAPTION_OPTIONS]
            kb = [l for l in ob if option_key(l) not in CAPTION_OPTIONS]
            if ka != kb:
                errors.append(f"cell {n}: options differ: {sorted(set(ka) ^ set(kb))}")
            if [option_key(l) for l in oa] != [option_key(l) for l in ob]:
                errors.append(f"cell {n}: option keys differ")
            ta, tb = tokens(ca), tokens(cb)
            sa, sb = [x for x in ta if x[0] != "fstr"], [x for x in tb if x[0] != "fstr"]
            if len(sa) != len(sb) or any(x[0] != y[0] or (x[0] != "str" and x[1] != y[1])
                                         for x, y in zip(sa, sb)):
                diff = next(((x, y) for x, y in zip(sa, sb) if x != y and (x[0] != "str" or y[0] != "str")),
                            (sa[len(sb):len(sb) + 1], sb[len(sa):len(sa) + 1]))
                errors.append(f"cell {n}: code differs beyond string literals, first at {diff}")
            else:
                strings += [(rel, n, x[1], y[1]) for x, y in zip(sa, sb) if x[1] != y[1]]
                fa, fb = [x[1] for x in ta if x[0] == "fstr"], [x[1] for x in tb if x[0] == "fstr"]
                if fa != fb:
                    strings.append((rel, n, " · ".join(fa), " · ".join(fb)))
        elif b[3]:  # a prompt: translated, its literals kept
            lits = (set(INLINE.findall(a[2])) | set(LITERAL_PATH.findall(a[2]))) - {"e.g", "i.e", "etc"}
            missing = sorted(l for l in lits if l not in b[2])
            if missing:
                errors.append(f"prompt in fence {n}: literals missing from the Spanish: {missing}")
        elif a[2] != b[2]:
            errors.append(f"fence {n} ({a[1] or 'plain'}): body differs")
    he, hs = headings(pe), headings(ps)
    if not REPEATED:
        REPEATED.update(repeated_auto_ids())
    # A Spanish heading may keep its own automatic ID only where the English one is automatic
    # and repeated (see repeated_auto_ids); an explicit English ID must always be kept.
    hs = [(lvl, en[1] if en[1] in REPEATED and not en[3] and not sx else sid, rest, en[3])
          for (lvl, sid, rest, sx), en in zip(hs, he + [(None, None, None, False)] * len(hs))]
    he = [(lvl, eid, rest, ex) for lvl, eid, rest, ex in he]
    if [h[:3] for h in he] != [h[:3] for h in hs]:
        errors.append(f"headings differ: {len(he)} vs {len(hs)}; first difference "
                      f"{next(((x, y) for x, y in zip(he, hs) if x != y), None)}")
    joined_e, joined_s = "\n".join(pe), "\n".join(ps)
    cells_e = "\n".join(b[2] for b in fe if b[1].startswith("{python"))
    cells_s = "\n".join(b[2] for b in fs if b[1].startswith("{python"))
    label = lambda t: set(re.findall(r"^#\|\s*label:\s*(\S+)", t, re.M))
    attrs = lambda t: " ".join(re.findall(r"\{[^{}\n]*\}", t))
    checks = {
        "IDs": (set(ID.findall(attrs(joined_e))) | label(cells_e) | {h[1] for h in he},
                set(ID.findall(attrs(joined_s))) | label(cells_s) | {h[1] for h in hs}),
        "cross-references": ({r.lower() for r in REF.findall(joined_e + cells_e)},
                             {r.lower() for r in REF.findall(joined_s + cells_s)}),
        "URLs": ({norm_url(u) for u in URL.findall(en)}, {norm_url(u) for u in URL.findall(es)}),
        "image paths": (set(IMAGE.findall(joined_e)), set(IMAGE.findall(joined_s))),
        "shortcodes": (set(SHORTCODE.findall(joined_e)), set(SHORTCODE.findall(joined_s))),
        "inline {python}": (Counter(mask(c) for c in INLINE.findall(joined_e) if c.startswith("{python}")),
                            Counter(mask(c) for c in INLINE.findall(joined_s) if c.startswith("{python}"))),
    }
    accepted = EXCEPTIONS.get(rel, {})
    for what, (a, b) in checks.items():
        if a != b:
            gone = sorted((a - b) if isinstance(a, set) else (a - b).elements())
            new = sorted((b - a) if isinstance(b, set) else (b - a).elements())
            ok = accepted.get(what, {})
            for item in [*gone, *new]:
                if item in ok:
                    warnings.append(f"accepted exception in {what}: {item!r}: {ok[item]}")
            gone = [g for g in gone if g not in ok]
            new = [n for n in new if n not in ok]
            if gone or new:
                errors.append(f"{what} differ: only in English {gone}; only in Spanish {new}")
    ia = Counter(c for c in INLINE.findall(joined_e) if not c.startswith("{python}"))
    ib = Counter(c for c in INLINE.findall(joined_s) if not c.startswith("{python}"))
    if ia != ib:
        warnings.append(f"inline code differs: only in English {sorted((ia - ib).elements())}; "
                        f"only in Spanish {sorted((ib - ia).elements())}")
    return errors, warnings


def main(args: list[str]) -> int:
    rels = args or sorted(str(p.relative_to(ES)) for pattern in ("*.qmd", "chapters/*.qmd", "appendices/*.qmd")
                          for p in ES.glob(pattern))
    strings, failed = [], 0
    for rel in rels:
        rel = str(Path(rel).relative_to("book-es")) if rel.startswith("book-es/") else rel
        if not (EN / rel).exists():
            print(f"{rel}: no English original")
            failed += 1
            continue
        errors, warnings = compare(rel, strings)
        status = "ok" if not errors else "MISMATCH"
        print(f"{rel}: {status}" + (f" ({len(warnings)} warning)" if warnings else ""))
        for e in errors:
            print(f"  error: {e}")
        for w in warnings:
            print(f"  warning: {w}")
        failed += bool(errors)
    if not args:
        lines = ["# Code string literals changed in the Spanish edition",
                 "",
                 "Written by `translation/compare.py`: every string literal in an executable cell that",
                 "differs between `book/` and `book-es/` (decision D3 in `PLAN.md`). Everything else",
                 "in the cells is identical. Review that each one only reaches the page.",
                 "",
                 "| File | Cell | English | Spanish |",
                 "|---|--:|---|---|"]
        esc = lambda s: s.replace("|", "\\|").replace("\n", "\\n")
        lines += [f"| `{r}` | {n} | `{esc(a)}` | `{esc(b)}` |" for r, n, a, b in strings]
        REPORT.write_text("\n".join(lines) + "\n")
        print(f"{len(strings)} changed string literals listed in {REPORT.relative_to(ROOT)}")
    print(f"{len(rels)} files compared, {failed} with mismatches")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
