class Match: 
    """Classe représentant une rencontre sportive."""

    def __init__(
        self, 
        dateMatch: date, 
        saison: str,
        score: str,
        stadeLieu: str,
        equipe_1, # De type Equipe
        equipe_2, # De type Equipe
        score_equipe_1: float, # Mis en float pour anticiper les chronos
        score_equipe_2: float
        ) -> None:

        self.dateMatch = dateMatch
        self.saison = saison
        self.score = score
        self.stadeLieu = stadeLieu
        self.equipe_1 = equipe_1
        self.equipe_2 = equipe_2
        self.score_equipe_1 = score_equipe_1
        self.score_equipe_2 = score_equipe_2

    def vainqueur_match(self):
        """Détermine l'équipe gagnante ou retourne None s'il y a match nul."""
        if self.score_equipe_1 > self.score_equipe_2:
            return self.equipe_1
        elif self.score_equipe_2 > self.score_equipe_1:
            return self.equipe_2
        else:
            return None