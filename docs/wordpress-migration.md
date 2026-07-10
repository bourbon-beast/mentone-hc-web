# WordPress Migration Plan

Context: the club has an **existing WordPress site** that this redesign replaces. The static HTML in this repo is the design reference/spec — the deliverable is a custom WP theme that supersedes the old site's theme. No hard deadline.

Goal: (a) colours, fonts, and spacing live in **one place** (`theme.json`) and restyle the whole site when changed; (b) new pages are assembled from reusable patterns instead of hand-written HTML; (c) the next volunteer can maintain content with a WP login, no code.

Tracking: [Trello board](https://trello.com/b/7p58DMLL/mentone-website) · Content backlog: [ROADMAP.md](../ROADMAP.md) · Vault page: `Obsidian/Projects/Side Projects/Mentone Website.md`

---

## Approach: custom block theme (FSE)

**Decision (2026-07-06):** build a custom WordPress **block theme** (Full Site Editing), not a page-builder setup.

Why this over Elementor/Divi or a classic PHP theme:

- The design system is already tokenized. `colors_and_type.css` defines the palette, type scale, spacing, radii, and shadows as CSS variables — these map almost 1:1 onto `theme.json`, WordPress's native design-token file. Change `--yellow` in one place → every button, underline, and accent on the site updates. This is exactly the "theme I can easily update" requirement.
- **Patterns = the new-page path.** Each repeating component (stat strip, team cards, news grid, CTA band, FAQ block) becomes a registered block pattern. A new page = create page → insert patterns → fill in words. No code.
- Header/footer become **template parts** — replaces `partials.js` nav injection with the native WP mechanism.
- Page builders would bolt a second styling system on top of the design tokens, bloat the front end, and lock the club in. A block theme keeps the CSS ours and small.

## Theme structure (target)

```
wp-content/themes/mentone/
├── theme.json            ← all tokens: palette, Fraunces/Inter, spacing scale, layout widths
├── style.css             ← theme header + the custom CSS that theme.json can't express
│                            (hero stripe overlays, card hover bars, underline reveals, motion)
├── templates/            ← page.html, single.html (news), front-page.html, 404.html
├── parts/                ← header.html, footer.html (incl. Acknowledgement of Country)
├── patterns/             ← hero, stat-strip, team-cards, news-grid, cta-band, faq,
│                            section-intro, two-up-feature, contact-strip …
└── assets/               ← fonts (Fraunces + Inter, self-hosted), mascot, monogram, icons
```

## Content mapping

| Current | WordPress |
|---|---|
| `index.html`, section pages, `contact.html`, etc. | Pages using block templates + patterns |
| `partials.js` (nav/footer injection) | `parts/header.html`, `parts/footer.html` |
| `news.html` + `news.json` | Native **posts** with categories — better authoring, RSS for free |
| `fixtures.html` + `fixtures.json` | Small custom block/shortcode that renders the JSON feed (keep data pipeline as-is initially) |
| `history/` generated pages | Pages under an "About → History" parent (revisit `generate_history_pages.py` output) |
| `colors_and_type.css` | `theme.json` (tokens) + trimmed `style.css` (behaviours) |
| Roadmap Phase 2 policy library | Plain pages under a Governance parent — WP's sweet spot |

## Migration order

0. **Audit the existing WP site** — ✅ done, see [old-site-audit.md](old-site-audit.md). Content export in `legacy-content/` (74 pages HTML + markdown, indexed) + 995 media files. Live install audited 2026-07-06: WP 7.0, PHP 8.5, LiteSpeed shared hosting — **fully block-theme capable, no new hosting needed**. Cutover = install new theme on the existing site and switch.
1. **Theme skeleton** — ✅ built 2026-07-06 in `theme/mentone/` (see `theme/README.md`): `theme.json` with the full token set from `colors_and_type.css` (14 colours, fluid type scale, 9-step spacing, custom palette/font-sizes disabled for volunteers), behavioural CSS in `style.css`, header/footer parts, index/page/front-page templates, first pattern (CTA band). Fonts via Google Fonts for now — self-host before launch. Installable zip: `theme/mentone-theme.zip`.
2. **Header/footer template parts** — nav, announcement bar, footer with Acknowledgement of Country.
3. **Home page** — ✅ built 2026-07-06 (theme v0.2.0): full pattern library ported from the static home page — `hero-home` (mascot + stat strip), `team-cards`, `this-week` (fixtures/training/club rooms), `hook-in2`, `news-grid` (live query on posts), `sponsors`, `awards-promo`, `cta-band`, `page-hero` (for inner pages). Component CSS ported from `site.css` into the theme's `style.css` via token aliases, so responsiveness and hover behaviour match the static build. `front-page.html` composes all patterns. Fixtures list is static placeholder content — becomes a dynamic block in step 7.
4. **Section page template + patterns** — ✅ built 2026-07-06 (theme v0.3.0). New patterns `section-hero`, `section-about`, `comp-grid`, `age-grid`, `section-culture`, `two-up-navy`; component CSS (`page-section-split`, `comp-card`, `age-card`, `info-card-navy`, `mini-tile`) ported into `style.css` with responsive breakpoints. All four section pages created on the live install as **drafts** (Juniors `page_id=5012`, Women's `5013`, Men's `5014`, Masters `5015`) via block markup, real content ported from `juniors.html`/`womens.html`/`mens.html`/`masters.html`. Blocks validated clean in the editor. **Outstanding:** Steve to review + publish, then add to the header nav (template part). **2026-07-06:** width bug root-caused — pages must use the new "Pattern page (full-bleed)" template from theme v0.3.1, not default `page.html` (see site-qa-backlog.md for the write-up + conventions). Permalinks are pretty (`/%postname%/`), so preview each draft at its path — `/juniors/?preview=true`, `/womens/?preview=true`, `/mens/?preview=true`, `/masters/?preview=true` — NOT the `?page_id=N` form: the homepage 301 fires on the bare root regardless of query, so `?page_id=…` bounces to revsport while `/slug/` paths resolve to WP normally. Published pages will live at `/juniors/` etc. and are unaffected by the redirect.
5. **Remaining static pages** — ✅ new players, contact, uniforms built, pushed and **published** 2026-07-07 (block markup in `content/pages/`, uniform images in the media library). 404 template built (v0.3.3) — the static `404.html` was just a legacy-redirect shim; real redirects happen at cutover (step 9).
6. **News → posts** — ⚠ partially done 2026-07-07: `single.html` template built (v0.3.3); the 6 `news.json` articles imported as **draft** posts with categories (Men's/Women's/Juniors/Masters/Club) — they're demo content from the design phase (fake matches, Unsplash images), so they stay drafts; real club news replaces them before cutover. Outstanding: a `/news/` archive page/template (the static `news.html` design), featured images. Note `news.json` has a corrupted tail (duplicate partial document appended) — the importer reads the first valid document.
7. **Fixtures — parked as a possible side project** (Steve, 2026-07-07). Don't just render `fixtures.json`; Steve has existing GCP functions that could make fixtures properly dynamic. Ideas on the table: (a) a table of all teams with links out to each team's Hockey Victoria ladder/fixtures pages, (b) scrape HV and render our own weekend-fixtures table, (c) GCP function feeds a small WP block. Decide approach later — after the history section and the site-wide nav/legacy work.
8. **Content migration** — ✅ history/heritage section done 2026-07-07: all 43 Awards & Records pages (hub + 6 sub-pages + honour-boards hub + 35 boards) pushed and published via `scripts/push_history_pages.py` — verbatim static markup in `wp:html` blocks, links rewritten to WP paths, board photos linked to the existing 2017 media files (no re-upload needed). `club-history.css`/`.js` ported into theme assets (v0.3.3). This covers most of the ROADMAP Phase 2 heritage content. Remaining general imports from `legacy-content/` (markdown versions are import-ready; uploads re-uploaded to the new media library). Note: the heritage content in ROADMAP Phase 2 (premierships, honour boards, life members, club song, team XI histories) already exists here in markdown — that phase is formatting, not research.
9. **QA pass & cutover** — mobile nav, roadmap Phase 0 checklist, redirects for any changed URLs, then activate the new theme on the live site.

Build locally first (`wp-env` or LocalWP), then stage against a copy of the existing site before cutover — the old site stays live and untouched throughout.

## Open items

- [ ] Editor lockdown: how much freedom do club volunteers get in the editor? (Recommend: locked templates, patterns only, no custom colours.)
- [ ] Which legacy uploads are worth carrying to the new media library vs archiving (293MB total — likely prune).
- [ ] Plugin purge plan: 39 installed → target under ~10 (list and housekeeping tasks in [old-site-audit.md](old-site-audit.md)).
- [ ] Events Manager: 7 upcoming events on the old site — decide if the new club calendar (ROADMAP Phase 1) keeps Events Manager or goes simpler.
