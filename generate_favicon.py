"""
Generates the favicon set from the highest-res master logo icon
(exports/sui/logo/sui-p5-icon-2160.png), with its solid #1A1633 background
removed so the favicon has a transparent background instead of a navy tile.

Background removal uses the "color to alpha" technique (same idea as
GIMP's Color to Alpha): since the source background is a perfectly flat,
known color, per-pixel alpha is recovered from how far each pixel is from
that background color, then the background tint is un-blended out of
anti-aliased edge pixels. This avoids leaving a dark halo ring around the
bars/rim/arc where anti-aliasing used to blend into the navy.

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
SOURCE = os.path.join(ROOT, "exports", "sui", "logo", "sui-p5-icon-2160.png")
OUT_DIR = os.path.join(ROOT, "favicon")
os.makedirs(OUT_DIR, exist_ok=True)

SIZES = [16, 32, 48, 180]
BG = (26, 22, 51)  # #1A1633


def color_to_alpha(im, bg):
    r0, g0, b0 = bg

    def lut_up(bc):
        return [min(255, round((p - bc) * 255 / (255 - bc))) if p >= bc else 0 for p in range(256)]

    def lut_down(bc):
        return [min(255, round((bc - p) * 255 / bc)) if p < bc else 0 for p in range(256)]

    lut_r = lut_up(r0) if r0 < 255 else [0] * 256
    lut_g = lut_up(g0) if g0 < 255 else [0] * 256
    lut_b = lut_up(b0) if b0 < 255 else [0] * 256
    lut_r_dn = lut_down(r0) if r0 > 0 else [0] * 256
    lut_g_dn = lut_down(g0) if g0 > 0 else [0] * 256
    lut_b_dn = lut_down(b0) if b0 > 0 else [0] * 256

    px = im.load()
    w, h = im.size
    out = Image.new("RGBA", (w, h))
    outpx = out.load()

    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            ar = lut_r[r] if r >= r0 else lut_r_dn[r]
            ag = lut_g[g] if g >= g0 else lut_g_dn[g]
            ab = lut_b[b] if b >= b0 else lut_b_dn[b]
            alpha = max(ar, ag, ab)
            if alpha == 0:
                outpx[x, y] = (0, 0, 0, 0)
            else:
                af = alpha / 255.0
                nr = min(255, max(0, round(r0 + (r - r0) / af)))
                ng = min(255, max(0, round(g0 + (g - g0) / af)))
                nb = min(255, max(0, round(b0 + (b - b0) / af)))
                outpx[x, y] = (nr, ng, nb, round(alpha * (a / 255.0)))
    return out


def main():
    src = Image.open(SOURCE).convert("RGBA")
    transparent = color_to_alpha(src, BG)

    resized = {}
    for size in SIZES:
        name = (
            "apple-touch-icon-180x180.png"
            if size == 180
            else f"favicon-{size}x{size}.png"
        )
        im = transparent.resize((size, size), Image.LANCZOS)
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
            mode = im.mode
        print(f"{name}  {dims}  {mode}  {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
