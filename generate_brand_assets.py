"""
Generates SUI English Academy social media profile pictures and banners
directly to disk using Playwright (headless Chromium) + Pillow.

Run:  .venv-assets\\Scripts\\python.exe generate_brand_assets.py
"""

import os
import random
import sys

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


def p5_lockup(mark_height, glow_opacity=0.35, glow_scale=1.75, glow_blur_factor=0.13):
    """Full logo lockup exactly as in the nav: mark + 'SUI' / 'ENGLISH ACADEMY'
    wordmark, laid out with the site's own proportions (.logo{display:flex;
    align-items:center;gap:12px} at mark height 52px), scaled uniformly to
    mark_height. A soft gold bloom sits behind the mark only. Never use
    p5_mark() alone on a banner — this is the only lockup banners should use."""
    scale = mark_height / 52
    gap = 12 * scale
    sui_size = 21.12 * scale
    sub_size = 8.8 * scale
    margin_top = 6 * scale
    mark_w = mark_height * 64 / 80
    mark = p5_mark(mark_height)

    glow_size = mark_height * glow_scale
    glow_left = mark_w / 2 - glow_size / 2
    blur_px = mark_height * glow_blur_factor
    glow = (
        f'<div style="position:absolute;left:{glow_left:.0f}px;top:50%;'
        f'transform:translateY(-50%);width:{glow_size:.0f}px;height:{glow_size:.0f}px;'
        f'border-radius:50%;background:radial-gradient(circle, rgba(245,166,35,{glow_opacity}), '
        f'rgba(245,166,35,0) 70%);filter:blur({blur_px:.0f}px);z-index:0;pointer-events:none;"></div>'
    )
    return f"""<div style="display:flex;align-items:center;gap:{gap:.0f}px;position:relative;flex:none;">
      {glow}
      <div style="position:relative;z-index:1;line-height:0;">{mark}</div>
      <div style="position:relative;z-index:1;display:flex;flex-direction:column;line-height:1;">
        <span style="font-family:'Sora',sans-serif;font-weight:800;font-size:{sui_size:.1f}px;color:{WHITE};letter-spacing:.02em;white-space:nowrap;">SUI</span>
        <span style="font-family:'Sora',sans-serif;font-weight:600;font-size:{sub_size:.1f}px;letter-spacing:.3em;text-transform:uppercase;margin-top:{margin_top:.0f}px;color:{GOLD};white-space:nowrap;">English Academy</span>
      </div>
    </div>"""


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
# PART 2 — BANNERS (premium redesign — full lockup only, never the icon alone)
# ---------------------------------------------------------------------------

def radial_spotlight_bg(cx=50, cy=42):
    """Center-lighter, edge-darker radial gradient — 'spotlight/stage' feel."""
    return (
        f'<div style="position:absolute;inset:0;'
        f'background:radial-gradient(ellipse at {cx}% {cy}%, {BG2} 0%, {BG1} 72%);"></div>'
    )


def linear_lr_bg():
    """Left (where the logo sits) slightly lighter, fading darker to the right."""
    return (
        f'<div style="position:absolute;inset:0;'
        f'background:linear-gradient(90deg, {BG2}, {BG1} 75%);"></div>'
    )


def vignette_div(strength=0.32):
    """Subtle inner vignette — all four edges a touch darker than the center."""
    return (
        f'<div style="position:absolute;inset:0;'
        f'background:radial-gradient(ellipse at center, rgba(0,0,0,0) 56%, '
        f'rgba(0,0,0,{strength}) 100%);"></div>'
    )


def skyline_bars_lower_right(w, h, opacity=0.08, glow_opacity=0.15):
    """4 P5-style staircase bars at 3x scale, lower-right, like a glowing
    skyline rising from the bottom, plus a soft amber glow behind them."""
    bar_defs = [(0.60, 0.32), (0.71, 0.44), (0.82, 0.56), (0.91, 0.66)]
    bar_w = w * 0.075
    bars = ""
    for left_f, h_f in bar_defs:
        left = w * left_f
        bh = h * h_f
        bars += (
            f'<div style="position:absolute;left:{left:.0f}px;bottom:0;'
            f'width:{bar_w:.0f}px;height:{bh:.0f}px;border-radius:{bar_w/2:.0f}px '
            f'{bar_w/2:.0f}px 0 0;background:{GOLD};opacity:{opacity};"></div>'
        )
    glow_size = w * 0.5
    glow_left = w * 0.78 - glow_size / 2
    glow = (
        f'<div style="position:absolute;left:{glow_left:.0f}px;bottom:-{glow_size*0.42:.0f}px;'
        f'width:{glow_size:.0f}px;height:{glow_size:.0f}px;border-radius:50%;'
        f'background:radial-gradient(circle, rgba(245,166,35,{glow_opacity}), '
        f'rgba(245,166,35,0) 70%);"></div>'
    )
    return f'<div style="position:absolute;inset:0;overflow:hidden;">{glow}{bars}</div>'


