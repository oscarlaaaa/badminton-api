import csv
import asyncio
import timeit
from scrapers import ProgressBar, TournamentGatherer, MatchGatherer, AsyncMatchGatherer

####### START OF SCRIPT ########

def __main__():

    # Gathers tournment links from all years
    print("Started scraping tournaments...")
    tg = TournamentGatherer()

    start_tournament_scraping = timeit.default_timer()
    tournament = asyncio.run(tg.grab_tournaments_from_year(2014))
    end_tournament_scraping = timeit.default_timer()
    total_tournaments = 0
    print(f"Year: {tournament['year']}\t Count: {str(len(tournament['links']))}")
    total_tournaments = total_tournaments + len(tournament['links'])

    tournament_time_elapsed = end_tournament_scraping - start_tournament_scraping
    print(f"Finished scraping {total_tournaments} tournaments in {tournament_time_elapsed} seconds.") # should be 546



    # Gathers matches from a set year of tournaments (async)
    print("Started scraping matches async...")
    start_Amatch_scraping = timeit.default_timer()

    Amatch_list = []
    mg = AsyncMatchGatherer(event="MS", tournament_list=tournament['links'])
    tournament_match_list = asyncio.run(mg.collect_all_match_data())
    Amatch_list = Amatch_list + tournament_match_list

    sorter = AsyncMatchGatherer()
    sorter.sort_match_data2(Amatch_list)
    end_Amatch_scraping = timeit.default_timer()

    Amatch_time_elapsed = end_Amatch_scraping - start_Amatch_scraping
    print(f"Finished scraping {len(Amatch_list)} matches async in {Amatch_time_elapsed} seconds.")



    # Gathers matches from a set year of tournaments
    print("Started scraping matches...")
    start_match_scraping = timeit.default_timer()
    match_list = []

    mg = MatchGatherer(event="MS", tournament_list=tournament['links'])
    mg.collect_all_match_data()
    tournament_match_list = mg.get_match_list()
    match_list = match_list + tournament_match_list
    
    end_match_scraping = timeit.default_timer()

    match_time_elapsed = end_match_scraping - start_match_scraping
    print(f"Finished scraping {len(match_list)} matches in {match_time_elapsed} seconds.")
    
    with open('./bwfapi/benchmarks/scraping.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Functionality", "Count", "Time in seconds", "Async?"])
        writer.writerow(["Tournament Scrape", total_tournaments, tournament_time_elapsed, "Yes"])
        writer.writerow(["Match Scrape", len(match_list), match_time_elapsed, "No"])
        writer.writerow(["Match Scrape", len(Amatch_list), Amatch_time_elapsed, "collect_match_data"])


    # # matches = asyncio.run(mg.collect_all_match_data())
        
    # # Match list to be mass-processed into csv
    # # match_list = mg.get_match_list()
    # csv_bar = ProgressBar(len(match_list), prefix = 'Writing into .csv', suffix = 'of data written.')

    # with open('./bwfapi/scraped_data.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)

    #     count = 1
    #     total = len(match_list)

    #     writer.writerow(["Count", "Tournament", "Date", "Time", "Winner", "Loser", "Points", "Duration"])
    #     for match in match_list:
    #         writer.writerow([str(count), match.get_tournament(), match.get_date(), match.get_time(), match.get_winner(), match.get_loser(), match.get_points(), match.get_duration()])
    #         count = count + 1
    #         csv_bar.printProgressBar()

if __name__ == "__main__":
    __main__()