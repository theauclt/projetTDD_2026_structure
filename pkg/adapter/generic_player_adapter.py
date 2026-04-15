import pandas as pd
from pkg.adapters.base_adapter import BaseAdapter
from pkg.models.player import Player

class GenericPlayerAdapter(BaseAdapter):
    """Adaptateur générique pour lire n'importe quel fichier de joueurs."""

    def __init__(self, col_name, col_country, col_height=None, col_birthdate=None, col_birthplace=None, col_nickname=None):
        super().__init__()
        self.col_name = col_name
        self.col_country = col_country
        # Les champs suivants sont optionnels car tous les sports ne les ont pas
        self.col_height = col_height
        self.col_birthdate = col_birthdate
        self.col_birthplace = col_birthplace
        self.col_nickname = col_nickname

    def adapt(self, row) -> Player:
        # On gère intelligemment les colonnes : si la colonne n'existe pas ou est vide, on met une valeur par défaut
        height = int(row[self.col_height]) if self.col_height and pd.notna(row.get(self.col_height)) else 0
        birthdate = row[self.col_birthdate] if self.col_birthdate else "Inconnue"
        birthplace = row[self.col_birthplace] if self.col_birthplace else "Inconnu"
        
        nickname = None
        if self.col_nickname and pd.notna(row.get(self.col_nickname)):
             nickname = row[self.col_nickname]

        return Player(
            name=row[self.col_name],
            country_code=row[self.col_country],
            height=height,
            birth_date=birthdate,
            birth_place=birthplace,
            nickname=nickname
        )

    def to_row(self, player):
        pass # À implémenter si tu as besoin d'exporter/sauvegarder les joueurs modifiés