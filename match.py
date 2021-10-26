class Match:
    
    def __init__(self, player1, player2, points1, points2):
        self.player1 = player1
        self.player2 = player2
        self.points1 = points1
        self.points2 = points2
    
    def __str__(self):
        return self.player1 + " | " + self.player2 + "\n" + str(self.points1) + " | " + str(self.points2)