"""
Mentone Hockey Club — Club History page generator
Run from the project root:  python generate_history_pages.py

Reads legacy markdown files and generates Club History HTML pages:
  - history/honour-boards/*.html  (one per grade / award)
  - history/25th-anniversary-team.html
  - history/club-song.html
  - root redirect stubs for old URLs

Also patches index.html to add a Club History nav link.

Requirements: pip install markdown2 beautifulsoup4
"""

import os
import re
import sys
import json
from html import escape
from pathlib import Path

try:
    import markdown2
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install markdown2 beautifulsoup4 -q")
    import markdown2
    from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.resolve()
LEGACY = ROOT / "legacy-content" / "markdown"
OUT = ROOT
HISTORY_DIR = ROOT / "history"
HONOUR_BOARD_DIR = HISTORY_DIR / "honour-boards"
UPLOADS = "legacy-content/uploads"

ROOT_ASSET_PREFIX = ""
HISTORY_ASSET_PREFIX = "../"
HONOUR_ASSET_PREFIX = "../../"

ARROW_ICON = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7h8M7 3l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def honour_page_name(slug):
    """Strip the old root prefix for cleaner nested honour-board URLs."""
    return slug.removeprefix("honour-board-") + ".html"


def honour_page_href(slug):
    return f"history/honour-boards/{honour_page_name(slug)}"



# ─────────────────────────────────────────────────────────────────
# Page configs
# ─────────────────────────────────────────────────────────────────

# (file_id, slug, section, grade_num, label, image_filename, related_slugs)
GRADE_PAGES = [
    # Men's senior
    ("2604", "honour-board-mens-1st-xi",     "mens",       "1st XI",   "Men's 1st XI",
     "Honour-Board-Mens-First-XI-.png",
     ["2nd","3rd","4th","5th","6th","7th"]),
    ("2610", "honour-board-mens-2nd-xi",     "mens",       "2nd XI",   "Men's 2nd XI",
     "Honour-Board-Mens-Second-XI-.png",
     ["1st","3rd","4th","5th","6th","7th"]),
    ("2619", "honour-board-mens-3rd-xi",     "mens",       "3rd XI",   "Men's 3rd XI",
     None,
     ["1st","2nd","4th","5th","6th","7th"]),
    ("2625", "honour-board-mens-4th-xi",     "mens",       "4th XI",   "Men's 4th XI",
     "Honour-Board-Mens-Fourth-XI-.png",
     ["1st","2nd","3rd","5th","6th","7th"]),
    ("2629", "honour-board-mens-5th-xi",     "mens",       "5th XI",   "Men's 5th XI",
     "Honour-Board-Mens-Fifth-XI-.png",
     ["1st","2nd","3rd","4th","6th","7th"]),
    ("2633", "honour-board-mens-6th-xi",     "mens",       "6th XI",   "Men's 6th XI",
     "Honour-Board-Mens-Sixth-XI-.png",
     ["1st","2nd","3rd","4th","5th","7th"]),
    ("2637", "honour-board-mens-7th-xi",     "mens",       "7th XI",   "Men's 7th XI",
     "Honour-Board-Mens-Seventh-XI-.png",
     ["1st","2nd","3rd","4th","5th","6th"]),
    # Men's awards
    ("2641", "honour-board-mens-sharpshooter",   "mens-awards", "Sharpshooter",    "Men's Sharpshooter",
     "Honour-Board-Mens-Sharpshooter-.png", []),
    ("2645", "honour-board-mens-most-improved",  "mens-awards", "Most Improved",   "Men's Most Improved",
     "Honour-Board-Mens-Most-Improved-.png", []),
    ("2356", "honour-board-mens-best-1st-year",  "mens-awards", "Best 1st Year",   "Men's Best 1st Year Player",
     None, []),
    # Women's senior
    ("2663", "honour-board-womens-1st-xi",   "womens",     "1st XI",   "Women's 1st XI",
     "Honour-Board-Womens-First-XI-.png",
     ["2nd","3rd","4th","5th","6th"]),
    ("2668", "honour-board-womens-2nd-xi",   "womens",     "2nd XI",   "Women's 2nd XI",
     "Honour-Board-Womens-Second-XI-.png",
     ["1st","3rd","4th","5th","6th"]),
    ("2672", "honour-board-womens-3rd-xi",   "womens",     "3rd XI",   "Women's 3rd XI",
     "Honour-Board-Womens-Third-XI-.png",
     ["1st","2nd","4th","5th","6th"]),
    ("2679", "honour-board-womens-4th-xi",   "womens",     "4th XI",   "Women's 4th XI",
     "Honour-Board-Womens-Fourth-XI-.png",
     ["1st","2nd","3rd","5th","6th"]),
    ("2685", "honour-board-womens-5th-xi",   "womens",     "5th XI",   "Women's 5th XI",
     "Honour-Board-Womens-Fifth-XI-.png",
     ["1st","2nd","3rd","4th","6th"]),
    ("2689", "honour-board-womens-6th-xi",   "womens",     "6th XI",   "Women's 6th XI",
     "Honour-Board-Womens-Sixth-XI-.png",
     ["1st","2nd","3rd","4th","5th"]),
    # Women's awards
    ("2660", "honour-board-womens-sharpshooter",  "womens-awards", "Sharpshooter",  "Women's Sharpshooter",
     "Honour-Board-Womens-Shrpshooter-.png", []),
    ("2649", "honour-board-womens-most-improved", "womens-awards", "Most Improved", "Women's Most Improved",
     "Honour-Board-Womens-Most-Improved-.png", []),
    ("2654", "honour-board-womens-best-1st-year", "womens-awards", "Best 1st Year", "Women's Best 1st Year Player",
     "Honour-Board-Womens-Best-First-year-.png", []),
    # Men's Masters
    ("2694", "honour-board-mens-masters-1st-xi", "mens-masters", "1st XI", "Men's Masters 1st XI",
     "Honour-Board-Mens-Masters-1st-XI-.png",
     ["2nd","3rd","4th"]),
    ("2699", "honour-board-mens-masters-2nd-xi", "mens-masters", "2nd XI", "Men's Masters 2nd XI",
     "Honour-Board-Mens-Masters-2nd-XI-.png",
     ["1st","3rd","4th"]),
    ("2704", "honour-board-mens-masters-3rd-xi", "mens-masters", "3rd XI", "Men's Masters 3rd XI",
     "Honour-Board-Mens-Masters3rd-XI-.png",
     ["1st","2nd","4th"]),
    ("2707", "honour-board-mens-masters-4th-xi", "mens-masters", "4th XI", "Men's Masters 4th XI",
     "Honour-Board-Mens-Masters-4th-XI-.png",
     ["1st","2nd","3rd"]),
    # Women's Masters
    ("2712", "honour-board-womens-masters-1st-xi", "womens-masters", "1st XI", "Women's Masters 1st XI",
     "Honour-Board-Womens-Masters-1st-XI-.png",
     ["2nd","3rd"]),
    ("2716", "honour-board-womens-masters-2nd-xi", "womens-masters", "2nd XI", "Women's Masters 2nd XI",
     "Honour-Board-Womens-Masters-2nd-XI-.png",
     ["1st","3rd"]),
    ("2720", "honour-board-womens-masters-3rd-xi", "womens-masters", "3rd XI", "Women's Masters 3rd XI",
     "Honour-Board-Womens-Masters-3rd-XI-.png",
     ["1st","2nd"]),
    # Coaching & Admin
    ("2487", "honour-board-coach-of-year",       "coaching", "Coach of the Year",  "Coach of the Year",
     None, []),
    ("496",  "honour-board-mens-coaching",        "coaching", "Men's Senior Coaches","Men's Senior Coaches",
     None, []),
    ("501",  "honour-board-womens-coaching",      "coaching", "Women's Senior Coaches","Women's Senior Coaches",
     None, []),
    ("2334", "honour-board-executive",            "admin",    "Executive Committee","Executive Committee",
     None, []),
    ("2336", "honour-board-coordinators",         "admin",    "Section Coordinators","Section Coordinators",
     None, []),
]

