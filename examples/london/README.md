# London guide: finished Part 1 project

The finished Part 1 project: `london.qmd` in six formats, the dashboard (attractions and churches pages), the partner brief and its covering email, the flyer, the ⭐ social card and the ⭐ white paper, published as one website by `_quarto.yml`. Every number comes from `data/` (cited ALVA tables); photo credits are in `images/ATTRIBUTION.md`.

`london-whitepaper.qmd` is an academic-style paper (abstract, introduction, methods, results, conclusions and references from `references.bib`) on the pandemic loss and recovery of visits, 2015–2025. It is a Typst PDF styled like a LaTeX article: New Computer Modern, the font Typst bundles, so it needs no LaTeX install.

`AGENTS.md` holds the project's rules for the coding assistant, and `pyproject.toml` with `uv.lock` its Python environment, which `uv run` builds on first use.

## Catch up

Ask your coding assistant, started in `london-guide/`:

```text
Catch me up: follow ../quarto-workshop/examples/london/README.md
```

The steps, run inside `london-guide/` (by the assistant, or by you in a terminal):

1. Keep your work, all but the `.venv/` environment (`uv run` rebuilds it from `uv.lock`): `b="../london-guide-backup-final-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"` (a new time-stamped copy beside `london-guide/`, so earlier backups are kept).
2. Copy the finished project here: `cp -R ../quarto-workshop/examples/london/. .`
3. If you have published already, keep your repository's README, which step 2 overwrote: `git checkout -- README.md`.
4. Remove `london.md` if it is still there: `london.qmd` replaces it, and both would write `london.html`.
5. Render the site: `uv run quarto render` (writes `_site/`).
6. Check: `_site/index.html` opens with Guide, Dashboard and Downloads in the navbar, and Downloads links the white paper, `_site/london-whitepaper.pdf`.
7. Rejoin: if your site is not live yet, paste the prompt and run the publish command on 🚀 *Publish* ([slide](https://project-delphi.github.io/quarto-workshop/#/london-publish)); after the 🍽️ meal break, everyone starts 💧 *Part 2* together at 2:55 ([slide](https://project-delphi.github.io/quarto-workshop/#/part-2)).

## Publishing troubleshooting

*(See also the repository-wide [Troubleshooting Guide](../../TROUBLESHOOTING.md).)*

- The first `uv run quarto publish gh-pages` must be interactive: answer its question with
  Enter. With `--no-prompt`, Quarto 1.6.40 stops with "the remote origin does not have a
  branch named gh-pages"; Quarto's guide asks for one local publish first
  (https://quarto.org/docs/publishing/github-pages.html, checked 2026-11-01). Once the
  `gh-pages` branch exists, `--no-prompt` works for updates.
- A push that fails with `HTTP 400` (`RPC failed`, `the remote end hung up unexpectedly`)
  usually succeeds after `git config http.postBuffer 524288000`.
- A 404 right after publishing: wait a minute and reload.
