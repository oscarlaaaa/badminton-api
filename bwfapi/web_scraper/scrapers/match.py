class Match:
    
    def __init__(self, event, winner, loser, points, date, time, duration=0, tournament='undefined', level='undefined'):
        self.event = event
        self.winner = winner
        self.loser = loser
        self.points = points
        self.date = date
        self.time = time
        self.duration = duration
        self.tournament = tournament
        self.level = level
    
    def __str__(self):
        return str(self.winner) + " | " + str(self.loser) + "\t" + str(self.points) + "\t" + str(self.date)
    
    def get_tournament(self):
        return self.tournament
    
    def get_date(self):
        return self.date
    
    def get_time(self):
        return self.time
    
    def get_winner(self):
        return self.winner
    
    def get_loser(self):
        return self.loser

    def get_points(self):
        return str(self.points)

    def get_duration(self):
        return str(self.duration)

    def get_year(self):
        calendar_date = self.date.split(' ')[2]
        return calendar_date[-4:]
        
    # def get_month(self):
    #     calendar_date = self.date.split(' ')[2]
    #     index = calendar_date.index('/') + 1
    #     return calendar_date[ + 1:]

    def get_day(self):
        calendar_date = self.date.split(' ')[2]
        index = calendar_date.index('/')
        return calendar_date[:index]

    @staticmethod
    def get_header():
        return ['Count','Tournament','Date','Time','Winner','Loser','Points','Duration']
    
    def get_formatted_data(self, count):
        return [count, self.tournament, self.date, self.time, self.winner, self.loser, self.points, self.duration]