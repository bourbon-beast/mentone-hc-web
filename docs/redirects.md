# Redirect map — old site → new site

Source of truth for the `.htaccess` redirect block. Edit the tables, then run:

```bash
python scripts/build_redirects.py      # writes export/htaccess-redirects.txt
python scripts/check_redirects.py      # curls every row, expects 301 → destination → 200
```

Paste `export/htaccess-redirects.txt` into `public_html/.htaccess` (cPanel File Manager) **above** the `# BEGIN WordPress` block, replacing any previous `# BEGIN Mentone redirects` block. `.htaccess` rules fire before WordPress, so these override WP's own old-slug guesses (which currently send `/mens-masters/` to an honour board).

**Rules for adding rows**
- Closest real page, never the homepage by default. Homepage only when the old page genuinely has no better home.
- Destination must be a published page — `check_redirects.py` fails the row otherwise.
- Old paths come from `legacy-content/_all_pages.json` (full parent paths) plus URLs seen in Google results. The builder also emits the **flat-slug variant** of every nested path (e.g. `/contacts/` as well as `/administration/contacts/`), because the old site resolved both and both are indexed — unless the flat slug is a live page.
- Match is case-insensitive (Google has `/Mens-Masters/` capitalised).

**Don't map `/login/`** — the old site had a page there, but WordPress core uses `/login/` as its shortcut to `wp-login.php`. Redirecting it would lock volunteers out of their muscle-memory login URL.

**Baseline 2026-09-24 (before the block is pasted):** 58 rows already pass via WordPress's own old-slug redirects (mostly `/club-history/*`), 85 return 404, and WP mis-routes `/mens-masters/`, `/womens-masters/` (→ 1st XI honour boards) and `/home/` (→ `/home-preview/`). The two PDFs still serve.

Status: **live-ready now** except rows marked *cutover* — those go in only when the `/` → revsport 301 comes off.

---

## Sections & joining

| Old path | New path | Why |
|---|---|---|
| /junior-section/ | /juniors/ | section page |
| /mentone-junior-development-programs/ | /juniors/ | junior programs live on /juniors/ |
| /hookin2hockey/ | /juniors/ | intro programs + clinics on /juniors/ |
| /mens-section/ | /mens/ | section page |
| /mens-section/mens-player-profiles/ | /mens/ | no profiles on new site |
| /womens-section/ | /womens/ | section page |
| /womens-section/womens-player-profiles/ | /womens/ | no profiles on new site |
| /mens-masters/ | /masters/ | WP was guessing an honour board — wrong |
| /womens-masters/ | /masters/ | as above |
| /sections/ | /new-players/ | old hub of all sections; new-players routes to each |
| /training-times/ | /new-players/ | training overview; times per section page |
| /new-to-the-club/ | /new-players/ | direct replacement |
| /membership-join/ | /new-players/ | direct replacement |
| /membership-join/membership-registration/ | /new-players/ | registration section |
| /registration/ | /new-players/ | registration section |
| /2023-player-registration/ | /new-players/ | registration section |
| /administration/registration-membership-fees/ | /new-players/ | fees now on /new-players/ |
| /administration/registration-membership-fees-2/ | /new-players/ | as above |
| /administration/registration-membership-fees-2021/ | /new-players/ | as above |

## Governance & contacts

| Old path | New path | Why |
|---|---|---|
| /administration/ | /resources/ | old admin hub |
| /administration/club-policies/ | /resources/ | policies — **needs club policies added to /resources/ (Phase 1)** |
| /administration/archived-club-policies/ | /resources/ | as above |
| /administration/injury-and-insurance/ | /resources/ | HA/HV insurance links |
| /member-protection/ | /resources/ | HA integrity & policies link |
| /administration/injury-insurance-and-member-protection-information-officer-contacts/ | /contact/ | contacts |
| /administration/contacts/ | /contact/ | direct replacement |
| /administration/committee-roles-responsibilities/ | /contact/ | committee listing |
| /administration/mhc-annual-report/ | /resources/ | governance docs |
| /administration/strategic-plan/ | /resources/ | governance docs |
| /facility-hire/ | /contact/ | enquiries |

## Sponsorship

| Old path | New path | Why |
|---|---|---|
| /administration/sponsors-2019/ | / | sponsor band is on the homepage (no sponsors page yet) |
| /are-you-interested-in-sponsoring-mentone-hockey-club/ | /contact/ | sponsorship enquiries |
| /interested-in-sponsoring-mentone-hockey-club/ | /contact/ | as above |

## History & honour boards

