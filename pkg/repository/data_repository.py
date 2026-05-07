from typing import List

from pandas import DataFrame, read_csv

from pkg.models.match import Match


class DataRepository:
    """Dépôt responsable de la lecture et de l'écriture des données en CSV."""

    def __init__(self, file, adapter, sep=";"):
        self.adapter = adapter
        self.file = file
        self.sep = sep

    def load(self) -> List[Match]:
        """Charger les données du fichier CSV et les convertir en objets métier."""
        self.df = read_csv(self.file, sep=self.sep)
        return [self.adapter.adapt(row) for _, row in self.df.iterrows()]

    def save(self, objects):
        """Sauvegarder une liste d'objets métier dans le fichier CSV d'origine."""
        rows = [self.adapter.to_row(obj) for obj in objects]
        df = DataFrame(rows)
        df.to_csv(self.file, index=False)
