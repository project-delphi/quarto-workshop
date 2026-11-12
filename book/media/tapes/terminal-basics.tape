# terminal-basics.gif: the Chapter 3 exercise, run for real in bash. A demo account keeps the
# recording free of personal paths: HOME is /tmp/home/ana, so `pwd` prints /tmp/home/ana where
# yours prints /home/<you> (Linux, WSL) or /Users/<you> (Mac).
# poster: media/build.py puts the finished screen first, as a still for readers that don't animate.
Output ../gifs/terminal-basics.gif
Set Shell "bash"
Set FontSize 18
Set Width 800
Set Height 560
Set Padding 18
Set Framerate 12
Set Theme "Builtin Dark"
Set TypingSpeed 65ms
Hide
Type "export HOME=/tmp/home/ana && mkdir -p $HOME && cd ~ && rm -rf demo && export PS1='\[\e[1;32m\]ana@laptop\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]$ ' && clear" Enter
Sleep 500ms
Show
Type "pwd" Sleep 300ms Enter Sleep 900ms
Type "date" Sleep 300ms Enter Sleep 900ms
Type "mkdir demo" Sleep 300ms Enter Sleep 600ms
Type "ls" Sleep 300ms Enter Sleep 900ms
Type "cd demo" Sleep 300ms Enter Sleep 700ms
Type "mkdir notes" Sleep 300ms Enter Sleep 500ms
Type "cd notes" Sleep 300ms Enter Sleep 700ms
Type "pwd" Sleep 300ms Enter Sleep 1000ms
Type "cd .." Sleep 300ms Enter Sleep 700ms
Type "cd ~" Sleep 300ms Enter Sleep 700ms
Type "rmdir demo/notes demo" Sleep 300ms Enter Sleep 2500ms
