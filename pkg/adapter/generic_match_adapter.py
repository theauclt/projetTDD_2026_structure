from pkg.adapters.base_adapter import BaseAdapter
from pkg.models.match import Match

class GenericMatchAdapter(BaseAdapter):
    """
    Adaptateur universel capable de lire n'importe quel CSV de matchs
    en lui indiquant simplement le nom des colonnes à utiliser.
    """

    def __init__(self, col_date, col_team1, col_team2, col_score1, col_score2):
        """
        Initialise l'adaptateur avec les noms des colonnes du CSV.
        """
        super().__init__()
        self.col_date = col_date
        self.col_team1 = col_team1
        self.col_team2 = col_team2
        self.col_score1 = col_score1
        self.col_score2 = col_score2

    def adapt(self, row) -> Match:
        """
        Transforme une ligne de données brutes en un objet Match propre.
        """
        return Match(
            id=None,
            date=row[self.col_date],
            team1=row[self.col_team1],
            team2=row[self.col_team2],
            score1=int(row[self.col_score1]),
            score2=int(row[self.col_score2])
        )

    def to_row(self, match: Match):
        """
        Opération inverse : transforme un objet Match en dictionnaire pour sauvegarde.
        """
        return {
            self.col_date: match.date,
            self.col_team1: match.team1,
            self.col_team2: match.team2,
            self.col_score1: match.score1,
            self.col_score2: match.score2
        }