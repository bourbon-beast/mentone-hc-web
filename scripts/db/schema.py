"""
Mentone Hockey Club records database schema.

Run this script to create a fresh mhc.db with all tables.
Idempotent: drops and recreates tables every run (safe until we have real edits).

Schema philosophy:
- `people` is the single source of truth for human names (deduped across awards)
- `awards` lists every award/honour type once
- `award_winners` is the many-to-many: who won what, in what year
- Premierships, life members, and roles get their own tables since they're shaped differently
- `photos` is separate from people so we can have multiple photos per person over time

To inspect: install "DB Browser for SQLite" (free GUI) and open mhc.db
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "mhc.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


SCHEMA = """
-- People are deduped across the whole DB.
-- One row per distinct human, regardless of how many awards/roles they have.
CREATE TABLE people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_people_slug ON people(slug);


-- Optional photos for people. Multiple photos per person allowed.
CREATE TABLE photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER REFERENCES people(id) ON DELETE CASCADE,
    relative_path TEXT NOT NULL,
    caption TEXT,
    is_primary INTEGER DEFAULT 0,
    source_url TEXT
);
CREATE INDEX idx_photos_person ON photos(person_id);


-- The list of distinct awards/honours the club gives out.
CREATE TABLE awards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    slug TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    display_order INTEGER DEFAULT 0
);
CREATE INDEX idx_awards_category ON awards(category);


-- Who won what, when.
CREATE TABLE award_winners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    award_id INTEGER NOT NULL REFERENCES awards(id) ON DELETE CASCADE,
    person_id INTEGER REFERENCES people(id) ON DELETE SET NULL,
    year INTEGER,
    grade TEXT,
    notes TEXT,
    UNIQUE(award_id, year, person_id)
);
CREATE INDEX idx_winners_award ON award_winners(award_id);
CREATE INDEX idx_winners_person ON award_winners(person_id);
CREATE INDEX idx_winners_year ON award_winners(year);


-- Life members get their own table for curated rendering.
CREATE TABLE life_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL UNIQUE REFERENCES people(id) ON DELETE CASCADE,
    year_inducted INTEGER,
    display_order INTEGER DEFAULT 0,
    notes TEXT
);


-- Premierships: a team won a flag in a year.
CREATE TABLE premierships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    year INTEGER NOT NULL,
    grade TEXT,
    season_type TEXT DEFAULT 'winter',
    notes TEXT,
    UNIQUE(team_name, year, grade, season_type)
);
CREATE INDEX idx_premierships_year ON premierships(year);


-- Executive / committee / coordinator roles over time.
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    role_name TEXT NOT NULL,
    role_category TEXT,
    year_from INTEGER,
    year_to INTEGER,
    notes TEXT
);
CREATE INDEX idx_roles_person ON roles(person_id);
CREATE INDEX idx_roles_year ON roles(year_from);


-- Track what's been ingested for idempotent re-runs.
CREATE TABLE ingest_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    parser_name TEXT NOT NULL,
    rows_inserted INTEGER DEFAULT 0,
    rows_skipped INTEGER DEFAULT 0,
    notes TEXT,
    run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db(db_path: Path = DB_PATH, drop_existing: bool = True) -> sqlite3.Connection:
    """Create a fresh database with the full schema."""
    if drop_existing and db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


if __name__ == "__main__":
    conn = init_db()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    print(f"Created {DB_PATH}")
    print(f"Tables: {', '.join(tables)}")
    conn.close()
