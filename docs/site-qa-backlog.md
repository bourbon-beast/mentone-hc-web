# Site QA Backlog

Running list of fixes found while walking the live install (theme v0.3.0). Newest issues at the top of each section; tick as done.

> Note: the Chrome extension used to build this can only reach **wp-admin**, not the public front-end, so visual issues are captured from Steve's browsing + structural checks via the REST API. Preview/verify at the real paths (`/juniors/`, `/womens/`, `/mens/`, `/masters/`) — never `?page_id=N` (the homepage 301 catches the bare root + query and bounces to revsport).

## Section pages (Juniors / Women's / Men's / Masters) — published 2026-07-06

### Open
- [ ] **History pages: Steve review pass** — 43 pages under `/history/` (hub, 6 sub-pages, honour-boards hub + 35 boards). Converted verbatim from the static build (single `wp:html` block each — deliberate: historical records, not volunteer-editable content; conversion script `scripts/push_history_pages.py`, idempotent, safe to re-run after edits to the static sources).
- [ ] **Mobile pass on-device.** Verified at 375px in a desktop-browser simulation (grids stack to 1 col, no horizontal overflow, hero type clamps; clash table scrolls horizontally — improvement over the static site which clipped it) — still worth a quick real-phone check.

### Done
- [x] **Section pages fixed on live + reviewed by Steve** (2026-07-07): all four switched to "Pattern page (full-bleed)", render full-width correctly.
- [x] **New Players / Contact / Uniforms published** (2026-07-07): ids 5035–5037, reviewed by Steve, live at `/new-players/` `/contact/` `/uniforms/`. 13 uniform PNGs in the media library.
- [x] **Grids squished to centre on desktop — root-caused and fixed in theme v0.3.1.** (2026-07-06) The earlier `wp:html`/align:wide hypothesis was wrong — the grid markup was fine. Actual cause, confirmed by downloading the live pages and rendering them locally: `page.html` wraps `post-content` in a **constrained group**, so post-content itself (and therefore every full-bleed band inside it) was capped at `contentSize` 720px. The home page never hit this because `front-page.html` drops patterns straight into the template. Fix in v0.3.1:
    - New **`templates/page-patterns.html`** ("Pattern page (full-bleed)"): header + free-flowing `post-content` (blockGap 0) + footer — no constrained wrapper, no `post-title` (which was also rendering a duplicate H1 above the pattern hero), no 20px cream gaps between bands.
    - `section-hero` / `page-hero` patterns: copy now wrapped in an inner `wp:group {"align":"wide"}` so the lead isn't auto-centred by the layout engine; `.hero > .lead` CSS guard keeps the four already-published heroes aligned without content edits.
    - `.section-head` text capped at 760px again (the layout engine was overriding the old max-width on the group itself).

    **Convention for all pattern pages moving forward:** assign the **"Pattern page (full-bleed)" template** (never the default `page.html`, which is for plain prose pages); inside a band group, never place copy as a direct child of the constrained group — wrap it in an `align:wide` inner group (the layout engine force-centres any narrower direct child with `margin:auto !important`).
- [x] **Juniors showed old content.** `/juniors/` was resolving to attachment media #334 (slug `juniors`), which had forced the new page to slug `juniors-2`. Renamed the attachment slug to `juniors-image-334`, set the page slug to `juniors`, published. (2026-07-06)

## Working notes
- **REST API access works** (2026-07-07): application password in `.wp-auth` (gitignored, repo root), user `uUhW97t1Os`. Basic auth via curl against `/wp-json/wp/v2/...`. Host blocks the `/users/*` endpoints (403 HTML at the server layer) — everything else fine. This replaces driving wp-admin through Chrome for content work: pages, media, template assignment all done via API.
- **Page-push workflow:** author block markup in `content/pages/<slug>.html` → `POST /wp-json/wp/v2/pages` with `{"template":"page-patterns","status":"draft",...}` — strip the repo header comment, check slug collisions against pages *and* media first (the `/juniors/` attachment lesson).

## Whole-site scan — TODO
- [ ] **Steve: upload theme v0.3.5** (supersedes the earlier v0.3.5 note — zip now also carries the fees-table styling for `/new-players/#registration`, the footer Resources link, and the home This-Week training card fix). Until it lands the fee table renders unstyled-but-readable.
- [ ] **Waiting on Steve (⚑ list):** 2026 season start/end + holiday-break dates (key-dates strip is stubbed with rego + H2H only); premiership records (page skipped — no data); resources link-set review (prune/extend `/resources/`); decision: point site-wide Register buttons at Majestri instead of revolutionise?
- [ ] **Re-survey members after launch** — the July feedback CSV predates the rebuild.
- [ ] Walk every published page under the new theme and log issues here.
- [ ] Iterate nav/footer from feedback once the first working model is being shown around.
- [ ] Add **Fixtures** to nav + footer ("Fixtures & Results") and **Sponsors** to footer when those pages exist — left out for now to avoid dead links.

### Done (site-wide pass, 2026-07-07)
- [x] **2026 training times live** on all four section pages (Training block in each "Get in touch" card is the **source of truth**; home This-Week card and contact-page ground card carry one-liners only — update all three places if times change). Men's Tue 7:00–8:20 all grades / Thu 8:30–10:00 PL+PLR; Women's the reverse; junior boys Tue 5pm & 6pm, girls Thu 5pm & 6pm; U18 mixed trains in the Tuesday 6pm slot; Masters no set session. All blocks carry the "arrive 15 minutes early, warm-up off the pitch" note. Home card fix ships in **v0.3.5** (also swaps the dead "See training schedule" link for /new-players/).
- [x] **Header nav rebuilt** (nav menu post 4849 via REST): Men's / Women's / Juniors / Masters / New Players / News / Awards & Records / Contact — copied from the static site nav, minus Fixtures (parked).
- [x] **News posts page** created (id 5091) and set as `page_for_posts` → `/news/` lists posts.
- [x] **113 legacy pages drafted** (reversible; all content archived in `legacy-content/`). Kept: our 51 new pages + the front page (id 4894, carries the revsport redirect).
- [x] **Est. 1926 → Est. 1976** fixed in header/footer parts (static site + honour-board records both say 1976; the 1926 was a typo from the first theme build).
