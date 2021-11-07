import requests
from .match import Match
from bs4 import BeautifulSoup

class MatchGatherer:

    PLAYERS_IN_ROW = 2

    def __init__(self, event="MS", tournament='unknown', year=0):
        event = event.upper().strip()

        if event != "MS" and event != "WS":
            raise NameError("Not a valid event. Please input either MS or WS")


        self.event = event
        self.tournament = tournament
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

    ## converts a time string into an integer value minutes
    def convert_time_string_to_minutes(self, time):
        output = 0
        if 'h' in time:
            try:
                output = output + (int(time[0]) * 60)
            except ValueError:
                pass
        try:
            output = output + int(time[-3:-1])
        except ValueError:
            pass
                
        return output

    ## collects and creates a match object from a given match row and appends to master matches list
    def collect_match_row_data(self, match_row, matches, tournament_title, level):
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
        date = date_time[4]

        duration = self.convert_time_string_to_minutes([duration.text for duration in match_row.find_all('td')][-2])

        matches.append(Match(self.event, winner, loser, points, date, duration, tournament_title, level))

    ## scrapes all match links, and returns a list of match objects
    def collect_all_matches(self, match_link, level):
        html_text = requests.get(match_link).text
        soup = BeautifulSoup(html_text, 'lxml')

        match_section = soup.find('table', class_='ruler matches').find('tbody', recursive=False)
        match_rows = match_section.find_all('tr', recursive=False)

        tournament_title = soup.find('h2', class_='media__title media__title--large').text

        matches = []

        for match_row in match_rows:
            self.collect_match_row_data(match_row, matches, tournament_title, level)

        return matches


    ## outputs a full list of all match data scraped for that tournament and event for storage
    def collect_match_data(self, tournament_id):
        draws_link = self.convert_to_draws_link(tournament_id)
        html_text = requests.get(draws_link).text
        
        relevant_draws = self.collect_draw_links(html_text, self.event)
        relevant_match_links = [self.convert_to_matches_link(link) for link in relevant_draws]

        soup = BeautifulSoup(html_text, 'lxml')

        tournament_level = soup.find('span', class_='tag tag--mono').text

        for match_link in relevant_match_links:
            matches = self.collect_all_matches(match_link, tournament_level)
            if matches != None:
                self.match_list = self.match_list + matches



    
## tests for the fn
# xd = collect_match_data("a6128cae-03b8-492c-a398-ad3505e8ec16", "MS")
# print(len(xd))