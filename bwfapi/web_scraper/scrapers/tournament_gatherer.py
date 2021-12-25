import asyncio, nest_asyncio
import random, time
from datetime import date
from requests_html import AsyncHTMLSession

nest_asyncio.apply()

class TournamentGatherer:
    MIN_START_YEAR = 2007
    MAX_END_YEAR = 2022

    def __init__(self, end_year=2022):
        if end_year < self.MIN_START_YEAR or end_year > self.MAX_END_YEAR:
            raise ValueError("Year is invalid. Please input a year between 2007 and 2022")

        self.end_year = end_year

    def format_year_into_link(self, year):
        return f"https://bwf.tournamentsoftware.com/find?DateFilterType=0&StartDate={year}-01-01&EndDate={year}-12-31&page=5&TournamentCategoryIDList%5B0%5D=false&TournamentCategoryIDList%5B1%5D=false&TournamentCategoryIDList%5B2%5D=false&TournamentCategoryIDList%5B3%5D=false&TournamentCategoryIDList%5B4%5D=false&TournamentCategoryIDList%5B5%5D=20&TournamentCategoryIDList%5B6%5D=21&TournamentCategoryIDList%5B7%5D=22&TournamentCategoryIDList%5B8%5D=23&TournamentCategoryIDList%5B9%5D=24&TournamentCategoryIDList%5B10%5D=25&TournamentCategoryIDList%5B11%5D=1&TournamentCategoryIDList%5B12%5D=8&TournamentCategoryIDList%5B13%5D=2&TournamentCategoryIDList%5B14%5D=3&TournamentCategoryIDList%5B15%5D=4&TournamentCategoryIDList%5B16%5D=false&TournamentCategoryIDList%5B17%5D=6&TournamentCategoryIDList%5B18%5D=false&TournamentCategoryIDList%5B19%5D=false&TournamentCategoryIDList%5B20%5D=false&TournamentCategoryIDList%5B21%5D=false&TournamentCategoryIDList%5B22%5D=false&TournamentCategoryIDList%5B23%5D=false&TournamentCategoryIDList%5B24%5D=false&TournamentCategoryIDList%5B25%5D=false&TournamentCategoryIDList%5B26%5D=false&TournamentCategoryIDList%5B27%5D=false&TournamentCategoryIDList%5B28%5D=false&TournamentCategoryIDList%5B29%5D=false&TournamentCategoryIDList%5B30%5D=false&TournamentCategoryIDList%5B31%5D=false&TournamentCategoryIDList%5B32%5D=false"
    
    def current_month_link(self):
        time = date.today()

        next_month = 0
        if time.month < 9:
            next_month = "0" + str(time.month + 1)
        elif time.month == 12:
            next_month = "01"
        else:
            next_month = str(time.month + 1)
        
        next_year = time.year if time.month != 12 else time.year+1
        return f"https://bwf.tournamentsoftware.com/find?DateFilterType=0&StartDate={time.year}-{time.month}-01&EndDate={next_year}-{next_month}-01&page=5&TournamentCategoryIDList%5B0%5D=false&TournamentCategoryIDList%5B1%5D=false&TournamentCategoryIDList%5B2%5D=false&TournamentCategoryIDList%5B3%5D=false&TournamentCategoryIDList%5B4%5D=false&TournamentCategoryIDList%5B5%5D=20&TournamentCategoryIDList%5B6%5D=21&TournamentCategoryIDList%5B7%5D=22&TournamentCategoryIDList%5B8%5D=23&TournamentCategoryIDList%5B9%5D=24&TournamentCategoryIDList%5B10%5D=25&TournamentCategoryIDList%5B11%5D=1&TournamentCategoryIDList%5B12%5D=8&TournamentCategoryIDList%5B13%5D=2&TournamentCategoryIDList%5B14%5D=3&TournamentCategoryIDList%5B15%5D=4&TournamentCategoryIDList%5B16%5D=false&TournamentCategoryIDList%5B17%5D=false&TournamentCategoryIDList%5B18%5D=false&TournamentCategoryIDList%5B19%5D=false&TournamentCategoryIDList%5B20%5D=false&TournamentCategoryIDList%5B21%5D=false&TournamentCategoryIDList%5B22%5D=false&TournamentCategoryIDList%5B23%5D=false&TournamentCategoryIDList%5B24%5D=false&TournamentCategoryIDList%5B25%5D=false&TournamentCategoryIDList%5B26%5D=false&TournamentCategoryIDList%5B27%5D=false&TournamentCategoryIDList%5B28%5D=false&TournamentCategoryIDList%5B29%5D=false&TournamentCategoryIDList%5B30%5D=false&TournamentCategoryIDList%5B31%5D=false&TournamentCategoryIDList%5B32%5D=false"
    
    def format_date(self, date):
        if date == None:
            return None
        vals = date.split('/')
        return f"{vals[2]}-{vals[0]}-{vals[1]}"
        
    def parse_tournament(self, tournament):
        title = list(tournament.find('.media__title'))[0]
        name = title.text.upper()

        dates = tournament.find('time')
        start_date = None
        end_date = None
        if len(dates) == 2:
            start_date = dates[0].text
            end_date = dates[1].text

        link = list(title.links)[0]
        link = link[(link.index('=') + 1):]

        return {'name': name, 'start': self.format_date(start_date), 'end': self.format_date(end_date), 'link': link}

    async def grab_tournaments_from_current_month(self):
        link = self.current_month_link()

        s = AsyncHTMLSession()
        time.sleep(random.randint(0, 10))
        response = await s.get(link)
        await response.html.arender(timeout=30, sleep=4) 

        content = response.html.find('#searchResultArea', first=True)
        tournaments = content.find('.media')

        output = [self.parse_tournament(tournament) for tournament in tournaments]
        return output

    async def grab_tournaments_from_year(self, year):
        link = self.format_year_into_link(year)

        s = AsyncHTMLSession()
        response = await s.get(link)
        await response.html.arender(timeout=30, sleep=4) 

        content = response.html.find('#searchResultArea', first=True)
        tournaments = content.find('.media')

        output = [self.parse_tournament(tournament) for tournament in tournaments]
        return output

    async def grab_all_tournaments(self):
        return await asyncio.gather(*[self.grab_tournaments_from_year(i) for i in range(self.MIN_START_YEAR, self.MAX_END_YEAR)])
        