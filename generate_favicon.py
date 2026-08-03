"""
Generates the favicon set by simply RESIZING the existing WhatsApp profile
picture (exports/sui/profile-pictures/whatsapp-profile-640x640.png) down to
each favicon size. It's the highest-resolution profile picture on hand and
has the cleanest, most complete render of the logo (bars + dotted arc +
plane all clearly visible) — nothing is recomposed or re-rendered here,
only resized (LANCZOS, proportional, no cropping).

Outputs (all under /favicon/):
  favicon-16x16.png
  favicon-32x32.png
  favicon-48x48.png
  apple-touch-icon-180x180.png
  favicon.ico            (16x16 + 32x32 combined)

Run:  .venv-assets\\Scripts\\python.exe generate_favicon.py
"""

import os

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(
    ROOT, "exports", "sui", "profile-pictures", "whatsapp-profile-640x640.png"
)
OUT_DIR = os.path.join(ROOT, "favicon")
os.makedirs(OUT_DIR, exist_ok=True)

SIZES = [16, 32, 48, 180]


def main():
    src = Image.open(SOURCE).convert("RGBA")

    resized = {}
    for size in SIZES:
        name = (
            "apple-touch-icon-180x180.png"
            if size == 180
            else f"favicon-{size}x{size}.png"
        )
        im = src.resize((size, size), Image.LANCZOS)
        im.save(os.path.join(OUT_DIR, name), format="PNG")
        resized[size] = im
        print(f"done: {name}")

    resized[32].save(
        os.path.join(OUT_DIR, "favicon.ico"),
        format="ICO",
        sizes=[(16, 16), (32, 32)],
        append_images=[resized[16]],
    )
    print("done: favicon.ico")

    print("\n--- Verification ---")
    for name in sorted(os.listdir(OUT_DIR)):
        path = os.path.join(OUT_DIR, name)
        size_kb = os.path.getsize(path) / 1024
        with Image.open(path) as im:
            dims = im.size
        print(f"{name}  {dims}  {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
