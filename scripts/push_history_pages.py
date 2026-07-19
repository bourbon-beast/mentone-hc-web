"""
Convert the static history/ pages (Awards & Records hub, listing pages, 35
honour boards) to WordPress pages and push them via the REST API.

Usage (from repo root):
    python scripts/push_history_pages.py            # convert only -> content/pages/history/
    python scripts/push_history_pages.py --push     # convert + upload media + create/update pages

Approach: the history section keeps its static markup verbatim inside a single
wp:html block per page (theme v0.3.3+ ships club-history.css/js). Only links
and image sources are rewritten. Pages are created published, nested:
    /history/  (Awards & Records)
      /history/best-and-fairest/ ... etc
      /history/honour-boards/           (generated hub - no static equivalent)
        /history/honour-boards/mens-1st-xi/ ... x35

Auth: reads .wp-auth (gitignored, "user:application-password").
Idempotent: re-running updates existing pages found by slug+parent.
"""
import json, re, sys, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://mentonehockey.org.au/wp-json/wp/v2'
OUT = ROOT / 'content' / 'pages' / 'history'
LEGACY_IMG_DIR = ROOT / 'legacy-content' / 'uploads' / '2017' / '06'

# order controls menu_order under /history/
HUB_PAGES = ['best-and-fairest', 'club-awards', 'life-members',
             'heritage-traditions', 'club-song', '25th-anniversary-team']

HONOUR_BOARDS_HUB = """
<section class="hb-hero"><div class="wrap"><div class="hb-hero-grade"><span class="eyebrow">Awards &amp; Records</span></div><h1>Honour <em>Boards</em></h1><div class="hb-hero-meta"><div class="hb-hero-meta-item"><span class="label">Boards</span><span class="value">35</span></div><div class="hb-hero-meta-item"><span class="label">Records</span><span class="value">All eras</span></div></div></div></section>
<div class="wrap">
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span class="breadcrumb-sep">›</span><a href="/history/">Awards &amp; Records</a><span class="breadcrumb-sep">›</span><span>Honour Boards</span></nav>
<div class="related-links" style="margin:32px 0 64px;">
  <a class="related-link" href="/history/best-and-fairest/"><strong>Best &amp; Fairest</strong> — every team, every season on record</a>
  <a class="related-link" href="/history/club-awards/"><strong>Club Awards</strong> — club person, coaching and special awards</a>
  <a class="related-link" href="/history/life-members/"><strong>Life Members</strong> — the people who built the club</a>
</div>
</div>
"""

class WordPressAPIError(RuntimeError):
    """Raised when a WordPress request cannot be safely applied."""


def api(path, method='GET', payload=None, binary=None, ctype=None, fname=None):
    auth = (ROOT / '.wp-auth').read_text().strip()
    cmd = ['curl', '--silent', '--show-error', '--fail-with-body',
           '-u', auth, '-X', method, BASE + path]
    if payload is not None:
        p = ROOT / '_payload.json'
        p.write_text(json.dumps(payload), encoding='utf-8')
        cmd += ['-H', 'Content-Type: application/json', '--data-binary', '@' + str(p)]
    if binary is not None:
        cmd += ['-H', f'Content-Type: {ctype}',
                '-H', f'Content-Disposition: attachment; filename="{fname}"',
                '--data-binary', '@' + str(binary)]
    result = subprocess.run(cmd, capture_output=True)
    out = result.stdout
    if result.returncode:
        detail = (out or result.stderr)[:300].decode('utf-8', 'replace')
        raise WordPressAPIError(
            f'WordPress API {method} {path} failed '
            f'(curl exit {result.returncode}): {detail}'
        )
    try:
        response = json.loads(out)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        detail = out[:300].decode('utf-8', 'replace')
        raise WordPressAPIError(
            f'WordPress API {method} {path} returned invalid JSON: {detail}'
        ) from exc
    if isinstance(response, dict) and response.get('code') and response.get('message'):
        raise WordPressAPIError(
            f"WordPress API {method} {path} failed "
            f"({response['code']}): {response['message']}"
        )
    return response

def rewrite_href(href, depth):
    """Map static relative links to WP paths. depth 1 = history/, 2 = honour-boards/."""
    if href.startswith(('http', 'mailto', '#')) or href.endswith('.css'):
        return href
    anchor = ''
    if '#' in href:
        href, anchor = href.split('#', 1)
        anchor = '#' + anchor
    up = '../' * depth
    if href in (up + 'index.html', up):
        return '/' + anchor
    m = re.fullmatch(re.escape(up) + r'([\w-]+)\.html', href)
    if m:
        return f'/{m.group(1)}/' + anchor
    if depth == 2:
        if href in ('../', '../index.html'):
            return '/history/' + anchor
        m = re.fullmatch(r'\.\./([\w-]+)\.html', href)
        if m:
            return f'/history/{m.group(1)}/' + anchor
        m = re.fullmatch(r'([\w-]+)\.html', href)
        if m:
            return f'/history/honour-boards/{m.group(1)}/' + anchor
    else:
        if href == 'index.html':
            return '/history/' + anchor
        m = re.fullmatch(r'honour-boards/([\w-]+)\.html', href)
        if m:
            return f'/history/honour-boards/{m.group(1)}/' + anchor
        m = re.fullmatch(r'([\w-]+)\.html', href)
        if m:
            return f'/history/{m.group(1)}/' + anchor
    print(f'  ! unmapped href (kept as-is): {href}')
    return href + anchor

