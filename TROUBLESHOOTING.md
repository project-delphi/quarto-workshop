# Troubleshooting & Common Gotchas

This guide collects tested solutions for common issues encountered during the Quarto workshop, organized by category.

---

## 0. Windows setup (WSL / Ubuntu)

*Written from Microsoft's, GitHub's and Quarto's documentation. At the workshop of 2026-11-05 Windows participants found the WSL install and finding their way through the setup slides hardest; the deck now numbers the setup steps (🧭 1–6) and has a stuck-table slide. Not yet re-run on a clean Windows machine.*

### Any error, any step
- **Fix**: copy the command and the full error, paste them into a web chat (Gemini, Claude or ChatGPT) with your system (Windows + Ubuntu, or Mac), and try the suggested fix one step at a time. No passwords or keys in the paste. Still stuck: Discord `#help`.

### Downloads stall or time out
- A weak connection is the usual cause. Use a wired or strong Wi-Fi connection (or a phone hotspot) and rerun the step.

### `wsl --install -d Ubuntu` hangs, fails, or Ubuntu will not start
- **Fix**: Run PowerShell **as administrator**. A hang at 0.0%: `wsl --install --web-download -d Ubuntu`. **Restart your computer** when it finishes. Already installed ("already exists")? Skip the install and open "Ubuntu" from the Start menu. Check with `wsl -l -v` (VERSION 2).
- **Error `0x80370102`**: virtualization is off in the BIOS/UEFI (Task Manager → Performance → CPU shows "Virtualization"). Without administrator rights or BIOS access you cannot fix this: tell the organiser before the day.
- **Needs** Windows 10 build 19041 or later, or Windows 11.

### The Ubuntu password prompt shows nothing while typing
- Normal: Linux hides the password. Type it and press Enter. `sudo` asks for the same password later.

