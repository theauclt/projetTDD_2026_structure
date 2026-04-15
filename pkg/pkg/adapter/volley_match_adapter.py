from typing import Dict

from pkg.adapter.base_adapter import BaseAdapter
from pkg.models.match import Match


class VolleyMatchAdapter(BaseAdapter):

    def __init__(self):
        super().__init__()

    def adapt(self, row) -> Match:
        """Converti une ligne provenant d'un fichier csv lu par pandas en objet python

        Args:
            row (_type_): _description_

        Returns:
            Match: _description_
        """
        score1 = int(row["set_country_1"])
        score2 = int(row["set_country_2"])

        return Match(
            id=None,  # ou généré si besoin
            date=row["date"],
            team1=row["country_code_1"],
            team2=row["country_code_2"],
            score1=score1,
            score2=score2,
        )

    def to_row(self, match) -> Dict[str, str]:
        return {
            "date": match.date,
            "country_code_1": match.team1,
            "country_code_2": match.team2,
            "set_country_1": match.score1,
            "set_country_2": match.score2,
        }
