# Mentone Hockey Club — Design System

A design system for **Mentone Hockey Club (MHC)** — a family-friendly community hockey club on Melbourne's Bayside, established 1926. The club fields teams across every Hockey Victoria competition from Hook in2 Hockey (ages 5–10) through Men's and Women's Premier League to Masters.

This system is derived from the club's 2026 site redesign concept — a warm, editorial, sports-journal aesthetic built on a navy/powder-blue/yellow palette with Fraunces display type and Inter body.

---

## Sources

- **Brand mark:** `uploads/ChatGPT Image Jan 13, 2026, 02_05_24 PM.png` — a roaring panther mascot (navy body, yellow outline, yellow eyes). Club mascot / esports-style emblem.
- **Website codebase:** GitHub `bourbon-beast/mentone-hc-web` (branch `design/concept`). Five files — `index.html`, `juniors.html`, `mens.html`, `new-players.html`, `styles.css`. Imported to `src/`.
- **Product context:** public-facing marketing site (home, section pages, new-player onboarding). No member portal or fixture API in the concept repo — just the brochure site.

Team hierarchy from the site:
- **Men's** · Premier League → Metro grades
- **Women's** · Premier League → Metro grades
- **Juniors** · Hook in2 Hockey (5–10), U8/U10/U12, U14/U16, U18
- **Masters** · Men's & Women's

---

## Index

**Foundations**
- `colors_and_type.css` — Design tokens: palette, type, spacing, shadows, radii. Import this file to use the system.
- `preview/` — Design-system preview cards (rendered in the Design System tab).

**Assets**
- `assets/panther-mascot.png` — Club mascot illustration.
- `assets/` — Logos, wordmark, and brand ornaments (generated from the mascot + wordmark conventions in the site).

**UI kit**
- `ui_kits/marketing-site/` — Interactive recreation of the Mentone website. Pixel-faithful to the `design/concept` branch.

**Reference**
- `src/` — Original imported HTML/CSS from the concept branch (read-only reference — do not edit).
- `SKILL.md` — Agent skill descriptor for portable use.

---

## Content Fundamentals

The Mentone voice is **warm, plain-spoken Australian community-club**. It sounds like the coach at the sausage sizzle, not the marketing department. No jargon, no corporate polish, no hype.

**Tone**
- Welcoming and unpretentious. Family-friendly above all.
- Confident about quality (Premier League, accredited coaches) but never boastful.
- Specific, concrete details — times, costs, ages, gear. Avoid vague claims.
- Gentle Australian idiom — "turf", "a feed", "come down", "grab a stick", "stuck in", "a bit of a debrief".

**Voice & person**
- Second person ("your child", "you") when addressing the reader directly.
- First person plural ("we", "our") for the club itself — it's a community, not an institution.
- Never "the Club" with a capital C. It's "the club".

**Casing**
- **Sentence case** for everything — nav, buttons, body, headings. No Title Case.
- UPPERCASE only for eyebrows, micro-labels, and stat captions (letter-spacing always ≥ 0.14em when uppercase).
- Brand italic emphasis is lowercase too — "A team for *every* player".

**Examples of voice (verbatim from the site)**
- "A fun, friendly *first taste* of hockey."
- "Turn up, get stuck in."
- "Come down for a drink, a feed, and a bit of a debrief."
- "Not at all." (FAQ opening)
- "Like most community sports clubs, we run on volunteers…"
- "Happens sometimes — and that's completely fine."

**Emoji**
- **Not used.** The only decorative glyph in the site is a single ★ (used sparingly as a badge/callout — e.g. "★ For Kids · Ages 5–10"). Treat ★ as part of the type system, not emoji. No smileys, no hockey-stick emoji.

**Punctuation**
- Em-dashes ( — ) used liberally to add texture and cadence.
- Middle-dot ( · ) separates parallel items in compact metadata ("Est. 1926 · Bayside", "U8 · U10 · U12").
- Ampersand ( & ) in headings/nav ("Events & Masters"). Avoid in body copy.
- Arrow ( → ) on secondary links ("Register now →", "Your Business Here →").

