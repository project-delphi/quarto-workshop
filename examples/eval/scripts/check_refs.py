"""Check every reference with a DOI in references.bib against the DOI's registry.

Run from the project root, with network access, before publishing a document that cites
references.bib (it is not part of the render):

    uv run python scripts/check_refs.py

For each entry with a `doi`, it asks doi.org which agency registered the DOI, then fetches
the record from that agency's public API: Crossref (https://api.crossref.org/works/<doi>)
for journal articles and proceedings, DataCite (https://api.datacite.org/dois/<doi>) for
datasets such as the UCI one. It fails when the DOI does not resolve, or when the record's
year, first author's family name or title disagrees with the .bib entry. Names and titles
are compared after normalising: accents, braces, capitals and punctuation are ignored.
Entries without a DOI (the statute) are listed and must be checked by hand.

It prints one row per entry and exits with status 1 if any check fails.
"""

import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BIB = Path("references.bib")
# A plain client name and no contact address: the APIs accept requests without one.
HEADERS = {"User-Agent": "acme-eval-check (scripts/check_refs.py)"}
TIMEOUT = 30  # seconds per request


def entries(text: str) -> dict[str, dict[str, str]]:
    """The entries of a .bib file: {key: {field: value}}, values without their outer braces."""
    found = {}
    for match in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,", text):
        key, depth, i = match.group(1), 1, match.end()
        start = i
        while depth and i < len(text):  # find the entry's closing brace
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        if depth:
            raise ValueError(f"{key}: unbalanced braces: the entry never closes")
        body, fields = text[start:i - 1], {}
        # A value is in braces, in double quotes, or bare (a number such as a year), as
        # reference managers export them.
        for field in re.finditer(r'(\w+)\s*=\s*(\{|"|(?=\d))', body):
            name, opener, j = field.group(1).lower(), field.group(2), field.end()
            if opener == "{":
                depth = 1
                while depth and j < len(body):
                    depth += {"{": 1, "}": -1}.get(body[j], 0)
                    j += 1
                if depth:
                    raise ValueError(f"{key}: unbalanced braces in {name}")
                value = body[field.end():j - 1]
            elif opener == '"':
                end = body.index('"', j)
                value = body[j:end]
            else:
                value = re.match(r"\d+", body[j:]).group(0)
            fields[name] = " ".join(value.split())
        found[key] = fields
    return found


def plain(text: str) -> str:
    """Lower-case letters and digits only: no LaTeX accents, braces, accents or punctuation."""
    text = re.sub(r"\\[`'^\"~=.]|\\[a-zA-Z]+\s*", "", text).replace("{", "").replace("}", "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def first_family(authors: str) -> str:
    """The family name of the first author in a BibTeX author list."""
    first = re.split(r"\s+and\s+", authors)[0]
    return first.split(",")[0] if "," in first else first.split()[-1]


def get(url: str) -> dict:
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return json.load(response)


def record(doi: str) -> dict:
    """Year, first author's family name and title from the DOI's registration agency."""
    quoted = urllib.parse.quote(doi, safe="/")
    answer = get(f"https://doi.org/doiRA/{quoted}")[0]
    agency = answer.get("RA")
    if agency is None:
        raise LookupError(f"doi.org: {answer.get('status', 'no registration agency')}")
    if agency == "Crossref":
        work = get(f"https://api.crossref.org/works/{quoted}")["message"]
        title = " ".join(work.get("title", [""])[:1] + work.get("subtitle", [])[:1])
        date = work.get("published-print") or work.get("issued")
        return {"agency": agency, "year": str(date["date-parts"][0][0]),
                "family": work["author"][0].get("family", ""), "title": title}
    if agency == "DataCite":
        work = get(f"https://api.datacite.org/dois/{quoted}")["data"]["attributes"]
        creator = work["creators"][0]
        return {"agency": agency, "year": str(work["publicationYear"]),
                "family": creator.get("familyName") or creator.get("name", ""),
                "title": work["titles"][0]["title"]}
    raise LookupError(f"registered with {agency}, whose records this script does not read")


def check(key: str, fields: dict[str, str]) -> tuple[str, list[str]]:
    """One row of the table and the entry's problems."""
    doi = fields["doi"]
    try:
        found = record(doi)
    except (OSError, LookupError, KeyError, IndexError, ValueError) as error:  # OSError: URLError, timeouts
        return f"{key:30} {doi:40} {'?':9} DOES NOT RESOLVE", [f"{key}: {doi}: {error}"]
    problems = []
    if found["year"] != fields.get("year"):
        problems.append(f"{key}: year {fields.get('year')} in .bib, {found['year']} at {found['agency']}")
    family, theirs = plain(first_family(fields.get("author", ""))), plain(found["family"])
    # DataCite records sometimes hold "S. Moro" as the family name: accept the name as a word in it.
    if family != theirs and family not in theirs.split():
        problems.append(f"{key}: first author {family!r} in .bib, {theirs!r} at {found['agency']}")
    if plain(fields.get("title", "")) != plain(found["title"]):
        problems.append(f"{key}: title differs from {found['agency']}: {found['title']!r}")
    status = "ok" if not problems else "MISMATCH"
    return (f"{key:30} {doi:40} {found['agency']:9} {found['year']} "
            f"{found['family'][:16]:16} {status}"), problems


def main() -> int:
    failures = []
    print(f"{'entry':30} {'doi':40} {'agency':9} year first author     result")
    try:
        found = entries(BIB.read_text(encoding="utf-8"))
    except ValueError as error:
        print(f"{BIB} cannot be read: {error}", file=sys.stderr)
        return 1
    for key, fields in found.items():
        if "doi" not in fields:
            print(f"{key:30} {'(no DOI: check by hand)':40}")
            continue
        row, problems = check(key, fields)
        print(row)
        failures += problems
    for failure in failures:
        print(failure, file=sys.stderr)
    print(f"{len(failures)} problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
