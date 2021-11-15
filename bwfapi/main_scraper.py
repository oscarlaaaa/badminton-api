import csv
import asyncio
from scrapers import ProgressBar, TournamentGatherer, MatchGatherer

####### START OF SCRIPT ########

# Gathers tournment links from all years
tg = TournamentGatherer()
tournament_list = asyncio.run(tg.grab_all_tournaments())
print("Total tournaments: " + str(len(tournament_list))) # should be 15
for tournament in tournament_list:
    print(f"Year: {tournament['year']}\t Count: {str(len(tournament['links']))}")

# Gathers matches from a set year of tournaments
match_list = []
for tournament in tournament_list:
    mg = MatchGatherer(event="MS", tournament_list=tournament['links'])
    mg.collect_all_match_data()
    tournament_match_list = mg.get_match_list()
    match_list = match_list + tournament_match_list

# matches = asyncio.run(mg.collect_all_match_data())
    
# Match list to be mass-processed into csv
# match_list = mg.get_match_list()
csv_bar = ProgressBar(len(match_list), prefix = 'Writing into .csv', suffix = 'of data written.')

with open('./bwfapi/test.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    count = 1
    total = len(match_list)

    writer.writerow(["Count", "Tournament", "Date", "Time", "Winner", "Loser", "Points", "Duration"])
    for match in match_list:
        writer.writerow([str(count), match.get_tournament(), match.get_date(), match.get_time(), match.get_winner(), match.get_loser(), match.get_points(), match.get_duration()])
        count = count + 1
        csv_bar.printProgressBar()