### `command not found` for `uv`, `claude`, `codex` or `agy` right after installing
- **Fix**: open a **new** Ubuntu tab (the installer changed your shell's search path), then try again.

### `quarto: command not found`, or it works in PowerShell but not Ubuntu
- Windows installers put tools where Ubuntu cannot use them. Install Quarto **inside Ubuntu** by running the 🐧 install prompt from the deck in your assistant, then open a new tab. Check `quarto --version` (1.10 or newer).

### The prompt shows `/mnt/c/...`
- You are in a Windows folder (for example OneDrive). Run `cd ~` and keep workshop folders there.

### `gh auth login` or the assistant cannot open a browser
- Expected in WSL. Copy the URL or one-time code it prints into your Windows browser (for `gh`: github.com/login/device), authorise, and return to the terminal. Codex: `codex login --device-auth` if the browser sign-in fails.

### Downloads or `git clone` fail on a company network
- A proxy or TLS inspection can block `curl`, `git` and `uv`. Try another network (phone hotspot) and tell the organiser.

### `git commit` says "Please tell me who you are"
- Run the two `git config --global` lines from the Setup Check with **your** name and email.

### `not a valid Python environment` (a stale `.venv`)
- Delete it and run again; `uv run` rebuilds it: `rm -rf .venv`.

---

## 1. Publishing to GitHub Pages

### First publish fails with "the remote origin does not have a branch named gh-pages"
- **Cause**: In Quarto 1.6.40, `quarto publish gh-pages --no-prompt` cannot create the `gh-pages` branch if it does not already exist on GitHub.
- **Fix**: The first publish **must be run interactively**:
  ```bash
  uv run quarto publish gh-pages
  ```
  When prompted with `? Update site at https://<user>.github.io/<repo>/? (Y/n)`, press **Enter** (Yes).
- **Subsequent updates**: Once the `gh-pages` branch exists on GitHub, non-interactive updates work smoothly:
  ```bash
  uv run quarto publish gh-pages --no-prompt
  ```
  *(See official [Quarto GitHub Pages documentation](https://quarto.org/docs/publishing/github-pages.html).)*

### Push fails with `HTTP 400` (`RPC failed`, `the remote end hung up unexpectedly`)
- **Cause**: Git's default HTTP post buffer is too small when pushing larger project builds (such as Plotly dashboards with bundled GeoJSON maps, typically 12–20 MB).
- **Fix**: Increase the buffer size in your local project configuration:
  ```bash
  git config http.postBuffer 524288000
  ```
  Then re-run the publish or push command.

### 404 Not Found immediately after publishing
- **Cause**: GitHub Pages takes between 20 and 60 seconds to process the pushed `gh-pages` branch and deploy it to the CDN edge.
- **Fix**: Wait 60 seconds, then hard-refresh the page in your browser (`Cmd+Shift+R` on macOS, `Ctrl+F5` on Linux/Windows). You can also verify build status under **Repository Settings → Pages**.

---

## 2. Rendering & Live Preview

### File conflict error: `readfile 'london.quarto_ipynb'` or locked files
- **Cause**: A live `quarto preview` process was running in the background while your coding assistant or terminal ran `quarto render`. Both processes attempt to read and write temporary Jupyter notebook cache files simultaneously.
- **Fix**:
  1. Do not run manual `quarto render` commands while `quarto preview` is actively running. Quarto preview automatically detects file changes and re-renders pages on save.
  2. If switching to multi-format exports (`docx`, `pdf`, `pptx`), stop the preview server (`Ctrl+C` in the terminal where preview is running), run `uv run quarto render`, and restart preview afterward.

### PDF generation fails in Typst: `cannot parse length '60px'`
- **Cause**: Quarto's bundled Typst engine does not accept CSS pixel units (`px`) in Markdown image dimension attributes.
- **Fix**: Use unitless numbers for height/width (which Typst parses as points) or relative percentages:
  - ❌ Incorrect: `![](image.png){height=60px}`
  - ✅ Correct: `![](image.png){height=60}` or `![](image.png){width="30%"}`

### Plotly charts appear twice inside Quarto Dashboard cards
- **Cause**: A cell calls `fig.show()` or returns the figure object multiple times, causing Quarto's dashboard renderer to insert both the standard output and the returned object.
- **Fix**: Do not call `fig.show()`. Simply assign the figure and end the cell with the figure name:
  ```python
  fig = px.bar(...)
  fig
  ```

### `itables` drops rows silently in the water dashboard
- **Cause**: By default, `itables` limits the serialized data size to prevent large payloads from freezing the browser.
- **Fix**: Set `maxBytes=0` when rendering tables intended to display the full dataset:
  ```python
  from itables import show
  show(df, maxBytes=0)
  ```

---

## 3. Python, Jupyter & Environment

### `quarto check` reports `Jupyter: (None)` or `Jupyter is not available`
- **Status**: **Harmless — ignore during setup**.
- **Reason**: The workshop intentionally does not rely on a globally installed Jupyter environment. Each project folder (`london-guide/`, `water-quality/`) manages its own self-contained virtual environment via [uv](https://docs.astral.sh/uv/) (`pyproject.toml` and `uv.lock`). Quarto runs Python and Jupyter through `uv run`.

### Warning: `Kernel is running over TCP`
- **Status**: **Harmless**.
- **Reason**: `ipykernel` reports communication over local TCP loopback when Quarto launches kernel instances. It does not affect computation or output.

### Missing data in checkpoints 05–13
- **Cause**: To keep checkpoint snapshots lightweight, checkpoints 05 through 13 contain analysis and document sources only; they do not bundle the 5.1 MB `water_municipal.csv` dataset.
- **Fix**: Copy `data/` from the workshop examples:
  ```bash
  cp -R ../quarto-workshop/examples/water/data .
  ```

### Backup commands copying hundreds of megabytes of `.venv`
- **Cause**: Running naive recursive copy (`cp -R`) copies the entire local virtual environment.
- **Fix**: Exclude `.venv/` using `tar` (which works uniformly across macOS, Linux, and WSL):
  ```bash
  b="../project-backup-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"
  ```
  The virtual environment can always be recreated instantly with `uv run`.

---

## 4. Coding Assistants & Automated Checks

### Automated link checker reports `403 Forbidden` on official museum/attraction links
- **Cause**: Certain websites (such as the British Museum and Historic Royal Palaces) deploy Cloudflare or bot protection that returns HTTP 403 to automated CLI tools (`curl`, python scripts, agent scrapers).
- **Fix**: These links are valid for human visitors. Verify them in a regular web browser rather than letting an agent flag them as broken.

### Dashboard MathJax console error
- **Status**: **Harmless**.
- **Reason**: Plotly figures attempt to load MathJax from a public CDN when initialized. If offline or if blocked by a content filter, an error appears in the browser developer console, but charts render normally.
