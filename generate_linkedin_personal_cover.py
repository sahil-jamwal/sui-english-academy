"""
Generates the LinkedIn PERSONAL PROFILE cover photo for Tanya Pal.

This is a separate, standalone script — it does NOT import-and-run or modify
generate_brand_assets.py's main(), so the existing LinkedIn Company Page
banner (exports/sui/covers-banners/linkedin-banner-1128x191.png) is never
touched or regenerated. It only reuses that script's brand constants and
HTML-building helpers (colors, the exact P5 logo SVG, gradient/vignette/arc
helpers, and the Playwright capture() routine) so this new asset matches the
same visual system as our other banners.

Output: exports/sui/covers-banners/linkedin-personal-cover-1584x396.png
For manual download + upload to LinkedIn only — not referenced by the site.

Run:  .venv-assets\\Scripts\\python.exe generate_linkedin_personal_cover.py
"""

import os

from playwright.sync_api import sync_playwright
from PIL import Image

from generate_brand_assets import (
    GOLD,
    WHITE,
    LAVENDER,
    BANNER_DIR,
    SCALE,
    page_shell,
    p5_mark,
    linear_lr_bg,
    vignette_div,
    diagonal_sweep_arc,
    capture,
)

W, H = 1584, 396
OUT_PATH = os.path.join(BANNER_DIR, "linkedin-personal-cover-1584x396.png")

# LinkedIn's circular profile photo overlaps the bottom ~60% of the left
# 320px of this banner — keep all content clear of that 320x240 box, with
# extra breathing room. Content is pushed right and pinned to the upper-
# middle of the canvas rather than vertically centered across full height.
SAFE_ZONE_W = 320
SAFE_ZONE_H = 240
CONTENT_LEFT = 380
CONTENT_TOP = 64


def amber_glow_bottom_right(w, h, opacity=0.24):
    """Soft amber glow rising from the bottom-right — kept clear of the
    bottom-left avatar safe zone so it's never hidden under the overlay."""
    size = h * 1.7
    left = w - size * 0.55
    bottom = -size * 0.4
    return (
        f'<div style="position:absolute;left:{left:.0f}px;bottom:{bottom:.0f}px;'
        f'width:{size:.0f}px;height:{size:.0f}px;border-radius:50%;'
        f'background:radial-gradient(circle, rgba(245,166,35,{opacity}), '
        f'rgba(245,166,35,0) 70%);"></div>'
    )


def build_html():
    mark = p5_mark(30)
    body = f"""
    <div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;">
      {linear_lr_bg()}
      {amber_glow_bottom_right(W, H)}
      {diagonal_sweep_arc(W, H, opacity=0.10, stroke_w=6)}
      {vignette_div(0.30)}
      <div style="position:absolute;top:26px;right:30px;opacity:.85;">{mark}</div>
      <div style="position:absolute;left:{CONTENT_LEFT}px;top:{CONTENT_TOP}px;width:{W - CONTENT_LEFT - 60}px;
                  display:flex;flex-direction:column;">
        <div style="font-family:'Sora',sans-serif;font-weight:800;font-size:54px;
                    line-height:1.1;letter-spacing:-.01em;color:{WHITE};">Tanya Pal</div>
        <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:20px;
                    letter-spacing:.02em;color:{GOLD};margin-top:10px;">Founder &amp; Lead Trainer, SUI English Academy</div>
        <div style="width:220px;height:2px;background:{GOLD};margin:20px 0;"></div>
        <div style="font-family:'Sora',sans-serif;font-weight:400;font-style:italic;
                    font-size:16px;letter-spacing:.01em;color:{LAVENDER};">Helping India speak English with confidence</div>
      </div>
    </div>"""
    return page_shell(body, W, H)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(device_scale_factor=SCALE)
        page = context.new_page()
        html = build_html()
        capture(page, html, W, H, OUT_PATH)
        browser.close()

    size_kb = os.path.getsize(OUT_PATH) / 1024
    with Image.open(OUT_PATH) as im:
        dims = im.size
    print(f"Saved: {OUT_PATH}")
    print(f"Dimensions: {dims[0]}x{dims[1]}")
    print(f"File size: {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
