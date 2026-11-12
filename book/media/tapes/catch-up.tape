# catch-up.gif: the checkpoint 01 catch-up steps, typed by hand (Chapter 4), run for real under
# the demo account in _demo-env.sh. ~/quarto-workshop links to this repository, read-only use.
# poster: media/build.py puts the finished screen first, as a still for readers that don't animate.
Output ../gifs/catch-up.gif
Set Shell "bash"
Set FontSize 15
Set Width 800
Set Height 560
Set Padding 16
Set Framerate 12
Set Theme "Builtin Dark"
Set TypingSpeed 18ms
Set PlaybackSpeed 1.5
Hide
Type "REPO=$(cd ../../.. && pwd) && source _demo-env.sh && rm -rf ~/london-guide* ~/quarto-workshop && ln -s $REPO ~/quarto-workshop && mkdir -p ~/london-guide && printf '# Visit Londn\n' > ~/london-guide/london.md && cd ~/london-guide && clear" Enter
Sleep 1s
Show
Type "ls" Sleep 300ms Enter Sleep 1000ms
Type `b="../london-guide-backup-01-$(date +%Y%m%d-%H%M%S)" && mkdir "$b" && tar -cf - --exclude=.venv . | tar -xf - -C "$b"` Sleep 300ms Enter Sleep 1000ms
Type "cp -R ../quarto-workshop/checkpoints/01-london-markdown/. ." Sleep 300ms Enter Sleep 800ms
Type "uv run quarto render london.md" Sleep 300ms Enter Sleep 9s
Type "ls && ls -d ../london-guide*" Sleep 300ms Enter Sleep 3s
