#!/usr/bin/env python3
"""
update_fixtures.py — Scrapes Hockey Victoria and writes fixtures.json
for the Mentone Hockey Club static website.

Usage:
    pip install requests beautifulsoup4
    python scripts/update_fixtures.py
    python scripts/update_fixtures.py --dry-run   # preview JSON, don't write file
    python scripts/update_fixtures.py --config scripts/mentone_teams_2026.json

Reads team URLs from mentone_teams_2026.json (same directory as this script).
Writes fixtures.json to the project root.
"""

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ── Paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR  = Path(__file__).parent
REPO_ROOT   = SCRIPT_DIR.parent
CONFIG_FILE = SCRIPT_DIR / "mentone_teams_2026.json"
OUTPUT_FILE = REPO_ROOT / "fixtures.json"


class FixtureSourceError(RuntimeError):
    """Raised when a configured Hockey Victoria source is missing or wrong."""

# ── HTTP ──────────────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


# ── Parsing ───────────────────────────────────────────────────────────────────

def clean_opponent(raw: str) -> str:
    """Strip competition prefixes from Hockey Victoria team labels."""
    m = re.search(r" - 20\d\d (.+)$", raw)
    if m:
        return m.group(1).strip()

    midweek = re.search(
        r"^20\d\d\s+Midweek\s+(?:Monday\s+)?"
        r"(?:Men's|Mens|Women's|Womens)\s+"
        r"(?:Open\s+)?(?:\d+\+\s+)?(?:[A-Z]+\s+){1,3}(.+)$",
        raw,
    )
    return midweek.group(1).strip() if midweek else raw.strip()


def parse_hv_date(date_str: str) -> tuple[str, str] | tuple[None, None]:
    """
    Parse '26 Apr 2026' → ('2026-04-26', 'Sun').
    Returns (None, None) if parsing fails.
    """
    if not date_str:
        return None, None
    try:
        dt = datetime.strptime(date_str.strip(), "%d %b %Y")
        return dt.strftime("%Y-%m-%d"), dt.strftime("%a")
    except ValueError:
        return None, None


def normalise_time(raw: str) -> str:
    """'13:30' → '1:30pm', '09:00' → '9:00am', '13:00' → '1:00pm'"""
    if not raw:
        return raw
    try:
        t = datetime.strptime(raw.strip(), "%H:%M")
        h, m = t.hour, t.minute
        period = "am" if h < 12 else "pm"
        h12 = h % 12 or 12
        return f"{h12}:{m:02d}{period}"
    except ValueError:
        return raw.strip()


def determine_venue(venue_name: str, is_home: bool) -> str:
    """Map venue name + home/away flag to 'Home', 'Away', or the full venue string."""
    if venue_name is None:
        return "Away" if not is_home else "Home"
    name_lower = venue_name.lower()
    if "mentone" in name_lower:
        return "Home"
    return "Away"


def determine_result(block: str, status: str) -> str | None:
    """
    Return 'W', 'L', or 'D' for played games; None for upcoming.
    Also returns None for forfeits/walkovers.
    """
    if status != "played":
        return None
    m = re.search(r"\b(Win|Loss|Draw)\b", block)
    if not m:
        return None
    return {"Win": "W", "Loss": "L", "Draw": "D"}.get(m.group(1))


def normalise_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def validate_expected_title(soup: BeautifulSoup, expected_title: str, grade_label: str) -> None:
    page_text = normalise_text(soup.get_text(separator=" ", strip=True))
    expected = normalise_text(expected_title)
    if expected not in page_text:
        raise FixtureSourceError(
            f"{grade_label}: expected source title {expected!r} was not found"
        )


