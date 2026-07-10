# Mentone WordPress theme

`mentone/` is the custom block theme — the WordPress translation of the static design in this repo.

## Where the design lives

| What | File | Change it to… |
|---|---|---|
| Colours, fonts, sizes, spacing | `mentone/theme.json` | restyle the entire site in one place |
| Hover effects, underlines, hero stripes | `mentone/style.css` | behaviours theme.json can't express |
| Header / footer | `mentone/parts/` | edit site chrome |
| Page layouts | `mentone/templates/` | change page structure |
| Reusable sections (CTA bands etc.) | `mentone/patterns/` | add building blocks for new pages |

Fonts (Fraunces + Inter) load from Google Fonts for now — see `functions.php`. Self-host under `mentone/assets/fonts/` before launch if we want zero external dependencies.

## Installing / updating on the site

1. Zip the theme folder: `Compress-Archive -Path theme/mentone -DestinationPath mentone-theme.zip -Force` (or right-click → compress; the zip must contain the `mentone/` folder at its root)
2. wp-admin → Appearance → Themes → Add Theme → Upload Theme → choose the zip
3. Re-uploading the same version needs the old theme deleted first, or bump `Version:` in `style.css` and WP offers "replace current with uploaded"
4. **Preview before activating:** Appearance → Themes → Live Preview

## Editing philosophy

- Tokens in `theme.json`, never hard-coded in templates or patterns
- Custom colours/font-sizes are disabled in the editor on purpose — volunteers pick from the palette, the design stays coherent
- New page sections = new patterns, not one-off layouts
