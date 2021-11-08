import csv
from progress_bar import ProgressBar
from tournament_gatherer import TournamentGatherer
from match_gatherer import MatchGatherer
import match

####### START OF SCRIPT ########

# Gathers tournment links from certain year
tg = TournamentGatherer()
tournaments = tg.grab_tournaments_from_year(2010)

# Gathers matches from a set year of tournaments
mg = MatchGatherer(year=tournaments['year'], event="MS", tournament_list=tournaments['links'])
mg.collect_all_match_data()
    
# Match list to be mass-processed into csv
match_list = mg.get_match_list()
csv_bar = ProgressBar(len(match_list), prefix = 'Writing into .csv', suffix = 'of data written.')

with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    count = 1
    total = len(match_list)

    writer.writerow(match.header_row())
    for match in match_list:
        writer.writerow([str(count), match.get_tournament(), match.get_date(), match.get_time(), match.get_winner(), match.get_loser(), match.get_points(), match.get_duration()])
        count = count + 1
        csv_bar.printProgressBar()