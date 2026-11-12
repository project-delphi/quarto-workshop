"""A scripted replay of a typical coding-assistant session, for agent-session.tape.

This is an illustration, not a recording: no assistant runs and nothing calls a model
(AGENTS.md rules out paid assistant sessions for teaching material). The exchange follows
the book's first prompt (Chapter 2, "How to read the assistant boxes"): the assistant
writes london.md, asks before running a command, renders, and reports. The screen starts
on the finished session for two seconds, so the GIF's first frame is a usable still, then
replays it.
"""
import sys
import textwrap
import time

DIM, BOLD, RESET = "\033[2m", "\033[1m", "\033[0m"
VIOLET, AMBER, GREEN, CYAN = "\033[38;5;141m", "\033[38;5;179m", "\033[38;5;79m", "\033[38;5;117m"
PROMPT = 'Create london.md with a level-1 heading "Visit London" and one welcome paragraph.'

SCRIPT = [
    ("banner", f"{DIM} Illustration: a scripted replay of a typical session{RESET}"),
    ("line", f"{DIM} ─────────────────────────────────────────────────────────{RESET}"),
    ("prompt", PROMPT),
    ("pause", 0.8),
    ("line", ""),
    ("say", "I'll create london.md with the heading and a short welcome."),
    ("line", ""),
    ("line", f"  {AMBER}Write{RESET} london.md"),
    ("slow", f"  {DIM}│{RESET} # Visit London"),
    ("slow", f"  {DIM}│{RESET}"),
    ("slow", f"  {DIM}│{RESET} Welcome to **London**: free museums, royal history"),
    ("slow", f"  {DIM}│{RESET} and *riverside walks*."),
    ("line", ""),
    ("say", "Now I'll render it to check the output."),
    ("line", ""),
    ("line", f"  {AMBER}Run{RESET} quarto render london.md"),
    ("line", f"  {BOLD}Allow this command?{RESET}  {GREEN}❯ Yes{RESET}   No"),
    ("pause", 1.6),
    ("line", f"  {GREEN}✓{RESET} Output created: london.html"),
    ("line", ""),
    ("say", "Done: london.md has the heading and one welcome paragraph,"),
    ("cont", "and quarto render wrote london.html with no errors."),
    ("line", ""),
    ("end", f"{VIOLET}❯{RESET} "),
]


def emit(kind, value, animate):
    out = sys.stdout
    if kind == "pause":
        if animate:
            time.sleep(value)
        return
    if kind == "prompt":
        out.write(f"{VIOLET}❯{RESET} ")
        for i, line in enumerate(textwrap.wrap(value, 66)):
            if i:
                out.write("\n  ")
            for ch in line:
                out.write(ch)
                out.flush()
                if animate:
                    time.sleep(0.025)
        out.write("\n")
    elif kind == "say":
        out.write(f"{CYAN}●{RESET} {value}\n")
        if animate:
            time.sleep(0.9)
    elif kind == "cont":
        out.write(f"  {value}\n")
        if animate:
            time.sleep(0.5)
    elif kind == "slow":
        out.write(value + "\n")
        if animate:
            time.sleep(0.25)
    elif kind == "end":
        out.write(value)
    else:
        out.write(value + "\n")
        if animate:
            time.sleep(0.15)
    out.flush()


def run(animate):
    for kind, value in SCRIPT:
        emit(kind, value, animate)


if __name__ == "__main__":
    sys.stdout.write("\033[2J\033[H")
    run(animate=False)          # the poster frame: the finished session
    sys.stdout.flush()
    time.sleep(2.0)
    sys.stdout.write("\033[2J\033[H")
    run(animate=True)
    time.sleep(3.5)