def convert(path, depth):
    h = path.read_text(encoding='utf-8')
    title = re.search(r'<title>(.*?)\s+[—–]\s+Mentone', h).group(1)
    title = title.replace('&amp;', '&')
    body = h[h.index('<div id="site-nav"></div>') + len('<div id="site-nav"></div>'):]
    for marker in ('<div id="site-cta">', '<div id="site-footer">'):
        if marker in body:
            body = body[:body.index(marker)]
    # the filter script ships in the theme (assets/club-history.js)
    body = re.sub(r'<script>.*?</script>\s*', '', body, flags=re.S)
    body = re.sub(r'href="([^"]+)"', lambda m: f'href="{rewrite_href(m.group(1), depth)}"', body)
    # legacy upload images -> media placeholders, resolved at push time
    body = re.sub(r'src="(?:\.\./)+legacy-content/uploads/2017/06/([^"]+)"',
                  lambda m: 'src="{{MEDIA:' + m.group(1) + '}}"', body)
    return title, '<!-- wp:html -->\n' + body.strip() + '\n<!-- /wp:html -->'

def find_page(slug, parent):
    r = api(f'/pages?slug={slug}&status=publish,draft,pending,private&context=edit&per_page=100')
    if not isinstance(r, list):
        raise WordPressAPIError(
            f'WordPress page lookup for {slug!r} returned {type(r).__name__}, not a list'
        )
    for p in r:
        if p.get('parent') == parent:
            return p
    return None

def upsert(slug, parent, title, content, order):
    payload = {'title': title, 'slug': slug, 'status': 'publish', 'parent': parent,
               'template': 'page-patterns', 'menu_order': order, 'content': content}
    existing = find_page(slug, parent)
    r = api(f"/pages/{existing['id']}" if existing else '/pages', 'POST', payload)
    verb = 'updated' if existing else 'created'
    if (not isinstance(r, dict) or not isinstance(r.get('id'), int) or
            r.get('slug') != slug or r.get('status') != 'publish'):
        raise WordPressAPIError(
            f'WordPress page {verb} failed validation for {slug!r}: {str(r)[:300]}'
        )
    print(f"  {verb} {r['id']} {r.get('link')}")
    return r['id']


def resolve_parent_id(ids, parent_key):
    if parent_key is None:
        return 0
    parent = ids.get(parent_key)
    if not isinstance(parent, int) or parent <= 0:
        raise WordPressAPIError(
            f'Cannot publish child page: parent {parent_key!r} was not published'
        )
    return parent

def main():
    push = '--push' in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    pages = []  # (slug, parent_key, title, content, order)

    t, c = convert(ROOT / 'history' / 'index.html', 1)
    pages.append(('history', None, t, c, 0))
    for i, slug in enumerate(HUB_PAGES):
        t, c = convert(ROOT / 'history' / f'{slug}.html', 1)
        pages.append((slug, 'history', t, c, i + 1))
    pages.append(('honour-boards', 'history', 'Honour Boards',
                  '<!-- wp:html -->\n' + HONOUR_BOARDS_HUB.strip() + '\n<!-- /wp:html -->',
                  len(HUB_PAGES) + 1))
    for i, f in enumerate(sorted((ROOT / 'history' / 'honour-boards').glob('*.html'))):
        t, c = convert(f, 2)
        pages.append((f.stem, 'honour-boards', t, c, i))

    media_files = sorted({m for _, _, _, c, _ in pages for m in re.findall(r'\{\{MEDIA:([^}]+)\}\}', c)})
    print(f'{len(pages)} pages, {len(media_files)} legacy images')

    for slug, parent, title, content, _ in pages:
        (OUT / f'{slug}.html').write_text(f'<!-- {title} (parent: {parent}) -->\n' + content, encoding='utf-8')
    print('converted markup written to', OUT)

    if not push:
        return

    # media: find-or-upload each legacy board photo
    url_map = {}
    for f in media_files:
        wp_slug = re.sub(r'-+$', '', pathlib.Path(f).stem.lower().replace(' ', '-'))
        r = api(f'/media?slug={wp_slug}')
        if not isinstance(r, list):
            raise WordPressAPIError(
                f'WordPress media lookup for {f!r} returned {type(r).__name__}, not a list'
            )
        if r:
            url_map[f] = r[0]['source_url']
            print('  media exists', f)
        else:
            r = api('/media', 'POST', binary=LEGACY_IMG_DIR / f, ctype='image/png', fname=f)
            if 'source_url' not in r:
                sys.exit(f'media upload failed for {f}: {str(r)[:200]}')
            url_map[f] = r['source_url']
            print('  uploaded', f)

    ids = {}
    for slug, parent_key, title, content, order in pages:
        content = re.sub(r'\{\{MEDIA:([^}]+)\}\}', lambda m: url_map[m.group(1)], content)
        parent = resolve_parent_id(ids, parent_key)
        ids[slug] = upsert(slug, parent, title, content, order)

if __name__ == '__main__':
    main()
