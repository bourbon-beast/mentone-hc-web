"""Audit which WordPress images are referenced in the important data files,
and check whether each one is already downloaded locally."""
import re
from pathlib import Path

ROOT = Path(r"F:\Documents\Steve\Development\mentone-hc-web\legacy-content")
MARKDOWN_DIR = ROOT / "markdown"
UPLOADS_DIR = ROOT / "uploads"

url_pattern = re.compile(
    r'(?:https?:)?//mentonehockey\.org\.au/(?:wpdev/)?wp-content/uploads/([^\s\)\]"\'>]+)'
)

# These are the data-heavy files that the DB will be built from
important_files = [
    "462_life-members.md",
    "2604_mens-1st-xi.md", "2610_mens-2nd-xi.md", "2619_mens-3rd-xi.md",
    "2625_mens-4th-xi.md", "2629_mens-5th-xi.md", "2633_mens-6th-xi.md",
    "2637_mens-7th-xi.md",
    "2663_womens-1st-xi.md", "2668_womens-2nd-xi.md", "2672_womens-3rd-xi.md",
    "2679_womens-4th-xi.md", "2685_womens-5th-xi.md", "2689_womens-6th-xi.md",
    "2694_mens-masters-1st-xi.md", "2699_mens-masters-2nd-xi.md",
    "2704_mens-masters-3rd-xi.md", "2707_mens-masters-4th-xi.md",
    "2712_womens-masters-1st-xi.md", "2716_womens-masters-2nd-xi.md",
    "2720_womens-masters-3rd-xi.md",
    "2329_s-holliday-club-woman-award.md",
    "2327_ap-dayton-clubman-award.md",
    "2331_j-burt-junior-club-person-award.md",
    "2487_coach-of-the-year.md",
    "2077_the-presidents-cup.md",
    "2334_executive-committee.md",
    "2336_coordinators.md",
    "2356_mens-best-1st-year-player.md",
    "2654_womens-best-1st-year-player.md",
    "2641_mens-sharpshooter.md", "2660_womens-sharpshooter.md",
    "2645_mens-most-improved.md", "2649_womens-most-improved.md",
    "496_mens-senior-coach.md", "501_womens-senior-coach-and-manager.md",
    "494_25th-anniversary-team.md",
]

print(f"{'FILE':<55} {'REFS':<6} {'MISSING':<8}")
print("-" * 75)
total_refs = 0
total_missing = 0
all_missing = []
for fname in important_files:
    f = MARKDOWN_DIR / fname
    if not f.exists():
        print(f"{fname:<55} FILE NOT FOUND")
        continue
    text = f.read_text(encoding="utf-8", errors="ignore")
    refs = set(url_pattern.findall(text))
    missing = [p for p in refs if not (UPLOADS_DIR / p).exists()]
    total_refs += len(refs)
    total_missing += len(missing)
    all_missing.extend((fname, m) for m in missing)
    if refs or missing:
        print(f"{fname:<55} {len(refs):<6} {len(missing):<8}")

print("-" * 75)
print(f"{'TOTAL':<55} {total_refs:<6} {total_missing:<8}")

if all_missing:
    print("\n--- MISSING IMAGES IN IMPORTANT FILES ---")
    for fname, m in all_missing:
        print(f"  {fname}: {m}")
