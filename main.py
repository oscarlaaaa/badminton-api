from bs4 import BeautifulSoup
from match import Match
import requests
from selenium import webdriver

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
        new_player = {'name': name, 'link': link}
        player_list.append(new_player)
    
    return player_list

## gathers all matches, records player names/points, and outputs list of matches
def collect_matches(matches):
    match_list = []

    for match in matches:
        match_row = match.find_all('div', class_='match__row')

        player1 = ''
        player2 = ''
        points1 = []
        points2 = []

        for row in match_row:
            if not player1:
                player1 = row.find('span', class_='nav-link__value').text
                points = row.find_all('li', class_='points__cell')
                for point in points:
                    points1.append(int(point.text))
            else:
                player2 = row.find('span', class_='nav-link__value').text
                points = row.find_all('li', class_='points__cell')
                for point in points:
                    points2.append(int(point.text))
        
        new_match = Match(player1, player2, points1, points2)
        match_list.append(new_match)      
        
    return match_list

## Testing beautiful soup
html_text = requests.get('https://bwf.tournamentsoftware.com/player-profile/39ec811a-3bdf-4e29-93e9-cd1f0bd65990/tournaments/2019').text
soup = BeautifulSoup(html_text, 'lxml')
matches = soup.find_all('div', class_='match__body')
match_list = collect_matches(matches)

    

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
