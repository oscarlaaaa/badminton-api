# Copyright © 2022 Oscar La
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this 
# software and associated documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to the following 
# conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies 
# or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

import csv
import timeit
from bwfapi.web_scraper.db.db_operator import DBOperator
from bwfapi.web_scraper.scrapers.tournament_gatherer import TournamentGatherer
from bwfapi.web_scraper.scrapers.match_gatherer_async import AsyncMatchGatherer
from bwfapi.web_scraper.scrapers.match import Match 
from bwfapi.web_scraper.scrapers.player_gatherer import PlayerGatherer
from bwfapi.web_scraper.services import EchoService
import asyncio
import time, random

class BwfScraper:
    def __init__(self, year=0):
        self.year = year
        self.tournament_list = {}
        self.match_list = []
        self.men_players = {}
        self.women_players = {}
        self.player_list = {}
        self.men_pg = None
        self.women_pg = None

    def get_tournament_list(self):
        return self.tournament_list

    def get_match_list(self):
        return self.match_list

    def get_player_list(self):
        return self.player_list

    async def scrape_year_tournaments(self):
        print("Started scraping tournaments...")
        tg = TournamentGatherer()

        start_tournament_scraping = timeit.default_timer()
        tournaments = await tg.grab_tournaments_from_year(self.year)
        end_tournament_scraping = timeit.default_timer()
        total_tournaments = len(tournaments)

        tournament_time_elapsed = end_tournament_scraping - start_tournament_scraping
        self.tournament_list = tournaments

        print(f"Finished scraping {total_tournaments} tournaments in {tournament_time_elapsed} seconds.") 
        return {"count": total_tournaments, "time": tournament_time_elapsed}

    async def scrape_current_month_tournaments(self):
        EchoService.echo(f"Started scraping tournaments from current month")
        print(f"Started scraping tournaments from current month")
        start_tournament_scraping = timeit.default_timer()

        tg = TournamentGatherer()
        tournaments = await tg.grab_tournaments_from_current_month()

        end_tournament_scraping = timeit.default_timer()
        print(f"Year: {self.year}\t Count: {str(len(tournaments))}")
        total_tournaments = len(tournaments)

        tournament_time_elapsed = end_tournament_scraping - start_tournament_scraping
        self.tournament_list = tournaments

        EchoService.echo(f"Finished scraping {total_tournaments} tournaments in {tournament_time_elapsed} seconds.")
        print(f"Finished scraping {total_tournaments} tournaments in {tournament_time_elapsed} seconds.")
        return {"count": total_tournaments, "time": tournament_time_elapsed}

    async def scrape_matches(self):
        EchoService.echo(f"Started scraping matches...")
        print(f"Started scraping matches...")
        start_Amatch_scraping = timeit.default_timer()

        tournament_links = [tournament['link'] for tournament in self.tournament_list]
        mg_mens = AsyncMatchGatherer(event="MS", tournament_list=tournament_links)
        tournament_match_list = await mg_mens.collect_all_match_data()

        mg_womens = AsyncMatchGatherer(event="WS", tournament_list=tournament_links)
        tournament_match_list = tournament_match_list + await mg_womens.collect_all_match_data()

        # AsyncMatchGatherer.sort_match_data2(tournament_match_list)

        end_Amatch_scraping = timeit.default_timer()
        Amatch_time_elapsed = end_Amatch_scraping - start_Amatch_scraping

        self.men_players = mg_mens.get_player_links() 
        self.women_players = mg_womens.get_player_links()
        self.match_list = tournament_match_list

        EchoService.echo(f"Finished scraping {len(tournament_match_list)} matches in {Amatch_time_elapsed} seconds.")
        print(f"Finished scraping {len(tournament_match_list)} matches in {Amatch_time_elapsed} seconds.")
        return {"count": len(tournament_match_list), "time": Amatch_time_elapsed}

    async def scrape_players(self):
        EchoService.echo(f"Started scraping players...")
        print(f"Started scraping players...")
        start_player_scraping = timeit.default_timer()

        self.men_pg = PlayerGatherer(self.men_players, "MS")
        await self.men_pg.grab_all_players()

        self.women_pg = PlayerGatherer(self.women_players, "WS")
        await self.women_pg.grab_all_players()

        end_player_scraping = timeit.default_timer()
        player_time_elapsed = end_player_scraping - start_player_scraping

        EchoService.echo(f"Finished scraping {len(self.men_pg.get_player_list()) + len(self.women_pg.get_player_list())} players in {player_time_elapsed} seconds.")
        print(f"Finished scraping {len(self.men_pg.get_player_list()) + len(self.women_pg.get_player_list())} players in {player_time_elapsed} seconds.")
        return {"count": len(self.men_pg.get_player_list()) + len(self.women_pg.get_player_list()), "time": player_time_elapsed}
    
    async def scrape_players_info(self):
        EchoService.echo(f"Started scraping player info...")
        print(f"Started scraping player info...")
        start_info_scraping = timeit.default_timer()
        
        await self.men_pg.grab_all_player_info()
        await self.women_pg.grab_all_player_info()
        
        end_info_scraping = timeit.default_timer()
        info_time_elapsed = end_info_scraping - start_info_scraping

        self.player_list.update(self.women_pg.get_player_list())
        self.player_list.update(self.men_pg.get_player_list())

        EchoService.echo(f"Finished scraping {len(self.player_list)} player infos in {info_time_elapsed} seconds.")
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
            writer.writerow([self.year, "Tournament Scrape", tournament_bm['count'], tournament_bm['time']])
            writer.writerow([self.year, "Match Scrape", match_bm['count'], match_bm['time']])
            writer.writerow([self.year, "Player Scrape", player_bm['count'], player_bm['time']])
            writer.writerow([self.year, "Player Info Scrape", player_info_bm['count'], player_info_bm['time']])

    async def scrape_current_month(self):
        await self.scrape_current_month_tournaments()
        time.sleep(random.randint(0, 10))
        await self.scrape_matches()
        time.sleep(random.randint(0, 10))
        await self.scrape_players()
        time.sleep(random.randint(0, 10))
        await self.scrape_players_info()
        self.change_names_to_ids()
        # self.record_scraping_benchmarks(tournament_bm, match_bm, player_bm, player_info_bm)

    async def scrape_year(self):
        tournament_bm = await self.scrape_year_tournaments()
        match_bm = await self.scrape_matches()
        player_bm = await self.scrape_players()
        player_info_bm = await self.scrape_players_info()
        self.change_names_to_ids()
        self.record_scraping_benchmarks(tournament_bm, match_bm, player_bm, player_info_bm)