CLUB_AWARD_PAGES = [
    ("2077", "honour-board-presidents-cup", "President's Cup", "Club Awards",
     "Premier team performance recognised each season."),
    ("2327", "honour-board-dayton-clubman-award", "A.P. Dayton Clubman Award", "Club Awards",
     "Recognising outstanding service and contribution to club culture."),
    ("2329", "honour-board-holliday-club-woman-award", "S. Holliday Club Woman Award", "Club Awards",
     "Celebrating outstanding contribution from women across the club."),
    ("2331", "honour-board-burt-junior-club-person-award", "J. Burt Junior Club Person Award", "Club Awards",
     "Recognising junior community impact and club spirit."),
]


def legacy_redirect_targets():
    targets = {
        "club-history.html": "history/",
        "club-song.html": "history/club-song.html",
        "25th-anniversary-team.html": "history/25th-anniversary-team.html",
    }
    for _, slug, *_ in GRADE_PAGES:
        targets[f"{slug}.html"] = honour_page_href(slug)
    for _, slug, *_ in CLUB_AWARD_PAGES:
        targets[f"{slug}.html"] = honour_page_href(slug)
    return targets


def write_404_redirects():
    redirects = legacy_redirect_targets()
    redirects_json = json.dumps(redirects, indent=2, sort_keys=True)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Page moved — Mentone Hockey Club</title>
<meta name="robots" content="noindex" />
<link rel="stylesheet" href="colors_and_type.css">
<link rel="stylesheet" href="site.css">
</head>
<body>
<section class="section">
  <div class="wrap">
    <h1>Page moved</h1>
    <p id="redirect-message">Checking whether this page has moved.</p>
    <p><a id="redirect-link" href="index.html" class="btn btn-primary">Go to the home page</a></p>
  </div>
</section>
<script>
const legacyRedirects = {redirects_json};
const fileName = window.location.pathname.split('/').pop();
const target = legacyRedirects[fileName];
if (target) {{
  const basePath = window.location.pathname.slice(0, -fileName.length);
  const destination = basePath + target + window.location.hash;
  document.getElementById('redirect-message').textContent = 'Redirecting to the new page location.';
  document.getElementById('redirect-link').href = destination;
  document.getElementById('redirect-link').textContent = 'Continue to the new page';
  window.location.replace(destination);
}} else {{
  document.getElementById('redirect-message').textContent = 'We could not find that page.';
}}
</script>
</body>
</html>
"""
    (ROOT / "404.html").write_text(html, encoding="utf-8")
    print(f"OK  404.html written with {len(redirects)} legacy redirects")

SECTION_LABELS = {
    "mens":          "Men's Senior",
    "mens-awards":   "Men's Awards",
    "womens":        "Women's Senior",
    "womens-awards": "Women's Awards",
    "mens-masters":  "Men's Masters",
    "womens-masters":"Women's Masters",
    "coaching":      "Coaching",
    "admin":         "Administration",
}

NON_WINNER_MARKERS = ("covid", "no season", "no presentation", "not awarded")

# ─────────────────────────────────────────────────────────────────
# Markdown parser helpers
# ─────────────────────────────────────────────────────────────────

def read_md(file_id):
    """Read a legacy markdown file by its numeric ID prefix."""
    for f in LEGACY.glob(f"{file_id}_*.md"):
        return f.read_text(encoding="utf-8")
    return ""


PLACEHOLDER_VALUES = {"", "—", "-", "–"}


def clean_markdown_cell(value):
    """Remove lightweight markdown formatting used in legacy table cells."""
    value = re.sub(r"!\[.*?\]\(.*?\)", "", value)
    value = re.sub(r"^\*{1,2}(.+?)\*{1,2}$", r"\1", value.strip())
    return value.strip()


def normalise_header(value):
    return re.sub(r"\s+", " ", clean_markdown_cell(value)).lower()


def split_markdown_row(line):
    cells = [clean_markdown_cell(c) for c in line.split("|")]
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return cells


def is_separator_row(cells):
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells)


def has_recorded_value(values):
    return any(v.strip() not in PLACEHOLDER_VALUES for v in values)


def parse_table(md_text):
    """
    Extract rows from a Markdown table.
    Returns list of dicts with keys from header row.
    Strips empty/placeholder rows (year with no player).
    """
    rows = []
    in_table = False
    headers = []
    for line in md_text.splitlines():
        line = line.strip()
        if not line:
            if in_table:
                break
            continue
        if "|" not in line:
            if in_table:
                break
            continue
        cells = split_markdown_row(line)
        if not cells:
            continue
        if is_separator_row(cells):
            continue
        if not headers:
            headers = [normalise_header(h) for h in cells]
            in_table = True
            continue
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        elif len(cells) > len(headers):
            cells = cells[:len(headers)]
        if len(cells) < 2:
            continue
        row = dict(zip(headers, cells))
        # Skip placeholder rows only when every non-year column is empty.
        # Admin/coaching boards often have valid records after blank middle cells.
        if not has_recorded_value(row.get(h, "") for h in headers[1:]):
            continue
        rows.append(row)
    return rows, headers


def count_wins(rows, player_key):
    """Return sorted list of (player, count) for multiple-win players."""
    from collections import Counter
    counts = Counter()
    for r in rows:
        name = r.get(player_key, "").strip()
        lowered = name.lower()
        if name and not any(marker in lowered for marker in NON_WINNER_MARKERS):
            counts[name] += 1
    return counts.most_common(8)


def table_stats(rows, year_key, player_key, value_keys=None):
    """Return (first_year, last_year, total_seasons)."""
    years = []
    for r in rows:
        y = r.get(year_key, "").strip()
        if y.isdigit():
            years.append(int(y))
    if not years:
        return "—", "—", 0
    keys = value_keys or [player_key]
    valid_rows = []
    for row in rows:
        values = [row.get(key, "").strip() for key in keys]
        row_text = " ".join(values).lower()
        if has_recorded_value(values) and not any(marker in row_text for marker in NON_WINNER_MARKERS):
            valid_rows.append(row)
    return min(years), max(years), len(valid_rows)


def latest_valid_record(rows, year_key, winner_key):
    """Return (year, winner) for the most recent valid recipient row."""
    best = None
    for r in rows:
        y = r.get(year_key, "").strip()
        winner = r.get(winner_key, "").strip()
        if not y.isdigit() or not winner:
            continue
        lowered = winner.lower()
        if any(marker in lowered for marker in NON_WINNER_MARKERS):
            continue
        y_val = int(y)
        if best is None or y_val > best[0]:
            best = (y_val, winner)
    return best

# ─────────────────────────────────────────────────────────────────
# HTML template helpers
# ─────────────────────────────────────────────────────────────────

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{page_title} — Mentone Hockey Club</title>
<meta name="description" content="{meta_desc}" />
<link rel="stylesheet" href="{asset_prefix}colors_and_type.css">
<link rel="stylesheet" href="{asset_prefix}site.css">
<link rel="stylesheet" href="{asset_prefix}club-history.css">
</head>
<body>
<div id="site-announce"></div>
<div id="site-nav"></div>
"""

