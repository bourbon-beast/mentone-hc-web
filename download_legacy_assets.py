"""
Download all legacy assets from the old Mentone Hockey Club WordPress site
before it gets shut down.

Run from the project root:
    python download_legacy_assets.py

What it does:
1. Auto-creates legacy-content/ and legacy-content/uploads/ if missing
2. Reads _attachments.json (914 attachments from the WP database)
3. Reads _image_urls_in_pages.txt (172 inline image URLs)
4. Downloads each one to legacy-content/uploads/<year>/<month>/<filename>
   (preserves the WordPress folder structure)
5. Skips files that already exist (safe to re-run)
6. Logs successes & failures to download_log.txt
7. Reports a summary at the end

Tested on: Python 3.9+
Dependencies: requests (pip install requests)
"""

import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run:  pip install requests")
    sys.exit(1)

# ──────────────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.resolve()
LEGACY_DIR = PROJECT_ROOT / "legacy-content"
ATTACHMENTS_JSON = LEGACY_DIR / "_attachments.json"
EXTRA_URLS_FILE = LEGACY_DIR / "_image_urls_in_pages.txt"
DOWNLOAD_DIR = LEGACY_DIR / "uploads"
LOG_FILE = LEGACY_DIR / "download_log.txt"

# Be polite — small delay between requests
DELAY_SECONDS = 0.15
TIMEOUT_SECONDS = 30
USER_AGENT = "Mozilla/5.0 (MentoneHC-legacy-backup/1.0)"

# ──────────────────────────────────────────────────────────────────────────────


def ensure_folders():
    """Create all required folders if they don't exist."""
    created = []
    for folder in (LEGACY_DIR, DOWNLOAD_DIR):
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            created.append(folder)
    if created:
        print("Created folders:")
        for f in created:
            print(f"  {f}")
    else:
        print("All folders already present.")


def log(msg, file_handle=None):
    """Print to console AND write to log file if provided."""
    print(msg)
    if file_handle:
        file_handle.write(msg + "\n")
        file_handle.flush()


def url_to_local_path(url, base_dir):
    """
    Convert a wp-content/uploads URL to a local path that preserves structure.

    https://mentonehockey.org.au/wp-content/uploads/2023/10/KenPridgett.jpg
        -> base_dir/2023/10/KenPridgett.jpg
    """
    parsed = urlparse(url)
    path = parsed.path
    marker = "/wp-content/uploads/"
    if marker in path:
        rel = path.split(marker, 1)[1]
    else:
        # Just use the filename if structure is unknown
        rel = path.lstrip("/")
    return base_dir / rel


def download_one(session, url, local_path):
    """Download a single URL. Returns ('downloaded' | 'skipped' | 'failed', detail)."""
    if local_path.exists() and local_path.stat().st_size > 0:
        return ("skipped", f"exists ({local_path.stat().st_size:,} bytes)")

    local_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = session.get(url, timeout=TIMEOUT_SECONDS, stream=True)
        if response.status_code != 200:
            return ("failed", f"HTTP {response.status_code}")

        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return ("downloaded", f"{local_path.stat().st_size:,} bytes")
    except requests.exceptions.RequestException as e:
        # Clean up partial file if any
        if local_path.exists():
            try:
                local_path.unlink()
            except OSError:
                pass
        return ("failed", str(e))


def collect_urls():
    """Collect all URLs to download from both sources, deduplicated."""
    urls = set()

    # Source 1: WP attachments (from the database)
    if ATTACHMENTS_JSON.exists():
        with open(ATTACHMENTS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            guid = item.get("guid")
            if guid and guid.startswith("http"):
                urls.add(guid)
        print(f"  Loaded {len(data)} URLs from _attachments.json")
    else:
        print(f"  WARNING: {ATTACHMENTS_JSON} not found - skipping attachments")

    # Source 2: image URLs referenced inside page content
    if EXTRA_URLS_FILE.exists():
        before = len(urls)
        with open(EXTRA_URLS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("http"):
                    urls.add(line)
        added = len(urls) - before
        print(f"  Added {added} extra URLs from _image_urls_in_pages.txt")
    else:
        print(f"  WARNING: {EXTRA_URLS_FILE} not found - skipping inline URLs")

    return sorted(urls)


def main():
    print("=" * 60)
    print("Mentone HC - Legacy WordPress assets downloader")
    print("=" * 60)
    print(f"Project root:  {PROJECT_ROOT}")
    print(f"Saving to:     {DOWNLOAD_DIR}")
    print()

    # Make sure folders exist
    ensure_folders()
    print()

    # Check we have at least one source of URLs
    if not ATTACHMENTS_JSON.exists() and not EXTRA_URLS_FILE.exists():
        print(f"ERROR: Neither {ATTACHMENTS_JSON.name} nor {EXTRA_URLS_FILE.name}")
        print(f"       were found in {LEGACY_DIR}")
        print()
        print("Make sure you've extracted legacy-content.zip so the JSON/TXT files")
        print("sit directly inside the legacy-content/ folder.")
        sys.exit(1)

    print("Collecting URLs to download...")
    urls = collect_urls()
    print(f"  Total unique URLs: {len(urls)}")
    print()

    if not urls:
        print("Nothing to download.")
        return

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    stats = {"downloaded": 0, "skipped": 0, "failed": 0}
    failures = []
    total = len(urls)

    with open(LOG_FILE, "w", encoding="utf-8") as log_fh:
        log_fh.write(f"Mentone HC legacy download log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_fh.write("=" * 60 + "\n\n")

        for i, url in enumerate(urls, 1):
            local_path = url_to_local_path(url, DOWNLOAD_DIR)
            status, detail = download_one(session, url, local_path)
            stats[status] += 1

            marker = {"downloaded": "[OK]", "skipped": "[--]", "failed": "[XX]"}[status]
            line = f"[{i:>4}/{total}] {marker} {url}"

            if status == "failed":
                failures.append((url, detail))
                log(f"{line}  ->  FAILED: {detail}", log_fh)
            elif i % 10 == 0 or i == total:
                log(f"{line}  ->  {status}: {detail}", log_fh)
            else:
                log_fh.write(f"{line}  ->  {status}: {detail}\n")

            if status == "downloaded":
                time.sleep(DELAY_SECONDS)

    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"  Downloaded:  {stats['downloaded']}")
    print(f"  Skipped:     {stats['skipped']}  (already existed)")
    print(f"  Failed:      {stats['failed']}")
    print()
    print(f"Files saved to:   {DOWNLOAD_DIR}")
    print(f"Full log:         {LOG_FILE}")

    if failures:
        print()
        print(f"  {len(failures)} failure(s) - first 10:")
        for url, err in failures[:10]:
            print(f"    {url}")
            print(f"      -> {err}")
        if len(failures) > 10:
            print(f"    ...and {len(failures) - 10} more (see download_log.txt)")


if __name__ == "__main__":
    main()