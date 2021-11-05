import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from player_link import PlayerLink
from match import Match
from match_link import MatchLink
from player_info import PlayerInfo


def convert_to_draws_link(tournament_id):
    return f"https://bwf.tournamentsoftware.com/sport/draws.aspx?id={tournament_id}"

def convert_to_matches_link(draw_link):
    return f"https://bwf.tournamentsoftware.com/sport/{draw_link[0:4]}matches{draw_link[4:]}"

def collect_draw_links(html_text, event):
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

def collect_all_matches(match_link):
    html_text = requests.get(match_link).text
    soup = BeautifulSoup(html_text, 'lxml')

    match_section = soup.find('table', class_='ruler matches').find('tbody', recursive=False)
    match_rows = match_section.find_all('tr', recursive=False)
    print(len(match_rows))
    for match_row in match_rows:
        if match_row.find('span', class_='score') is None:
            continue

        players = [name.text.encode('utf-8') for name in match_row.find_all('a') if "player" in name['href']]
        print(str(players))
        print('xd')
        # date_time = match_row.find('td', class_='plannedtime').text
        # winner_name = match_row.find('strong').find('a').text
        # loser_name = match_row.find




def collect_match_data(tournament_id, event):
    match_list = []

    draws_link = convert_to_draws_link(tournament_id)
    html_text = requests.get(draws_link).text
    
    relevant_draws = collect_draw_links(html_text, event)
    relevant_match_links = [convert_to_matches_link(link) for link in relevant_draws]

    for match_link in relevant_match_links:
        matches = collect_all_matches(match_link)
        if matches != None:
            match_list = match_list + matches



    

xd = collect_match_data("a6128cae-03b8-492c-a398-ad3505e8ec16", "MS")



######### Things I want to add: ##########
# - total point summation
# - head-to-head stats
# - win ratio
# - longest win streaks
# - timeline of tournaments
# - lifetime points won/lost
# - lifetime games won/lost
# - yoink an image for bg
# - top/worst 10 h2hs
