class PlayerInfo:

    def __init__(self, name, matches):
        self.name = name
        self.matches = matches
    
    def count_wins(self):
        count = 0
        for match in self.matches:
            if match.who_won() == self.name:
                count = count + 1
        return count