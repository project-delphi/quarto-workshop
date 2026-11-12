# uv-environment.gif: giving the London guide its own Python environment (Chapter 4), run for
# real under the demo account in _demo-env.sh. The packages come from uv's cache. The
# engine check's first render takes about 40 s; the recording cuts that wait (Hide/Show).
# poster: media/build.py puts the finished screen first, as a still for readers that don't animate.
Output ../gifs/uv-environment.gif
Set Shell "bash"
Set FontSize 16
Set Width 800
Set Height 560
Set Padding 16
Set Framerate 12
Set Theme "Builtin Dark"
Set TypingSpeed 35ms
Hide
Type "source _demo-env.sh && rm -rf ~/london-guide && mkdir -p ~/london-guide && cd ~/london-guide && clear" Enter
Sleep 1s
Show
Type "uv init --bare" Sleep 300ms Enter Sleep 1500ms
Type "uv add ipykernel nbclient nbformat pyyaml pandas matplotlib plotly" Sleep 300ms Enter Sleep 6s
Type "clear && ls -a" Sleep 300ms Enter Sleep 1500ms
Type "uv run quarto check jupyter" Sleep 300ms Enter Sleep 2s
Hide
Sleep 45s
Show
Sleep 3s
