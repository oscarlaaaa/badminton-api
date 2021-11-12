import csv
import requests
from scrapers import Match, ProgressBar, TournamentGatherer, MatchGatherer

####### START OF SCRIPT ########

# Gathers tournment links from certain year
tournament_list = []
tg = TournamentGatherer()

tournaments = tg.grab_all_tournaments()

# Gathers matches from a set year of tournaments
mg = MatchGatherer(year=tournaments['year'], event="MS", tournament_list=tournaments['links'])
mg.collect_all_match_data()
    
# Match list to be mass-processed into csv
match_list = mg.get_match_list()
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
