class MatchLink:

    def __init__(self, name, year, link):
        self.name = name
        self.year = year
        self.link = link
    
    def __str__(self):
        return self.name + "|" + str(self.year) + "|" + self.link
    
    def get_name(self):
        return self.name

    def get_year(self):
        return self.year

    def get_link(self):
        return self.link