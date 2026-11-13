"""media/gifs/kmeans-steps.gif: the k-means toy (Chapter 11, #sec-kmeans-steps) playing its steps
from the first random start, then fixed on the last step, the stable grouping, which is the
poster frame. Run from book/media/capture after `make book-html`."""
from _scene import record

LAST = ".deck-3d[data-scene='kmeans'] .t-picker button[data-state]:last-of-type"
# The scene's step and start buttons would mean nothing in the GIF: the frames leave them out.
record("chapters/11-cluster.html", "kmeans-steps.gif", [("hold", 8.5), ("click", LAST, 1.8)], index=0,
       hide=".t-picker, .c-picker")
