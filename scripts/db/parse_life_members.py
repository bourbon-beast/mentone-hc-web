"""
Parser for the life members page.

Source: legacy-content/markdown/462_life-members.md
Format: Markdown table with bold names, some prefixed with an image markdown link.

The page is a 4-column grid with one person per cell. We just extract every name
from the table, dedupe, and insert into life_members.

Example row format:
    **Margaret Rattle** | **William Burton** | **Marilyn Neary** | **Jan Higgins**
    ...
    **![](https://...KenPridgett.jpg)****Ken Pridgett** | ...
"""
import re
import sys
from pathlib import Path
from typing import Optional

# Make sibling imports work whether we run as a module or directly
sys.path.insert(0, str(Path(__file__).parent.parent))
from db.schema import init_db, DB_PATH  # noqa: E402
from db.utils import (  # noqa: E402
    clean_name,
    get_or_create_person,
    log_ingest,
)


SOURCE = Path(__file__).parent.parent.parent / "legacy-content" / "markdown" / "462_life-members.md"

IMG_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def parse_life_members(text: str) -> list[dict]:
    """Extract life members from the markdown.

    Strategy: split on table separators, treat each cell as one member.
    Cells look like:  **Name**                          (plain)
                  or: **![](url)****Name**              (image + name)
                  or: ****![](url)******Some Name**     (extra asterisks, source data noise)

    Returns: list of dicts with keys: name, image_url (optional).
    """
    members = []
    seen_names = set()

    # Skip the intro paragraph & header separator row
    lines = text.splitlines()
    cells = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        # Tables are pipe-separated. A cell with no pipes is intro/outro text.
        if "|" not in line:
            continue
        cells.extend(part.strip() for part in line.split("|"))

    for cell in cells:
        if not cell:
            continue

        # Pull out image URL if present, then strip the image markup
        img_match = IMG_PATTERN.search(cell)
        image_url = img_match.group(1) if img_match else None
        cell_no_img = IMG_PATTERN.sub("", cell)

        # Strip ALL asterisks but use them as a word boundary first.
        # The source has "Alan****Munt" (4 asterisks mid-name) which should be "Alan Munt".
        # Any run of 2+ asterisks between word chars implies a space got eaten.
        cell_no_img = re.sub(r"(\w)\*{2,}(\w)", r"\1 \2", cell_no_img)
        name = cell_no_img.replace("*", "").strip()
        name = clean_name(name)

        if not name or len(name) < 3:
            continue
        if name.lower() in {"life members"}:
            continue
        if name in seen_names:
            continue
        seen_names.add(name)

        members.append({"name": name, "image_url": image_url})

    return members


def wp_url_to_local_path(url: str) -> Optional[Path]:
    """Map a WordPress upload URL to its local file in legacy-content/uploads."""
    m = re.search(r"wp-content/uploads/(.+)$", url)
    if not m:
        return None
    local = Path(__file__).parent.parent.parent / "legacy-content" / "uploads" / m.group(1)
    return local if local.exists() else None


def ingest(verbose: bool = True) -> None:
    text = SOURCE.read_text(encoding="utf-8")
    members = parse_life_members(text)

    conn = init_db(drop_existing=True)
    inserted = 0
    skipped = 0

    for idx, member in enumerate(members):
        person_id = get_or_create_person(conn, member["name"])
        if person_id is None:
            skipped += 1
            continue

        # Insert into life_members
        try:
            conn.execute(
                "INSERT INTO life_members (person_id, display_order) VALUES (?, ?)",
                (person_id, idx),
            )
        except Exception as e:
            if verbose:
                print(f"  WARN: could not insert life member {member['name']}: {e}")
            skipped += 1
            continue

        # Link photo if we have one and the local file exists
        if member["image_url"]:
            local = wp_url_to_local_path(member["image_url"])
            if local:
                rel_path = f"assets/photos/people/{local.name}"
                conn.execute(
                    """INSERT INTO photos (person_id, relative_path, is_primary, source_url)
                       VALUES (?, ?, 1, ?)""",
                    (person_id, rel_path, member["image_url"]),
                )

        inserted += 1

    log_ingest(
        conn,
        source_file=SOURCE.name,
        parser_name="parse_life_members",
        rows_inserted=inserted,
        rows_skipped=skipped,
    )
    conn.commit()

    if verbose:
        print(f"Parsed {len(members)} entries from {SOURCE.name}")
        print(f"  Inserted: {inserted}")
        print(f"  Skipped:  {skipped}")
        print()
        print("--- Life members in DB ---")
        cur = conn.execute(
            """SELECT p.full_name,
                      (SELECT relative_path FROM photos WHERE person_id = p.id AND is_primary = 1) AS photo
               FROM life_members lm
               JOIN people p ON p.id = lm.person_id
               ORDER BY lm.display_order"""
        )
        for full_name, photo in cur.fetchall():
            marker = "[photo]" if photo else "       "
            print(f"  {marker} {full_name}")

    conn.close()


if __name__ == "__main__":
    ingest()
