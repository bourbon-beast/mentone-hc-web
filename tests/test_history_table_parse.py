"""Regression tests for honour-board markdown table parsing / rendering."""
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import generate_history_pages as g


PRESIDENTS_CUP = """
Year | Team | Coach | Captain | Position
---|---|---|---|---
2013 |  |  |  |
2014 | Men's Masters First XI (MM35A) |  | Mark Evans | Premier
2022 | Women's Masters First XI (WM35A) |  | Gina Leahy | Second
2023 | Men's Pennant D South East | Callen Paulauskas |  | Premiers
"""

EXECUTIVE = """
Year | President | Vice President | Secretary | Treasurer
---|---|---|---|---
1977 | Murray Hines |  | Stuart Hines | Stuart Hines
1984 | Anthony Dayton |  | Allan Munt | John Sword
"""

COORDINATORS = """
Year | Men's | Women's | Junior | Men's Masters | Women's Masters
---|---|---|---|---|---
2001 |  |  |  |  |
2003 |  |  | Lin Cooper | Rod Tansey |
2005 | Sam Gledhill | Brenda Boucher | Gillian Simmonds | Mik Becker |
"""


class ParseTableTests(unittest.TestCase):
    def test_preserves_empty_cells_without_shifting_columns(self):
        rows, headers = g.parse_table(PRESIDENTS_CUP)
        self.assertEqual(headers, ["year", "team", "coach", "captain", "position"])

        by_year = {r["year"]: r for r in rows}
        self.assertNotIn("2013", by_year)  # entirely empty data columns

        r2014 = by_year["2014"]
        self.assertEqual(r2014["coach"], "")
        self.assertEqual(r2014["captain"], "Mark Evans")
        self.assertEqual(r2014["position"], "Premier")

        r2023 = by_year["2023"]
        self.assertEqual(r2023["coach"], "Callen Paulauskas")
        self.assertEqual(r2023["captain"], "")
        self.assertEqual(r2023["position"], "Premiers")

    def test_executive_empty_vice_president_does_not_absorb_secretary(self):
        rows, headers = g.parse_table(EXECUTIVE)
        self.assertEqual(
            headers,
            ["year", "president", "vice president", "secretary", "treasurer"],
        )
        r = {row["year"]: row for row in rows}["1977"]
        self.assertEqual(r["president"], "Murray Hines")
        self.assertEqual(r["vice president"], "")
        self.assertEqual(r["secretary"], "Stuart Hines")
        self.assertEqual(r["treasurer"], "Stuart Hines")

        r1984 = {row["year"]: row for row in rows}["1984"]
        self.assertEqual(r1984["secretary"], "Allan Munt")
        self.assertEqual(r1984["treasurer"], "John Sword")

    def test_keeps_rows_when_first_data_column_empty_but_later_filled(self):
        rows, _ = g.parse_table(COORDINATORS)
        by_year = {r["year"]: r for r in rows}
        self.assertNotIn("2001", by_year)
        self.assertEqual(by_year["2003"]["junior"], "Lin Cooper")
        self.assertEqual(by_year["2003"]["men's"], "")
        self.assertEqual(by_year["2003"]["men's masters"], "Rod Tansey")


class RenderTableTests(unittest.TestCase):
    def test_multi_column_boards_use_source_headers(self):
        rows, headers = g.parse_table(EXECUTIVE)
        header_html = g.table_header_html(headers)
        self.assertIn("President", header_html)
        self.assertIn("Vice President", header_html)
        self.assertNotIn(">Player<", header_html)
        self.assertNotIn(">Grade<", header_html)

        body = g.table_rows_html(rows, headers)
        self.assertIn("<td class=\"year\">1977</td>", body)
        self.assertIn("<td></td><td>Stuart Hines</td><td>Stuart Hines</td>", body)
        self.assertNotIn("grade-pill", body)

    def test_best_and_fairest_tables_keep_player_grade_shape(self):
        md = """
Year | Player | Grade
---|---|---
1977 | Larry Rydqvist | A5
"""
        rows, headers = g.parse_table(md)
        self.assertTrue(g.is_best_and_fairest_table(headers))
        body = g.table_rows_html(rows, headers)
        self.assertIn('class="player"', body)
        self.assertIn("grade-pill", body)

    def test_live_presidents_cup_page_not_shifted(self):
        html = (ROOT / "history" / "honour-boards" / "presidents-cup.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("<th>Coach</th>", html)
        # 2014: empty coach, Mark Evans remains captain, Premier remains position.
        self.assertRegex(
            html,
            r"<tr><td>2014</td><td>Men.s Masters First XI \(MM35A\)</td>"
            r"<td></td><td>Mark Evans</td><td>Premier</td></tr>",
        )

    def test_live_executive_page_has_full_office_columns(self):
        html = (ROOT / "history" / "honour-boards" / "executive.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("<th>President</th>", html)
        self.assertIn("<th>Vice President</th>", html)
        self.assertIn("<th>Secretary</th>", html)
        self.assertIn("<th>Treasurer</th>", html)
        self.assertNotIn("<th>Player</th>", html)
        self.assertRegex(
            html,
            r"<tr><td class=\"year\">1977</td><td>Murray Hines</td>"
            r"<td></td><td>Stuart Hines</td><td>Stuart Hines</td></tr>",
        )


if __name__ == "__main__":
    unittest.main()
