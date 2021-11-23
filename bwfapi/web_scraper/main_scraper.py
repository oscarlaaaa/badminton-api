import csv
import asyncio
from re import match
import timeit
from scrapers import ProgressBar, TournamentGatherer, MatchGatherer, AsyncMatchGatherer, Match

####### START OF SCRIPT ########

class BwfScraper:

    def __init__(self, year, event):
        self.year = year
        self.event = event
        self.tournament_list = {}
        self.match_list = []
        self.player_list = []

    def scrape_tournaments(self):
        print("Started scraping tournaments...")
        tg = TournamentGatherer()

        start_tournament_scraping = timeit.default_timer()
        tournament = asyncio.run(tg.grab_tournaments_from_year(self.year))
        end_tournament_scraping = timeit.default_timer()
        total_tournaments = 0
        print(f"Year: {tournament['year']}\t Count: {str(len(tournament['links']))}")
        total_tournaments = total_tournaments + len(tournament['links'])

        tournament_time_elapsed = end_tournament_scraping - start_tournament_scraping
        print(f"Finished scraping {total_tournaments} tournaments in {tournament_time_elapsed} seconds.") # should be 546
        self.tournament_list = tournament
        return {"count": total_tournaments, "time": tournament_time_elapsed}


    def scrape_matches(self):
        # Gathers matches from a set year of tournaments (async)
        print("Started scraping matches async...")
        start_Amatch_scraping = timeit.default_timer()

        match_list = []
        mg = AsyncMatchGatherer(event=self.event, tournament_list=self.tournament_list['links'])
        tournament_match_list = asyncio.run(mg.collect_all_match_data())

        match_list = match_list + tournament_match_list

        sorter = AsyncMatchGatherer()
        sorter.sort_match_data2(match_list)
        end_Amatch_scraping = timeit.default_timer()

        Amatch_time_elapsed = end_Amatch_scraping - start_Amatch_scraping
        print(f"Finished scraping {len(match_list)} matches async in {Amatch_time_elapsed} seconds.")

        self.player_list = mg.get_player_list()
        self.match_list = match_list

        return {"count": len(match_list), "time": Amatch_time_elapsed}

    def write_into_csv(self):
        with open('./bwfapi/web_scraper/db/scraped_players.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            count = 1

            writer.writerow(["ID", "Player Name"])

            for player in self.player_list:
                writer.writerow([count, player])
                count = count + 1

        csv_bar = ProgressBar(len(self.match_list), prefix = 'Writing into .csv', suffix = 'of data written.')
        with open('./bwfapi/web_scraper/db/scraped_matches.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            count = 1

            writer.writerow(Match.get_header())
            for match in self.match_list:
                writer.writerow(match.get_formatted_data(count))
                count = count + 1
                csv_bar.printProgressBar()


############### BENCHMARKING SECTION #################
if __name__ == "__main__":
    
    scrape = BwfScraper(2014, "MS")
    tournament_bm = scrape.scrape_tournaments()
    match_bm = scrape.scrape_matches()
    scrape.write_into_csv()

    with open('./bwfapi/benchmarks/scraping.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Functionality", "Count", "Time in seconds"])
        writer.writerow(["Tournament Scrape", tournament_bm['count'], tournament_bm['time']])
        writer.writerow(["Match Scrape", match_bm['count'], match_bm['time']])