import pandas as pd
from pkg.adapter.base_adapter import BaseAdapter
from pkg.models.joueur import Joueur

class GenericJoueurAdapter(BaseAdapter):
    """Adaptateur générique pour lire n'importe quel fichier de joueurs."""

    def __init__(self, col_nom, col_pays, col_taille=None, col_date_naissance=None, col_birthplace=None, col_nicknom=None):
        super().__init__()
        self.col_nom = col_nom
        self.col_pays = col_pays
        # Les champs suivants sont optionnels car tous les sports ne les ont pas
        self.col_taille = col_taille
        self.col_date_naissance = col_date_naissance
        self.col_birthplace = col_birthplace
        self.col_nicknom = col_nicknom

    def adapt(self, row) -> Joueur:
        # On gère intelligemment les colonnes : si la colonne n'existe pas ou est vide, on met une valeur par défaut
        taille = int(row[self.col_taille]) if self.col_taille and pd.notna(row.get(self.col_taille)) else 0
        date_naissance = row[self.col_date_naissance] if self.col_date_naissance else "Inconnue"
        birthplace = row[self.col_birthplace] if self.col_birthplace else "Inconnu"
        
        nicknom = None
        if self.col_nicknom and pd.notna(row.get(self.col_nicknom)):
             nicknom = row[self.col_nicknom]

        return Joueur(
            nom=row[self.col_nom],
            code_pays=row[self.col_pays],
            taille=taille,
            date_naissance=date_naissance,
            lieu_naissance=birthplace,
            nicknom=nicknom
        )

    def to_row(self, joueur):
        pass # À implémenter si tu as besoin d'exporter/sauvegarder les joueurs modifiés