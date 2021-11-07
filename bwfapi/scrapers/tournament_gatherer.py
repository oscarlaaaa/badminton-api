from requests_html import HTMLSession

class TournamentGatherer:

    MAX_END_YEAR = 2022

    def __init__(self, end_year=2022):
        if end_year > self.MAX_END_YEAR:
            raise ValueError("Year cannot be greater than 2022.")

        self.end_year = end_year

    def grab_tournament_from_year(year):
        link = f"https://bwf.tournamentsoftware.com/find?DateFilterType=0&StartDate={year}-01-01&EndDate={year}-12-31&page=5&TournamentCategoryIDList%5B0%5D=false&TournamentCategoryIDList%5B1%5D=false&TournamentCategoryIDList%5B2%5D=false&TournamentCategoryIDList%5B3%5D=false&TournamentCategoryIDList%5B4%5D=false&TournamentCategoryIDList%5B5%5D=20&TournamentCategoryIDList%5B6%5D=21&TournamentCategoryIDList%5B7%5D=22&TournamentCategoryIDList%5B8%5D=23&TournamentCategoryIDList%5B9%5D=24&TournamentCategoryIDList%5B10%5D=25&TournamentCategoryIDList%5B11%5D=1&TournamentCategoryIDList%5B12%5D=8&TournamentCategoryIDList%5B13%5D=2&TournamentCategoryIDList%5B14%5D=3&TournamentCategoryIDList%5B15%5D=4&TournamentCategoryIDList%5B16%5D=false&TournamentCategoryIDList%5B17%5D=false&TournamentCategoryIDList%5B18%5D=false&TournamentCategoryIDList%5B19%5D=false&TournamentCategoryIDList%5B20%5D=false&TournamentCategoryIDList%5B21%5D=false&TournamentCategoryIDList%5B22%5D=false&TournamentCategoryIDList%5B23%5D=false&TournamentCategoryIDList%5B24%5D=false&TournamentCategoryIDList%5B25%5D=false&TournamentCategoryIDList%5B26%5D=false&TournamentCategoryIDList%5B27%5D=false&TournamentCategoryIDList%5B28%5D=false&TournamentCategoryIDList%5B29%5D=false&TournamentCategoryIDList%5B30%5D=false&TournamentCategoryIDList%5B31%5D=false&TournamentCategoryIDList%5B32%5D=false"

        s = HTMLSession()
        response = s.get(link)
        response.html.render(sleep=3)

        content = response.html.find('#searchResultArea', first=True).links
        links = list(content)

        return links

    ## USE SPARINGLY IT IS FAT
    def grab_all_tournaments(self):
        links = []
        for i in range(2007, self.MAX_END_YEAR):
            links = links + self.grab_tournament_from_year(i)
        return links

    ## test function - should be 507
    # print(len(grab_all_tournaments()))