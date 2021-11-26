import csv
import asyncio
from re import match
import timeit
from scrapers import ProgressBar, TournamentGatherer, MatchGatherer, AsyncMatchGatherer, Match

class BwfScraper:

    def __init__(self, year, event):
        self.year = year
        self.event = event
        self.tournament_list = {}
        self.match_list = []
        self.player_list = []

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

    def write_csv_headers(self, event, year):
        with open(f'./bwfapi/web_scraper/db/players/{event}/{year}_scraped_players.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Player Name", "Country"])

        with open(f'./bwfapi/web_scraper/db/matches/{event}/{year}_scraped_matches.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(Match.get_header())

        with open(f'./bwfapi/web_scraper/db/tournaments/{year}_scraped_tournaments.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Year", "Tournament Name"])

    def write_into_csv(self):
        start_csv_writing = timeit.default_timer()
        self.write_csv_headers(self.event, self.year)
        csv_bar = ProgressBar(len(self.get_player_list()), prefix = 'Writing players into .csv', suffix = 'of data written.')
        with open(f'./bwfapi/web_scraper/db/players/{self.event}/{self.year}_scraped_players.csv', 'a+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            count = 1

            for player in self.get_player_list():
                writer.writerow([count, player['name'], player['country']])
                count = count + 1
                csv_bar.printProgressBar()

        csv_bar = ProgressBar(len(self.get_match_list()), prefix = 'Writing matches into .csv', suffix = 'of data written.')
        with open(f'./bwfapi/web_scraper/db/matches/{self.event}/{self.year}_scraped_matches.csv', 'a+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            count = 1

            for match in self.get_match_list():
                writer.writerow(match.get_formatted_data(count))
                count = count + 1
                csv_bar.printProgressBar()
        
        csv_bar = ProgressBar(len(self.get_tournament_list()['links']), prefix = 'Writing tournament ids into .csv', suffix = 'of data written.')
        with open(f'./bwfapi/web_scraper/db/tournaments/{self.year}_scraped_tournaments.csv', 'a+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            count = 1

            for tournament in self.get_tournament_list()['links']:
                writer.writerow([count, self.get_tournament_list()['year'], tournament])
                count = count + 1
                csv_bar.printProgressBar()
        
        end_csv_writing = timeit.default_timer()
        total_time = end_csv_writing - start_csv_writing

        total_csv_lines = len(self.get_match_list()) + len(self.get_player_list()) + len(self.get_tournament_list())

        return {"count": total_csv_lines, "time": total_time}

def write_benchmark_headers():
     with open('./bwfapi/benchmarks/scraping.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Year", "Functionality", "Count", "Time in seconds"])

############### BENCHMARKING SECTION #################
if __name__ == "__main__":
    write_benchmark_headers()

    for i in range(2008, 2022):
        scrape = BwfScraper(i, "MS")
        tournament_bm = scrape.scrape_tournaments()
        match_bm = scrape.scrape_matches()
        time_bm = scrape.write_into_csv()

        with open('./bwfapi/benchmarks/scraping.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i, "Tournament Scrape", tournament_bm['count'], tournament_bm['time']])
            writer.writerow([i, "Match Scrape", match_bm['count'], match_bm['time']])
            writer.writerow([i, "CSV Write", time_bm['count'], time_bm['time']])

        

    