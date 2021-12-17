import csv
import asyncio
import timeit
import time
from .db import DBOperator
from .scrapers import TournamentGatherer, AsyncMatchGatherer, Match, PlayerGatherer
from .services import EchoService

class BwfScraper:
    def __init__(self, year=0, event="MS"):
        self.year = year
        self.event = event
        self.tournament_list = {}
        self.match_list = []
        self.player_links = []
        self.player_list = {}
        self.pg = None

    def get_tournament_list(self):
        return self.tournament_list

    def get_match_list(self):
        return self.match_list

    def get_player_list(self):
        return self.player_list

    def scrape_year_tournaments(self):
        print("Started scraping tournaments...")
        tg = TournamentGatherer()

        start_tournament_scraping = timeit.default_timer()
        tournaments = asyncio.run(tg.grab_tournaments_from_year(self.year))
        end_tournament_scraping = timeit.default_timer()
        # print(f"Year: {self.year}\t Count: {str(len(tournaments))}")
        total_tournaments = len(tournaments)

        tournament_time_elapsed = end_tournament_scraping - start_tournament_scraping
        print(f"Finished scraping {total_tournaments} tournaments in {tournament_time_elapsed} seconds.") # should be 546
        self.tournament_list = tournaments
        return {"count": total_tournaments, "time": tournament_time_elapsed}

    async def scrape_current_month_tournaments(self):
        EchoService.echo(f"Started scraping tournaments from current month")
        # print("Started scraping tournaments...")
        tg = TournamentGatherer()

        start_tournament_scraping = timeit.default_timer()
        EchoService.echo(f"aaaa")
        tournaments = await tg.grab_tournaments_from_current_month()
        EchoService.echo(f"aaaa")
        end_tournament_scraping = timeit.default_timer()
        print(f"Year: {self.year}\t Count: {str(len(tournaments))}")
        total_tournaments = len(tournaments)

        tournament_time_elapsed = end_tournament_scraping - start_tournament_scraping
        EchoService.echo(f"Finished scraping {total_tournaments} tournaments in {tournament_time_elapsed} seconds.")
        # print(f"Finished scraping {total_tournaments} tournaments in {tournament_time_elapsed} seconds.") # should be 546
        self.tournament_list = tournaments
        return {"count": total_tournaments, "time": tournament_time_elapsed}

    async def scrape_matches(self):
        EchoService.echo(f"Started scraping matches...")
        # print("Started scraping matches...")
        start_Amatch_scraping = timeit.default_timer()

        tournament_links = [tournament['link'] for tournament in self.tournament_list]
        mg_mens = AsyncMatchGatherer(event="MS", tournament_list=tournament_links)
        tournament_match_list = await mg_mens.collect_all_match_data()

        mg_womens = AsyncMatchGatherer(event="WS", tournament_list=tournament_links)
        tournament_match_list = tournament_match_list + await mg_womens.collect_all_match_data()

        AsyncMatchGatherer.sort_match_data2(tournament_match_list)

        end_Amatch_scraping = timeit.default_timer()
        Amatch_time_elapsed = end_Amatch_scraping - start_Amatch_scraping
        EchoService.echo(f"Finished scraping {len(tournament_match_list)} matches in {Amatch_time_elapsed} seconds.")
        # print(f"Finished scraping {len(tournament_match_list)} matches in {Amatch_time_elapsed} seconds.")

        self.player_links = mg_mens.get_player_links() + mg_womens.get_player_links()
        self.match_list = tournament_match_list

        return {"count": len(tournament_match_list), "time": Amatch_time_elapsed}

    async def scrape_players(self):
        EchoService.echo(f"Started scraping players...")
        # print("Started scraping players...")
        start_player_scraping = timeit.default_timer()

        self.pg = PlayerGatherer(self.player_links)
        await self.pg.grab_all_players()
        end_player_scraping = timeit.default_timer()
        player_time_elapsed = end_player_scraping - start_player_scraping

        EchoService.echo(f"Finished scraping {len(self.pg.get_player_list())} players in {player_time_elapsed} seconds.")
        # print(f"Finished scraping {len(self.pg.get_player_list())} players in {player_time_elapsed} seconds.")

        return {"count": len(self.pg.get_player_list()), "time": player_time_elapsed}
    
    async def scrape_players_info(self):
        EchoService.echo(f"Started scraping player info...")
        # print("Started scraping player info...")
        start_info_scraping = timeit.default_timer()
        
        await self.pg.grab_all_player_info()
        
        end_info_scraping = timeit.default_timer()
        info_time_elapsed = end_info_scraping - start_info_scraping

        self.player_list = self.pg.get_player_list()
        EchoService.echo(f"Finished scraping {len(self.player_list)} player infos in {info_time_elapsed} seconds.")
        # print(f"Finished scraping {len(self.player_list)} player infos in {info_time_elapsed} seconds.")

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

    async def scrape_current_month(self):
        try:
            await self.scrape_current_month_tournaments()
            await self.scrape_matches()
            await self.scrape_players()
            await self.scrape_players_info()
            self.change_names_to_ids()
        except:
            print("sad")
        # self.record_scraping_benchmarks(tournament_bm, match_bm, player_bm, player_info_bm)

    def scrape_year(self):
        tournament_bm = self.scrape_year_tournaments()
        match_bm = self.scrape_matches()
        player_bm = self.scrape_players()
        player_info_bm = self.scrape_players_info()
        self.change_names_to_ids()
        # self.record_scraping_benchmarks(tournament_bm, match_bm, player_bm, player_info_bm)

def write_benchmark_headers():
     with open('./bwfapi/benchmarks/scraping.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Year", "Event", "Functionality", "Count", "Time in seconds"])

def scrape_year_matches(event, year):
    scraper = BwfScraper(year, event)
    scraper.scrape_year()
    dboperator = DBOperator()

    dboperator.insert_tournaments(scraper.get_tournament_list()) #works
    dboperator.commit()
    
    dboperator.insert_players(scraper.get_player_list())  # works
    dboperator.commit()

    dboperator.insert_match_and_sets(scraper.get_match_list()) #works
    dboperator.commit()

    dboperator.close()

async def scrape_current_month_matches():
    scraper = BwfScraper()
    await scraper.scrape_current_month()
    dboperator = DBOperator()

    dboperator.insert_tournaments(scraper.get_tournament_list()) #works
    dboperator.commit()
    
    dboperator.insert_players(scraper.get_player_list())  # works
    dboperator.commit()

    dboperator.insert_match_and_sets(scraper.get_match_list()) #works
    dboperator.commit()

    dboperator.close()
    return {"message": "success"}

def lol(event, year):
    print(f"{event} {year}")

############### MAIN SCRAPER SECTION #################
if __name__ == "__main__":
    # write_benchmark_headers()
    dboperator = DBOperator()
    dboperator.reset_database()
    dboperator.close()

    asyncio.run(scrape_current_month_matches())

    # for year in range(2008, 2022):
    #     scrape_year_matches("MS", year)
    #     time.sleep(5)
    #     scrape_year_matches("WS", year)
