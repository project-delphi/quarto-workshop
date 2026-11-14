"""While the translation is in progress: limit book-es/'s generated profiles to the files that
exist, so a partial edition renders. `book/scripts/sync_chapters.py --book ../book-es` writes
the full lists back. Run from book-es/ with the book's environment:

    uv run --project ../book python ../translation/partial_profiles.py
"""
import os

import yaml

for name in ("html", "epub"):
    path = f"_quarto-{name}.yml"
    data = yaml.safe_load(open(path))

    def keep(items):
        out = []
        for item in items:
            if isinstance(item, dict):
                if os.path.exists(item["part"]):
                    out.append({"part": item["part"],
                                "chapters": [c for c in item["chapters"] if os.path.exists(c)]})
            elif os.path.exists(item):
                out.append(item)
        return out

    data["book"]["chapters"] = keep(data["book"]["chapters"])
    data["book"]["appendices"] = keep(data["book"].get("appendices", []))
    if not data["book"]["appendices"]:
        del data["book"]["appendices"]
    with open(path, "w") as f:
        f.write("# PARTIAL (translation/partial_profiles.py): only the files that exist.\n")
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
