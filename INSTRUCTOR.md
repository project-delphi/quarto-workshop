# Instructor Runbook & Facilitation Guide

A practical guide for instructors, teaching assistants, and facilitators delivering the Quarto workshop.

---

## 1. Workshop Architecture & Schedule

The workshop is designed as a **6-hour hands-on day** (360 minutes: 300 of teaching in four sessions of 65, 65, 85 and 85 minutes, plus two 15-minute breaks and a 30-minute meal):

| Time | Block | Focus | Checkpoint |
|---|---|---|---|
| **0:00** (10m) | Welcome & Objective | What we are building today | — |
| **0:10** (5m) | What Is Quarto? | Pandoc + Jupyter/knitr engine model | — |
| **0:15** (15m) | Setup Check & Boxes | Triage broken pre-work; explain the three boxes | — |
| **0:30** (35m) | Part 1: London in Markdown | First render, project rules (`AGENTS.md`), uv environment | `checkpoints/01-london-markdown` |
| **1:05** (15m) | **☕ Break & Catch-up** | Rest, pair anyone whose first render or environment is broken | — |
| **1:20** (20m) | Part 1: `.md` → `.qmd` | YAML headers, Python cells, multi-format export (docx/pdf) | `checkpoints/02-london-qmd` |
| **1:40** (15m) | Part 1: Three Audiences | Parallel sub-agents writing flyer, email, dashboard (⭐ social ad is self-paced) | `checkpoints/04-london-audiences` |
| **1:55** (20m) | Part 1: Publish to GitHub Pages | First interactive publish to GitHub Pages | `examples/london` |
| **2:15** (10m) | Part 1: Change an Input | No supplied prompt: change a value, rebuild, explain which outputs update | `examples/london` |
| **2:25** (30m) | **🍽️ Meal & Catch-up** | Eat, pair struggling participants, verify live sites | — |
| **2:55** (20m) | Part 2: Why, Rules, Data | The question, the dataset, project rules, environment | `checkpoints/05-water-explore` |
| **3:15** (20m) | Part 2: Explore | Look before modelling | `checkpoints/05-water-explore` |
| **3:35** (20m) | Part 2: Prepare | Select, transform, impute, scale | `checkpoints/06-water-prepare` |
| **3:55** (25m) | Part 2: Cluster | k-means, the 📤 route, the clusters page | `checkpoints/07-water-cluster` |
| **4:20** (15m) | **☕ Break & Catch-up** | Rest, get everyone a working `clusters.html` | — |
| **4:35** (20m) | Part 2: Interpret | Heatmap, names, outcomes by cluster | `checkpoints/08-water-interpret` |
| **4:55** (15m) | Part 2: Correlation ≠ Causation | Within-cluster check, discussion | `checkpoints/09-water-causation` |
| **5:10** (40m) | Part 2: Publish Many | Report, slides, blog + website, publish, change an input (⭐ dashboard is self-paced) | `checkpoints/10`–`13`, `examples/water` |
| **5:50** (10m) | **Wrap-up** | Showcase live websites; next steps | — |
| **6:00** | **Finish** | | — |

Times count from the start of the day, so add your start time: from 9:30, the meal is at 11:55 and the day ends at 15:30. If the venue fixes the meal time, move the start, not the meal: the meal belongs between the two parts, so everyone starts Part 2 together. Exercise times have not grown with the blocks: the extra minutes are for concept slides, showing results and recovery. Announce the clock time each break ends; the breaks and the meal are also the room's catch-up points.

---

## 2. Pre-Workshop Facilitator Checklist

1. **Verify Pre-Work Submissions**:
   - Confirm that attendees ran the setup check (`quarto check`, `uv --version`, `gh auth status`) and the 🧪 test run.
   - For anyone who did not confirm ahead of time, pair them with a neighbor or TA during the 0:15 block.
