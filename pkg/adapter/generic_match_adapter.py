from pkg.adapter.base_adapter import BaseAdapter
from pkg.models.match import Match

class GenericMatchAdapter(BaseAdapter):
    """
    Adaptateur universel capable de lire n'importe quel CSV de matchs
    en lui indiquant simplement le nom des colonnes à utiliser.
    """

    def __init__(self, col_date, col_equipe1, col_equipe2, col_score1, col_score2):
        """
        Initialise l'adaptateur avec les noms des colonnes du CSV.
        """
        super().__init__()
        self.col_date = col_date
        self.col_equipe1 = col_equipe1
        self.col_equipe2 = col_equipe2
        self.col_score1 = col_score1
        self.col_score2 = col_score2
        self.main_cols = [col_date, col_equipe1, col_equipe2, col_score1, col_score2]
    
    def adapt(self, row) -> Match:
        """
        Transforme une ligne de données brutes en un objet Match propre.
        """
        extra_stats = {key: value for key, value in row.items() if key not in self.main_cols}
        
        return Match(
            id=None,
            date=row[self.col_date],
            equipe1=row[self.col_equipe1],
            equipe2=row[self.col_equipe2],
            score1=int(row[self.col_score1]),
            score2=int(row[self.col_score2]),
            stats=extra_stats
        )

    def to_row(self, match: Match):
        """
        Opération inverse : transforme un objet Match en dictionnaire pour sauvegarde.
        """
        return {
            self.col_date: match.date,
            self.col_equipe1: match.equipe1,
            self.col_equipe2: match.equipe2,
            self.col_score1: match.score1,
            self.col_score2: match.score2
        }