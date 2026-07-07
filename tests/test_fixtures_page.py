from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class FixturesPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (REPO_ROOT / "fixtures.html").read_text(encoding="utf-8")

    def test_result_renderer_handles_scraper_result_letters(self):
        split_index = self.html.index("const parts = result.split('-').map(Number);")

        self.assertLess(self.html.index("if (result === 'W')"), split_index)
        self.assertLess(self.html.index("if (result === 'L')"), split_index)
        self.assertLess(self.html.index("if (result === 'D')"), split_index)


if __name__ == "__main__":
    unittest.main()
