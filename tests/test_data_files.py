import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class DataFileTests(unittest.TestCase):
    def test_static_json_feeds_are_valid(self):
        for filename in ("fixtures.json", "news.json"):
            with self.subTest(filename=filename):
                with open(REPO_ROOT / filename, encoding="utf-8") as fh:
                    json.load(fh)


if __name__ == "__main__":
    unittest.main()
