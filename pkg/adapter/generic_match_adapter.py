from pkg.adapter.base_adapter import BaseAdapter
from pkg.models.match import Match


class GenericMatchAdapter(BaseAdapter):
    """
    Adaptateur universel capable de lire n'importe quel CSV de matchs.
    Gère désormais une colonne optionnelle pour le type de match (Playoffs/Saison).
    """

    # On ajoute col_type_match=None pour qu'il soit facultatif
    def __init__(
        self,
        col_date,
        col_equipe1,
        col_equipe2,
        col_score1,
        col_score2,
        col_type_match=None,
    ):
        super().__init__()
        self.col_date = col_date
        self.col_equipe1 = col_equipe1
        self.col_equipe2 = col_equipe2
        self.col_score1 = col_score1
        self.col_score2 = col_score2
        self.col_type_match = col_type_match

        # On garde la trace des colonnes principales
        self.main_cols = [col_date, col_equipe1, col_equipe2, col_score1, col_score2]
        if col_type_match:
            self.main_cols.append(col_type_match)

    def adapt(self, row) -> Match:
        # On récupère toutes les autres colonnes automatiquement
        extra_stats = {
            key: value for key, value in row.items() if key not in self.main_cols
        }

        # Si on a défini une colonne pour le type de match, on la force dans les stats
        # Sinon, par défaut on dit que c'est un match de saison régulière
        if self.col_type_match and self.col_type_match in row:
            extra_stats["type_match"] = str(row[self.col_type_match])
        else:
            extra_stats["type_match"] = "Regular Season"

        return Match(
            id=None,
            date=row[self.col_date],
            equipe1=row[self.col_equipe1],
            equipe2=row[self.col_equipe2],
            score1=int(row[self.col_score1]),
            score2=int(row[self.col_score2]),
            stats=extra_stats,
        )

    def to_row(self, match: Match):
        row = {
            self.col_date: match.date,
            self.col_equipe1: match.equipe1,
            self.col_equipe2: match.equipe2,
            self.col_score1: match.score1,
            self.col_score2: match.score2,
        }
        if self.col_type_match and "type_match" in match.stats:
            row[self.col_type_match] = match.stats["type_match"]

        return row


class TennisMatchAdapter(BaseAdapter):
    """Adaptateur spécialisé pour lire les données d'un match de Tennis."""

    # 1. On ajoute col_id ici
    def __init__(self, col_id, col_date, col_vainqueur, col_perdant):
        self.col_id = col_id
        self.col_date = col_date
        self.col_vainqueur = col_vainqueur
        self.col_perdant = col_perdant

    def adapt(self, row):
        stats_tennis = {
            "minutes": row.get("minutes", 0),
            "w_ace": row.get("w_ace", 0),
            "w_df": row.get("w_df", 0),
            "w_bpSaved": row.get("w_bpSaved", 0),
            "w_bpFaced": row.get("w_bpFaced", 0),
            "l_ace": row.get("l_ace", 0),
            "l_df": row.get("l_df", 0),
            "l_bpSaved": row.get("l_bpSaved", 0),
            "l_bpFaced": row.get("l_bpFaced", 0),
            "tourney_name": row.get("tourney_name", "Tournoi Inconnu"),
            "round": row.get("round", ""),
        }

        # 2. On ajoute l'ID ici au moment de créer l'objet Match !
        return Match(
            id=row.get(self.col_id, "Inconnu"),
            date=row[self.col_date],
            equipe1=row[self.col_vainqueur],
            equipe2=row[self.col_perdant],
            score1=1,
            score2=0,
            stats=stats_tennis,
        )

    def to_row(self, match):
        """Transforme un objet Match en ligne (dictionnaire) pour l'écriture."""
        row = {
            self.col_id: match.id,  # On n'oublie pas l'ID pour l'écriture non plus
            self.col_date: match.date,
            self.col_vainqueur: match.equipe1,
            self.col_perdant: match.equipe2,
        }

        if hasattr(match, "stats") and isinstance(match.stats, dict):
            row.update(match.stats)

        return row
