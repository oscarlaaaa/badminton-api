class Set:
    def __init__(self, winner_score, loser_score, num):
        self.winner_score = winner_score
        self.loser_score = loser_score
        self.round = num
    
    def get_formatted_data(self, match_id):
        return (match_id, self.winner_score, self.loser_score, self.round)

class Match:
    
    def __init__(self, event, winner, loser, points, date, time, duration=0, tournament_id='undefined', level='undefined'):
        self.event = event
        self.winner = winner
        self.loser = loser
        self.points = points
        self.date = date
        self.time = time
        self.duration = duration
        self.tournament_id = tournament_id
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
    
    def set_winner(self, winner):
        self.winner = winner
    
    def get_loser(self):
        return self.loser

    def set_loser(self, loser):
        self.loser = loser

    def get_points(self):
        return str(self.points)

    def get_duration(self):
        return str(self.duration)

    def get_year(self):
        calendar_date = self.date.split(' ')[2]
        return calendar_date[-4:]
        
    def get_day(self):
        calendar_date = self.date.split(' ')[2]
        index = calendar_date.index('/')
        return calendar_date[:index]
    
    def get_formatted_data(self):
        return (self.winner, self.loser, self.tournament_id, self.event, self.time, self.duration)

    def get_sets(self):
        return [Set(game[0], game[1], i) for i, game in enumerate(self.points, 1)]
