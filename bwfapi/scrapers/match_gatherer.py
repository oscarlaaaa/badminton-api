import requests
from .match import Match
from bs4 import BeautifulSoup

class MatchGatherer:

    MIN_START_YEAR = 2007
    MAX_END_YEAR = 2022
    PLAYERS_IN_ROW = 2

    def __init__(self, event="MS", year=2022):
        event = event.upper().strip()

        if event != "MS" and event != "WS":
            raise NameError("Not a valid event. Please input either MS or WS")
        if year < self.MIN_START_YEAR or year > self.MAX_END_YEAR:
            raise ValueError("Year is invalid. Please input a year between 2007 and 2022")

        self.event = event
        self.year = year
        self.match_list = []

    def get_event(self):
        return self.event

    def get_year(self):
        return self.year

    def get_match_list(self):
        return self.match_list

    def is_valid_event(event):
        return event == "MS" or event == "WS"

    ## takes in a tournament id, and converts it into a link with all available draws
    def convert_to_draws_link(self, tournament_id):
        return f"https://bwf.tournamentsoftware.com/sport/draws.aspx?id={tournament_id}"

    ## takes in a draw link, and converts it into a link with all matches displayed for scraping
    def convert_to_matches_link(self, draw_link):
        if (len(draw_link) < 5):
            raise ValueError("Link too short.")
        return f"https://bwf.tournamentsoftware.com/sport/{draw_link[0:4]}matches{draw_link[4:]}"

    ## strips name down to just spaces and alphabet characters
    def clean_name_formatting(self, name):
        if '[' in name:
            return name[:name.index('[')].strip().upper()
        return name.strip().upper()

    ## finds all draws that correspond to the event parameter, and returns an array of draw links
    def collect_draw_links(self, html_text, event):
        soup = BeautifulSoup(html_text, 'lxml')

        ## locate draws links
        draws = soup.find('table', class_='ruler')
        draw_sections = draws.find_all('td', class_='drawname')

        ## grab links that match the desired event and store in array
        desired_draws = []
        for name in draw_sections:
            link = name.find('a', class_='nowrap')
            if event in link.text:
                desired_draws.append(link['href'])

        return desired_draws

    ## collects and creates a match object from a given match row and appends to master matches list
    def collect_match_row_data(self, match_row, matches, tournament_title):
        if match_row.find('span', class_='score') is None:
            return
        
        players = [name.text for name in match_row.find_all('a') if "player" in name['href']]
        # players = [name.text.encode('utf-8') for name in match_row.find_all('a') if "player" in name['href']]
        if len(players) < self.PLAYERS_IN_ROW:
            return

        winner = self.clean_name_formatting(players[0])
        loser = self.clean_name_formatting(players[1])
        points = [list(map(int, score.text.split('-'))) for score in match_row.find('span', class_='score').find_all('span')]
        date_time = match_row.find('td', class_='plannedtime').text
        year = date_time[-4:]

        matches.append(Match(winner, loser, points, year, tournament_title))

    ## scrapes all match links, and returns a list of match objects
    def collect_all_matches(self, match_link):
        html_text = requests.get(match_link).text
        soup = BeautifulSoup(html_text, 'lxml')

        match_section = soup.find('table', class_='ruler matches').find('tbody', recursive=False)
        match_rows = match_section.find_all('tr', recursive=False)

        tournament_title = soup.find('h2', class_='media__title media__title--large').text

        matches = []

        for match_row in match_rows:
            self.collect_match_row_data(match_row, matches, tournament_title)

        return matches


    ## outputs a full list of all match data scraped for that tournament and event for storage
    def collect_match_data(self, tournament_id):
        draws_link = self.convert_to_draws_link(tournament_id)
        html_text = requests.get(draws_link).text
        
        relevant_draws = self.collect_draw_links(html_text, self.event)
        relevant_match_links = [self.convert_to_matches_link(link) for link in relevant_draws]

        for match_link in relevant_match_links:
            matches = self.collect_all_matches(match_link)
            if matches != None:
                self.match_list = self.match_list + matches



    
## tests for the fn
# xd = collect_match_data("a6128cae-03b8-492c-a398-ad3505e8ec16", "MS")
# print(len(xd))
