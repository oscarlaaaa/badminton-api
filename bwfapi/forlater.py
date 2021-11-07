import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from player_link import PlayerLink
from match import Match
from match_link import MatchLink
from player_info import PlayerInfo


## returns a list of results from search terms
def search_player(search):
    player_list = []

    search.replace(' ', '+')

    html_text = requests.get(f'https://bwf.tournamentsoftware.com/find/player?q={search}').text
    soup = BeautifulSoup(html_text, 'lxml')
    search_area = soup.find('ul', {'id': 'searchResultArea'})
    players = search_area.find_all('li', {'class': 'list__item'})

    for player in players:
        name = player.find('h5', {'class': 'media__title'}).find('span', {'class': 'nav-link__value'}).text
        link = player.find('a', {'class': 'media__img'})['href']
        new_player = PlayerLink(name, link)
        player_list.append(new_player)
    
    return player_list

#  UNFINISHED
# def collect_player_info(player_link):
#     html_text = requests.get(f'https://bwf.tournamentsoftware.com{player_link.get_link()}').text
#     soup = BeautifulSoup(html_text, 'lxml')
#     info_section = soup.find

## returns links to matches from every year
def collect_year_links(player_link):
    html_text = requests.get(f'https://bwf.tournamentsoftware.com{player_link.get_link()}/tournaments').text
    soup = BeautifulSoup(html_text, 'lxml')
    tournament_tabs_area = soup.find('ul', {'id': 'tabs_tournaments'})
    links = tournament_tabs_area.find_all('a', {'class': 'page-nav__link js-tab'})
    year_links = []

    year = 2021
    for i in range(0, len(links)):

        if (i == len(links) - 1):
            year = 0
        
        year_link = 'https://bwf.tournamentsoftware.com' + links[i]['href']
        
        match = MatchLink(player_link.get_name(), year, year_link)
        year_links.append(match)
        year = year - 1
    
    return year_links




## gathers all matches, records player names/points, and outputs list of matches
def collect_matches(year_link):
    match_list = []

    html_text = requests.get(year_link).text
    soup = BeautifulSoup(html_text, 'lxml')
    match_bodies = soup.find_all('div', class_='match__body')
    for body in match_bodies:
        rows = body.find_all('div', {'class': 'match__row'})

        player1 = rows[0].find('span', {'class': 'nav-link__value'})

        if not player1: continue
        player1 = player1.text
        player1_points = rows[0].find_all('li', {'class': 'points__cell'})
        player1_point_list = []
        for point in player1_points:
            player1_point_list.append(int(point.text))

        player2 = rows[1].find('span', {'class': 'nav-link__value'})
        if not player2: continue
        player2 = player2.text
        player2_points = rows[1].find_all('li', {'class': 'points__cell'})
        player2_point_list = []
        for point in player2_points:
            player2_point_list.append(int(point.text))
        
        new_match = Match(player1, player2, player1_point_list, player2_point_list)
        match_list.append(new_match)
    
    return match_list