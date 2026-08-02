"""
Generates SUI English Academy social media profile pictures and banners
directly to disk using Playwright (headless Chromium) + Pillow.

Run:  .venv-assets\\Scripts\\python.exe generate_brand_assets.py
"""

import os
import random

from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(ROOT, "exports", "sui", "profile-pictures")
BANNER_DIR = os.path.join(ROOT, "exports", "sui", "covers-banners")
os.makedirs(PROFILE_DIR, exist_ok=True)
os.makedirs(BANNER_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# BRAND CONSTANTS
# ---------------------------------------------------------------------------
BG1 = "#1A1633"
BG2 = "#2a2450"
GOLD = "#F5A623"
GOLD_LIGHT = "#FFCE6B"
PALE_GOLD = "#FFE3A3"
LAVENDER = "#D7D2E6"
WHITE = "#FFFFFF"
INK = "#211C3D"

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800" '
    'rel="stylesheet">'
)

# ---------------------------------------------------------------------------
# EXACT P5 logo SVG — copied verbatim from index.html (nav section, lines 28-54).
# Do not redraw or alter any path/gradient/structure here. Only the outer
# width/height attributes are substituted (pure scaling) by p5_mark() below.
# ---------------------------------------------------------------------------
RAW_P5_SVG = """<svg class="plane-anim" width="42" height="52" viewBox="0 0 64 80" xmlns="http://www.w3.org/2000/svg" aria-label="SUI">
        <defs>
          <linearGradient id="lg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#7A3B0A"/><stop offset=".4" stop-color="#DE7A12"/><stop offset=".72" stop-color="#FFB020"/><stop offset="1" stop-color="#FFE18A"/></linearGradient>
          <mask id="trailMaskH" maskUnits="userSpaceOnUse" x="0" y="0" width="64" height="80">
            <rect x="0" y="0" width="64" height="80" fill="#000"/>
            <path d="M8,46 Q30,2 54,14" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1">
              <animate class="trailReveal" attributeName="stroke-dashoffset" from="1" to="0" dur="1.5s" begin="indefinite" fill="freeze"/>
            </path>
          </mask>
        </defs>
        <g class="bars">
          <rect class="bar" x="2" y="74" width="11" height="0" rx="5.5" fill="url(#lg)"><animate attributeName="height" from="0" to="22" dur=".5s" begin="indefinite" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22,1,.36,1" values="0;22"/><animate attributeName="y" from="74" to="52" dur=".5s" begin="indefinite" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22,1,.36,1" values="74;52"/></rect>
          <rect class="bar" x="18" y="74" width="11" height="0" rx="5.5" fill="url(#lg)"><animate attributeName="height" from="0" to="32" dur=".5s" begin="indefinite" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22,1,.36,1" values="0;32"/><animate attributeName="y" from="74" to="42" dur=".5s" begin="indefinite" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22,1,.36,1" values="74;42"/></rect>
          <rect class="bar" x="34" y="74" width="11" height="0" rx="5.5" fill="url(#lg)"><animate attributeName="height" from="0" to="44" dur=".5s" begin="indefinite" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22,1,.36,1" values="0;44"/><animate attributeName="y" from="74" to="30" dur=".5s" begin="indefinite" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22,1,.36,1" values="74;30"/></rect>
          <rect class="bar" x="50" y="74" width="11" height="0" rx="5.5" fill="url(#lg)"><animate attributeName="height" from="0" to="54" dur=".5s" begin="indefinite" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22,1,.36,1" values="0;54"/><animate attributeName="y" from="74" to="20" dur=".5s" begin="indefinite" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".22,1,.36,1" values="74;20"/></rect>
        </g>
        <g class="bars-rim">
          <rect class="rim" x="2" y="52" width="11" height="22" rx="5.5" fill="none" stroke="#FFF6DE" stroke-width="1.1" opacity="0"><animate class="rimReveal" attributeName="opacity" from="0" to=".9" dur=".35s" begin="indefinite" fill="freeze"/></rect>
          <rect class="rim" x="18" y="42" width="11" height="32" rx="5.5" fill="none" stroke="#FFF6DE" stroke-width="1.1" opacity="0"><animate class="rimReveal" attributeName="opacity" from="0" to=".9" dur=".35s" begin="indefinite" fill="freeze"/></rect>
          <rect class="rim" x="34" y="30" width="11" height="44" rx="5.5" fill="none" stroke="#FFF6DE" stroke-width="1.1" opacity="0"><animate class="rimReveal" attributeName="opacity" from="0" to=".9" dur=".35s" begin="indefinite" fill="freeze"/></rect>
          <rect class="rim" x="50" y="20" width="11" height="54" rx="5.5" fill="none" stroke="#FFF6DE" stroke-width="1.1" opacity="0"><animate class="rimReveal" attributeName="opacity" from="0" to=".9" dur=".35s" begin="indefinite" fill="freeze"/></rect>
        </g>
        <path class="trail" d="M8,46 Q30,2 54,14" fill="none" stroke-width="2" stroke-linecap="round" stroke-dasharray="1.6 4.2" mask="url(#trailMaskH)"/>
        <g class="plane"><path d="M-6,-3.5 L7,0 L-6,3.5 L-3,0 Z"/>
          <animateMotion class="planeMotion" path="M8,46 Q30,2 54,14" dur="1.5s" begin="indefinite" fill="freeze" rotate="auto" repeatCount="1"/>
        </g>
      </svg>"""

