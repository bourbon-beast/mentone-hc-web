# Claude Context — mentone-hc-web

Custom WordPress block theme + content sources for the Mentone Hockey Club site.
Live install: https://mentonehockey.org.au (the live install *is* the staging
environment — the homepage `/` sits behind a 301 to revolutioniseSPORT until launch,
inner pages serve publicly).

Why/decisions live in the vault: `Projects/Side Projects/Mentone Website.md`.
What/how lives here: `ROADMAP.md`, `docs/wordpress-migration.md`,
`docs/site-qa-backlog.md`, `docs/PROJECT.md`.

---

## Keep the repo aligned — this is the one that keeps biting

Most work on this site lands **on the live WordPress install** (REST API pushes,
or Steve editing in the block editor), not in the repo. The repo does not update
itself, so it silently drifts behind live unless someone commits.

**Rules:**

1. **Commit and push in the same session the change ships.** Don't leave content
   work sitting uncommitted — a later session will read the stale repo source,
   push it, and clobber whatever's on live. That has already happened once
   (2026-08-04: a stale `content/pages/new-players.html` wiped the Registration
   & fees section that had been live since 8 Jul).
2. **Live WP is master for any page edited in the editor.** Before pushing a page
   from the repo, `GET` it with `context=edit` and diff the raw content against
   the repo source. Only push when the only differences are the ones you intend.
3. **Push to `origin/main`, don't just commit.** Weekly automated
   `chore: update fixtures.json` commits land on origin, so local `main` goes
   behind fast and an unpushed local commit is easy to lose.
4. **Every content change touches two sources**: the static reference at repo root
   (e.g. `uniforms.html`) and the WP block source (`content/pages/uniforms.html`).
   Update both, or note explicitly why not.
5. **Log what shipped** in `docs/site-qa-backlog.md` as part of the same commit.

Working state should be clean at the end of a session. `git status` showing a pile
of modified content files means the repo and live have diverged.

---

## Access

- REST API: application password in `.wp-auth` (gitignored, repo root), basic auth
  against `/wp-json/wp/v2/...`. The host blocks `/users/*` (403 at the server layer);
  everything else works.
- Page-push workflow: author block markup in `content/pages/<slug>.html` →
  `POST /wp-json/wp/v2/pages` with `{"template":"page-patterns","status":"draft",...}`.
  Strip the repo header comment; check slug collisions against pages *and media*
  first (the `/juniors/` attachment lesson).
- Preview at real paths (`/juniors/`, `/womens/`), never `?page_id=N` — the homepage
  301 catches the bare root plus query and bounces to revsport.

## Conventions

- Pattern pages get the **"Pattern page (full-bleed)"** template, never the default
  `page.html` (which constrains `post-content` to 720px and caps every band inside it).
- Inside a band group, never place copy as a direct child of the constrained group —
  wrap it in an `align:wide` inner group, or the layout engine force-centres it.
- Design tokens live once in `theme/mentone/theme.json`. Custom colours/sizes are
  disabled in the editor on purpose so volunteers can't drift off-brand.
