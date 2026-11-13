# render-many-formats.gif: one render of checkpoint 02's london.qmd writes six files (Chapter 5),
# run for real under the demo account in _demo-env.sh. The middle of the render is cut
# (Hide/Show); the listing at the end is the real result.
# poster: media/build.py puts the finished screen first, as a still for readers that don't animate.
# The frame is tall enough to keep the format block, the render and the listing on one screen.
Output ../gifs/render-many-formats.gif
Set Shell "bash"
Set FontSize 16
Set Width 800
Set Height 760
Set Padding 16
Set Framerate 12
Set Theme "Builtin Dark"
Set TypingSpeed 35ms
Hide
Type "REPO=$(cd ../../.. && pwd) && source _demo-env.sh && rm -rf ~/london-guide && mkdir -p ~/london-guide && cd ~/london-guide && cp -R $REPO/checkpoints/02-london-qmd/. . && uv sync -q && clear" Enter
Sleep 8s
Show
Type "grep -A12 '^format:' london.qmd" Sleep 300ms Enter Sleep 3s
Type "uv run quarto render london.qmd 2>&1 | grep -E 'Output created|^\[' " Sleep 300ms Enter Sleep 4s
Hide
Sleep 150s
Show
Sleep 1500ms
Type "ls -1 london.* london-slides.html" Sleep 300ms Enter Sleep 4s
