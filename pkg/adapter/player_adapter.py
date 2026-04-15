import pandas as pd
from typing import Dict, Any

from pkg.adapter.base_adapter import BaseAdapter
from pkg.models.player import Player


class PlayerAdapter(BaseAdapter):
    """
    Adaptateur pour convertir les données brutes des fichiers CSV de joueurs
    en objets de la classe Player, et inversement.
    """

    def __init__(self):
        super().__init__()

    def adapt(self, row) -> Player:
        """
        Convertit une ligne lue par Pandas (Series) en un objet Player.

        Args:
            row: Une ligne de données contenant les informations du joueur.

        Returns:
            Player: Une instance de la classe Player prête à être utilisée.
        """
        # Dans tes données, le surnom ("nickname") est parfois manquant.
        # Pandas lit les cases vides comme "NaN" (Not a Number). 
        # On vérifie ça pour mettre proprement "None" en Python.
        nickname = row["nickname"]
        if pd.isna(nickname):
            nickname = None

        return Player(
            name=row["name"],
            country_code=row["country_code"],
            height=int(row["height"]),
            birth_date=row["birth_date"],
            birth_place=row["birth_place"],
            nickname=nickname
        )

    def to_row(self, player: Player) -> Dict[str, Any]:
        """
        Fait l'opération inverse : convertit un objet Player en dictionnaire
        pour pouvoir le sauvegarder plus tard dans un fichier CSV.

        Args:
            player (Player): L'objet joueur à sauvegarder.

        Returns:
            Dict: Les données prêtes à être écrites dans un fichier.
        """
        return {
            "name": player.name,
            "country_code": player.country_code,
            "height": player.height,
            "birth_date": player.birth_date,
            "birth_place": player.birth_place,
            "nickname": player.nickname if player.nickname is not None else ""
        }