2. **Windows Attendees**:
   - Ensure Windows users are operating within **WSL2 (Ubuntu)**; the deck has no supported native PowerShell route (the catch-up and backup commands rely on POSIX utilities such as `tar` and `date`, and Windows installers put tools where WSL cannot use them). The WSL install (admin rights, restart, first Ubuntu start) is 🏠 pre-work. Ask for `wsl -l -v` output (VERSION 2) before the day, and pair anyone who cannot install WSL (no admin rights, virtualization off in the BIOS, Store or downloads blocked by a proxy) with a neighbour for the day. Windows participants struggled most with the WSL install and with finding their place in the setup slides (2026-11-05), so the deck now has numbered steps and a step 1 slide for every system that sends Windows participants to a separate page, `windows-setup.qmd`, with one action per step, what to expect after each, and a stuck-table; tell everyone to have a stable, fast connection and to use an AI web chat for errors. Run `windows-setup.qmd` once on a clean Windows machine before teaching: it has only been checked from documentation and a Mac.
3. **Network Readiness**:
   - Confirm venue Wi-Fi permits SSH/HTTPS to GitHub, package downloads via `uv`, and access to GitHub Pages.

---

## 3. Room Management & The "Two-Minute Rule"

The core rule for keeping the entire room synchronized:

> **The Two-Minute Rule**: If a participant is stuck on a command, agent error, or syntax glitch for more than two minutes, **they do not debug on stage or hold back the room**. They immediately copy that exercise's catch-up prompt.

### How Catch-ups Work
Every exercise slide includes a copyable catch-up prompt pointing to its corresponding checkpoint README:
```text
Catch me up: follow ../quarto-workshop/checkpoints/02-london-qmd/README.md
```
The catch-up script:
1. Safely archives existing student work to a timestamped backup directory (excluding `.venv/`).
2. Copies the clean milestone snapshot into the project directory.
3. Renders the output and verifies that key files exist.
4. Identifies the exact slide URL to rejoin the group.

---

## 4. Part 2 Routing: Normal vs. Challenge

From Part 2's *Cluster* block onward, the analysis offers two paths:
- **Normal Route (📤 Default)**: Participants copy `scripts/analysis.py` directly from the checkpoint and focus their time on authoring documents, dashboards, and publications.
- **Challenge Route (⭐ Self-Paced)**: Participants prompt their assistant to write the k-means clustering and PCA logic from scratch.

*Note for facilitators:* Agenda timing assumes the normal 📤 route. Direct participants to stick to the normal route unless they are well ahead of the room.

---

## 5. Publishing Pacing & Common Failure Points

### First Publish Takes ~2 Minutes
During `#london-publish` (in the block starting 1:55) and `#water-ship` (5:34):
- Rendering pre-computations and generating assets takes 40–50 seconds.
- Pushing 12–20 MB of site assets to GitHub Pages takes 20–40 seconds.
- GitHub Pages CDN deployment takes 30–60 seconds.
- *Teaching strategy:* While sites are deploying, do not wait in silence. Project one of the instructor example sites or discuss how GitHub Pages branches operate under the hood.

### Top 3 Real-Time Gotchas and Fixes
1. **Quarto 1.6.40 `--no-prompt` failure on first publish**:
   - Instruct participants to run `uv run quarto publish gh-pages` interactively and press **Enter** at the prompt.
2. **Git push HTTP 400**:
   - Have them run `git config http.postBuffer 524288000` in their terminal.
3. **Live preview file locking**:
   - If an assistant says a file is locked or cannot read `.quarto_ipynb`, have the participant press `Ctrl+C` to stop `quarto preview` before the assistant renders.

---

## 6. Verifying Checkpoints (Contributor / Maintainer)

Before running the workshop with a new cohort or after updating dependencies, verify that the finished reference projects render cleanly:

```bash
# Test Part 1 (London)
cd examples/london
uv run quarto render
test -f _site/index.html && test -f _site/london-whitepaper.pdf && echo "Part 1 OK"

# Test Part 2 (Water Safety)
cd ../water
uv run python scripts/analysis.py
uv run quarto render
test -f _site/index.html && test -f _site/dashboard.html && test -f _site/whitepaper.pdf && echo "Part 2 OK"
```