FOOT = """
<div id="site-footer"></div>
<script src="{asset_prefix}partials.js"></script>
{extra_js}
</body>
</html>
"""

def breadcrumb(label, extra=None, home_href="index.html", history_href="club-history.html"):
    parts = [
        f'<a href="{home_href}">Home</a>',
        '<span class="breadcrumb-sep">›</span>',
        f'<a href="{history_href}">Club History</a>',
    ]
    if extra:
        parts += [
            '<span class="breadcrumb-sep">›</span>',
            f'<a href="{history_href}#honour-board">{extra}</a>',
        ]
    parts += [
        '<span class="breadcrumb-sep">›</span>',
        f'<span>{label}</span>',
    ]
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def wins_sidebar_html(wins, max_wins):
    if not wins:
        return ""
    html = '<div class="sidebar-card"><div class="sidebar-card-head">Most wins</div><div class="sidebar-card-body"><div class="stat-block">'
    for name, count in wins[:6]:
        pct = int((count / max_wins) * 100)
        html += f"""
        <div>
          <div class="stat-row">
            <span class="stat-name">{name}</span>
            <span class="stat-count">{count}×</span>
          </div>
          <div class="stat-bar-track"><div class="stat-bar-fill" style="width:{pct}%"></div></div>
        </div>"""
    html += "</div></div></div>"
    return html


def related_grades_html(section, grade_num, related_nums, section_label):
    """Build sidebar related links for other grades in same section."""
    if not related_nums:
        return ""
    # Build slug pattern from section
    slug_map = {
        "mens":          ("honour-board-mens", "Men's"),
        "womens":        ("honour-board-womens", "Women's"),
        "mens-masters":  ("honour-board-mens-masters", "Men's Masters"),
        "womens-masters":("honour-board-womens-masters", "Women's Masters"),
    }
    if section not in slug_map:
        return ""
    base_slug, section_name = slug_map[section]
    links = ""
    for num in related_nums:
        num_slug = {"1st":"1st","2nd":"2nd","3rd":"3rd","4th":"4th","5th":"5th","6th":"6th","7th":"7th"}[num]
        href = honour_page_name(f"{base_slug}-{num_slug.lower()}-xi")
        links += f'<a href="{href}" class="related-link">{num} XI {ARROW_ICON}</a>'
    return f'<div class="sidebar-card"><div class="sidebar-card-head">Other {section_name} grades</div><div class="related-links">{links}</div></div>'


def image_block_html(image_file):
    if not image_file:
        return ""
    img_path = f"{HONOUR_ASSET_PREFIX}{UPLOADS}/2017/06/{image_file}"
    return f"""
    <div class="hb-photo-board">
      <img src="{img_path}" alt="Physical honour board" loading="lazy" class="hb-photo-img" />
      <div class="hb-photo-caption">The physical honour board at Mentone Hockey Club</div>
    </div>"""


def header_label(header):
    labels = {
        "year": "Year",
        "player": "Player",
        "coach": "Coach",
        "club coach": "Club Coach",
        "manager": "Manager",
        "grade": "Grade",
        "result": "Result",
        "president": "President",
        "vice president": "Vice President",
        "secretary": "Secretary",
        "treasurer": "Treasurer",
        "men's": "Men's",
        "women's": "Women's",
        "junior": "Junior",
        "men's masters": "Men's Masters",
        "women's masters": "Women's Masters",
    }
    return labels.get(header, " ".join(part.capitalize() for part in header.split()))


def row_state(row, headers):
    year_key = headers[0] if headers else "year"
    data_values = [row.get(h, "").strip() for h in headers[1:]]
    row_text = " ".join(data_values).lower()
    is_covid = any(marker in row_text for marker in NON_WINNER_MARKERS)
    return year_key, is_covid


def latest_recorded_year(rows, headers):
    year_key = headers[0] if headers else "year"
    years = []
    for row in rows:
        year = row.get(year_key, "").strip()
        values = [row.get(h, "").strip() for h in headers[1:]]
        row_text = " ".join(values).lower()
        if year.isdigit() and has_recorded_value(values) and not any(marker in row_text for marker in NON_WINNER_MARKERS):
            years.append(int(year))
    return max(years) if years else None


