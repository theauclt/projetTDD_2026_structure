from pkg.adapter.base_adapter import BaseAdapter
from pkg.models.entraineur import Entraineur

class GenericEntraineurAdapter(BaseAdapter):
    def __init__(self, col_nom, col_pseudo=None, col_pays=None, col_date_naissance=None, col_role=None, col_equipe=None):
        super().__init__()
        self.params = locals() # On stocke les noms des colonnes

    def adapt(self, row) -> Entraineur:
        return Entraineur(
            nom=row[self.params['col_nom']],
            pseudo=row[self.params['col_pseudo']] if self.params['col_pseudo'] else None,
            pays=row[self.params['col_pays']] if self.params['col_pays'] else None,
            date_naissance=row[self.params['col_date_naissance']] if self.params['col_date_naissance'] else None,
            role=row[self.params['col_role']] if self.params['col_role'] else None,
            equipe_nom=row[self.params['col_equipe']] if self.params['col_equipe'] else None
        )

    def to_row(self, entraineur):
        pass