import unittest

from generate_history_pages import full_table_rows_html, parse_table


class HistoryTableParsingTests(unittest.TestCase):
    def test_parse_table_preserves_blank_middle_cells(self):
        rows, headers = parse_table(
            "Year | President | Vice President | Secretary | Treasurer\n"
            "---|---|---|---|---\n"
            "1977 | Murray Hines |  | Stuart Hines | Stuart Hines\n"
        )

        self.assertEqual(
            headers,
            ["year", "president", "vice president", "secretary", "treasurer"],
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["president"], "Murray Hines")
        self.assertEqual(rows[0]["vice president"], "")
        self.assertEqual(rows[0]["secretary"], "Stuart Hines")
        self.assertEqual(rows[0]["treasurer"], "Stuart Hines")

    def test_full_table_rows_render_all_columns(self):
        rows, headers = parse_table(
            "Year | Men's | Women's | Junior | Men's Masters | Women's Masters\n"
            "---|---|---|---|---|---\n"
            "2003 |  |  | Lin Cooper | Rod Tansey | \n"
        )

        html = full_table_rows_html(rows, headers)

        self.assertIn('<td class="year">2003</td>', html)
        self.assertIn('<td class="player"></td>', html)
        self.assertIn("<td>Lin Cooper</td>", html)
        self.assertIn("<td>Rod Tansey</td>", html)
        self.assertEqual(html.count("<td"), 6)


if __name__ == "__main__":
    unittest.main()