# CSS the live site applies to this exact SVG when placed on a dark background
# (see .on-dark rules in css/style.css) — required for the trail/plane to show
# their intended gold color; the SVG itself has no inline fill/stroke for them.
P5_ON_DARK_CSS = (
    ".plane-anim .plane path{fill:#F0C864}"
    ".plane-anim .trail{stroke:#F0C864;stroke-opacity:.95}"
)


def p5_mark(height_px):
    """Exact P5 SVG, scaled only via outer width/height (viewBox untouched)."""
    width_px = height_px * 64 / 80
    if width_px == int(width_px):
        width_px = int(width_px)
    svg = RAW_P5_SVG.replace('width="42"', f'width="{width_px}"', 1)
    svg = svg.replace('height="52"', f'height="{height_px}"', 1)
    return svg


def trigger_and_freeze(page):
    """Fire the SVG's own SMIL animations so they settle into their frozen
    end state (bars raised, rim visible, trail drawn, plane at path end) —
    same mechanism js/main.js uses for prefers-reduced-motion, just applied
    to every instance on the page."""
    page.evaluate(
        """() => {
            document.querySelectorAll('svg.plane-anim animate, svg.plane-anim animateMotion')
                .forEach(el => { try { el.beginElement(); } catch (e) {} });
        }"""
    )
    page.wait_for_timeout(1800)


def page_shell(body, width, height):
    return f"""<!doctype html>
<html><head><meta charset="utf-8">
{FONT_LINK}
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:{width}px;height:{height}px;overflow:hidden;background:{BG1}}}
  body{{font-family:'Sora',sans-serif}}
  {P5_ON_DARK_CSS}
</style>
</head>
<body>
{body}
</body></html>"""


# ---------------------------------------------------------------------------
# PART 1 — PROFILE PICTURES
# Solid #1A1633 bg, P5 mark centered filling 62% of canvas (its taller
# dimension), logo only, safely clear of any circular-crop edge.
# ---------------------------------------------------------------------------
def profile_picture_html(size):
    logo_h = round(size * 0.62)
    body = f"""
    <div style="width:{size}px;height:{size}px;background:{BG1};
                display:flex;align-items:center;justify-content:center;">
      {p5_mark(logo_h)}
    </div>"""
    return page_shell(body, size, size)


PROFILE_PICTURES = [
    ("facebook-profile-180x180.png", 180),
    ("instagram-profile-320x320.png", 320),
    ("youtube-profile-800x800.png", 800),
    ("linkedin-profile-300x300.png", 300),
    ("whatsapp-profile-640x640.png", 640),
    ("telegram-profile-512x512.png", 512),
]


