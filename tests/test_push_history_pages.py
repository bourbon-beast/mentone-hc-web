import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import push_history_pages


class WordPressApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp_dir.name)
        (self.root / '.wp-auth').write_text('user:password', encoding='utf-8')
        self.root_patch = mock.patch.object(push_history_pages, 'ROOT', self.root)
        self.root_patch.start()

    def tearDown(self):
        self.root_patch.stop()
        self.temp_dir.cleanup()

    @mock.patch.object(push_history_pages.subprocess, 'run')
    def test_api_raises_on_http_failure(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=22,
            stdout=b'{"code":"rest_forbidden","message":"Forbidden"}',
            stderr=b'curl: (22) HTTP 403',
        )

        with self.assertRaisesRegex(push_history_pages.WordPressAPIError, 'curl exit 22'):
            push_history_pages.api('/pages')

        self.assertIn('--fail-with-body', run.call_args.args[0])

    @mock.patch.object(push_history_pages.subprocess, 'run')
    def test_api_raises_on_wordpress_error_response(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0,
            stdout=b'{"code":"rest_invalid_param","message":"Invalid parent"}',
            stderr=b'',
        )

        with self.assertRaisesRegex(push_history_pages.WordPressAPIError, 'Invalid parent'):
            push_history_pages.api('/pages', 'POST', {})

    @mock.patch.object(push_history_pages.subprocess, 'run')
    def test_api_raises_on_non_json_response(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=b'<html>Server error</html>', stderr=b''
        )

        with self.assertRaisesRegex(push_history_pages.WordPressAPIError, 'invalid JSON'):
            push_history_pages.api('/pages')


class PagePublishingTests(unittest.TestCase):
    @mock.patch.object(push_history_pages, 'api')
    def test_lookup_failure_cannot_be_treated_as_missing_page(self, api):
        api.return_value = {'unexpected': 'response'}

        with self.assertRaisesRegex(push_history_pages.WordPressAPIError, 'not a list'):
            push_history_pages.find_page('history', 0)

    @mock.patch.object(push_history_pages, 'api')
    def test_invalid_upsert_response_stops_publishing(self, api):
        api.side_effect = [[], {'status': 'publish', 'slug': 'history'}]

        with self.assertRaisesRegex(push_history_pages.WordPressAPIError, 'failed validation'):
            push_history_pages.upsert('history', 0, 'History', '<p>History</p>', 0)

    def test_child_requires_successfully_published_parent(self):
        with self.assertRaisesRegex(push_history_pages.WordPressAPIError, 'was not published'):
            push_history_pages.resolve_parent_id({'history': None}, 'history')

        self.assertEqual(
            push_history_pages.resolve_parent_id({'history': 123}, 'history'),
            123,
        )


if __name__ == '__main__':
    unittest.main()
