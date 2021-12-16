import csv
import asyncio
import timeit
import time
from db import DBOperator
from scrapers import TournamentGatherer, AsyncMatchGatherer, Match, PlayerGatherer

class BwfScraper:
    def __init__(self, year, event):
        self.year = year
        self.event = event
        self.tournament_list = {}
        self.match_list = []
        self.player_links = []
        self.pg = None

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
        print("Started scraping matches...")
        start_Amatch_scraping = timeit.default_timer()

        tournament_links = [tournament['link'] for tournament in self.tournament_list]
        mg = AsyncMatchGatherer(event=self.event, tournament_list=tournament_links)
        tournament_match_list = asyncio.run(mg.collect_all_match_data())
        mg.sort_match_data2(tournament_match_list)

        end_Amatch_scraping = timeit.default_timer()
        Amatch_time_elapsed = end_Amatch_scraping - start_Amatch_scraping
        print(f"Finished scraping {len(tournament_match_list)} matches in {Amatch_time_elapsed} seconds.")

        self.player_links = mg.get_player_links()
        self.match_list = tournament_match_list

        return {"count": len(tournament_match_list), "time": Amatch_time_elapsed}

    def scrape_players(self):
        print("Started scraping players...")
        start_player_scraping = timeit.default_timer()

        self.pg = PlayerGatherer(self.player_links)
        asyncio.run(self.pg.grab_all_players())

        end_player_scraping = timeit.default_timer()
        player_time_elapsed = end_player_scraping - start_player_scraping

        print(f"Finished scraping {len(self.pg.get_player_list())} players in {player_time_elapsed} seconds.")

        return {"count": len(self.pg.get_player_list()), "time": player_time_elapsed}
    
    def scrape_players_info(self):
        print("Started scraping player info...")
        start_info_scraping = timeit.default_timer()
        
        asyncio.run(self.pg.grab_all_player_info())
        
        end_info_scraping = timeit.default_timer()
        info_time_elapsed = end_info_scraping - start_info_scraping

        self.player_list = self.pg.get_player_list()
        print(f"Finished scraping {len(self.player_list)} player infos in {info_time_elapsed} seconds.")

        return {"count": len(self.player_list), "time": info_time_elapsed}
    
    def change_names_to_ids(self):
        for match in self.match_list:
            if match.get_winner().strip() in self.player_list:
                match.set_winner(self.player_list[match.get_winner().strip()]['id'])
            else:
                print(f"Couldn't find {match.get_winner()}")

            if match.get_loser().strip() in self.player_list:
                match.set_loser(self.player_list[match.get_loser().strip()]['id'])
            else:
                print(f"Couldn't find {match.get_loser()}")

    def record_scraping_benchmarks(self, tournament_bm, match_bm, player_bm, player_info_bm):
        with open('./bwfapi/benchmarks/scraping.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.year, self.event, "Tournament Scrape", tournament_bm['count'], tournament_bm['time']])
            writer.writerow([self.year, self.event, "Match Scrape", match_bm['count'], match_bm['time']])
            writer.writerow([self.year, self.event, "Player Scrape", player_bm['count'], player_bm['time']])
            writer.writerow([self.year, self.event, "Player Info Scrape", player_info_bm['count'], player_info_bm['time']])

    def scrape(self):
        tournament_bm = self.scrape_tournaments()
        match_bm = self.scrape_matches()
        player_bm = self.scrape_players()
        player_info_bm = self.scrape_players_info()
        self.change_names_to_ids()
        self.record_scraping_benchmarks(tournament_bm, match_bm, player_bm, player_info_bm)

def write_benchmark_headers():
     with open('./bwfapi/benchmarks/scraping.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Year", "Event", "Functionality", "Count", "Time in seconds"])

def scrape_matches(event, year):
    scraper = BwfScraper(year, event)
    scraper.scrape()
    dboperator = DBOperator()

    dboperator.insert_tournaments(scraper.get_tournament_list()) #works
    dboperator.commit()
    
    dboperator.insert_players(scraper.get_player_list())  # works
    dboperator.commit()

    dboperator.insert_match_and_sets(scraper.get_match_list()) #works
    dboperator.commit()

    dboperator.close()

############### MAIN SCRAPER SECTION #################
if __name__ == "__main__":
    write_benchmark_headers()
    dboperator = DBOperator()
    dboperator.reset_database()
    dboperator.close()

    for year in range(2008, 2022):
        scrape_matches("MS", year)
        time.sleep(5)
        scrape_matches("WS", year)
