"""media/gifs/cluster-cloud-orbit.gif: the clusters on three principal components (Chapter 11,
#sec-cloud-3d): face on, turning, then PC3 upright, which is the poster frame. Run from
book/media/capture after `make book-html`."""
from _scene import record

record("chapters/11-cluster.html", "cluster-cloud-orbit.gif", [
    ("hold", 1.2),
    ("view", "turn", 3.0),
    ("view", "pc3", 3.0),
    ("hold", 0.8),
], index=1)
