from requests_html import AsyncHTMLSession
import asyncio

import nest_asyncio
nest_asyncio.apply()

class TournamentGatherer:

    MIN_START_YEAR = 2007
    MAX_END_YEAR = 2022

    def __init__(self, end_year=2022):
        if end_year < self.MIN_START_YEAR or end_year > self.MAX_END_YEAR:
            raise ValueError("Year is invalid. Please input a year between 2007 and 2022")

        self.end_year = end_year

    def format_year_into_link(self, year):
        return f"https://bwf.tournamentsoftware.com/find?DateFilterType=0&StartDate={year}-01-01&EndDate={year}-12-31&page=5&TournamentCategoryIDList%5B0%5D=false&TournamentCategoryIDList%5B1%5D=false&TournamentCategoryIDList%5B2%5D=false&TournamentCategoryIDList%5B3%5D=false&TournamentCategoryIDList%5B4%5D=false&TournamentCategoryIDList%5B5%5D=20&TournamentCategoryIDList%5B6%5D=21&TournamentCategoryIDList%5B7%5D=22&TournamentCategoryIDList%5B8%5D=23&TournamentCategoryIDList%5B9%5D=24&TournamentCategoryIDList%5B10%5D=25&TournamentCategoryIDList%5B11%5D=1&TournamentCategoryIDList%5B12%5D=8&TournamentCategoryIDList%5B13%5D=2&TournamentCategoryIDList%5B14%5D=3&TournamentCategoryIDList%5B15%5D=4&TournamentCategoryIDList%5B16%5D=false&TournamentCategoryIDList%5B17%5D=false&TournamentCategoryIDList%5B18%5D=false&TournamentCategoryIDList%5B19%5D=false&TournamentCategoryIDList%5B20%5D=false&TournamentCategoryIDList%5B21%5D=false&TournamentCategoryIDList%5B22%5D=false&TournamentCategoryIDList%5B23%5D=false&TournamentCategoryIDList%5B24%5D=false&TournamentCategoryIDList%5B25%5D=false&TournamentCategoryIDList%5B26%5D=false&TournamentCategoryIDList%5B27%5D=false&TournamentCategoryIDList%5B28%5D=false&TournamentCategoryIDList%5B29%5D=false&TournamentCategoryIDList%5B30%5D=false&TournamentCategoryIDList%5B31%5D=false&TournamentCategoryIDList%5B32%5D=false"
    async def grab_tournaments_from_year(self, year):
        link = self.format_year_into_link(year)
        print(f"scanning from year {year}")
        s = AsyncHTMLSession()
        response = await s.get(link)

        await response.html.arender(timeout=30, sleep=4) 

        content = response.html.find('#searchResultArea', first=True)

        tournaments = content.find('.media')

        output = []

        for t in tournaments:
            title = list(t.find('.media__title'))[0]

            name = title.text
            print(str(name))

            dates = t.find('time')
            start_date = dates[0].text
            end_date = dates[1].text
            print(start_date)
            print(end_date)

            link = list(title.links)[0]
            link = link[(link.index('=') + 1):]
            print(str(link))

            output.append({'name': name, 'start': start_date, 'end': end_date, 'link': link})
        
        return output

    async def grab_all_tournaments(self):
        return await asyncio.gather(*[self.grab_tournaments_from_year(i) for i in range(self.MIN_START_YEAR, self.MAX_END_YEAR)])
        

# test function
tg = TournamentGatherer()
zzz = asyncio.run(tg.grab_tournaments_from_year(2008))
for t in zzz:
    print(str(t))