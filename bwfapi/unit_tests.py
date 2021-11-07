import unittest
import requests
from scrapers.match_gatherer import MatchGatherer 

class testMatchMethods(unittest.TestCase):
    def test_constructor(self):
        self.assertIsInstance(MatchGatherer(), MatchGatherer)
        self.assertIsInstance(MatchGatherer("MS", 2021), MatchGatherer)

        with self.assertRaises(NameError):
            MatchGatherer("asdfg", 2010)
        with self.assertRaises(ValueError):
            MatchGatherer("WS", 2500)

    def test_event(self):
        gatherer = MatchGatherer("ms", 2010)
        self.assertEqual(gatherer.get_event(), "MS")
        
        gatherer = MatchGatherer("mS ", 2010)
        self.assertEqual(gatherer.get_event(), "MS")
        
        gatherer = MatchGatherer("        ws ", 2010)
        self.assertEqual(gatherer.get_event(), "WS")

    def test_year(self):
        gatherer = MatchGatherer("ms", 2010)
        self.assertEqual(gatherer.get_year(), 2010)

        gatherer = MatchGatherer()
        self.assertEqual(gatherer.get_year(), 2022)
    
    def test_draw_link_converter(self):
        gatherer = MatchGatherer()

        val = str(50)
        self.assertEqual(gatherer.convert_to_draws_link(val), f"https://bwf.tournamentsoftware.com/sport/draws.aspx?id={val}")

        val = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.assertEqual(gatherer.convert_to_draws_link(val), f"https://bwf.tournamentsoftware.com/sport/draws.aspx?id={val}")

    def test_matches_link_converter(self):
        gatherer = MatchGatherer()
        
        val = "abcdefghijklmopqrstuvwxyz"
        self.assertEqual(gatherer.convert_to_matches_link(val), f"https://bwf.tournamentsoftware.com/sport/{val[0:4]}matches{val[4:]}")

        val = "zzzzzzz"
        self.assertEqual(gatherer.convert_to_matches_link(val), f"https://bwf.tournamentsoftware.com/sport/{val[0:4]}matches{val[4:]}")

        with self.assertRaises(ValueError):
            gatherer.convert_to_matches_link("a")
    
    def test_name_formatter(self):
        gatherer = MatchGatherer()
        
        self.assertEqual("BRIAN YANG", gatherer.clean_name_formatting("Brian Yang"))
        self.assertEqual("BRIAN YANG", gatherer.clean_name_formatting("Brian Yang [1] "))
        self.assertEqual("BRIAN YANG", gatherer.clean_name_formatting("Brian Yang [QLF] "))
        self.assertEqual("BRIAN YANG", gatherer.clean_name_formatting("     Brian Yang "))
    
    def test_collect_draw_links(self):
        gatherer = MatchGatherer("MS", 2021)
        draws_link = gatherer.convert_to_draws_link("4E6160C1-6ABB-43CF-A535-2F0175C84D7D")
        html_text = requests.get(draws_link).text
        relevant_draws = gatherer.collect_draw_links(html_text, gatherer.get_event())
        self.assertEqual(len(relevant_draws), 1)

        draws_link = gatherer.convert_to_draws_link("595206f6-cafd-41fb-bd2a-87f5655c040c")
        html_text = requests.get(draws_link).text
        relevant_draws = gatherer.collect_draw_links(html_text, gatherer.get_event())
        self.assertEqual(len(relevant_draws), 2)
    
    def test_collect_all_matches(self):
        gatherer = MatchGatherer("MS", 2021)
        matches = gatherer.collect_all_matches("https://bwf.tournamentsoftware.com/sport/drawmatches.aspx?id=595206F6-CAFD-41FB-BD2A-87F5655C040C&draw=2")
        self.assertEqual(len(matches), 31)



    def test_collect_match_data(self):
        gatherer = MatchGatherer("MS", 2021)
        gatherer.collect_match_data("a6128cae-03b8-492c-a398-ad3505e8ec16")
        match_list = gatherer.get_match_list()
        self.assertEqual(len(match_list), 85)

if __name__ == '__main__':
    unittest.main(exit=False)