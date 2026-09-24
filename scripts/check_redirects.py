"""Check every row of docs/redirects.md against the live site.

Usage:
    python scripts/check_redirects.py            # all rows (incl. flat-slug variants)
    python scripts/check_redirects.py --cutover  # also check "Cutover only" rows

Per row: GET the old path without following redirects -> expect 301 to the mapped
destination; then GET the destination -> expect 200. Prefix rows are checked with
a sample path under the prefix. Before cutover, a destination of "/" still 301s to
revolutioniseSPORT - that's reported as PRE-CUTOVER, not a failure.

Exit code 1 if any row fails.
"""
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_redirects import expand, parse  # noqa: E402

BASE = "https://mentonehockey.org.au"
REVSPORT = "https://www.revolutionise.com.au/mentonehockey/"
UA = {"User-Agent": "mentone-redirect-check/1.0"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


opener = urllib.request.build_opener(NoRedirect)


def fetch(path):
    req = urllib.request.Request(BASE + path, headers=UA, method="GET")
    try:
        r = opener.open(req, timeout=20)
        return r.status, r.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", "")


def main():
    cutover = "--cutover" in sys.argv
    pairs = expand(parse(include_cutover=cutover))
    dest_cache, fails, pre = {}, 0, 0
    for old, new, kind in pairs:
        probe = old + ("sample-path/" if kind == "prefix" and old.endswith("/") else "sample" if kind == "prefix" else "")
        status, loc = fetch(probe)
        want = BASE + new
        if status == 301 and loc.rstrip("/") == want.rstrip("/"):
            if new not in dest_cache:
                dest_cache[new] = fetch(new)
            ds, dloc = dest_cache[new]
            if ds == 200:
                result = "OK"
            elif new == "/" and ds == 301 and dloc == REVSPORT:
                result, pre = "PRE-CUTOVER", pre + 1
            else:
                result, fails = f"DEST {ds}", fails + 1
        else:
            result, fails = f"FAIL {status} -> {loc or '-'}", fails + 1
        print(f"{result:<14} {probe}  ->  {new}")
    print(f"\n{len(pairs)} checked, {fails} failing" + (f", {pre} waiting on cutover" if pre else ""))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
