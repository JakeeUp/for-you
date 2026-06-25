#!/usr/bin/env python3
"""
Remove the background from the three Robin images and save clean,
auto-cropped transparent PNGs for the date site.

SETUP
  1) Save the three original screenshots into the  images/  folder as:
        images/love.png     -> heart-eyes Robin   (in love)
        images/neutral.png  -> straight-face Robin (unimpressed)
        images/cry.png      -> crying Robin        (waterworks)
     Any image extension works (.png .jpg .jpeg .webp).
  2) Install deps once:
        pip install "rembg[cpu]" pillow
  3) Run:
        python make-transparent.py

OUTPUT
  images/robin-love.png, images/robin-neutral.png, images/robin-cry.png
  (these are the files index.html already points at)
"""
import glob
import sys
from pathlib import Path

try:
    from rembg import remove, new_session
    from PIL import Image
except ImportError:
    sys.exit('Missing deps. Run:  pip install "rembg[cpu]" pillow')

HERE = Path(__file__).resolve().parent
IMG = HERE / "images"
IMG.mkdir(exist_ok=True)

# isnet-anime is trained on anime/cartoon art -> ideal for Teen Titans Go.
session = new_session("isnet-anime")

JOBS = {
    "love":    "robin-love.png",
    "neutral": "robin-neutral.png",
    "cry":     "robin-cry.png",
}


def find_source(key: str):
    """Find images/<key>.* (but never an already-generated robin-*.png)."""
    hits = sorted(p for p in glob.glob(str(IMG / f"{key}.*"))
                  if not Path(p).name.startswith("robin-"))
    return hits[0] if hits else None


def autocrop(img: Image.Image, pad: int = 14) -> Image.Image:
    """Trim transparent margins so every face is framed consistently."""
    bbox = img.getbbox()
    if not bbox:
        return img
    l, t, r, b = bbox
    return img.crop((max(0, l - pad), max(0, t - pad),
                     min(img.width, r + pad), min(img.height, b + pad)))


def main():
    any_done = False
    for key, out_name in JOBS.items():
        src = find_source(key)
        if not src:
            print(f"  [skip ] images/{key}.* not found")
            continue
        print(f"  [clean] {Path(src).name}  ->  images/{out_name}")
        img = Image.open(src).convert("RGBA")
        cut = remove(
            img,
            session=session,
            alpha_matting=True,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=15,
            alpha_matting_erode_size=8,
        )
        autocrop(cut).save(IMG / out_name)
        any_done = True

    if any_done:
        print("\nDone! Transparent PNGs saved in images/. Refresh the page.")
    else:
        print("\nNothing processed. Put love/neutral/cry images in the images/ folder.")


if __name__ == "__main__":
    main()
