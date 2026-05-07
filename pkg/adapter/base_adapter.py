from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """Classe de base abstraite pour tous les adaptateurs."""

    @abstractmethod
    def adapt(self, row):
        """Convertir une ligne de données brute en objet."""
        raise NotImplementedError

    @abstractmethod
    def to_row(self, match):
        """Convertir un objet en ligne de dictionnaire."""
        raise NotImplementedError
