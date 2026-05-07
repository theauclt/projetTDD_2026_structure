class Match:
    """Modèle représentant une rencontre sportive."""

    def __init__(self, id, date, equipe1, equipe2, score1, score2, stats=None):

        self.id = id
        self.date = date
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.score1 = score1
        self.score2 = score2
        self.stats = stats if stats is not None else {}

    def vainqueur(self):
        """Déterminer le vainqueur du match."""
        if self.score1 > self.score2:
            return self.equipe1
        elif self.score2 > self.score1:
            return self.equipe2
        return None

    def perdant(self):
        """Déterminer le perdant du match."""
        if self.score1 < self.score2:
            return self.equipe1
        elif self.score2 < self.score1:
            return self.equipe2
        return None

    def obtenir_total_points(self):
        """Calcule le volume total de points du match."""
        return self.score1 + self.score2

    def obtenir_points_pour(self, nom_equipe):
        """Retourner les points marqués par une équipe spécifique lors de ce match."""
        if nom_equipe == self.equipe1:
            return self.score1
        elif nom_equipe == self.equipe2:
            return self.score2
        return 0

    def obtenir_points_contre(self, nom_equipe):
        """Retourner les points encaissés par une équipe spécifique lors de ce match."""
        if nom_equipe == self.equipe1:
            return self.score2
        elif nom_equipe == self.equipe2:
            return self.score1
        return 0

    def implique_equipe(self, nom_equipe):
        """Filtrer booléen pour savoir si une équipe a participé à ce match."""
        return self.equipe1 == nom_equipe or self.equipe2 == nom_equipe

    def obtenir_difference_points(self):
        """Retourner l'écart de points entre les deux équipes."""
        return abs(self.score1 - self.score2)

    def __str__(self):
        """Fournir une représentation textuelle courte du match."""
        return f"{self.date} | {self.equipe1} {self.score1} - {self.score2} {self.equipe2}"

    def __repr__(self):
        """Fournir une représentation technique et officielle du match."""
        return (
            f"Match(date='{self.date}', "
            f"equipe1='{self.equipe1}', equipe2='{self.equipe2}', "
            f"score1={self.score1}, score2={self.score2})"
        )
