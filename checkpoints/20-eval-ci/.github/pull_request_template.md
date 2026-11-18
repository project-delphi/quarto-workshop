## What this changes

<!-- One coherent change: what it does and why, in a sentence or two. -->

## Review: the three checks

Every change passes them, whoever or whatever made it.

- [ ] **Scope.** Only the files this change needs are in *Files changed*. Nothing in `data/`
      (read-only); no `outputs/`, `reports/`, `_site/`, `.venv/` or rendered files
      (`*.html`, `*.docx`, `*.pdf`, `*.pptx`, `*_files/`) except the reference documents in
      `templates/`; `tests/` changed only if the
      change is to what is tested, and then says why. A change to `_brand.yml` comes with
      the remade `templates/`.
- [ ] **Correctness.** At least one changed number or sentence checked against its source:
      a figure against `outputs/metrics.csv`, `outputs/summary.json` or
      `outputs/segments.csv` (after `uv run python scripts/evaluate.py`), never typed by
      hand; new wording that depends on results ("best", "higher") has a `claim(...)` guard;
      a new citation is in `references.bib` with a DOI and was read; anything from
      `data/synthetic_business.csv` says SYNTHETIC.
- [ ] **Rebuild.** The *Check* workflow is green on this pull request: it computes
      `outputs/`, runs the tests, renders the site and checks it, from a fresh clone. A red
      *Render the site* step with `ClaimError` names the sentence the results no longer
      support.

## Made with a coding agent?

<!-- Which agent and model, and what it did not verify (for example: "Claude Code; did not
open the PDF", "Codex; check_refs.py not run, no network"). Write "No" if not. -->
