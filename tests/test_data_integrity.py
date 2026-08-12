import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DataIntegrityTests(unittest.TestCase):
    def test_site_json_files_parse(self):
        for filename in ("news.json", "fixtures.json"):
            with self.subTest(filename=filename):
                with (ROOT / filename).open(encoding="utf-8") as handle:
                    json.load(handle)

    def test_fixture_result_codes_have_renderer_classes(self):
        with (ROOT / "fixtures.json").open(encoding="utf-8") as handle:
            fixtures = json.load(handle)

        result_codes = {
            fixture["result"]
            for section in fixtures["sections"]
            for grade in section["grades"]
            for fixture in grade["fixtures"]
            if fixture.get("result") in {"W", "L", "D"}
        }

        fixtures_html = (ROOT / "fixtures.html").read_text(encoding="utf-8")
        mapping_match = re.search(
            r"const resultClassByCode = \{(?P<body>[^}]+)\};",
            fixtures_html,
        )
        self.assertIsNotNone(mapping_match, "fixtures renderer must map scraped result codes")

        rendered_classes = dict(
            re.findall(r"\b([WLD]):\s*'([^']+)'", mapping_match.group("body"))
        )
        self.assertEqual(
            {"W": "win", "L": "loss", "D": "draw"},
            {code: rendered_classes.get(code) for code in ("W", "L", "D")},
        )
        self.assertLessEqual(result_codes, rendered_classes.keys())


if __name__ == "__main__":
    unittest.main()