def grade_cell_html(value):
    if not value:
        return '<td class="grade-tag"></td>'
    is_pl = "premier league" in value.lower()
    pill_class = "grade-pill pl" if is_pl else "grade-pill"
    return f'<td class="grade-tag"><span class="{pill_class}">{escape(value)}</span></td>'


def table_rows_html(rows, headers):
    """Generate HTML table rows, colouring COVID/no-season rows differently."""
    html = ""
    year_key = headers[0] if headers else "year"
    player_key = headers[1] if len(headers) > 1 else "player"
    grade_key = headers[2] if len(headers) > 2 else None

    latest_year = latest_recorded_year(rows, headers)

    for r in rows:
        year = r.get(year_key, "").strip()
        player = r.get(player_key, "").strip()
        grade = r.get(grade_key, "").strip() if grade_key else ""

        _, is_covid = row_state(r, headers[:2])
        is_current = year.isdigit() and int(year) == latest_year and not is_covid

        row_class = ""
        if is_covid:
            row_class = " class=\"covid\""
        elif is_current:
            row_class = " class=\"current\""

        # Grade pill
        grade_cell = grade_cell_html(grade) if grade_key else ""

        # Data attrs for filtering
        data_attrs = ""
        if year.isdigit() and int(year) >= 2010:
            data_attrs += ' data-era="recent"'
        if grade and "premier league" in grade.lower():
            data_attrs += ' data-grade="pl"'

        html += f'<tr{row_class}{data_attrs}><td class="year">{escape(year)}</td><td class="player">{escape(player)}</td>{grade_cell}</tr>\n'
    return html


def full_table_rows_html(rows, headers):
    """Generate rows for wide honour-board tables without dropping columns."""
    html = ""
    year_key = headers[0] if headers else "year"
    latest_year = latest_recorded_year(rows, headers)

    for row in rows:
        year = row.get(year_key, "").strip()
        _, is_covid = row_state(row, headers)
        is_current = year.isdigit() and int(year) == latest_year and not is_covid
        row_class = ' class="covid"' if is_covid else (' class="current"' if is_current else "")

        cells = []
        for idx, header in enumerate(headers):
            value = row.get(header, "").strip()
            if idx == 0:
                cells.append(f'<td class="year">{escape(value)}</td>')
            elif idx == 1:
                cells.append(f'<td class="player">{escape(value)}</td>')
            elif header == "grade":
                cells.append(grade_cell_html(value))
            else:
                cells.append(f"<td>{escape(value)}</td>")
        html += f"<tr{row_class}>{''.join(cells)}</tr>\n"
    return html


# ─────────────────────────────────────────────────────────────────
# Grade page generator
# ─────────────────────────────────────────────────────────────────

FILTER_JS = """
<script>
function filterTable(filter, btn) {
  document.querySelectorAll('.hb-filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const rows = document.querySelectorAll('#honours-table tbody tr');
  rows.forEach(row => {
    if (filter === 'all') {
      row.style.display = '';
    } else if (filter === 'recent') {
      row.style.display = (row.dataset.era === 'recent' || row.classList.contains('covid')) ? '' : 'none';
    } else if (filter === 'pl') {
      row.style.display = (row.dataset.grade === 'pl') ? '' : 'none';
    }
  });
}
</script>
"""

def generate_grade_page(file_id, slug, section, grade_num, label, image_file, related_nums):
    md = read_md(file_id)
    if not md:
        print(f"  SKIP {slug} — no markdown found for ID {file_id}")
        return

    rows, headers = parse_table(md)
    if not rows:
        print(f"  SKIP {slug} — no table data parsed")
        return

    year_key = headers[0]
    player_key = headers[1] if len(headers) > 1 else headers[0]
    use_full_table = len(headers) > 3 or section in ("admin", "coaching")
    has_grade_col = len(headers) > 2 and not use_full_table

    first_yr, last_yr, total = table_stats(
        rows,
        year_key,
        player_key,
        headers[1:] if use_full_table else None,
    )
    wins = count_wins(rows, player_key)
    max_wins = wins[0][1] if wins else 1
    most_wins_str = f"{wins[0][0]} · {wins[0][1]}" if wins else "—"
    section_label = SECTION_LABELS.get(section, "")
    is_awards_page = section in ("mens-awards","womens-awards","coaching","admin")

    # Show filter only if has grade column and is a grade page
    filter_html = ""
    filter_js = ""
    if has_grade_col and not is_awards_page:
        filter_html = """
        <div class="hb-filter">
          <button class="hb-filter-btn active" onclick="filterTable('all',this)">All</button>
          <button class="hb-filter-btn" onclick="filterTable('recent',this)">2010–present</button>
          <button class="hb-filter-btn" onclick="filterTable('pl',this)">Premier League</button>
        </div>"""
        filter_js = FILTER_JS

    if use_full_table:
        table_header_html = "".join(f"<th>{escape(header_label(h))}</th>" for h in headers)
        rows_html = full_table_rows_html(rows, headers)
    else:
        grade_th = f'<th style="text-align:right">Grade</th>' if has_grade_col else ""
        table_header_html = f"""
                <th>Year</th>
                <th>{escape(header_label(player_key))}</th>
                {grade_th}
              """
        rows_html = table_rows_html(rows, headers)

    sidebar_wins = wins_sidebar_html(wins, max_wins)
    sidebar_related = related_grades_html(section, grade_num, related_nums, section_label)
    img_block = image_block_html(image_file)

    html = HEAD.format(
        page_title=label,
        meta_desc=f"Best & fairest / award winners for Mentone Hockey Club {label} — every season on record.",
        asset_prefix=HONOUR_ASSET_PREFIX,
    )

    html += f"""
<section class="hb-hero">
  <div class="wrap">
    <div class="hb-hero-grade">
      <span class="eyebrow">{section_label}</span>
    </div>
    <h1>{label.replace("Men's","Men&#8217;s").replace("Women's","Women&#8217;s")} <em>Honour Board</em></h1>
    <div class="hb-hero-meta">
      <div class="hb-hero-meta-item">
        <span class="label">Records from</span>
        <span class="value">{first_yr}</span>
      </div>
      <div class="hb-hero-meta-item">
        <span class="label">Seasons recorded</span>
        <span class="value">{total}</span>
      </div>
      <div class="hb-hero-meta-item">
        <span class="label">Most wins</span>
        <span class="value">{most_wins_str}</span>
      </div>
    </div>
  </div>
</section>

<div class="wrap">
  {breadcrumb(label, "Honour Board", "../../index.html", "../")}
  <div class="hb-layout">
    <div class="hb-main">
      {img_block}
      <div class="hb-table-wrap">
        <div class="hb-table-head">
          <div class="hb-table-title">All seasons</div>
          {filter_html}
        </div>
        <div style="overflow-x:auto;">
          <table class="hb-table" id="honours-table">
            <thead>
              <tr>{table_header_html}</tr>
            </thead>
            <tbody>
              {rows_html}
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <aside class="hb-sidebar">
      {sidebar_wins}
      {sidebar_related}
      <div class="sidebar-card">
        <div class="sidebar-card-head">Navigation</div>
        <div class="related-links">
          <a href="../" class="related-link">Club History hub {ARROW_ICON}</a>
          <a href="../#club-awards" class="related-link">Club Awards {ARROW_ICON}</a>
          <a href="../#life-members" class="related-link">Life Members {ARROW_ICON}</a>
        </div>
      </div>
    </aside>
  </div>
  <a href="../" class="back-link">
    <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 7H3M7 3l-4 4 4 4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    Back to Club History
  </a>
  <div style="height:var(--space-8)"></div>
</div>
"""
    html += FOOT.format(extra_js=filter_js, asset_prefix=HONOUR_ASSET_PREFIX)

    out_path = HONOUR_BOARD_DIR / honour_page_name(slug)
    out_path.write_text(html, encoding="utf-8")
    print(f"  OK  {honour_page_href(slug)}  ({total} seasons, {len(wins)} multi-win players)")


