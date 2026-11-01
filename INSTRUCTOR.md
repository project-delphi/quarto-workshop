# Instructor Runbook & Facilitation Guide

A practical guide for instructors, teaching assistants, and facilitators delivering the Quarto workshop.

---

## 1. Workshop Architecture & Schedule

The workshop is designed as a **3 h 20 min hands-on session** (200 minutes total, including a 10-minute break):

| Time | Block | Focus | Checkpoint |
|---|---|---|---|
| **0:00** (5m) | Welcome & Objective | What we are building today | — |
| **0:05** (5m) | What is Quarto? | Pandoc + Jupyter/knitr engine model | — |
| **0:10** (5m) | Setup Check & Boxes | Triage broken pre-work; explain the three boxes | — |
| **0:15** (20m) | Part 1: London in Markdown | First render, project rules (`AGENTS.md`), uv environment | `checkpoints/01-london-markdown` |
| **0:35** (10m) | Part 1: `.md` → `.qmd` | YAML headers, Python cells, multi-format export (docx/pdf) | `checkpoints/02-london-qmd` |
| **0:45** (9m) | Part 1: Three Audiences | Parallel sub-agents writing flyer, email, dashboard (⭐ social ad is self-paced) | `checkpoints/04-london-audiences` |
| **0:54** (11m) | Part 1: Publish to GitHub Pages | First interactive publish to GitHub Pages | `examples/london` |
| **1:05** (5m) | Part 1: Change an Input | No supplied prompt: change a value, rebuild, explain which outputs update | `examples/london` |
| **1:10** (10m) | **Break & Catch-up** | Rest, pair struggling participants, verify live sites | — |
| **1:20** (120m) | Part 2: Colombia Water Safety | Explore, prepare, cluster, report, multi-site publish, change an input (⭐ dashboard is self-paced) | `checkpoints/05`–`13`, `examples/water` |
| **3:20** | **Wrap-up** | Showcase live websites; next steps | — |

---

## 2. Pre-Workshop Facilitator Checklist

1. **Verify Pre-Work Submissions**:
   - Confirm that attendees ran the setup check (`quarto check`, `uv --version`, `gh auth status`) and the 🧪 test run.
   - For anyone who did not confirm ahead of time, pair them with a neighbor or TA during the 0:10 block.
2. **Windows Attendees**:
   - Ensure Windows users are operating within **WSL2 (Ubuntu)**. Native PowerShell works with `uv` and `quarto`, but shell catch-up scripts and backup commands rely on POSIX utilities (`tar`, `date`).
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
During `#london-publish` (0:54) and `#water-ship` (3:07):
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
