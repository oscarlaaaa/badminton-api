import aiohttp
import asyncio
from bs4 import BeautifulSoup

class PlayerGatherer:

    def __init__(self, player_links):
        self.player_links = player_links
        self.player_list = {}
    
    def format_link(self, link):
        return f'https://bwf.tournamentsoftware.com/sport/{link}'

    def get_player_list(self):
        return self.player_list

    async def grab_player(self, link, session):
        print(f"collecting data for player {link}")
        html_text = ""

        async with session.get(self.format_link(link)) as resp:
            html_text = await resp.text()

        soup = BeautifulSoup(html_text, 'lxml')
        player_name = soup.find('div', class_='subtitle').find('h2').text.strip()

        link = soup.find('div', class_='subtitle').find('a')
        
        if link:
            name = player_name[:player_name.index("Profile")]
            player_id = link['href'][len('/player-profile/'):]
            self.player_list[name] = player_id
    
    async def grab_all_players(self):
        async with aiohttp.ClientSession() as session:
            loop = asyncio.get_event_loop()
            tasks = [self.grab_player(player_link, session) for player_link in self.player_links]
            loop.run_until_complete(asyncio.wait(tasks))
