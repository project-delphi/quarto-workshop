# Checkpoint 20 · Pull requests and builds you can trust

Checkpoint 19 plus what a team needs to accept changes, an agent's or a person's, without
taking them on trust. `.github/workflows/check.yml` rebuilds the project on every pull
request and push to `main` (compute `outputs/`, run the tests, render the site, check it), so
a guard that no longer holds (`ClaimError`) turns the pull request red. `publish.yml` runs the
same build on `main` and deploys `_site/` to GitHub Pages; `monthly.yml` renders every report
as PDF on the 2nd of each month, keeps them as a downloadable artifact, and checks the
references. `.github/pull_request_template.md` puts the three checks (scope, correctness,
rebuild) and a line on what an agent did not verify on every pull request. `AGENTS.md` adds
the team rules: a branch per change, one change per pull request, never push to `main`, run
CI's commands before saying a change is done, and treat CI as the source of truth. Acme
Signals is a fictional company; the bank data are real (`data/README.md`).

The workflows run only on GitHub, once `acme-eval/` is a repository there; *Publish* also
needs the one-time setting Settings → Pages → Source: GitHub Actions. Copying this
checkpoint changes no setting and pushes nothing.

Sources and data only: no `outputs/`, no `reports/` and no rendered files. `uv run` builds
`.venv/` from `uv.lock` on first use.

## Catch up

Ask your coding agent, started in `acme-eval/`:

```text
Catch me up: follow ../quarto-workshop/checkpoints/20-eval-ci/README.md
```

The steps, run inside `acme-eval/` (by the agent, or by you in a terminal):

1. Keep your work, all but the `.venv/` environment (`uv run` rebuilds it from `uv.lock`): `b="../acme-eval-backup-20-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"` (a new time-stamped copy beside `acme-eval/`, so earlier backups are kept).
2. Copy the checkpoint here: `cp -R ../quarto-workshop/checkpoints/20-eval-ci/. .`
3. Compute and test, as CI does: `uv run python scripts/evaluate.py && uv run pytest -q` (about 20 seconds; every test passes).
4. Build the site and check it, as CI does: `uv run quarto render && uv run python scripts/check_site.py` (about 50 seconds; the check ends "6 pages checked, 0 problems").
5. Check: `ls .github/workflows` lists `check.yml`, `monthly.yml` and `publish.yml`, and `.github/pull_request_template.md` lists the three checks. If `acme-eval/` is on GitHub, commit them on a branch, push the branch and open a pull request: the *Check* run appears on it and turns green.
6. Rejoin: your folder now holds the end of these steps. Continue at the catch-up box of the team chapter, "Pull Requests and Builds You Can Trust".