# ---------------------------------------------------------------------------
# PART 2 — BANNERS
# ---------------------------------------------------------------------------

def bg_gradient_div(width, height, angle="135deg"):
    return (
        f'<div style="position:absolute;inset:0;'
        f'background:linear-gradient({angle}, {BG1}, {BG2});"></div>'
    )


def skyline_bars_decor(canvas_w, canvas_h):
    """4 P5-style staircase bars, scaled very large, faded, lower-half skyline."""
    bar_defs = [
        (0.12, 0.28), (0.30, 0.42), (0.48, 0.56), (0.66, 0.70),
    ]  # (left fraction, height fraction of canvas)
    bar_w = round(canvas_w * 0.11)
    bars_html = ""
    for left_f, h_f in bar_defs:
        left = round(canvas_w * left_f)
        h = round(canvas_h * h_f)
        bars_html += (
            f'<div style="position:absolute;left:{left}px;bottom:0;'
            f'width:{bar_w}px;height:{h}px;border-radius:{bar_w//2}px '
            f'{bar_w//2}px 0 0;background:{GOLD};opacity:.08;"></div>'
        )
    glow_size = round(canvas_w * 0.55)
    glow = (
        f'<div style="position:absolute;left:50%;bottom:-{round(glow_size*0.45)}px;'
        f'width:{glow_size}px;height:{glow_size}px;transform:translateX(-50%);'
        f'border-radius:50%;'
        f'background:radial-gradient(circle, rgba(245,166,35,.28), rgba(245,166,35,0) 70%);"></div>'
    )
    return f'<div style="position:absolute;inset:0;overflow:hidden;">{glow}{bars_html}</div>'


def dotted_arc_decor(canvas_w, canvas_h, opacity, stroke_w, arc_y_frac=0.5, sag_frac=0.35):
    """A single sweeping dotted arc spanning the full canvas width."""
    y0 = canvas_h * arc_y_frac
    peak = canvas_h * (arc_y_frac - sag_frac)
    d = f"M0,{y0:.0f} Q{canvas_w/2:.0f},{peak:.0f} {canvas_w:.0f},{y0:.0f}"
    return f"""<svg style="position:absolute;inset:0;" width="{canvas_w}" height="{canvas_h}"
      viewBox="0 0 {canvas_w} {canvas_h}" xmlns="http://www.w3.org/2000/svg">
      <path d="{d}" fill="none" stroke="{GOLD}" stroke-width="{stroke_w}"
        stroke-linecap="round" stroke-dasharray="2 {stroke_w*3.2:.0f}" opacity="{opacity}"/>
    </svg>"""


def scattered_dots_decor(canvas_w, canvas_h, count, opacity, seed=42):
    rnd = random.Random(seed)
    dots = ""
    for _ in range(count):
        x = rnd.uniform(0, canvas_w)
        y = rnd.uniform(0, canvas_h)
        r = rnd.uniform(1, 2.6)
        dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#FFFFFF"/>'
    return f"""<svg style="position:absolute;inset:0;" width="{canvas_w}" height="{canvas_h}"
      viewBox="0 0 {canvas_w} {canvas_h}" xmlns="http://www.w3.org/2000/svg" opacity="{opacity}">
      {dots}
    </svg>"""


def equalizer_decor(canvas_w, canvas_h):
    """P5 bars repeated horizontally like a sound-wave / equalizer, centered."""
    rnd = random.Random(7)
    n = 26
    total_w = canvas_w * 0.82
    bar_w = total_w / (n * 1.7)
    gap = bar_w * 0.7
    start_x = (canvas_w - (n * bar_w + (n - 1) * gap)) / 2
    mid_y = canvas_h * 0.5
    bars = ""
    for i in range(n):
        h = rnd.uniform(canvas_h * 0.05, canvas_h * 0.22)
        x = start_x + i * (bar_w + gap)
        bars += (
            f'<rect x="{x:.1f}" y="{mid_y - h/2:.1f}" width="{bar_w:.1f}" height="{h:.1f}" '
            f'rx="{bar_w/2:.1f}" fill="{GOLD}"/>'
        )
    return f"""<svg style="position:absolute;inset:0;" width="{canvas_w}" height="{canvas_h}"
      viewBox="0 0 {canvas_w} {canvas_h}" xmlns="http://www.w3.org/2000/svg" opacity=".07">
      {bars}
    </svg>"""