**Numbers & times**
- Lowercase am/pm, no space: `5:15–6:00pm`, `9:30am`.
- En-dash for time ranges. Tabular numerals on fixtures lists (`font-variant-numeric: tabular-nums`).
- Stats shown large and terse: `160+` / `Junior Players`.

**Acknowledgement of Country** appears in every footer — italic, reverent, never decorated.

---

## Visual Foundations

### Palette
A restrained, three-color brand. Navy dominates; yellow is the accent; powder blue bridges them.

- `--navy #041C2C` Primary. Nav text, buttons, hero backgrounds, headings.
- `--navy-soft #0d3048` Navy-on-navy hovers and panel variations.
- `--navy-deep #02121c` Announcement bar, deepest CTA bands.
- `--blue #7DA1C4` Powder blue — decorative gradients, women's team accent.
- `--blue-wash #e6eef6` Pale section backgrounds (news, coaches, gear).
- `--yellow #F1B434` Brand yellow. CTAs, hover underlines, accent strokes, highlight text.
- `--yellow-bright #f5c966` Yellow on hover / on-navy contexts.
- `--yellow-deep #c89120` Eyebrows on cream, link underlines, italic emphasis color.
- `--cream #f6f1e6` Default page background. Warm, slightly off-white.
- `--muted #5a6b7a` Secondary text.

Imagery rule: colors lean **cool and editorial** — navy/blue gradients, cream neutral. Yellow is the only warm accent. No gradients outside of hero photos and featured tiles.

### Typography
- **Display:** Fraunces (serif, variable optical size). Weight **400** for most display sizes, **500** for smaller card titles. Italics at **300** for emphasized words — the italic is the brand's signature flourish ("fall in *love* with hockey").
- **Body:** Inter at 400/500/600/700. 16px default, 1.5–1.7 line-height.
- Letter-spacing: tighter on display (−0.02em to −0.025em), wider on uppercase eyebrows (0.14em–0.24em).

### Spacing & layout
- **Section padding** 110px top/bottom on desktop, 72px mobile.
- **Wrap** max-width 1240px, 28px horizontal gutter.
- **Grid** rhythms: 4-up (stat strips, team cards), 3-up (news, grades), 2-up (feature splits).
- **Section rhythm alternates backgrounds**: cream → navy → cream → blue-wash → cream. Never two consecutive sections the same color.

### Cards, surfaces, borders
- **Card default:** white (`#fff`) or cream, `border-radius: 4px` (essentially rectangular — this is a newspaper aesthetic, not a bubbly app).
- Borders are 1px `rgba(4,28,44,0.08–0.12)` — a whisper of ink, not a hard line.
- **Card hover:** raises 4px (`translateY(-4px)`), gains `--shadow-md`, border darkens slightly. Sometimes a 3px yellow bar slides in at the top (scaleX 0 → 1, 0.3s).
- Featured / inverted cards: navy background, cream text, yellow top bar always on.
- **Shadows:** three-step — `sm` (list separators), `md` (hover), `lg` (floating hero cards). All shadows are navy-tinted (not neutral gray), keeping the whole surface unified.

### Backgrounds
- **Hero navy panels** layer three effects:
  1. Solid `--navy` base
  2. A soft radial blue glow top-right
  3. Faint 120px-pitch vertical stripes at 3% opacity (evokes pitch lines / newspaper column rule)
- **Yellow feature tiles** use a 135° yellow gradient with a diagonal white radial highlight — sunny and physical.
- No stock-photo washes, no complex photo collages — photos are shown full-bleed in defined aspect ratios (4:5 hero, 3:2 news).

### Motion
- **Entry:** everything above-the-fold `rise` — 20px translateY + opacity 0→1, staggered 0.1s–0.7s.
- **Hover:** 0.2s–0.3s. Buttons translateY(-1px); cards translateY(-4px); images scale(1.05) on card hover. Underline reveals use `transform: scaleX(0→1)` (origin left), 0.3s ease.
- **No bounces.** No springs. Everything is calm ease.
- Navigation underlines are yellow, 2px, animated on hover and persistent on `.active`.

