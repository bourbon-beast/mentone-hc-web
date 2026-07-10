# Old Site Audit — mentonehockey.org.au

Captured 2026-07-06 from the live WP admin (Site Health, Themes, Plugins screens). This is migration step 0.

## Environment — ✅ ready for the new block theme

| Item | Value | Verdict |
|---|---|---|
| WordPress | 7.0 | Current — full block theme (FSE) support |
| PHP | 8.5.6 | Modern, no upgrade needed |
| Web server | LiteSpeed on Linux (CloudLinux/cPanel-style shared hosting) | Fine for a club site |
| Database | MariaDB 11.4, db `mentoneh_wpprod` (matches the `mentoneh_wpprod_sql.gz` dump behind `legacy-content/`) | Healthy |
| Limits | 256M PHP memory, 128M uploads, opcache on | Generous |
| HTTPS | Yes; permalinks `/%postname%/` | Keep same permalink structure for redirect-free cutover |
| Users | 3 admin-side users | Review before launch |
| Site Health | "Should be improved" — 3 critical issues + 17 plugin updates pending | Triage below |

### Site Health issues (checked 2026-07-06)

**Critical:**
1. **PHP `gd` module missing (required), plus imagick, zip, fileinfo, intl (optional) all missing/disabled.** With neither GD nor Imagick, WordPress cannot generate thumbnails or resized images — uploads exist only at original size, galleries degrade, pages serve full-size photos. Missing `zip` can also break plugin/theme installs from upload. Likely cause: host bumped PHP to 8.5 and the extension set didn't carry over. **Fix: cPanel → "Select PHP Version" / PHP Extensions → enable `gd`, `imagick`, `zip`, `fileinfo`, `intl`** (2-minute job if cPanel access exists; otherwise a support ticket to the host). Must be fixed before the new site — the design leans on photography.
2. An active PHP session detected — some plugin calls `session_start()` (suspects: Simple Membership, Tiqbiz). Performance issue; likely resolves itself in the plugin purge.
3. Jetpack's WordPress.com connection is broken — reconnect, or more likely just remove Jetpack in the purge.

**Recommended:** remove inactive plugins (13); keep a default theme installed as fallback (none present — our new theme install helps, but add Twenty Twenty-Five too); a scheduled cron event is late; no persistent object cache (fine at this scale).

**Conclusion:** no new hosting needed. Build the theme locally, then install it on this WP as a second theme, build out pages, and switch themes when ready. UpdraftPlus is already installed for pre-change backups.

## Themes installed

- **Hello Elementor** — ACTIVE (update pending). Note: Elementor itself is *not* installed, so the active theme is essentially a blank canvas.
- **btw** — inactive (likely the older custom theme; Gantry 4 framework plugin suggests a RocketTheme era)
- **OceanWP** — inactive

## Plugins — ✅ PURGED 2026-07-06: 39 → 5

Now installed (all active): **UpdraftPlus, WPForms Lite, PDF Embedder, Akismet, Advanced Google reCAPTCHA**. Fresh backup taken first (local set complete; Google Drive upload was retrying — verify it landed). Events Manager deleted — **events will be fed from Majestri** (club money/events system), not WordPress.

Historical record of what was there and why, kept for reference:

### Pre-purge state: 39 installed (26 active, 13 inactive), 17 updates pending

**Likely load-bearing (assess before removing):**
- Events Manager 7.2 (7 events badge — active use; club calendar candidate for the new site)
- WPForms Lite (contact forms)
- PDF Embedder (policy docs — relevant to Phase 2 governance pages)
- UpdraftPlus (backups — keep)
- Akismet, Advanced Google reCAPTCHA (spam protection)
- Simple Membership + Page Restrict (members-only content — check what's restricted)
- Logo Carousel (sponsors display)
- Media Library Folders, Enable Media Replace (media management)
- Jetpack, Activity Log, Site Kit (Site Kit never completed setup)

**Cruft / candidates to delete (mostly inactive or redundant):**
- Display Widgets (abandoned; infamous supply-chain history — remove)
- WP MySQLi, Gantry 4, AMP for WP, Black Studio TinyMCE Widget (legacy era)
- 4× overlapping gallery/Instagram plugins (Photonic, MaxGalleria, Social Feed Gallery, Enjoy Instagram, Google Photos Albums Gallery)
- 2nd reCAPTCHA plugin (reCaptcha by BestWebSoft, inactive)
- Tiqbiz API (defunct service), WP FullCalendar, Recent Posts widgets ×2, Easy Custom Sidebars, Import/export users, MonsterInsights (inactive), Yoast Duplicate Post, MaxButtons, Simple Like Page, Photonic

**Target for the new site:** under ~10 plugins. The block theme replaces MaxButtons, sidebar/widget plugins, and gallery plugins natively.

## Immediate housekeeping (worth doing now, independent of migration)

- [x] Plugin purge 39 → 5 (done 2026-07-06; Steve running updates on the remaining 5)
- [x] Backups confirmed running (scheduled fortnightly to Google Drive; fresh set taken 2026-07-06 pre-purge)
- [ ] Verify the 2026-07-06 backup finished uploading to Google Drive (upload was in auto-retry when last checked)
- [ ] Fix PHP extensions in cPanel: enable `gd`, `imagick`, `zip`, `fileinfo`, `intl` (blocks image handling on the new site)
- [ ] Disk (13.44/15GB used): **email accounts are 12.5GB** — 22 role mailboxes (president 1.76GB, archive 1.7GB, treasurer 1.6GB, juniors 1.13GB, secretary 1.05GB, …) almost certainly forward-to-Gmail with local copies accumulating. ⚠️ Club email runs on this hosting account — cutover must never touch the mail side.
  - **Agreed plan (2026-07-06, pending confirmation with the club's email admin):** verify each address's forwarder + destination is current; confirm nobody reads these boxes directly (webmail/IMAP); then delete each role *mailbox* keeping its *forwarder* (address keeps working, frees ~10GB, stops re-accumulation). Keep `archive@` as a real mailbox — optionally add archive@ as a second destination on every forwarder so it becomes the single club-wide mail record.
- [ ] Prune old UpdraftPlus sets (2.6GB in `public_html/wp-content/updraft`) once the 2026-07-06 set confirms in Google Drive; `tmp/` has 418MB clearable
- [ ] Delete unused themes (btw, OceanWP) when the new theme goes on; keep one default WP theme as fallback
- [ ] Review the 3 user accounts
- [ ] Investigate the redirects making the site invisible on the web (fine while rebuilding; must be resolved at cutover)

## Cutover implications

- Same install, same domain → no DNS/hosting work at all
- Old permalink structure `/%postname%/` matches slug-style URLs in `legacy-content/INDEX.md` → redirect map only needed for pages whose slugs change in the new IA
- Events Manager data (7 upcoming events) and any WPForms entries should be checked before plugin removal