def club_award_related_links(current_slug):
    links = []
    for _, slug, label, _, _ in CLUB_AWARD_PAGES:
        if slug == current_slug:
            continue
        links.append(f'<a href="{honour_page_name(slug)}" class="related-link">{label} {ARROW_ICON}</a>')
    return "".join(links)


def generate_club_award_page(file_id, slug, label, section_label, summary):
    md = read_md(file_id)
    if not md:
        print(f"  SKIP {slug} — no markdown found for ID {file_id}")
        return

    rows, headers = parse_table(md)
    if not rows or len(headers) < 2:
        print(f"  SKIP {slug} — no table data parsed")
        return

    year_key = headers[0]
    winner_key = headers[1]
    first_yr, _, total = table_stats(rows, year_key, winner_key)
    wins = count_wins(rows, winner_key)
    max_wins = wins[0][1] if wins else 1
    most_wins_str = f"{wins[0][0]} · {wins[0][1]}" if wins else "—"
    latest = latest_valid_record(rows, year_key, winner_key)
    latest_label = f"{latest[1]} ({latest[0]})" if latest else "—"
    latest_year = latest[0] if latest else None

    header_html = "".join(f"<th>{escape(h.title())}</th>" for h in headers)
    row_html = ""
    for row in rows:
        year_val = row.get(year_key, "").strip()
        winner_val = row.get(winner_key, "").strip()
        winner_lower = winner_val.lower()
        is_invalid = any(marker in winner_lower for marker in NON_WINNER_MARKERS)
        is_current = latest_year is not None and year_val.isdigit() and int(year_val) == latest_year and not is_invalid
        row_class = ' class="covid"' if is_invalid else (' class="current"' if is_current else "")
        cells = "".join(f"<td>{escape(row.get(h, '').strip())}</td>" for h in headers)
        row_html += f"<tr{row_class}>{cells}</tr>\n"

    html = HEAD.format(
        page_title=label,
        meta_desc=f"{label} award recipients for Mentone Hockey Club — every season on record.",
        asset_prefix=HONOUR_ASSET_PREFIX,
    )
    html += f"""
<section class="hb-hero">
  <div class="wrap">
    <div class="hb-hero-grade">
      <span class="eyebrow">{section_label}</span>
    </div>
    <h1>{label} <em>Roll of Honour</em></h1>
    <div class="hb-hero-meta">
      <div class="hb-hero-meta-item">
        <span class="label">Records from</span>
        <span class="value">{first_yr}</span>
      </div>
      <div class="hb-hero-meta-item">
        <span class="label">Seasons recorded</span>
        <span class="value">{total}</span>
      </div>
      <div class="hb-hero-meta-item">
        <span class="label">Most wins</span>
        <span class="value">{most_wins_str}</span>
      </div>
      <div class="hb-hero-meta-item">
        <span class="label">Latest winner</span>
        <span class="value">{latest_label}</span>
      </div>
    </div>
  </div>
</section>

<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="../../index.html">Home</a><span class="breadcrumb-sep">›</span><a href="../">Club History</a><span class="breadcrumb-sep">›</span><a href="../#club-awards">Club Awards</a><span class="breadcrumb-sep">›</span><span>{label}</span></nav>
  <div class="hb-layout">
    <div class="hb-main">
      <p style="margin-bottom:var(--space-4);">{summary}</p>
      <div class="hb-table-wrap">
        <div class="hb-table-head">
          <div class="hb-table-title">All seasons</div>
        </div>
        <div style="overflow-x:auto;">
          <table class="hb-table">
            <thead>
              <tr>{header_html}</tr>
            </thead>
            <tbody>
              {row_html}
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <aside class="hb-sidebar">
      {wins_sidebar_html(wins, max_wins)}
      <div class="sidebar-card">
        <div class="sidebar-card-head">Other Club Awards</div>
        <div class="related-links">
          {club_award_related_links(slug)}
        </div>
      </div>
      <div class="sidebar-card">
        <div class="sidebar-card-head">Navigation</div>
        <div class="related-links">
          <a href="../" class="related-link">Club History hub {ARROW_ICON}</a>
          <a href="../#club-awards" class="related-link">Club Awards {ARROW_ICON}</a>
          <a href="../#honour-board" class="related-link">Best &amp; Fairest Winners {ARROW_ICON}</a>
        </div>
      </div>
    </aside>
  </div>
  <a href="../" class="back-link">
    <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 7H3M7 3l-4 4 4 4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    Back to Club History
  </a>
  <div style="height:var(--space-8)"></div>
</div>
"""
    html += FOOT.format(extra_js="", asset_prefix=HONOUR_ASSET_PREFIX)
    out_path = HONOUR_BOARD_DIR / honour_page_name(slug)
    out_path.write_text(html, encoding="utf-8")
    print(f"  OK  {honour_page_href(slug)}  ({total} seasons)")


