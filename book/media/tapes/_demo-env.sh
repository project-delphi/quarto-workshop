# Sourced (hidden) by the tapes: a demo account, so recordings show no personal paths.
# uv keeps using the real cache and Python installs, so nothing is downloaded again.
export UV_CACHE_DIR="$(uv cache dir)" UV_PYTHON_INSTALL_DIR="$(uv python dir)"
export HOME=/tmp/home/ana
mkdir -p "$HOME"
export PS1='\[\e[1;32m\]ana@laptop\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]$ '
