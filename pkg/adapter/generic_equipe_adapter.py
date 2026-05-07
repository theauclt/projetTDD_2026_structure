from pkg.adapter.base_adapter import BaseAdapter
from pkg.models.equipe import Equipe


class GenericEquipeAdapter(BaseAdapter):
    """Adaptateur générique pour transformer les données en équipes."""

    def __init__(self, col_id, col_nom, col_abbr=None, col_loc=None, col_reg=None):
        super().__init__()
        self.col_id = col_id
        self.col_nom = col_nom
        self.col_abbr = col_abbr
        self.col_loc = col_loc
        self.col_reg = col_reg

    def adapt(self, row) -> Equipe:
        """Extraire une ligne de CSV pour créer un objet Equipe."""
        return Equipe(
            id=row[self.col_id],
            nom=row[self.col_nom],
            abreviation=row[self.col_abbr] if self.col_abbr else None,
            lieu=row[self.col_loc] if self.col_loc else None,
            region=row[self.col_reg] if self.col_reg else None,
        )

    def to_row(self, equipe):
        """Convertir un objet Equipe en ligne de dictionnaire."""
        pass
