"""
Generates the favicon set by reusing the EXACT SAME logo composition
already used for the social media profile pictures — profile_picture_html()
in generate_brand_assets.py (the p5_mark() full logo, centered, filling 62%
of the canvas, on solid #1A1633 background). No new bar proportions, no
separate rendering logic — this script only calls that existing function at
different output sizes and saves the results as the favicon files.

Outputs (all under /favicon/):
  favicon-16x16.png
  favicon-32x32.png
  favicon-48x48.png
  apple-touch-icon-180x180.png
  favicon.ico            (16x16 + 32x32 combined)

Run:  .venv-assets\\Scripts\\python.exe generate_favicon.py
"""

import os

from playwright.sync_api import sync_playwright
from PIL import Image

from generate_brand_assets import profile_picture_html, capture, SCALE

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "favicon")
os.makedirs(OUT_DIR, exist_ok=True)

SIZES = [16, 32, 48, 180]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(device_scale_factor=SCALE)
        page = context.new_page()

        for size in SIZES:
            name = (
                "apple-touch-icon-180x180.png"
                if size == 180
                else f"favicon-{size}x{size}.png"
            )
            out_path = os.path.join(OUT_DIR, name)
            html = profile_picture_html(size)  # exact same function used for the profile pictures
            capture(page, html, size, size, out_path)
            print(f"done: {name}")

        browser.close()

    icon_16 = Image.open(os.path.join(OUT_DIR, "favicon-16x16.png"))
    icon_32 = Image.open(os.path.join(OUT_DIR, "favicon-32x32.png"))
    icon_32.save(
        os.path.join(OUT_DIR, "favicon.ico"),
        format="ICO",
        sizes=[(16, 16), (32, 32)],
        append_images=[icon_16],
    )

    print("\n--- Verification ---")
    for name in sorted(os.listdir(OUT_DIR)):
        path = os.path.join(OUT_DIR, name)
        size_kb = os.path.getsize(path) / 1024
        with Image.open(path) as im:
            dims = im.size
        print(f"{name}  {dims}  {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