def generate_club_award_pages():
    print(f"Generating {len(CLUB_AWARD_PAGES)} club award pages...")
    for page in CLUB_AWARD_PAGES:
        generate_club_award_page(*page)


# ─────────────────────────────────────────────────────────────────
# Special pages
# ─────────────────────────────────────────────────────────────────

def generate_club_song():
    md = read_md("486")
    if not md:
        print("  SKIP club-song.html — no source")
        return

    # Clean up the markdown a bit
    content = md.strip()

    html = HEAD.format(
        page_title="Club Song",
        meta_desc="The Mentone Hockey Club song — sung after every Panthers victory since 1976.",
        asset_prefix=HISTORY_ASSET_PREFIX,
    )
    html += f"""
<section class="hb-hero">
  <div class="wrap">
    <div class="hb-hero-grade"><span class="eyebrow">Traditions</span></div>
    <h1>The Club <em>Song</em></h1>
    <div class="hb-hero-meta">
      <div class="hb-hero-meta-item">
        <span class="label">Sung since</span>
        <span class="value">1976</span>
      </div>
      <div class="hb-hero-meta-item">
        <span class="label">Occasion</span>
        <span class="value">Every Panthers win</span>
      </div>
    </div>
  </div>
</section>
<div class="wrap">
  {breadcrumb("Club Song", home_href="../index.html", history_href="index.html")}
  <div class="hb-layout" style="grid-template-columns:1fr 280px">
    <div>
      <div class="song-full">
        <pre class="song-text">{content}</pre>
      </div>
    </div>
    <aside class="hb-sidebar">
      <div class="sidebar-card">
        <div class="sidebar-card-head">Navigation</div>
        <div class="related-links">
          <a href="index.html" class="related-link">Club History {ARROW_ICON}</a>
        </div>
      </div>
    </aside>
  </div>
  <a href="index.html" class="back-link">
    <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 7H3M7 3l-4 4 4 4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    Back to Club History
  </a>
  <div style="height:var(--space-8)"></div>
</div>
"""
    html += FOOT.format(extra_js="", asset_prefix=HISTORY_ASSET_PREFIX)
    (HISTORY_DIR / "club-song.html").write_text(html, encoding="utf-8")
    print("  OK  history/club-song.html")


def generate_25th_anniversary():
    md = read_md("494")
    if not md:
        print("  SKIP 25th-anniversary-team.html — no source")
        return

    content_html = markdown2.markdown(md, extras=["tables"])

    html = HEAD.format(
        page_title="25th Anniversary Team",
        meta_desc="The Mentone Hockey Club 25th Anniversary Team — named in 2001 to honour the best players from the club's first 25 years.",
        asset_prefix=HISTORY_ASSET_PREFIX,
    )
    html += f"""
<section class="hb-hero">
  <div class="wrap">
    <div class="hb-hero-grade"><span class="eyebrow">Club History · 2001</span></div>
    <h1>25th Anniversary <em>Team</em></h1>
    <div class="hb-hero-meta">
      <div class="hb-hero-meta-item">
        <span class="label">Named in</span>
        <span class="value">2001</span>
      </div>
      <div class="hb-hero-meta-item">
        <span class="label">Covering</span>
        <span class="value">1976–2001</span>
      </div>
    </div>
  </div>
</section>
<div class="wrap">
  {breadcrumb("25th Anniversary Team", home_href="../index.html", history_href="index.html")}
  <div class="hb-layout" style="grid-template-columns:1fr 280px">
    <div class="history-prose">
      {content_html}
    </div>
    <aside class="hb-sidebar">
      <div class="sidebar-card">
        <div class="sidebar-card-head">Navigation</div>
        <div class="related-links">
          <a href="index.html" class="related-link">Club History {ARROW_ICON}</a>
          <a href="index.html#life-members" class="related-link">Life Members {ARROW_ICON}</a>
        </div>
      </div>
    </aside>
  </div>
  <a href="index.html" class="back-link">
    <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 7H3M7 3l-4 4 4 4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    Back to Club History
  </a>
  <div style="height:var(--space-8)"></div>
</div>
"""
    html += FOOT.format(extra_js="", asset_prefix=HISTORY_ASSET_PREFIX)
    (HISTORY_DIR / "25th-anniversary-team.html").write_text(html, encoding="utf-8")
    print("  OK  history/25th-anniversary-team.html")


# ─────────────────────────────────────────────────────────────────
# Shared CSS for all history sub-pages
# ─────────────────────────────────────────────────────────────────

