class Match:
    
    def __init__(self, player1, player2, points1, points2):
        self.player1 = player1
        self.player2 = player2
        self.points1 = points1
        self.points2 = points2
    
    def __str__(self):
        return self.player1 + " | " + self.player2 + "\n" + str(self.points1) + " | " + str(self.points2)
    
    def who_won(self):
        if len(self.points1) == 0 and len(self.points2) == 0:
            return "walkover"
        else:
            p1_wins = 0
            p2_wins = 0
            for i in range(len(points1)):
                if self.points1[i] > self.points2[i]:
                    p1_wins = p1_wins + 1
                else:
                    p2_wins = p2_wins + 1

            return self.player1 if p1_wins > p2_wins else self.player2