def parse_team_page(
    team_url: str,
    grade_label: str,
    expected_title: str | None = None,
) -> list[dict]:
    """
    Scrape one HV team page and return a list of fixture dicts matching the
    fixtures.json schema:
        { date, day, time, opponent, venue, result }
    """
    print(f"  Fetching {grade_label} … {team_url}", flush=True)
    try:
        soup = fetch_soup(team_url)
    except Exception as exc:
        raise FixtureSourceError(f"{grade_label}: could not fetch page — {exc}") from exc

    if expected_title:
        validate_expected_title(soup, expected_title, grade_label)

    fixtures = []
    seen_rounds: set[int] = set()

    for b_tag in soup.find_all("b"):
        text = b_tag.get_text(strip=True)
        m = re.match(r"^Round\s+(\d+)$", text)
        if not m:
            continue
        round_num = int(m.group(1))
        if round_num in seen_rounds:
            continue
        seen_rounds.add(round_num)

        # Walk up until we have both a /venues/ link and a /games/team/ link
        container = b_tag.find_parent()
        found_match_container = False
        for _ in range(12):
            if container is None:
                break
            if (container.find("a", href=re.compile(r"/venues/")) and
                    container.find("a", href=re.compile(r"/games/team/"))):
                found_match_container = True
                break
            container = container.find_parent()

        if container is None or not found_match_container:
            continue

        block = container.get_text(separator="\n", strip=True)
        if len(re.findall(r"\bRound\s+\d+\b", block)) != 1:
            continue

        # Date + time
        dm = re.search(
            r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\d{1,2}\s+\w{3}\s+\d{4})\s+(\d{1,2}:\d{2})",
            block,
        )
        date_iso, day_str = parse_hv_date(dm.group(1) if dm else None)
        time_raw = dm.group(2) if dm else None

        # Venue
        venue_tag = container.find("a", href=re.compile(r"/venues/"))
        venue_name = venue_tag.get_text(strip=True) if venue_tag else None

        # Opponent
        opp_tag  = container.find("a", href=re.compile(r"/games/team/"))
        opponent = clean_opponent(opp_tag.get_text(strip=True)) if opp_tag else None

        # Home / Away  (venue name is the ground used)
        is_home = "mentone" in (venue_name or "").lower()

        # Status + result
        status = "played" if "Played" in block else "upcoming"
        result = determine_result(block, status)

        fixtures.append({
            "date":     date_iso,
            "day":      day_str,
            "time":     normalise_time(time_raw),
            "opponent": opponent,
            "venue":    determine_venue(venue_name, is_home),
            "result":   result,
        })

    fixtures.sort(key=lambda f: f["date"] or "")
    if not fixtures:
        raise FixtureSourceError(f"{grade_label}: no fixtures parsed from source page")
    return fixtures


# ── Main ──────────────────────────────────────────────────────────────────────

def build_fixtures_json(config: dict) -> dict:
    output_sections = []

    for section in config["sections"]:
        grades_out = []
        print(f"\n[{section['label']}]")
        for grade_cfg in section["grades"]:
            fixtures = parse_team_page(
                grade_cfg["team_url"],
                grade_cfg["grade"],
                grade_cfg.get("expected_title"),
            )
            grades_out.append({
                "grade":    grade_cfg["grade"],
                "fixtures": fixtures,
            })

        output_sections.append({
            "id":     section["id"],
            "label":  section["label"],
            "color":  section["color"],
            "grades": grades_out,
        })

    return {
        "updated":  date.today().isoformat(),
        "sections": output_sections,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Update fixtures.json from Hockey Victoria")
    parser.add_argument("--dry-run",  action="store_true", help="Print JSON to stdout, don't write file")
    parser.add_argument("--config",   default=str(CONFIG_FILE), help="Path to team config JSON")
    parser.add_argument("--output",   default=str(OUTPUT_FILE), help="Path to write fixtures.json")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"ERROR: config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, encoding="utf-8") as fh:
        config = json.load(fh)

    print(f"Scraping fixtures for {config.get('season', 'unknown')} season …")
    result = build_fixtures_json(config)

    if args.dry_run:
        print("\n── fixtures.json (dry run) ──────────────────────────")
        print(json.dumps(result, indent=2))
    else:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
            fh.write("\n")
        print(f"\nWritten to {output_path}")
        print(f"Updated: {result['updated']}")
        total = sum(
            len(g["fixtures"])
            for s in result["sections"]
            for g in s["grades"]
        )
        print(f"Fixtures: {total} across {sum(len(s['grades']) for s in result['sections'])} grades")


if __name__ == "__main__":
    main()
