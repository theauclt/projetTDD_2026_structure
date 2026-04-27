class Match:
    """
    Modèle représentant une rencontre sportive.

    Parameters
    ----------
    id_match : str ou int
        Identifiant unique du match.
    date : str
        Date à laquelle le match a eu lieu (ex: '2024-05-12').
    equipe1 : str ou Equipe
        Nom de la première équipe ou objet Equipe (souvent l'équipe à domicile).
    equipe2 : str ou Equipe
        Nom de la seconde équipe ou objet Equipe (souvent l'équipe à l'extérieur).
    score1 : float ou int
        Score final obtenu par l'équipe 1.
    score2 : float ou int
        Score final obtenu par l'équipe 2.
    """

    def __init__(self, id_match, date, equipe1, equipe2, score1, score2):
        self.id_match = id_match
        self.date = date
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.score1 = score1
        self.score2 = score2

    def vainqueur(self):
        """Détermine le gagnant."""
        if self.score1 > self.score2:
            return self.equipe1
        elif self.score2 > self.score1:
            return self.equipe2
        return None

    def perdant(self):
        """Détermine le perdant."""
        if self.score1 < self.score2:
            return self.equipe1
        elif self.score2 < self.score1:
            return self.equipe2
        return None

    def obtenir_total_points(self):
        """
        Calcule le volume total de points du match.
        Utile pour les statistiques globales de la compétition (ex: "tournoi le plus offensif").
        """
        return self.score1 + self.score2

    def obtenir_points_pour(self, nom_equipe):
        """Retourne les points marqués par une équipe spécifique lors de ce match."""
        if nom_equipe == self.equipe1:
            return self.score1
        elif nom_equipe == self.equipe2:
            return self.score2
        return 0

    def obtenir_points_contre(self, nom_equipe):
        """Retourne les points encaissés par une équipe spécifique lors de ce match."""
        if nom_equipe == self.equipe1:
            return self.score2
        elif nom_equipe == self.equipe2:
            return self.score1
        return 0

    def implique_equipe(self, nom_equipe):
        """
        Filtre booléen pour savoir si une équipe a participé à ce match.
        Essentiel pour récupérer l'historique d'une équipe.
        """
        return self.equipe1 == nom_equipe or self.equipe2 == nom_equipe

    def obtenir_difference_points(self):
        """Retourne l'écart de points (ou de buts/kills) entre les deux équipes."""
        return abs(self.score1 - self.score2)

    def __str__(self):
        return f"{self.date} | {self.equipe1} {self.score1} - {self.score2} {self.equipe2}"

    def __repr__(self):
        return (
            f"Match(date='{self.date}', "
            f"equipe1='{self.equipe1}', equipe2='{self.equipe2}', "
            f"score1={self.score1}, score2={self.score2})"
        )