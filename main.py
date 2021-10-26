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
        link = player.find('a', {'class': 'media__img'})['href'] + '/tournaments'
        new_player = {'name': name, 'link': link}
        player_list.append(new_player)
    
    return player_list

## returns links to matches from every year
def collect_player_matches(link):
    html_text = requests.get(f'https://bwf.tournamentsoftware.com{link}').text
    soup = BeautifulSoup(html_text, 'lxml')
    tournament_tabs_area = soup.find('ul', {'id': 'tabs_tournaments'})
    year_links = tournament_tabs_area.find_all('a', {'class': 'page-nav__link js-tab'})
    links = []
    year = 2021
    for i in range(0, len(year_links)):
        year_section = {}

        if (i == len(year_links) - 1):
            year_section['year'] = 0
        else:
            year_section['year'] = year
        
            
        string_year = str(year_section['year'])
        year_section['link'] = 'https://bwf.tournamentsoftware.com' + year_links[i]['href']
        links.append(year_section)
        year = year - 1
    
    print(str(links))
    return links




## gathers all matches, records player names/points, and outputs list of matches
def collect_matches(matches):
    match_list = []

    for match in matches:
        html_text = requests.get(match['link']).text
        soup = BeautifulSoup(html_text, 'lxml')
        match_row = soup.find_all('div', class_='match__row')

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
results = search_player("Kento Momota")
print(str(results))
all_matches = []
if (len(results) == 1):
    matches = collect_player_matches(results[0]['link'])
    games = collect_matches(matches)



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
