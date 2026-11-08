"""Draw assets/windows-session.gif: one PowerShell window, start to finish.

A picture only: nothing here runs a command. The session shows the steps of
windows-setup.qmd in one window, ending with `wsl` starting Ubuntu and `whoami`
printing the username. Needs Pillow and macOS's Menlo font:

    python3 -m venv /tmp/gifenv && /tmp/gifenv/bin/pip install pillow
    /tmp/gifenv/bin/python assets/windows-session/make_gif.py
    gifsicle -O3 --colors 32 -b assets/windows-session.gif   # optional, shrinks it
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "windows-session.gif"
W, H, BAR, NOTE = 960, 470, 34, 64
FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
SMALL = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 15)
NOTE_FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 19)
LINE, PAD = 29, 16
BG, BARBG, TEXT = (1, 36, 86), (42, 47, 55), (238, 237, 240)
YELLOW, GREEN, MUTED = (255, 255, 102), (138, 226, 52), (150, 160, 175)
NOTEBG, NOTEFG = (255, 255, 255), (20, 30, 50)

PS = "PS C:\\Users\\ana>"
UB = "ana@LAPTOP:~$"

# Each step: prompt, command, output lines, and the note shown while it runs.
STEPS = [
    (PS, "wsl --install -d Ubuntu --no-launch",
     ["Ubuntu has been installed."],
     "1. Install Ubuntu. (On the real page you restart the computer after this.)"),
    (PS, "wsl -l -v",
     ["  NAME      STATE           VERSION", "* Ubuntu    Running         2"],
     "2. Check it: Ubuntu with a 2 in the VERSION column is good."),
    (PS, "wsl",
     [],
     "3. Type wsl: PowerShell starts Ubuntu in this same window."),
    (UB, "whoami",
     ["ana"],
     "4. The prompt now ends in $ . You are inside Ubuntu. whoami prints your name."),
    (UB, "exit",
     [],
     "5. exit takes you back to PowerShell, whose prompt ends in > ."),
]

frames, durations = [], []


def draw(lines, note, cursor_at=None):
    """lines: list of rows, each a list of (text, colour) runs. Cursor after the last run of cursor_at."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, BAR], fill=BARBG)
    d.text((PAD, 8), "Windows PowerShell", font=SMALL, fill=MUTED)
    d.text((W - 110, 8), "\u2500   \u25a2   \u2715", font=SMALL, fill=MUTED)
    cw = d.textlength("M", font=FONT)
    y = BAR + 14
    for i, row in enumerate(lines):
        x = PAD
        for text, colour in row:
            d.text((x, y), text, font=FONT, fill=colour)
            x += cw * len(text)
        if i == cursor_at:
            d.rectangle([x, y + 3, x + cw - 1, y + LINE - 5], fill=TEXT)
        y += LINE
    d.rectangle([0, H - NOTE, W, H], fill=NOTEBG)
    d.text((PAD, H - NOTE + 20), note, font=NOTE_FONT, fill=NOTEFG)
    return im


def add(im, ms):
    frames.append(im)
    durations.append(ms)


lines = []
note = "One window, five steps. Watch it once."
add(draw([[(PS + " ", TEXT)]], note, 0), 1800)
lines = []
for n, (prompt, cmd, out, step_note) in enumerate(STEPS):
    pcolour = GREEN if prompt == UB else TEXT
    ccolour = TEXT if prompt == UB else YELLOW
    base = list(lines)
    for i in range(len(cmd) + 1):
        row = [(prompt + " ", pcolour), (cmd[:i], ccolour)]
        add(draw(base + [row], step_note, len(base)), 70 if i else 700)
    add(draw(base + [row], step_note), 450)  # Enter pressed, cursor gone
    lines = base + [row]
    for text in out:
        lines = lines + [[(text, TEXT)]]
        add(draw(lines, step_note), 450)
    nxt = STEPS[n + 1][0] if n + 1 < len(STEPS) else PS
    ncolour = GREEN if nxt == UB else TEXT
    # Pause, then show the next prompt with a cursor (for `wsl` the prompt changes to Ubuntu's).
    add(draw(lines + [[(nxt + " ", ncolour)]], step_note, len(lines)), 1700 if n < len(STEPS) - 1 else 3500)

# The window never scrolls: check every row fits.
max_rows = (H - BAR - NOTE - 28) // LINE
assert len(lines) + 1 <= max_rows, (len(lines), max_rows)

frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True)
print(OUT, len(frames), "frames,", sum(durations) / 1000, "s")
