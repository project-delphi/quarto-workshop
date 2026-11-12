"""media/gifs/colombia-relief-orbit.gif: urban zones as columns at their head towns' altitude
(Chapter 11, #sec-relief): the map, a tilt, and the flight into the highlands, whose last frame is the poster. Run from
book/media/capture after `make book-html`."""
from _scene import record

record("chapters/11-cluster.html", "colombia-relief-orbit.gif", [
    ("hold", 1.0),
    ("view", "tilt", 2.5),
    ("view", "focus", 4.5),
], index=2)
