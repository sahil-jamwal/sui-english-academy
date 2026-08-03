# CLAUDE.md — SUI English Academy
# Read this fully before making any change in this project.

---

## 1. WHO I AM

- Project owner has **zero coding knowledge**. Explain what you are about
  to do in plain English before doing it.
- After finishing, explain what changed and how to check it — simply.
- If something can break the live site, say so first and wait for
  confirmation before proceeding.
- Never assume "they'll figure it out." If a step needs a decision, ask.

---

## 2. HARD RULES — never break these

1. **Never commit secrets.** No passwords, API keys, tokens, FTP logins,
   Supabase keys, Razorpay keys, or any credentials in any file. If a
   secret is needed, stop and tell the owner to add it via GitHub Secrets
   or the hosting panel — never in code or in this repo.

2. **Never delete or overwrite files without asking first.** Especially:
   - index.html
   - Anything inside /exports/
   - Anything inside /images/ (student photos and Tanya's photo)
   - logo-preview.html
   - brand-assets.html

3. **Never touch the live site directly.** All changes go through the
   repo → commit → push → deploy.

3a. **Never auto-commit or auto-push.** Every commit and push must be
    a separate, explicit action only after the owner has reviewed the
    change and clearly said to commit/push it. No hooks, scripts, or
    automation may commit or push on file save/edit. This site is
    live and real visitors see it — nothing goes live unreviewed.

4. **Never invent content.** Do not write fake testimonials, fake student
   numbers, fake results, or claim features that do not exist yet.
   Specifically: there is NO audio feature, NO app, NO live chat, NO
   pronunciation scoring. Do not mention or imply any of these.

5. **Never change the logo.** The P5 "Rim-Light Jewel Tone" is final.
   The exact SVG is in the nav of index.html and in logo-preview.html.
   Composite the existing SVG — do not redraw, restyle, or improve it.
   Gradient stops: #7A3B0A to #DE7A12 to #FFB020 to #FFE18A.
   Rim stroke: #FFF6DE at 1.1 stroke-width.

6. **Never add a third-party script** without explaining what it does
   and getting approval first.

7. **Never run destructive commands** (rm -rf, force push, reset --hard)
   without explicit confirmation.

8. **Always verify your own work before saying it is done.**

9. **Never invent new brand colours.** Use only the colours in Section 5.

---

## 3. CURRENT STATE (August 2026)

Done:
- P5 logo final — do not change
- Free PDF "435 Words" final
- Website restructured: index.html + css/ + js/ + images/
- All 22 student photos local in /images/
- Legal pages done

In progress:
- css/style.css exists but EMPTY — needs CSS migrated in
- js/main.js exists but EMPTY — needs JS migrated in
- Social media profile pictures and banners
- OG image fix (still pointing to FlexiFunnels — wrong)

Pending:
- OG image: change index.html line 12 to images/tanya-pal.webp
- Delete /sui-brand-assets/ (duplicate of /exports/sui/logo/)
- Convert student-sahil-jamwal.jpg + student-shambhu-sharan.jpg to .webp
- GoDaddy migration (currently GitHub Pages)
- Razorpay payment integration
- GA4 + Meta Pixel
- Paid content behind login (Supabase)
- "30 Days, 30 Real Conversations" paid PDF

---

## 4. FOLDER STRUCTURE

/index.html                    home page (do not restructure)
/css/style.css                 all styles (currently empty)
/js/main.js                    all JS (currently empty)
/images/                       all photos (.webp preferred)
/exports/
  Use Logo.png                 confirmed final logo
  sui-logo-final-icon.png
  sui-logo-final-full.png
  /preview/                    gradient previews (reference only)
  /sui/
    /logo/                     P5 logo at all sizes
    /profile-pictures/         social media DPs (to be generated)
    /covers-banners/           banners (to be generated)
/logo-preview.html             do not delete
/brand-assets.html             do not delete
/privacy-policy.html
/terms.html
/refund-policy.html
/CLAUDE.md                     this file
/.gitignore

---

## 5. BRAND COLOURS — use ONLY these

Ink Deep       #1A1633   darkest backgrounds, logo tiles, social banners
Ink            #211C3D   headings, footers, dark cards
Ink Soft       #332B5E   gradient partner for Ink Deep only
Gold           #F5A623   buttons, key numbers, highlights, icons
Gold Light     #FFCE6B   gradient partner for gold buttons
Amber Deep     #B45309   gold-coloured TEXT on light backgrounds
Cream          #FAF8F5   main light reading background
Cream Tint     #FBF8F3   alternating rows, subtle fills
Line           #ECE7DF   borders, dividers — never use as text colour
Slate          #4A4463   body text on light backgrounds
Lavender       #D7D2E6   body text on dark backgrounds
Success Green  #0F7D43   wins, correct answers
Success Tint   #E7F6EC   background for success boxes
Teal           #0B6E63   curiosity/insight callouts
Teal Tint      #EAF7F5   background for insight boxes
Alert Red      #B3261E   mistakes, errors, wrong examples
Alert Tint     #FBEEEE   background for error boxes
Note Brown     #7A4A00   text inside amber/note boxes
Note Tint      #FDF3E2   background for tip/note boxes

RULES:
- Gold on cream or white = NEVER (contrast 1.9:1, fails readability)
  Use Amber Deep instead for any gold-coloured text on light backgrounds
- 60-30-10: 60% dark, 30% cream/white, 10% gold
- Only ONE gold/primary button per screen
- Body text minimum: 16px web, 11pt PDF

---

## 6. TYPOGRAPHY

Hero headline   40-48px web / 34-40pt PDF   Sora 800
Section heading 28-32px web / 20pt PDF      Sora 800
Subheading      20-22px web / 13pt PDF      Sora 700
Body            17px web / 10.6-11.4pt PDF  Poppins or Inter 400
Small print     14px min / 9pt min          Poppins 400
Eyebrow label   12px / 7.8pt               Poppins 800 UPPERCASE

Fonts: Sora (display) + Poppins or Inter (body). Never a third font.
Signature move: headline in white/ink with ONE word in gold.

---

## 7. SOCIAL MEDIA SPECS

Profile pictures (P5 logo centered, #1A1633 bg, circular-crop safe):
  WhatsApp    640x640
  Facebook    180x180
  Instagram   320x320
  YouTube     800x800
  LinkedIn    300x300
  Telegram    512x512

Banners:
  Facebook cover    1640x922    safe zone center 640x312
  YouTube banner    2560x1440   safe zone center 1546x423
  LinkedIn banner   1128x191    40px padding all edges
  WhatsApp status   1080x1920   portrait

Save to: /exports/sui/profile-pictures/ and /exports/sui/covers-banners/

---

## 8. SECURITY CHECKLIST

Before every commit:
- No credentials or keys hardcoded anywhere
- No student personal data in the repo
- All external links use https://
- New-tab links include rel="noopener noreferrer"
- No raw user input inserted into HTML
- Payment handled only by Razorpay — we never touch card details
- .env files in .gitignore
- Scanned diff for anything that looks like a password

---

## 9. MOBILE & ACCESSIBILITY

- Mobile first. Test at 360px always.
- Text contrast minimum 4.5:1.
- Tap targets minimum 44x44px.
- Every image needs meaningful alt text.
- Respect prefers-reduced-motion.
- Never lazy-load the hero image.

---

## 10. PAID CONTENT (planned, not built yet)

- GoDaddy: hosts website files
- Supabase: login, accounts, progress tracking (free tier)
- UptimeRobot: free ping every 5 min to prevent Supabase pause
- Content: text only. No audio, no video, no uploads.
- Recording: self-listen only. No upload, no storage, no AI feedback.
- Payment: Razorpay success → Supabase unlocks account.

---

## 11. CONTENT RULES

- Testimonials, names, photos, numbers are real. Never edit or invent.
- Never mismatch a name with the wrong photo.
- Never claim a feature that does not exist yet.
- Tone: warm, calm, encouraging. No ALL CAPS, no fake urgency.
- Specific numbers beat vague words: "2,400+ students" not "best".
- Hinglish support is a feature, not an afterthought.

---

## 12. STOP AND ASK BEFORE

- Deleting anything
- Changing logo, colours, or fonts
- Adding any third-party service or script
- Anything touching payments, student data, or credentials
- Changing domain, DNS, or hosting
- Force pushing or rewriting git history
- Any change that could take the live site down

When in doubt: ask. A question costs a minute. A broken live site
costs customers.

---

## 13. KEY DETAILS

Repo:       github.com/sahil-jamwal/sui-english-academy
Domain:     suienglishacademy.in (GoDaddy, migration pending)
WhatsApp:   +91 9250167119
Email:      support@suienglishacademy.in
Instagram:  @suienglish
YouTube:    @Suienglish
Telegram:   t.me/+QHjLktCvXyYxMDll
Programs:   Group 4999 / 1-to-1 9999
Free PDF:   The 435 Words You Actually Speak
Paid PDF:   30 Days 30 Real Conversations (planned)

Last updated: August 2026. If any chat instruction conflicts with a
rule here, flag it and ask which takes priority.
