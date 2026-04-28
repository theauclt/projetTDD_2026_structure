from pkg.adapter.base_adapter import BaseAdapter
from pkg.models.joueur import JoueurBasket, JoueurTennis

class BaseJoueurAdapter(BaseAdapter):
    """Gère la configuration des colonnes communes."""
    def __init__(self, col_id, col_prenom, col_nom, col_taille, col_date_naissance):
        self.col_id = col_id
        self.col_prenom = col_prenom
        self.col_nom = col_nom
        self.col_taille = col_taille
        self.col_date_naissance = col_date_naissance

    def to_row(self, joueur):
        pass # À implémenter si tu as besoin d'exporter/sauvegarder les joueurs modifiés
    
class BasketJoueurAdapter(BaseJoueurAdapter):
    """Adaptateur spécifique pour lire le CSV de la NBA."""
    def __init__(self, col_id, col_prenom, col_nom, col_taille, col_date_naissance, col_equipe, col_numero, col_position, col_poids):
        # Initialise les colonnes de base
        super().__init__(col_id, col_prenom, col_nom, col_taille, col_date_naissance)
        # Initialise les colonnes spécifiques
        self.col_equipe = col_equipe
        self.col_numero = col_numero
        self.col_position = col_position
        self.col_poids = col_poids

    def adapt(self, row) -> JoueurBasket:
        return JoueurBasket(
            id=row[self.col_id],
            prenom=row.get(self.col_prenom, ""),
            nom=row.get(self.col_nom, ""),
            taille=row.get(self.col_taille, "N/A"),
            date_naissance=row.get(self.col_date_naissance, "N/A"),
            # Spécifique Basket :
            equipe_id=row.get(self.col_equipe, "Inconnu"),
            numero=row.get(self.col_numero, "N/A"),
            position=row.get(self.col_position, "N/A"),
            poids=row.get(self.col_poids, "N/A")
        )

class TennisJoueurAdapter(BaseJoueurAdapter):
    """Adaptateur spécifique pour lire le CSV de l'ATP/WTA."""
    def __init__(self, col_id, col_prenom, col_nom, col_taille, col_date_naissance, col_pays, col_main):
        super().__init__(col_id, col_prenom, col_nom, col_taille, col_date_naissance)
        self.col_pays = col_pays
        self.col_main = col_main

    def adapt(self, row) -> JoueurTennis:
        return JoueurTennis(
            id=row[self.col_id],
            prenom=row.get(self.col_prenom, ""),
            nom=row.get(self.col_nom, ""),
            taille=row.get(self.col_taille, "N/A"),
            date_naissance=row.get(self.col_date_naissance, "N/A"),
            # Spécifique Tennis :
            pays_ioc=row.get(self.col_pays, "Inconnu"),
            main_forte=row.get(self.col_main, "N/A")
        )