### Interaction states
- **Primary button** (yellow bg, navy text): hover → `--yellow-bright`, lift 1px, navy-tinted shadow.
- **Navy button** (navy bg, cream text): hover → `--navy-soft`.
- **Ghost button** (transparent, cream border at 30%): hover → border full cream, 5% cream wash behind.
- **Links in text:** 1px yellow bottom border with 2px padding-bottom — never the whole word underlined.
- **Focus:** inherits browser default (no custom focus styling in the source — a candidate for later improvement).

### Transparency, blur, tinting
- Nav uses `backdrop-filter: blur(8px)` over cream — subtle.
- On-navy overlays use cream at 0.04–0.15 alpha for layered cards.
- No glassmorphism, no heavy blur. Restrained.

### Capsules, badges, pills
- `grade-tag` and `news-cat`: tiny uppercase pills, 10–11px, 0.18em spacing, 3px radius, solid backgrounds. Very small — they whisper, not shout.
- `hook-badge`: 100px pill radius, navy bg, yellow text, ★ prefix. Used sparingly as a featured callout.
- Stat numbers and big numerals are Fraunces 40–140px with `-0.02–-0.04em` tracking — they anchor sections visually.

### Iconography (placeholder — see ICONOGRAPHY section below)
- Inline SVGs, 1.2–2px stroke, rounded caps/joins. No filled icons. No emoji.

---

## Iconography

**Approach:** The site uses hand-rolled, lightweight inline SVG icons. There is **no icon library or icon font** in the codebase — icons are small one-off SVG paths embedded directly in HTML. They're utility glyphs (arrow, envelope, hamburger, social), not illustrative.

**Characteristics**
- **Stroke-based.** `fill="none"`, `stroke="currentColor"`, `stroke-width` 1.2–2 (typically 2), `stroke-linecap="round"`, `stroke-linejoin="round"`.
- **Sized tiny-to-small** — 12/14/24px in viewBox equivalents. Arrows in buttons are 14×14.
- **Color-inherit** via `currentColor` so the same icon works on light and dark grounds.
- **Minimal set used on the site:**
  - Arrow right (`M3 7h8M7 3l4 4-4 4`) — used on every CTA and card link.
  - Hamburger (`M3 6h18M3 12h18M3 18h18`) — mobile nav.
  - Envelope — contact strip, coach FAQ contact CTA.
  - Facebook (filled glyph — the one exception to the stroke rule).
  - Instagram (stroke camera outline).

**Since the set is so small**, this design system copies the actual inline SVGs into `assets/icons.svg` as a sprite, plus provides them as individual files under `assets/icons/*.svg`. For anything beyond the core set, **substitute with [Lucide](https://lucide.dev/)** — same stroke style, 2px weight, rounded caps/joins, so it drops in cleanly next to the existing icons. When you do substitute, flag it to the user.

**Emoji / unicode glyphs**
- **No emoji.** None of the site's copy uses emoji.
- **★ (U+2605)** is the one unicode glyph used decoratively — in the Hook in2 Hockey badge. Treat it as part of the type system.
- **· (middle dot, U+00B7)** is a structural separator in metadata strings.
- **→ (rightwards arrow, U+2192)** in inline text links ("Register now →") as an alternative to the SVG arrow.

**Logos / brand**
- `assets/panther-mascot.png` — full-color roaring panther on navy background (esports-style).
- `assets/monogram-m.svg` — the "M" roundel used in the site nav (navy circle, yellow M, 2px yellow stroke).
- `assets/wordmark.svg` — "Mentone Hockey Club" lockup in Fraunces, paired with "Est. 1926 · Bayside" micro-label.

No full-bleed hero photography is in the repo — the site uses gradient placeholders. Treat photography as a TODO; when the user provides match photos, they should be shot cool/editorial (navy/blue tones with yellow highlights).
