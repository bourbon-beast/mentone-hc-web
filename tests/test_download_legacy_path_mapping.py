"""Regression tests for legacy asset local path mapping."""
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "download_legacy_assets.py"


def load_downloader():
    spec = importlib.util.spec_from_file_location("download_legacy_assets", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UrlToLocalPathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_downloader()

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.base = Path(self._tmpdir.name) / "uploads"
        self.base.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_double_slash_uploads_stays_under_base_dir(self):
        """Guids with /uploads//file must not escape to filesystem root."""
        url = (
            "http://mentonehockey.org.au/wp-content/uploads//IMG_0130-edited.jpg"
        )
        local = self.mod.url_to_local_path(url, self.base)
        self.assertEqual(local, (self.base / "IMG_0130-edited.jpg").resolve())
        self.assertTrue(str(local).startswith(str(self.base.resolve())))
        self.assertNotEqual(local, Path("/IMG_0130-edited.jpg"))

    def test_normal_year_month_path_preserved(self):
        url = (
            "https://mentonehockey.org.au/wp-content/uploads/2023/10/KenPridgett.jpg"
        )
        local = self.mod.url_to_local_path(url, self.base)
        self.assertEqual(
            local, (self.base / "2023" / "10" / "KenPridgett.jpg").resolve()
        )

    def test_parent_segment_rejected(self):
        url = "https://mentonehockey.org.au/wp-content/uploads/../../etc/passwd"
        with self.assertRaises(ValueError):
            self.mod.url_to_local_path(url, self.base)


if __name__ == "__main__":
    unittest.main()