def diagonal_sweep_arc(w, h, opacity=0.10, stroke_w=8):
    """One grand dotted arc, same dash style as the P5 trail, sweeping the
    full canvas width from bottom-left to upper-right."""
    x0, y0 = 0, h * 0.88
    x1, y1 = w * 0.5, h * 0.16
    x2, y2 = w, h * 0.04
    d = f"M{x0:.0f},{y0:.0f} Q{x1:.0f},{y1:.0f} {x2:.0f},{y2:.0f}"
    return f"""<svg style="position:absolute;inset:0;" width="{w}" height="{h}"
      viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
      <path d="{d}" fill="none" stroke="{GOLD}" stroke-width="{stroke_w}"
        stroke-linecap="round" stroke-dasharray="2 {stroke_w*3.4:.0f}" opacity="{opacity}"/>
    </svg>"""


def constellation_dots(w, h, count=13, opacity=0.08, seed=5):
    """A handful of tiny scattered dots, asymmetric, for quiet depth."""
    rnd = random.Random(seed)
    dots = ""
    for _ in range(count):
        x = rnd.uniform(0.04 * w, 0.96 * w)
        y = rnd.uniform(0.05 * h, 0.85 * h)
        r = rnd.uniform(1.4, 3.4)
        dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#FFFFFF"/>'
    return f"""<svg style="position:absolute;inset:0;" width="{w}" height="{h}"
      viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" opacity="{opacity}">{dots}</svg>"""


def top_edge_dotted_line(w, h, opacity=0.10, stroke_w=2.2):
    """A thin dotted trail-style accent line hugging the very top edge."""
    y0 = h * 0.16
    d = f"M0,{y0*1.1:.0f} Q{w/2:.0f},{y0*0.25:.0f} {w:.0f},{y0*0.6:.0f}"
    return f"""<svg style="position:absolute;inset:0;" width="{w}" height="{h}"
      viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
      <path d="{d}" fill="none" stroke="{GOLD}" stroke-width="{stroke_w}"
        stroke-linecap="round" stroke-dasharray="1.6 {stroke_w*3.4:.0f}" opacity="{opacity}"/>
    </svg>"""


def gold_separator(height_px, opacity=1):
    return (
        f'<div style="width:1px;height:{height_px:.0f}px;background:{GOLD};'
        f'opacity:{opacity};flex:none;"></div>'
    )


# ---- Facebook cover (1640x922, safe zone 640x312) --------------------------
def facebook_cover_html():
    W, H = 1640, 922
    safe_w, safe_h = 640, 312
    left, top = (W - safe_w) / 2, (H - safe_h) / 2
    lockup = p5_lockup(78, glow_opacity=0.38, glow_scale=1.9)
    sep_h = safe_h * 0.6
    body = f"""
    <div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;">
      {radial_spotlight_bg()}
      {skyline_bars_lower_right(W, H, opacity=0.08, glow_opacity=0.15)}
      {vignette_div(0.34)}
      <div style="position:absolute;left:{left:.0f}px;top:{top:.0f}px;width:{safe_w}px;height:{safe_h}px;
                  display:flex;align-items:center;">
        {lockup}
        {gold_separator(sep_h)}
        <div style="margin-left:26px;display:flex;flex-direction:column;">
          <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:22px;line-height:1.6;letter-spacing:.015em;color:{WHITE};">Most people learn English.</div>
          <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:22px;line-height:1.6;letter-spacing:.015em;color:{WHITE};">Nobody teaches them</div>
          <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:22px;line-height:1.6;letter-spacing:.015em;color:{WHITE};">how to actually speak it.</div>
          <div style="font-family:'Sora',sans-serif;font-weight:800;font-size:27px;line-height:1.4;letter-spacing:.015em;color:{GOLD};margin-top:8px;">We do.</div>
          <div style="font-family:'Sora',sans-serif;font-weight:400;font-size:14px;letter-spacing:.14em;color:{PALE_GOLD};margin-top:20px;">suienglishacademy.in</div>
        </div>
      </div>
    </div>"""
    return page_shell(body, W, H), W, H


