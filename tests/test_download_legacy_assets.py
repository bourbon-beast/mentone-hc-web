"""Regression tests for legacy WordPress asset URL normalization."""
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "download_legacy_assets.py"


def load_downloader():
    spec = importlib.util.spec_from_file_location("download_legacy_assets", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    # Avoid requiring network/requests side effects beyond import.
    spec.loader.exec_module(module)
    return module


class NormalizeDownloadUrlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_downloader()

    def test_wpdev_guid_rewritten_to_live_uploads(self):
        stale = (
            "http://mentonehockey.org.au/wpdev/wp-content/uploads/"
            "Logos/Sponsors_Logos/b1.png"
        )
        self.assertEqual(
            self.mod.normalize_download_url(stale),
            "https://mentonehockey.org.au/wp-content/uploads/"
            "Logos/Sponsors_Logos/b1.png",
        )

    def test_localhost_word_guid_rewritten_to_live_uploads(self):
        stale = "http://localhost/word/wp-content/uploads/2016/12/banner.jpg"
        self.assertEqual(
            self.mod.normalize_download_url(stale),
            "https://mentonehockey.org.au/wp-content/uploads/2016/12/banner.jpg",
        )

    def test_live_https_url_unchanged(self):
        live = (
            "https://mentonehockey.org.au/wp-content/uploads/2023/10/KenPridgett.jpg"
        )
        self.assertEqual(self.mod.normalize_download_url(live), live)

    def test_local_path_same_for_wpdev_and_live(self):
        wpdev = (
            "http://mentonehockey.org.au/wpdev/wp-content/uploads/"
            "2016/12/logo-echo.png"
        )
        live = self.mod.normalize_download_url(wpdev)
        base = Path("/tmp/mhc-uploads-test")
        self.assertEqual(
            self.mod.url_to_local_path(wpdev, base),
            self.mod.url_to_local_path(live, base),
        )


if __name__ == "__main__":
    unittest.main()
