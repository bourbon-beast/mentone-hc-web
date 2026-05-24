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
import sys
from datetime import date, datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ── Paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR  = Path(__file__).parent
REPO_ROOT   = SCRIPT_DIR.parent
CONFIG_FILE = SCRIPT_DIR / "mentone_teams_2026.json"
OUTPUT_FILE = REPO_ROOT / "fixtures.json"


class ScrapeValidationError(RuntimeError):
    """Raised when a source page cannot be trusted for fixture output."""

# ── HTTP ──────────────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        raise ScrapeValidationError(f"unexpected HTTP {resp.status_code}")
    if not resp.text.strip():
        raise ScrapeValidationError("empty response body")
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


# ── Parsing ───────────────────────────────────────────────────────────────────

def clean_opponent(raw: str) -> str:
    """Strip competition prefix: 'Mens PL - 2026 Doncaster HC' → 'Doncaster HC'"""
    m = re.search(r" - 20\d\d (.+)$", raw)
    return m.group(1).strip() if m else raw.strip()


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


def normalise_text(text: str) -> str:
    return " ".join(text.split())


def validate_team_page(
    soup: BeautifulSoup,
    expected_title: str | None,
    grade_label: str,
    team_url: str,
) -> None:
    if not expected_title:
        return

    page_text = normalise_text(soup.get_text(" ", strip=True))
    expected = normalise_text(expected_title)
    if expected not in page_text:
        raise ScrapeValidationError(
            f"{grade_label} page did not match expected title {expected!r}: {team_url}"
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
    soup = fetch_soup(team_url)
    validate_team_page(soup, expected_title, grade_label, team_url)

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
        for _ in range(12):
            if container is None:
                break
            if (container.find("a", href=re.compile(r"/venues/")) and
                    container.find("a", href=re.compile(r"/games/team/"))):
                break
            container = container.find_parent()

        if container is None:
            continue

        block = container.get_text(separator="\n", strip=True)

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
        team_tags = container.find_all("a", href=re.compile(r"/games/team/"))
        opp_tag = next(
            (
                tag for tag in team_tags
                if clean_opponent(tag.get_text(strip=True)) != "Mentone Hockey Club"
            ),
            team_tags[0] if team_tags else None,
        )
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
        raise ScrapeValidationError(f"{grade_label} produced no fixtures: {team_url}")
    if any(f.get("opponent") == "Mentone Hockey Club" for f in fixtures):
        raise ScrapeValidationError(
            f"{grade_label} produced Mentone as an opponent: {team_url}"
        )
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
