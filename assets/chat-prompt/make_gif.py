"""Draw assets/chat-prompt.gif: a free web chat writes a prompt for a coding assistant.

A picture only: nothing here calls a chat service or an assistant. The reply is an
illustration of what such a chat can return; real replies vary. Needs Pillow and
macOS's Menlo font:

    python3 -m venv /tmp/gifenv && /tmp/gifenv/bin/pip install pillow
    /tmp/gifenv/bin/python assets/chat-prompt/make_gif.py
    gifsicle -O3 --colors 32 -b assets/chat-prompt.gif   # optional, shrinks it
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "chat-prompt.gif"
W, H, BAR, NOTE = 960, 540, 34, 62
MENLO = "/System/Library/Fonts/Menlo.ttc"
FONT = ImageFont.truetype(MENLO, 17)
SMALL = ImageFont.truetype(MENLO, 15)
NOTE_FONT = ImageFont.truetype(MENLO, 19)
LINE, PAD = 25, 18
CW = FONT.getlength("M")
COLS = 62  # characters per bubble line

WEB_BG, WEB_BAR, WEB_TEXT = (250, 250, 252), (225, 229, 238), (30, 35, 50)
USER_BG, BOT_BG, BOT_LINE = (214, 228, 255), (255, 255, 255), (200, 205, 220)
PROMPT_BG, PROMPT_LINE, BUTTON = (240, 232, 255), (140, 100, 220), (90, 60, 190)
TERM_BG, TERM_BAR, TERM_TEXT, TERM_MUTED = (22, 24, 30), (42, 47, 55), (235, 235, 240), (150, 160, 175)
GREEN, AMBER = (138, 226, 52), (255, 190, 90)
NOTEBG, NOTEFG = (255, 255, 255), (20, 30, 50)

ASK = ("I am new to coding assistants. I want a one-page London visitor guide. "
       "Write me a prompt for my coding assistant: 1 to 4 lines, one task, "
       "concrete file names, and ask it to check its work.")
INTRO = "Here is a prompt to paste into your coding assistant:"
PROMPT = ('Create london.md with a level-1 heading "Visit London" and one welcome '
          'paragraph. Add a heading "Top sights" with three bullets. Run '
          "`quarto render london.md` and tell me if there were any errors.")
REPLY_OUT = ["wrote london.md", "ran quarto render london.md", "no errors; open london.html"]

frames, durations = [], []


def add(im, ms):
    frames.append(im)
    durations.append(ms)


def wrap(text):
    return textwrap.wrap(text, COLS)


def web(note, typed="", reply=0, copied=False):
    """The web chat. typed: characters of ASK in the input; reply: 0 none, 1 intro, 2 + prompt."""
    im = Image.new("RGB", (W, H), WEB_BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, BAR], fill=WEB_BAR)
    d.text((PAD, 8), "A free web chat (for example Gemini) · in your browser", font=SMALL, fill=WEB_TEXT)
    y = BAR + 14
    sent = typed == "SENT"
    if sent:
        lines = wrap(ASK)
        bw = CW * COLS + 24
        d.rounded_rectangle([W - PAD - bw, y, W - PAD, y + LINE * len(lines) + 14], 12, fill=USER_BG)
        for i, ln in enumerate(lines):
            d.text((W - PAD - bw + 12, y + 7 + i * LINE), ln, font=FONT, fill=WEB_TEXT)
        y += LINE * len(lines) + 28
    if reply >= 1:
        d.text((PAD, y), INTRO, font=FONT, fill=WEB_TEXT)
        y += LINE + 10
    if reply >= 2:
        lines = wrap(PROMPT)
        h = LINE * len(lines) + 20
        d.rounded_rectangle([PAD, y, PAD + CW * COLS + 24, y + h], 12, fill=PROMPT_BG, outline=PROMPT_LINE, width=2)
        for i, ln in enumerate(lines):
            d.text((PAD + 12, y + 10 + i * LINE), ln, font=FONT, fill=WEB_TEXT)
        bx = PAD + CW * COLS + 24 + 16
        label = "✓ Copied" if copied else "Copy"
        d.rounded_rectangle([bx, y, bx + 118, y + 38], 10, fill=BUTTON)
        d.text((bx + 59 - FONT.getlength(label) / 2, y + 9), label, font=FONT, fill=(255, 255, 255))
    # input box
    iy = H - NOTE - 126
    d.rounded_rectangle([PAD, iy, W - PAD, iy + 112], 16, fill=BOT_BG, outline=BOT_LINE, width=2)
    if not sent:
        for i, ln in enumerate(wrap(typed or " ")[:4] if typed else []):
            d.text((PAD + 14, iy + 12 + i * LINE), ln, font=FONT, fill=WEB_TEXT)
        if not typed:
            d.text((PAD + 14, iy + 12), "Ask here…", font=FONT, fill=(150, 155, 170))
        d.ellipse([W - PAD - 46, iy + 66, W - PAD - 12, iy + 100], fill=BUTTON if typed else BOT_LINE)
    else:
        d.text((PAD + 14, iy + 12), "Ask here…", font=FONT, fill=(150, 155, 170))
    d.rectangle([0, H - NOTE, W, H], fill=NOTEBG)
    d.text((PAD, H - NOTE + 20), note, font=NOTE_FONT, fill=NOTEFG)
    return im


def term(note, typed=None, out=0):
    """The coding assistant. typed: characters of PROMPT after the ❯; out: lines of REPLY_OUT shown."""
    im = Image.new("RGB", (W, H), TERM_BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, BAR], fill=TERM_BAR)
    d.text((PAD, 8), "Your coding assistant · in the terminal", font=SMALL, fill=TERM_MUTED)
    y = BAR + 18
    shown = PROMPT if typed is None else PROMPT[:typed]
    lines = textwrap.wrap(shown, 66) or [""]
    for i, ln in enumerate(lines):
        d.text((PAD, y), ("❯ " if i == 0 else "  ") + ln, font=FONT, fill=TERM_TEXT)
        y += LINE
    y += 14
    for ln in REPLY_OUT[:out]:
        d.text((PAD, y), "● " + ln, font=FONT, fill=GREEN)
        y += LINE
    d.rectangle([0, H - NOTE, W, H], fill=NOTEBG)
    d.text((PAD, H - NOTE + 20), note, font=NOTE_FONT, fill=NOTEFG)
    return im


n1 = "1. Open a free web chat. Describe what you want, in plain words."
for i in range(0, len(ASK) + 1, 4):
    add(web(n1, ASK[:i] if i else ""), 1200 if i == 0 else 60)
add(web(n1, ASK), 900)
n2 = "2. It answers with a ready prompt: file names, one task, a check."
add(web(n2, "SENT"), 900)
add(web(n2, "SENT", 1), 1100)
add(web(n2, "SENT", 2), 2600)
n3 = "3. Press Copy. Read the prompt first: is it what you want?"
add(web(n3, "SENT", 2, copied=True), 1800)
n4 = "4. Paste it into your coding assistant (not into the web chat)."
add(term(n4, 0), 900)
for i in range(0, len(PROMPT) + 1, 6):
    add(term(n4, i), 60)
add(term(n4, None), 1000)
n5 = "5. It runs the task. You check the result."
for k in range(1, len(REPLY_OUT) + 1):
    add(term(n5, None, k), 900)
add(term(n5, None, len(REPLY_OUT)), 3200)

frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True)
print(OUT, len(frames), "frames,", sum(durations) / 1000, "s")
