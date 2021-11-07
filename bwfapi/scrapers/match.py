class Match:
    
    def __init__(self, event, winner, loser, points, date, duration=0, tournament='undefined', level='undefined'):
        self.event = event
        self.winner = winner
        self.loser = loser
        self.points = points
        self.date = date
        self.duration = duration
        self.tournament = tournament
        self.level = level
    
    def __str__(self):
        return str(self.winner) + " | " + str(self.loser) + "\t" + str(self.points) + "\t" + str(self.date)
    
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
    # def who_won(self):
    #     if len(self.points1) == 0 and len(self.points2) == 0:
    #         return "walkover"
    #     else:
    #         p1_wins = 0
    #         p2_wins = 0
    #         for i in range(len(self.points1)):
    #             if self.points1[i] > self.points2[i]:
    #                 p1_wins = p1_wins + 1
    #             else:
    #                 p2_wins = p2_wins + 1

    #         return self.player1 if p1_wins > p2_wins else self.player2