HISTORY_CSS = """
/* ── Shared Club History styles ──────────────────────────────── */

/* Hero */
.hb-hero {
  background: var(--navy);
  padding: var(--space-8) 0 var(--space-7);
  position: relative;
  overflow: hidden;
}
.hb-hero::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(241,180,52,0.4), transparent);
}
.hb-hero-grade {
  display: inline-flex;
  align-items: center;
  background: rgba(241,180,52,0.12);
  border: 1px solid rgba(241,180,52,0.2);
  border-radius: var(--radius-pill);
  padding: 6px 14px;
  margin-bottom: var(--space-4);
}
.hb-hero-grade .eyebrow { margin: 0; font-size: 11px; }
.hb-hero h1 { color: var(--cream); margin-bottom: var(--space-3); }
.hb-hero h1 em { color: var(--yellow); }
.hb-hero-meta {
  display: flex;
  gap: var(--space-5);
  flex-wrap: wrap;
  margin-top: var(--space-5);
}
.hb-hero-meta-item .label {
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(246,241,230,0.4);
  font-weight: 600;
  display: block;
  margin-bottom: 2px;
}
.hb-hero-meta-item .value {
  font-family: var(--display);
  font-size: 22px;
  font-weight: 300;
  color: var(--yellow);
  letter-spacing: -0.02em;
}

/* Breadcrumb */
.breadcrumb {
  padding: var(--space-4) 0;
  border-bottom: 1px solid var(--line);
  font-size: 13px;
  color: var(--muted);
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.breadcrumb a { color: var(--muted); transition: color .15s; }
.breadcrumb a:hover { color: var(--navy); }
.breadcrumb-sep { color: var(--line); }

/* Layout */
.hb-layout {
  padding: var(--space-7) 0;
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: var(--space-7);
  align-items: start;
}
@media (max-width: 900px) {
  .hb-layout { grid-template-columns: 1fr; }
  .hb-sidebar { order: -1; }
}

/* Honour board photo */
.hb-photo-board {
  margin-bottom: var(--space-5);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.hb-photo-img { width: 100%; display: block; }
.hb-photo-caption {
  padding: var(--space-2) var(--space-4);
  font-size: 12px;
  color: var(--muted);
  background: var(--cream-warm);
  border-top: 1px solid var(--line-light);
  font-style: italic;
}

/* Table wrap */
.hb-table-wrap {
  background: var(--bg-surface);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.hb-table-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--line);
  gap: var(--space-3);
  flex-wrap: wrap;
}
.hb-table-title {
  font-family: var(--display);
  font-size: 18px;
  font-weight: 500;
  color: var(--navy);
}
.hb-filter { display: flex; gap: 6px; }
.hb-filter-btn {
  padding: 5px 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.08em;
  border: 1px solid var(--line);
  border-radius: var(--radius-pill);
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  transition: all .15s;
}
.hb-filter-btn.active, .hb-filter-btn:hover {
  background: var(--navy);
  color: var(--cream);
  border-color: var(--navy);
}
.hb-table { width: 100%; border-collapse: collapse; }
.hb-table thead tr {
  background: var(--cream-warm);
  border-bottom: 1px solid var(--line);
}
.hb-table th {
  padding: 10px var(--space-5);
  text-align: left;
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
  font-weight: 600;
}
.hb-table tbody tr {
  border-bottom: 1px solid var(--line-light);
  transition: background .1s;
}
.hb-table tbody tr:last-child { border-bottom: none; }
.hb-table tbody tr:hover { background: var(--blue-wash); }
.hb-table td {
  padding: 11px var(--space-5);
  font-size: 14px;
  color: var(--ink);
  line-height: 1.4;
}
.hb-table td.year {
  font-variant-numeric: tabular-nums;
  color: var(--muted);
  font-size: 13px;
  font-weight: 600;
  width: 58px;
}
.hb-table td.player { font-weight: 500; }
.hb-table td.grade-tag { text-align: right; }
.hb-table tr.covid td { color: var(--muted); font-style: italic; }
.hb-table tr.current { background: rgba(241,180,52,0.05); }
.hb-table tr.current td.player { font-weight: 600; color: var(--navy); }
.hb-table tr.current td.year::after {
  content: '';
  display: inline-block;
  width: 5px; height: 5px;
  background: var(--yellow);
  border-radius: 50%;
  margin-left: 6px;
  vertical-align: middle;
}
.grade-pill {
  display: inline-block;
  padding: 2px 8px;
  border-radius: var(--radius-pill);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.06em;
  background: var(--blue-wash);
  color: var(--navy);
}
.grade-pill.pl {
  background: rgba(241,180,52,0.15);
  color: var(--yellow-deep);
}

/* Sidebar */
.hb-sidebar { display: flex; flex-direction: column; gap: var(--space-4); }
.sidebar-card {
  background: var(--bg-surface);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.sidebar-card-head {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--line);
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  font-weight: 600;
  color: var(--muted);
}
.sidebar-card-body { padding: var(--space-4); }
.stat-block { display: flex; flex-direction: column; gap: var(--space-3); }
.stat-row { display: flex; justify-content: space-between; align-items: center; gap: var(--space-3); }
.stat-name { font-size: 14px; font-weight: 500; color: var(--navy); }
.stat-count {
  font-family: var(--display);
  font-size: 20px;
  font-weight: 300;
  color: var(--yellow-deep);
  letter-spacing: -0.02em;
  white-space: nowrap;
}
.stat-bar-track {
  height: 3px;
  background: var(--line-light);
  border-radius: 2px;
  margin-top: 4px;
}
.stat-bar-fill {
  height: 100%;
  background: var(--yellow);
  border-radius: 2px;
}
.related-links { display: flex; flex-direction: column; }
.related-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px var(--space-4);
  font-size: 14px;
  color: var(--ink);
  border-bottom: 1px solid var(--line-light);
  transition: background .1s, color .1s;
}
.related-link:last-child { border-bottom: none; }
.related-link:hover { background: var(--blue-wash); color: var(--navy); }
.related-link svg { width: 12px; height: 12px; opacity: 0.35; }

/* History hub cards */
.life-members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--space-4);
}
.life-member-card {
  background: var(--bg-surface);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-3);
}
.life-member-avatar {
  width: 86px;
  height: 86px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(241,180,52,0.25);
  background: var(--cream-warm);
}
.life-member-initials {
  display: grid;
  place-items: center;
  font-family: var(--display);
  font-size: 30px;
  font-style: italic;
  color: var(--yellow-deep);
  background: linear-gradient(135deg, rgba(241,180,52,0.18), rgba(51,88,128,0.12));
}
.life-member-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--navy);
  line-height: 1.25;
}
.awards-group-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--space-4);
}
.awards-group-card {
  background: var(--bg-surface);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.awards-group-card h3 {
  padding: var(--space-4) var(--space-4) 0;
  color: var(--navy);
}
.awards-latest {
  margin: var(--space-3) var(--space-4);
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  background: rgba(241,180,52,0.1);
  color: var(--muted);
  font-size: 13px;
}
.awards-latest strong {
  color: var(--navy);
  font-weight: 600;
}
.awards-link-list {
  display: flex;
  flex-direction: column;
  border-top: 1px solid var(--line-light);
}
.award-row {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: var(--space-4);
  border-bottom: 1px solid var(--line-light);
  color: var(--ink);
  transition: background .1s, color .1s;
}
.award-row:last-child { border-bottom: none; }
.award-row:hover { background: var(--blue-wash); color: var(--navy); }
.award-row-name {
  font-size: 15px;
  font-weight: 700;
  color: var(--navy);
}
.award-row-current {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.35;
}
.award-row-tradition .award-row-current {
  color: var(--yellow-deep);
  font-weight: 600;
}

/* Back link */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--muted);
  padding: var(--space-5) 0 0;
  transition: color .15s;
}
.back-link:hover { color: var(--navy); }
.back-link svg { width: 14px; height: 14px; }

/* Prose pages (25th ann, club song) */
.history-prose h1, .history-prose h2, .history-prose h3 {
  font-family: var(--display);
  color: var(--navy);
  margin: var(--space-5) 0 var(--space-3);
}
.history-prose p { line-height: 1.7; margin-bottom: var(--space-4); }
.history-prose table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: var(--space-5);
  font-size: 14px;
}
.history-prose th {
  padding: 8px var(--space-4);
  background: var(--cream-warm);
  border-bottom: 1px solid var(--line);
  text-align: left;
  font-weight: 600;
  font-size: 12px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
}
.history-prose td {
  padding: 9px var(--space-4);
  border-bottom: 1px solid var(--line-light);
}
.history-prose tr:last-child td { border-bottom: none; }

/* Club song */
.song-full { padding: var(--space-5) 0; }
.song-text {
  font-family: var(--display);
  font-style: italic;
  font-size: 22px;
  font-weight: 300;
  line-height: 1.8;
  color: var(--navy);
  white-space: pre-wrap;
  border-left: 3px solid var(--yellow);
  padding-left: var(--space-5);
  margin: 0;
}
"""


