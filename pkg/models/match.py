class Match:

    def __init__(self, id, date, team1, team2, score1, score2):
        self.date = date
        self.team1 = team1
        self.team2 = team2
        self.score1 = score1
        self.score2 = score2

    def winner(self):
        if self.score1 > self.score2:
            return self.team1
        elif self.score2 > self.score1:
            return self.team2
        return None

    def __str__(self):
        return f"{self.date} | {self.team1} {self.score1} - {self.score2} {self.team2}"

    def __repr__(self):
        return (
            f"Match(date='{self.date}', "
            f"team1='{self.team1}', team2='{self.team2}', "
            f"score1={self.score1}, score2={self.score2}')"
        )
