"""Check Spanish prose against translation/glossary.md: words the glossary rules out.

Code fences, inline code and URLs are skipped; everything else (prose, captions and alt
text) is checked. Run from the repository root:

    python3 translation/lint.py [book-es/chapters/09-explore.qmd ...]

With no arguments it checks every .qmd in book-es/ and ebook/es/. Exit status 1 on a hit.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (pattern, what to write instead). Patterns are case-insensitive and match whole words.
RULES = [
    (r"clusters?|clusteres", "clúster, clústeres"),
    (r"ordenador(es)?|computador(es)?", "computadora"),
    (r"ficheros?", "archivo"),
    (r"vosotros|vosotras|vuestr[oa]s?|habéis|tenéis|podéis|queréis|sabéis|(?-i:os)", "the tú form"),
    (r"usted", "the tú form"),
    (r"coger|cogemos|coge", "tomar"),
    (r"(un|el|tu|del|al) móvil|los móviles", "teléfono"),
    (r"renderización(es)?", "renderizado"),
    (r"carpeta de inicio", "carpeta personal"),
    (r"puntuaci[oó]n(es)? z", "puntaje z"),
    (r"desviaci[oó]n(es)? t[ií]picas?", "desviación estándar"),
    (r"commitear|commiteas?|pushear|pusheas?", "hacer commit / hacer push"),
    (r"el terminal|un terminal|los terminales", "la terminal"),
    (r"la commit|una commit", "el commit"),
    (r"checkpoints?|puntos? de chequeo", "punto de control"),
    (r"asistentes? de código", "asistente de programación"),
    (r"arn[eé]s", "harness"),
    (r"sub-agentes?", "subagente"),
    (r"prestar|rendir", "renderizar"),
    (r"zona-años", "zonas-año"),
    # The reader's gender is never assumed (glossary, conventions).
    (r"tú mism[oa]s?|est(ás|és|arás) (list[oa]|segur[oa]|atascad[oa]|perdid[oa]|preparad[oa])", "a neutral phrasing"),
    (r"(sé|seas) (específic[oa]|concret[oa]|cuidados[oa])", "a neutral phrasing"),
]
# Words the glossary rules out but a file must quote, such as a machine translation's mistakes.
ALLOW = {("book-es/appendices/f-translation.qmd", "Prestar")}
STRIP = [
    re.compile(r"^(\s*)(`{3,}).*?^\1\2\s*$", re.S | re.M),  # fences
    re.compile(r"`[^`\n]+`"),                                # inline code
    re.compile(r"https?://\S+"),                             # URLs
    re.compile(r"\]\([^)]*\)"),                              # link and image targets
    re.compile(r"\{#[^}]*\}|\{\.[^}]*\}"),                   # attribute blocks without text
    re.compile(r"@[A-Za-z]+-[\w-]+"),                        # cross-references
]


# A line that starts "@label." or "(@label)" becomes a Pandoc example list (book/README.md).
EXAMPLE_LIST = re.compile(r"^\s*(\(@[A-Za-z][\w-]*\)|@[A-Za-z][\w-]*\.)(\s|$)")


def lint(path: Path) -> list[str]:
    raw_lines = path.read_text().split("\n")
    early = [f"{path.relative_to(ROOT)}:{n}: a line starting with a cross-reference becomes an example list: rewrap it"
             for n, line in enumerate(raw_lines, 1) if EXAMPLE_LIST.match(line)]
    text = path.read_text()
    for pattern in STRIP:
        text = pattern.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    hits = list(early)
    references = False  # reading lists quote English titles
    for n, line in enumerate(text.split("\n"), 1):
        if line.startswith("#"):
            references = line.startswith("## Lecturas adicionales")
        if references:
            continue
        for pattern, instead in RULES:
            for m in re.finditer(rf"(?<![\w-])(?:{pattern})(?![\w-])", line, re.I):
                if (str(path.relative_to(ROOT)), m.group(0)) in ALLOW:
                    continue
                hits.append(f"{path.relative_to(ROOT)}:{n}: {m.group(0)!r} -> {instead}")
    return hits


def main(args: list[str]) -> int:
    paths = [Path(a).resolve() for a in args] or sorted(
        p for pattern in ("book-es/*.qmd", "book-es/chapters/*.qmd", "book-es/appendices/*.qmd",
                          "ebook/es/*.qmd") for p in ROOT.glob(pattern))
    hits = [h for p in paths for h in lint(p)]
    print("\n".join(hits) if hits else f"{len(paths)} files, no glossary hits")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