# ---- YouTube banner (2560x1440, safe zone 1546x423) ------------------------
def youtube_banner_html():
    W, H = 2560, 1440
    safe_w, safe_h = 1546, 423
    left, top = (W - safe_w) / 2, (H - safe_h) / 2
    lockup = p5_lockup(170, glow_opacity=0.36, glow_scale=1.8)
    sep_h = safe_h
    body = f"""
    <div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;">
      {radial_spotlight_bg()}
      {diagonal_sweep_arc(W, H, opacity=0.10, stroke_w=9)}
      {constellation_dots(W, H, count=14, opacity=0.08, seed=11)}
      {vignette_div(0.30)}
      <div style="position:absolute;left:{left:.0f}px;top:{top:.0f}px;width:{safe_w}px;height:{safe_h}px;
                  display:flex;align-items:center;">
        {lockup}
        {gold_separator(sep_h)}
        <div style="margin-left:46px;display:flex;flex-direction:column;">
          <div style="font-family:'Sora',sans-serif;font-weight:800;font-size:42px;line-height:1.35;letter-spacing:.01em;color:{WHITE};">Most people study English for years</div>
          <div style="font-family:'Sora',sans-serif;font-weight:800;font-size:42px;line-height:1.35;letter-spacing:.01em;color:{WHITE};">and never become fluent.</div>
          <div style="font-family:'Sora',sans-serif;font-weight:600;font-size:28px;line-height:1.4;letter-spacing:.01em;color:{GOLD};margin-top:14px;">Here's what they're missing.</div>
          <div style="font-family:'Sora',sans-serif;font-weight:400;font-size:17px;letter-spacing:.14em;color:{PALE_GOLD};margin-top:30px;">suienglishacademy.in</div>
        </div>
      </div>
    </div>"""
    return page_shell(body, W, H), W, H


# ---- LinkedIn banner (1128x191, 40px padding) ------------------------------
def linkedin_banner_html():
    W, H = 1128, 191
    pad = 40
    lockup = p5_lockup(110, glow_opacity=0.18, glow_scale=1.5)
    inner_h = H - 2 * pad
    body = f"""
    <div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;">
      {linear_lr_bg()}
      {top_edge_dotted_line(W, H, opacity=0.10)}
      <div style="position:absolute;left:{pad}px;top:{pad}px;width:{W-2*pad}px;height:{inner_h}px;
                  display:flex;align-items:center;">
        {lockup}
        <div style="margin:0 26px;">{gold_separator(round(inner_h*0.5))}</div>
        <div style="display:flex;flex-direction:column;">
          <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:18px;line-height:1.35;letter-spacing:.015em;color:{WHITE};">Spoken English is the highest-ROI</div>
          <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:18px;line-height:1.35;letter-spacing:.015em;color:{WHITE};">skill you're not investing in.</div>
        </div>
        <div style="flex:1;"></div>
        <div style="margin:0 26px;">{gold_separator(round(inner_h*0.5))}</div>
        <div style="display:flex;flex-direction:column;align-items:flex-end;text-align:right;">
          <div style="font-family:'Sora',sans-serif;font-weight:600;font-size:16px;letter-spacing:.02em;color:{PALE_GOLD};">2,400+ students coached</div>
          <div style="font-family:'Sora',sans-serif;font-weight:400;font-size:13px;letter-spacing:.04em;color:{LAVENDER};margin-top:4px;">suienglishacademy.in</div>
        </div>
      </div>
    </div>"""
    return page_shell(body, W, H), W, H


# ---- WhatsApp Business cover (1125x633, landscape) -------------------------
def whatsapp_cover_html():
    W, H = 1125, 633
    band_h = H * 0.72  # keep clear of the center-bottom circular-avatar overlap
    lockup = p5_lockup(120, glow_opacity=0.4, glow_scale=1.9)
    body = f"""
    <div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;">
      {radial_spotlight_bg(50, 38)}
      {skyline_bars_lower_right(W, H, opacity=0.08, glow_opacity=0.16)}
      {diagonal_sweep_arc(W, H, opacity=0.10, stroke_w=6)}
      {vignette_div(0.34)}
      <div style="position:absolute;left:0;top:0;width:100%;height:{band_h:.0f}px;
                  display:flex;align-items:center;justify-content:space-between;
                  padding:0 78px;">
        {lockup}
        <div style="display:flex;flex-direction:column;">
          <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:26px;line-height:1.55;letter-spacing:.015em;color:{WHITE};">Most people learn English.</div>
          <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:26px;line-height:1.55;letter-spacing:.015em;color:{WHITE};">Nobody teaches them</div>
          <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:26px;line-height:1.55;letter-spacing:.015em;color:{WHITE};">how to actually speak it.</div>
          <div style="font-family:'Sora',sans-serif;font-weight:800;font-size:32px;line-height:1.4;letter-spacing:.015em;color:{GOLD};margin-top:8px;">We do.</div>
          <div style="font-family:'Sora',sans-serif;font-weight:400;font-size:15px;letter-spacing:.14em;color:{PALE_GOLD};margin-top:22px;">suienglishacademy.in</div>
        </div>
      </div>
    </div>"""
    return page_shell(body, W, H), W, H


BANNERS = [
    ("facebook-cover-1640x922.png", facebook_cover_html),
    ("youtube-banner-2560x1440.png", youtube_banner_html),
    ("linkedin-banner-1128x191.png", linkedin_banner_html),
    ("whatsapp-cover-1125x633.png", whatsapp_cover_html),
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
