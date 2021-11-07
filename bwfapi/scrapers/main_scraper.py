import csv
from tournament_gatherer import TournamentGatherer
from match_gatherer import MatchGatherer
from match import Match


####### START OF SCRIPT ########

tg = TournamentGatherer()

tournaments = tg.grab_tournaments_from_year(2010)
print(str(tournaments['links']))

mg = MatchGatherer("MS", year=tournaments['year'])
for t in tournaments['links']:
    mg.collect_match_data(t)

match_list = mg.get_match_list()

for match in match_list:
    print(str(match))


# with open('test.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["SN", "Name", "Contribution"])
#     writer.writerow([1, "Linus Torvalds", "Linux Kernel"])
#     writer.writerow([2, "Tim Berners-Lee", "World Wide Web"])
#     writer.writerow([3, "Guido van Rossum", "Python Programmingxdd"])