class StatsService:

    def __init__(self, matches):
        self.matches = matches

    def compute_ranking(self):
        ranking = {}

        for match in self.matches:
            winner = match.winner()
            if winner:
                ranking[winner] = ranking.get(winner, 0) + 3

        return ranking
