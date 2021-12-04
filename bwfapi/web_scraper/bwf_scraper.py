import csv
import asyncio
import enum
import timeit
# from db import DBOperator
from scrapers import ProgressBar, TournamentGatherer, AsyncMatchGatherer, Match, PlayerGatherer

class BwfScraper:

    def __init__(self, year, event):
        self.year = year
        self.event = event
        self.tournament_list = {}
        self.match_list = []
        self.player_links = []

    def get_tournament_list(self):
        return self.tournament_list

    def get_match_list(self):
        return self.match_list

    def get_player_list(self):
        return self.player_list

    def scrape_tournaments(self):
        print("Started scraping tournaments...")
        tg = TournamentGatherer()

        start_tournament_scraping = timeit.default_timer()
        tournaments = asyncio.run(tg.grab_tournaments_from_year(self.year))
        end_tournament_scraping = timeit.default_timer()
        print(f"Year: {self.year}\t Count: {str(len(tournaments))}")
        total_tournaments = len(tournaments)

        tournament_time_elapsed = end_tournament_scraping - start_tournament_scraping
        print(f"Finished scraping {total_tournaments} tournaments in {tournament_time_elapsed} seconds.") # should be 546
        self.tournament_list = tournaments
        return {"count": total_tournaments, "time": tournament_time_elapsed}


    def scrape_matches(self):
        # Gathers matches from a set year of tournaments (async)
        print("Started scraping matches...")
        start_Amatch_scraping = timeit.default_timer()

        match_list = []
        tournament_links = [tournament['link'] for tournament in self.tournament_list]
        mg = AsyncMatchGatherer(event=self.event, tournament_list=tournament_links)
        tournament_match_list = asyncio.run(mg.collect_all_match_data())

        match_list = match_list + tournament_match_list

        sorter = AsyncMatchGatherer()
        sorter.sort_match_data2(match_list)
        end_Amatch_scraping = timeit.default_timer()

        Amatch_time_elapsed = end_Amatch_scraping - start_Amatch_scraping
        print(f"Finished scraping {len(match_list)} matches async in {Amatch_time_elapsed} seconds.")

        self.player_links = mg.get_player_links()
        self.match_list = match_list

        return {"count": len(match_list), "time": Amatch_time_elapsed}

    def scrape_players(self):
        print("Started scraping players...")
        start_player_scraping = timeit.default_timer()

        pg = PlayerGatherer(self.player_links)
        asyncio.run(pg.grab_all_players())

        end_player_scraping = timeit.default_timer()
        player_list = pg.get_player_list()

        player_time_elapsed = end_player_scraping - start_player_scraping

        self.player_list = player_list

        print(f"Finished scraping {len(self.player_list)} players async in {player_time_elapsed} seconds.")
        return {"count": len(player_list), "time": player_time_elapsed}


def write_benchmark_headers():
     with open('./bwfapi/benchmarks/scraping.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Year", "Functionality", "Count", "Time in seconds"])

############### BENCHMARKING SECTION #################
if __name__ == "__main__":
    write_benchmark_headers()

    for i in range(2008, 2009):
        scrape = BwfScraper(i, "MS")
        tournament_bm = scrape.scrape_tournaments()
        match_bm = scrape.scrape_matches()
        player_bm = scrape.scrape_players()

        # dboperator = DBOperator()
        
        for tournament in scrape.get_tournament_list():
            print(str(tournament))

        for match in scrape.get_match_list():
            print(str(match))

        for player in scrape.get_player_list():
            print(str(player))

        with open('./bwfapi/benchmarks/scraping.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i, "Tournament Scrape", tournament_bm['count'], tournament_bm['time']])
            writer.writerow([i, "Match Scrape", match_bm['count'], match_bm['time']])
            writer.writerow([i, "Player Scrape", player_bm['count'], player_bm['time']])
    