def write_benchmark_headers():
     with open('./bwfapi/benchmarks/scraping.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Year", "Functionality", "Count", "Time in seconds"])

async def scrape_year_matches(year):
    scraper = BwfScraper(year)
    await scraper.scrape_year()
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
    try:
        await scraper.scrape_current_month()
        EchoService.echo("Opening DB connection")
        dboperator = DBOperator()
        EchoService.echo("Inserting Tournaments into DB")
        dboperator.insert_tournaments(scraper.get_tournament_list()) #works
        dboperator.commit()
        
        EchoService.echo("Inserting Players into DB")
        dboperator.insert_players(scraper.get_player_list())  # works
        dboperator.commit()

        EchoService.echo("Inserting Matches and Sets into DB")
        dboperator.insert_match_and_sets(scraper.get_match_list()) #works
        dboperator.commit()

        EchoService.echo("Closing DB connection")
        dboperator.close()
        return {"STATUS": "SUCCESS"}
    except:
        return {"STATUS": "ERROR"}

############### MAIN SCRAPER SECTION #################
if __name__ == "__main__":
    # write_benchmark_headers()
    # dboperator = DBOperator()
    # dboperator.reset_database()
    # dboperator.close()
    asyncio.run(scrape_current_month_matches())
    # years_missed = []
    # for year in (2008, 2018):
        # failed = True
        # while failed:
            # try:
                # print(f'----------------------SCRAPING {year}-----------------------')
                # asyncio.run(scrape_year_matches(year))
                # failed = False
                # print("wooo")
            # except:
            #     years_missed.append(year)
            # finally:
                # print('\n\n\n')
            # time.sleep(10)
    
    # print(f"MISSING: {str(years_missed)}")
