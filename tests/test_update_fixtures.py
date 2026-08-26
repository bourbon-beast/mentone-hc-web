import unittest

from bs4 import BeautifulSoup

from scripts.update_fixtures import parse_fixtures_from_soup


def _match_card(label_html, date_line, venue, venue_href, status, opponent, opp_href, result_html=""):
    return f"""
    <div class="card card-hover mb-4">
      <div class="card-body font-size-sm">
        <div class="row align-items-center">
          <div class="col-lg-5">
            <div class="row align-items-center">
              <div class="col-md">{label_html}<br />{date_line}</div>
              <div class="col-md">
                <a href="{venue_href}">{venue}</a>
              </div>
            </div>
          </div>
          <div class="col-lg-3">
            <div class="text-muted">{status}</div>
            <a href="{opp_href}">{opponent}</a>
            {result_html}
          </div>
        </div>
      </div>
    </div>
    """


ROUND_18 = _match_card(
    "<b>Round 18</b>",
    "Sun 23 Aug 2026 12:30",
    "Mentone Grammar Playing Fields",
    "https://www.hockeyvictoria.org.au/venues/25879/16373",
    "Played",
    "Mens Metro 2 South - 2026 Frankston Hockey Club",
    "https://www.hockeyvictoria.org.au/games/team/25879/412307",
    '<b>3 - 1</b><div class="badge badge-success">Win</div>',
)

ELIMINATION_FINAL = _match_card(
    "<b>Finals</b><div><b>Elimination Final</b></div>",
    "Sun 30 Aug 2026 14:00",
    "Mentone Grammar Playing Fields",
    "https://www.hockeyvictoria.org.au/venues/25879/16373",
    "Playing",
    "Mens Metro 2 South - 2026 Maccabi Hockey Club",
    "https://www.hockeyvictoria.org.au/games/team/25879/412378",
)

GRAND_FINAL = _match_card(
    "<b>Finals</b><div><b>Grand Final</b></div>",
    "Sun 06 Sep 2026 15:00",
    "State Hockey Centre",
    "https://www.hockeyvictoria.org.au/venues/25879/1",
    "Playing",
    "Mens Metro 2 South - 2026 Camberwell Hockey Club",
    "https://www.hockeyvictoria.org.au/games/team/25879/99",
)


class ParseFinalsTests(unittest.TestCase):
    def test_elimination_final_is_kept_alongside_regular_round(self):
        soup = BeautifulSoup(ROUND_18 + ELIMINATION_FINAL, "html.parser")
        fixtures = parse_fixtures_from_soup(soup)
        self.assertEqual(len(fixtures), 2)
        self.assertEqual(fixtures[0]["opponent"], "Frankston Hockey Club")
        self.assertEqual(fixtures[0]["result"], "W")
        final = fixtures[1]
        self.assertEqual(final["date"], "2026-08-30")
        self.assertEqual(final["day"], "Sun")
        self.assertEqual(final["time"], "2:00pm")
        self.assertEqual(final["opponent"], "Maccabi Hockey Club")
        self.assertEqual(final["venue"], "Home")
        self.assertIsNone(final["result"])

    def test_bare_finals_header_does_not_duplicate_the_subtype_card(self):
        soup = BeautifulSoup(ELIMINATION_FINAL, "html.parser")
        fixtures = parse_fixtures_from_soup(soup)
        self.assertEqual(len(fixtures), 1)
        self.assertEqual(fixtures[0]["opponent"], "Maccabi Hockey Club")

    def test_successive_finals_are_not_collapsed(self):
        soup = BeautifulSoup(ELIMINATION_FINAL + GRAND_FINAL, "html.parser")
        fixtures = parse_fixtures_from_soup(soup)
        self.assertEqual(
            [(f["date"], f["opponent"]) for f in fixtures],
            [
                ("2026-08-30", "Maccabi Hockey Club"),
                ("2026-09-06", "Camberwell Hockey Club"),
            ],
        )

    def test_duplicate_round_labels_still_keep_first_hit_only(self):
        soup = BeautifulSoup(ROUND_18 + ROUND_18, "html.parser")
        fixtures = parse_fixtures_from_soup(soup)
        self.assertEqual(len(fixtures), 1)


if __name__ == "__main__":
    unittest.main()
