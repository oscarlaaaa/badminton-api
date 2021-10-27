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
        match_bodies = soup.find_all('div', class_='match__body')
        for body in match_bodies:
            rows = body.find_all('div', {'class': 'match__row'})

            player1 = rows[0].find('span', {'class': 'nav-link__value'})
            player1_points = player1.find_all('li', {'class': 'points__cell'})
            print(str(player1_points))
            player1_point_list = []
            for point in player1_points:
                print(point)
                player1_point_list.append(point.text)

            player2 = rows[1].find('span', {'class': 'nav-link__value'})
            player2_points = player2.find_all('li', {'class': 'points__cell'})
            print(player2_points)
            player2_point_list = []
            for point in player2_points:
                print(point)
                player2_point_list.append(point.text)
            
            print(player1)
            print(player2)
            print(str(player1_point_list))
            print(str(player2_point_list))

            new_match = Match(player1, player2, player1_point_list, player2_point_list)

         

   
        
    return match_list

## Testing beautiful soup
results = search_player("Kento Momota")
all_matches = []
if (len(results) == 1):
    matches = collect_player_matches(results[0]['link'])
    games = collect_matches(matches)
    # for game in games:
        # print(str(game))



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