# ---- Facebook cover (CLAUDE.md spec: 1640x922, safe zone 640x312) ----------
def facebook_cover_html():
    W, H = 1640, 922
    safe_w, safe_h = 640, 312
    left = (W - safe_w) / 2
    top = (H - safe_h) / 2
    body = f"""
    <div style="position:relative;width:{W}px;height:{H}px;">
      {bg_gradient_div(W, H)}
      {skyline_bars_decor(W, H)}
      <div style="position:absolute;left:{left}px;top:{top}px;width:{safe_w}px;height:{safe_h}px;">
        <div style="position:absolute;top:50%;left:0;transform:translateY(-50%);
                    display:flex;align-items:center;width:100%;">
          {p5_mark(100)}
          <div style="margin-left:34px;font-weight:700;font-size:38px;line-height:1.18;">
            <div style="color:{WHITE};">90 days from now</div>
            <div style="color:{WHITE};">you will wish</div>
            <div style="color:{GOLD};">you had started today.</div>
          </div>
        </div>
        <div style="position:absolute;bottom:0;right:0;font-size:16px;
                    color:{GOLD_LIGHT};font-weight:600;">suienglishacademy.in</div>
      </div>
    </div>"""
    return page_shell(body, W, H), W, H


# ---- YouTube banner (2560x1440, safe zone 1546x423) ------------------------
def youtube_banner_html():
    W, H = 2560, 1440
    safe_w, safe_h = 1546, 423
    left = (W - safe_w) / 2
    top = (H - safe_h) / 2
    body = f"""
    <div style="position:relative;width:{W}px;height:{H}px;">
      {bg_gradient_div(W, H)}
      {dotted_arc_decor(W, H, 0.10, 8, arc_y_frac=0.62, sag_frac=0.30)}
      {scattered_dots_decor(W, H, 140, 0.06, seed=11)}
      <div style="position:absolute;left:{left}px;top:{top}px;width:{safe_w}px;height:{safe_h}px;
                  display:flex;align-items:center;">
        {p5_mark(200)}
        <div style="width:2px;height:180px;background:{GOLD};margin:0 46px;"></div>
        <div style="display:flex;flex-direction:column;">
          <div style="font-weight:700;font-size:54px;line-height:1.2;color:{WHITE};">Most people study English for years</div>
          <div style="font-weight:700;font-size:54px;line-height:1.2;color:{WHITE};">and never become fluent.</div>
          <div style="font-weight:600;font-size:38px;line-height:1.3;color:{GOLD};margin-top:14px;">Here's what they're missing.</div>
          <div style="font-size:24px;color:{GOLD_LIGHT};font-weight:600;margin-top:28px;">SUI English Academy &middot; New videos every week</div>
        </div>
      </div>
    </div>"""
    return page_shell(body, W, H), W, H


# ---- LinkedIn banner (1128x191, 40px padding) ------------------------------
def linkedin_banner_html():
    W, H = 1128, 191
    pad = 40
    body = f"""
    <div style="position:relative;width:{W}px;height:{H}px;">
      {bg_gradient_div(W, H)}
      {dotted_arc_decor(W, H, 0.12, 3, arc_y_frac=0.16, sag_frac=0.12)}
      <div style="position:absolute;left:{pad}px;top:{pad}px;width:{W-2*pad}px;height:{H-2*pad}px;
                  display:flex;align-items:center;">
        {p5_mark(100)}
        <div style="margin-left:24px;display:flex;flex-direction:column;">
          <div style="font-weight:700;font-size:21px;line-height:1.3;color:{WHITE};">Spoken English is the highest-ROI</div>
          <div style="font-weight:700;font-size:21px;line-height:1.3;color:{WHITE};">skill you're not investing in.</div>
        </div>
        <div style="flex:1;"></div>
        <div style="width:2px;height:70px;background:{GOLD};margin:0 28px;"></div>
        <div style="display:flex;flex-direction:column;align-items:flex-start;">
          <div style="font-weight:700;font-size:19px;color:{GOLD_LIGHT};">2,400+ students coached</div>
          <div style="font-weight:600;font-size:14px;color:{WHITE};margin-top:4px;">SUI English Academy</div>
        </div>
      </div>
    </div>"""
    return page_shell(body, W, H), W, H


