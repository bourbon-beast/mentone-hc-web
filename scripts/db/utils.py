"""
Shared helpers used by every parser.

The most important one is `get_or_create_person` — name dedup logic.
WordPress markdown has the same person under slightly different name variants
(e.g. "Lum Chau" vs "Lum  Chau" vs "Tak Chau" vs "Tak  Chau"), so we normalise
hard and compare on the slug.
"""
import re
import sqlite3
import unicodedata
from typing import Optional


def slugify(text: str) -> str:
    """Convert a name or label to a URL-safe slug.

    Examples:
        "Tak  Chau"            -> "tak-chau"
        "Joshua O'Brien"       -> "joshua-obrien"
        "Mens 1st XI Best"     -> "mens-1st-xi-best"
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    # Strip apostrophes inside words first so "O'Brien" -> "obrien" not "o-brien"
    text = re.sub(r"['\u2019]", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def clean_name(name: str) -> str:
    """Clean up a person's name pulled out of the source markdown."""
    # Strip markdown bold markers, image markup, and HTML-escaped artefacts
    name = re.sub(r"!\[[^\]]*\]\([^\)]+\)", "", name)
    name = re.sub(r"\*+", "", name)
    name = re.sub(r"<[^>]+>", "", name)
    # Collapse internal whitespace
    name = re.sub(r"\s+", " ", name).strip()
    return name


def get_or_create_person(
    conn: sqlite3.Connection, full_name: str, notes: Optional[str] = None
) -> Optional[int]:
    """Insert a person if they don't exist, return their ID.

    Returns None if the name is unusable (empty, sentinel like "No Season").
    Matches existing people by slug, so "Tak Chau" and "Tak  Chau " resolve
    to the same row.
    """
    full_name = clean_name(full_name)
    if not full_name or len(full_name) < 2:
        return None

    # Sentinel values that shouldn't become "people"
    sentinels = {"no season", "no presentation night", "covid", "tba", "tbd"}
    if full_name.lower() in sentinels:
        return None

    slug = slugify(full_name)
    if not slug:
        return None

    cur = conn.cursor()
    row = cur.execute("SELECT id FROM people WHERE slug = ?", (slug,)).fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO people (full_name, slug, notes) VALUES (?, ?, ?)",
        (full_name, slug, notes),
    )
    return cur.lastrowid


def get_or_create_award(
    conn: sqlite3.Connection,
    name: str,
    category: str,
    description: Optional[str] = None,
    display_order: int = 0,
) -> int:
    """Insert an award if it doesn't exist, return its ID."""
    slug = slugify(name)
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM awards WHERE slug = ?", (slug,)).fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO awards (name, slug, category, description, display_order) VALUES (?, ?, ?, ?, ?)",
        (name, slug, category, description, display_order),
    )
    return cur.lastrowid


def log_ingest(
    conn: sqlite3.Connection,
    source_file: str,
    parser_name: str,
    rows_inserted: int = 0,
    rows_skipped: int = 0,
    notes: Optional[str] = None,
) -> None:
    """Record an ingest run for traceability."""
    conn.execute(
        """INSERT INTO ingest_log
           (source_file, parser_name, rows_inserted, rows_skipped, notes)
           VALUES (?, ?, ?, ?, ?)""",
        (source_file, parser_name, rows_inserted, rows_skipped, notes),
    )
