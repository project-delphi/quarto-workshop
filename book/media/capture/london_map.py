"""media/gifs/london-map-orbit.gif: the London 3-D map (Chapter 6, #sec-london-3d), from the
HTML edition: the flat map, a tilt that raises the columns, a slow turn, the close view of the
five sights, and back to the tilted overview, turned a little so the last frame (the GIF's
poster) shows all five columns. Run from
book/media/capture after `make book-html`."""
from _scene import record

record("chapters/06-audiences.html", "london-map-orbit.gif", [
    ("hold", 1.0),
    ("view", "tilt", 2.0),
    ("view", "focus", 2.5),
    ("view", "tilt", 1.5),
    ("drag", 120, 0, 2.0),
    ("hold", 0.8),
])
