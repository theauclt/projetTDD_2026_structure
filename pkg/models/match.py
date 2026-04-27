class Match:
    def __init__(self, id, date, team1, team2, score1, score2, stats=None):
        self.id = id
        self.date = date
        self.team1 = team1
        self.team2 = team2
        self.score1 = score1
        self.score2 = score2
        # Le sac à dos pour toutes les autres variables !
        self.stats = stats if stats is not None else {}
        
    def winner(self):
        if self.score1 > self.score2:
            return self.team1
        elif self.score2 > self.score1:
            return self.team2
        return None

    def loser(self):
        """Détermine le perdant."""
        if self.score1 < self.score2:
            return self.team1
        elif self.score2 < self.score1:
            return self.team2
        return None

    def get_total_points(self):
        """
        Calcule le volume total de points du match.
        Utile pour les statistiques globales de la compétition (ex: "tournoi le plus offensif").
        """
        return self.score1 + self.score2

    def get_points_for(self, team_name):
        """Retourne les points marqués par une équipe spécifique lors de ce match."""
        if team_name == self.team1:
            return self.score1
        elif team_name == self.team2:
            return self.score2
        return 0

    def get_points_against(self, team_name):
        """Retourne les points encaissés par une équipe spécifique lors de ce match."""
        if team_name == self.team1:
            return self.score2
        elif team_name == self.team2:
            return self.score1
        return 0

    def involves_team(self, team_name):
        """
        Filtre booléen pour savoir si une équipe a participé à ce match.
        Essentiel pour récupérer l'historique d'une équipe.
        """
        return self.team1 == team_name or self.team2 == team_name

    def get_point_difference(self):
        """Retourne l'écart de points (ou de buts/kills) entre les deux équipes."""
        return abs(self.score1 - self.score2)

    def __str__(self):
        return f"{self.date} | {self.team1} {self.score1} - {self.score2} {self.team2}"

    def __repr__(self):
        return (
            f"Match(date='{self.date}', "
            f"team1='{self.team1}', team2='{self.team2}', "
            f"score1={self.score1}, score2={self.score2}')"
        )
