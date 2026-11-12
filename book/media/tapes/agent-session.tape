# agent-session.gif: a scripted replay of a typical coding-assistant session (an
# illustration, not a recording: agent_replay.py prints it; no assistant or model runs).
# Re-record from book/ with: uv run --with playwright --with segno python media/build.py tapes
Output ../gifs/agent-session.gif
Set Shell "bash"
Set FontSize 17
Set Width 800
Set Height 560
Set Padding 18
Set Framerate 12
Set Theme "Builtin Dark"
Set TypingSpeed 0ms
Hide
Type "clear && python3 agent_replay.py" Enter
Sleep 300ms
Show
Sleep 21s
