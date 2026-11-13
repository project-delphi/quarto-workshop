"""The first page of a PDF as a sharp PNG, for the pictures of the projects' outputs.

macOS Quick Look (qlmanage) draws the page at the size asked for. sips, used before, draws a
PDF page at 72 dpi and then scales the bitmap up, which blurs a 12 cm page shown at 800 px.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


def first_page_png(pdf: Path, out: Path, long_side: int) -> None:
    """Write pdf's first page to out, with its longer side long_side pixels. An out ending in
    .jpg is saved as a JPEG: a page that is mostly photograph is a tenth of the PNG's size."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["qlmanage", "-t", "-s", str(long_side), "-o", tmp, str(pdf)],
                       check=True, capture_output=True)
        png = Path(tmp) / f"{pdf.name}.png"
        if out.suffix == ".jpg":
            from PIL import Image
            Image.open(png).convert("RGB").save(out, quality=88, optimize=True, progressive=True)
        else:
            shutil.move(png, out)