| Old path | New path | Why |
|---|---|---|
| /club-history/ | /history/ | hub |
| /premierships/ | /history/ | never filled in on old site |
| /club-history/25th-anniversary-team/ | /history/25th-anniversary-team/ | |
| /club-history/club-song/ | /history/club-song/ | |
| /club-history/honour-board/ | /history/honour-boards/ | |
| /club-history/honour-board/life-members/ | /history/life-members/ | |
| /club-history/honour-board/ap-dayton-clubman-award/ | /history/honour-boards/dayton-clubman-award/ | slug renamed |
| /club-history/honour-board/coach-of-the-year/ | /history/honour-boards/coach-of-year/ | slug renamed |
| /club-history/honour-board/coordinators/ | /history/honour-boards/coordinators/ | |
| /club-history/honour-board/executive-committee/ | /history/honour-boards/executive/ | slug renamed |
| /club-history/honour-board/j-burt-junior-club-person-award/ | /history/honour-boards/burt-junior-club-person-award/ | slug renamed |
| /club-history/honour-board/s-holliday-club-woman-award/ | /history/honour-boards/holliday-club-woman-award/ | slug renamed |
| /club-history/honour-board/the-presidents-cup/ | /history/honour-boards/presidents-cup/ | slug renamed |
| /club-history/mens-senior-coach/ | /history/honour-boards/mens-coaching/ | slug renamed |
| /club-history/womens-senior-coach-and-manager/ | /history/honour-boards/womens-coaching/ | slug renamed |
| /club-history/mens-best-1st-year-player/ | /history/honour-boards/mens-best-1st-year/ | slug renamed |
| /club-history/womens-best-1st-year-player/ | /history/honour-boards/womens-best-1st-year/ | slug renamed |
| /club-history/mens-most-improved/ | /history/honour-boards/mens-most-improved/ | |
| /club-history/womens-most-improved/ | /history/honour-boards/womens-most-improved/ | |
| /club-history/mens-sharpshooter/ | /history/honour-boards/mens-sharpshooter/ | |
| /club-history/womens-sharpshooter/ | /history/honour-boards/womens-sharpshooter/ | |
| /club-history/mens-1st-xi/ | /history/honour-boards/mens-1st-xi/ | |
| /club-history/mens-2nd-xi/ | /history/honour-boards/mens-2nd-xi/ | |
| /club-history/mens-3rd-xi/ | /history/honour-boards/mens-3rd-xi/ | |
| /club-history/mens-4th-xi/ | /history/honour-boards/mens-4th-xi/ | |
| /club-history/mens-5th-xi/ | /history/honour-boards/mens-5th-xi/ | |
| /club-history/mens-6th-xi/ | /history/honour-boards/mens-6th-xi/ | |
| /club-history/mens-7th-xi/ | /history/honour-boards/mens-7th-xi/ | |
| /club-history/mens-masters-1st-xi/ | /history/honour-boards/mens-masters-1st-xi/ | |
| /club-history/mens-masters-2nd-xi/ | /history/honour-boards/mens-masters-2nd-xi/ | |
| /club-history/mens-masters-3rd-xi/ | /history/honour-boards/mens-masters-3rd-xi/ | |
| /club-history/mens-masters-4th-xi/ | /history/honour-boards/mens-masters-4th-xi/ | |
| /club-history/womens-1st-xi/ | /history/honour-boards/womens-1st-xi/ | |
| /club-history/womens-2nd-xi/ | /history/honour-boards/womens-2nd-xi/ | |
| /club-history/womens-3rd-xi/ | /history/honour-boards/womens-3rd-xi/ | |
| /club-history/womens-4th-xi/ | /history/honour-boards/womens-4th-xi/ | |
| /club-history/womens-5th-xi/ | /history/honour-boards/womens-5th-xi/ | |
| /club-history/womens-6th-xi/ | /history/honour-boards/womens-6th-xi/ | |
| /club-history/womens-masters-1st-xi/ | /history/honour-boards/womens-masters-1st-xi/ | |
| /club-history/womens-masters-2nd-xi/ | /history/honour-boards/womens-masters-2nd-xi/ | |
| /club-history/womens-masters-3rd-xi/ | /history/honour-boards/womens-masters-3rd-xi/ | |

## News, media, events

| Old path | New path | Why |
|---|---|---|
| /home/mentone-in-the-news-2017/ | /news/ | |
| /mentone-media-2018/ | /news/ | |
| /hockey-photo-albums/ | /news/ | no gallery page yet — repoint to /gallery/ when built |
| /hockey-photo-albums-juniors/ | /news/ | as above |
| /videos-and-slideshows/ | /news/ | as above |
| /mhc-golf-club/ | /news/ | social club item |
| /calendar/ | /news/ | events now run through Majestri |
| /club-calendar/ | /news/ | as above |
| /mhc-club-calendar/ | /news/ | as above |
| /events/ | /news/ | Events Manager removed 2026-07-06 |

## Prefix rules (whole families)

| Old path prefix | New path | Why |
|---|---|---|
| /events/ | /news/ | Events Manager sub-pages (categories, locations, bookings, individual events) |
| /locations/ | /contact/ | Events Manager venue pages — ground details on /contact/ |
| /home-and-away-mentone-v- | /news/ | 2017–18 match-report pages |
| /mentone-v- | /news/ | 2018 finals match-report pages |
| /membership-login/ | / | Simple Membership removed — no member login any more |

## Leftover utility pages

| Old path | New path | Why |
|---|---|---|
| /home/ | / | old front page |
| /new-home/ | / | old draft front page |
| /thank-you/ | / | old form confirmation |

## Documents

Outdated guidance that could pass for current. Everything else in the 2017–2021 uploads is a Phase 5 prune job (see note below).

| Old path | New path | Why |
|---|---|---|
| /wp-content/uploads/2021/04/Mentone-Hockey-Club-Juniors-Information-Feb-2021.pdf | /juniors/ | 2021 fees/info pack |
| /wp-content/uploads/2017/02/MHC-Players-wanted-2017.pdf | /new-players/ | 2017 recruitment flyer |

## Cutover only

| Old path | New path | Why |
|---|---|---|
| /home-preview/ | / | review copy of the homepage (page 5211) — delete the page and add this row at cutover |

---

**Phase 5 note — old uploads:** the media library still serves ~900 legacy files, including 2017–18 **team selection sheets** (`/wp-content/uploads/2017/02/Round-*-selection*.pdf`, `2018-MHC-Womens-*`), which likely list junior and senior players by name. They're not linked from anywhere but are publicly fetchable and some are indexed. Candidate for deletion (after the media-library prune review), not redirection.