# ─────────────────────────────────────────────────────────────────
# index.html patcher
# ─────────────────────────────────────────────────────────────────

def patch_index():
    """Add Club History link to the main nav if not already present."""
    index_path = ROOT / "index.html"
    if not index_path.exists():
        print("  SKIP index.html patch — file not found")
        return

    content = index_path.read_text(encoding="utf-8")
    if "history/" in content:
        print("  OK  index.html — Club History link already present")
        return

    # Add a "Club History" section to the bottom of index.html just before footer
    promo = """
<!-- CLUB HISTORY PROMO -->
<section class="section" style="background:var(--navy);padding:var(--space-8) 0;">
  <div class="wrap">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-7);align-items:center;">
      <div>
        <div class="eyebrow" style="color:var(--yellow);margin-bottom:var(--space-3)">50 Years of History</div>
        <h2 style="color:var(--cream);margin-bottom:var(--space-4);">Life Members. Honour Boards. <em>Legends.</em></h2>
        <p style="color:rgba(246,241,230,0.6);margin-bottom:var(--space-5);max-width:440px;">From the founding members in 1976 through to today's Premier League squads — explore the full record of everyone who's worn the Panther jersey.</p>
        <a href="history/" class="btn btn-primary">Explore Club History
          <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7h8M7 3l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-3);">
        <a href="history/#life-members" style="background:rgba(246,241,230,0.05);border:1px solid rgba(246,241,230,0.1);border-radius:var(--radius-md);padding:var(--space-4);text-decoration:none;transition:background .2s;" onmouseover="this.style.background='rgba(246,241,230,0.1)'" onmouseout="this.style.background='rgba(246,241,230,0.05)'">
          <div style="font-family:var(--display);font-size:28px;font-weight:300;color:var(--yellow);letter-spacing:-0.02em;">20+</div>
          <div style="font-size:13px;color:rgba(246,241,230,0.6);margin-top:4px;">Life Members</div>
        </a>
        <a href="history/#honour-board" style="background:rgba(246,241,230,0.05);border:1px solid rgba(246,241,230,0.1);border-radius:var(--radius-md);padding:var(--space-4);text-decoration:none;transition:background .2s;" onmouseover="this.style.background='rgba(246,241,230,0.1)'" onmouseout="this.style.background='rgba(246,241,230,0.05)'">
          <div style="font-family:var(--display);font-size:28px;font-weight:300;color:var(--yellow);letter-spacing:-0.02em;">20</div>
          <div style="font-size:13px;color:rgba(246,241,230,0.6);margin-top:4px;">Honour Boards</div>
        </a>
        <a href="history/#club-awards" style="background:rgba(246,241,230,0.05);border:1px solid rgba(246,241,230,0.1);border-radius:var(--radius-md);padding:var(--space-4);text-decoration:none;transition:background .2s;" onmouseover="this.style.background='rgba(246,241,230,0.1)'" onmouseout="this.style.background='rgba(246,241,230,0.05)'">
          <div style="font-family:var(--display);font-size:28px;font-weight:300;color:var(--yellow);letter-spacing:-0.02em;">35+</div>
          <div style="font-size:13px;color:rgba(246,241,230,0.6);margin-top:4px;">Years of Awards</div>
        </a>
        <a href="history/25th-anniversary-team.html" style="background:rgba(246,241,230,0.05);border:1px solid rgba(246,241,230,0.1);border-radius:var(--radius-md);padding:var(--space-4);text-decoration:none;transition:background .2s;" onmouseover="this.style.background='rgba(246,241,230,0.1)'" onmouseout="this.style.background='rgba(246,241,230,0.05)'">
          <div style="font-family:var(--display);font-size:28px;font-weight:300;color:var(--yellow);letter-spacing:-0.02em;">2001</div>
          <div style="font-size:13px;color:rgba(246,241,230,0.6);margin-top:4px;">Anniversary Team</div>
        </a>
      </div>
    </div>
  </div>
</section>

"""
    # Insert before footer div
    content = content.replace('<div id="site-footer"></div>', promo + '<div id="site-footer"></div>')
    index_path.write_text(content, encoding="utf-8")
    print("  OK  index.html — Club History promo section added")


# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Mentone HC — Club History page generator")
    print("="*60 + "\n")

    if not LEGACY.exists():
        print(f"ERROR: {LEGACY} not found.")
        print("Make sure legacy-content/ is in your project root.")
        sys.exit(1)

    HISTORY_DIR.mkdir(exist_ok=True)
    HONOUR_BOARD_DIR.mkdir(parents=True, exist_ok=True)

    # Write shared CSS
    css_path = ROOT / "club-history.css"
    css_path.write_text(HISTORY_CSS, encoding="utf-8")
    print(f"OK  club-history.css written\n")

    write_404_redirects()
    print()

    # Generate all grade/admin pages
    print(f"Generating {len(GRADE_PAGES)} honour board pages...")
    for page in GRADE_PAGES:
        generate_grade_page(*page)
    print()
    generate_club_award_pages()

    # Special pages
    print("\nGenerating special pages...")
    generate_club_song()
    generate_25th_anniversary()

    # Patch index
    print("\nPatching index.html...")
    patch_index()

    print("\n" + "="*60)
    print(f"Done. Pages written to: {OUT}")
    print("Open index.html in your browser to see the Club History")
    print("promo section, then click through to history/")
    print("="*60 + "\n")