# ---- WhatsApp Business banner (1080x1920 portrait) -------------------------
def whatsapp_banner_html():
    W, H = 1080, 1920
    body = f"""
    <div style="position:relative;width:{W}px;height:{H}px;">
      {bg_gradient_div(W, H, angle="180deg")}
      {equalizer_decor(W, H)}
      <div style="position:relative;width:100%;height:100%;display:flex;
                  flex-direction:column;align-items:center;justify-content:center;">
        <div style="margin-bottom:90px;">{p5_mark(600)}</div>
        <div style="text-align:center;">
          <div style="font-weight:800;font-size:66px;line-height:1.22;color:{WHITE};">The problem isn't your English.</div>
          <div style="font-weight:700;font-size:46px;line-height:1.3;color:{WHITE};margin-top:16px;">It's that nobody ever taught you</div>
          <div style="font-weight:700;font-size:46px;line-height:1.3;color:{GOLD};margin-top:4px;">how to practice it.</div>
        </div>
        <div style="margin-top:90px;background:{GOLD};border-radius:999px;padding:26px 50px;">
          <span style="font-weight:700;font-size:32px;color:{INK};">WhatsApp +91 9250167119</span>
        </div>
        <div style="margin-top:22px;font-size:24px;font-weight:600;color:{GOLD_LIGHT};">suienglishacademy.in</div>
      </div>
    </div>"""
    return page_shell(body, W, H), W, H


BANNERS = [
    ("facebook-cover-1640x922.png", facebook_cover_html),
    ("youtube-banner-2560x1440.png", youtube_banner_html),
    ("linkedin-banner-1128x191.png", linkedin_banner_html),
    ("whatsapp-banner-1080x1920.png", whatsapp_banner_html),
]


# ---------------------------------------------------------------------------
# RENDER
# ---------------------------------------------------------------------------
SCALE = 2  # supersample factor for anti-aliasing, downsampled with LANCZOS


def capture(page, html, width, height, out_path):
    page.set_viewport_size({"width": width, "height": height})
    page.set_content(html, wait_until="networkidle")
    page.evaluate("() => document.fonts.ready")
    trigger_and_freeze(page)
    raw_path = out_path + ".raw.png"
    page.screenshot(path=raw_path)
    img = Image.open(raw_path)
    img = img.resize((width, height), Image.LANCZOS)
    img.save(out_path, format="PNG", optimize=True, compress_level=9)
    img.close()
    os.remove(raw_path)


def main():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(device_scale_factor=SCALE)
        page = context.new_page()

        for filename, size in PROFILE_PICTURES:
            out_path = os.path.join(PROFILE_DIR, filename)
            html = profile_picture_html(size)
            capture(page, html, size, size, out_path)
            results.append(out_path)
            print(f"done: {filename}")

        for filename, builder in BANNERS:
            out_path = os.path.join(BANNER_DIR, filename)
            html, w, h = builder()
            capture(page, html, w, h, out_path)
            results.append(out_path)
            print(f"done: {filename}")

        browser.close()

    print("\n--- Verification ---")
    for path in results:
        size_kb = os.path.getsize(path) / 1024
        with Image.open(path) as im:
            dims = im.size
        print(f"{os.path.relpath(path, ROOT)}  {dims[0]}x{dims[1]}  {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
