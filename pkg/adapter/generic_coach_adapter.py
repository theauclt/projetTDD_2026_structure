from pkg.adapter.base_adapter import BaseAdapter
from pkg.models.coach import Coach

class GenericCoachAdapter(BaseAdapter):
    def __init__(self, col_name, col_pseudo=None, col_country=None, col_birthdate=None, col_role=None, col_team=None):
        super().__init__()
        self.params = locals() # On stocke les noms des colonnes

    def adapt(self, row) -> Coach:
        return Coach(
            name=row[self.params['col_name']],
            pseudo=row[self.params['col_pseudo']] if self.params['col_pseudo'] else None,
            country=row[self.params['col_country']] if self.params['col_country'] else None,
            birthdate=row[self.params['col_birthdate']] if self.params['col_birthdate'] else None,
            role=row[self.params['col_role']] if self.params['col_role'] else None,
            team_name=row[self.params['col_team']] if self.params['col_team'] else None
        )

    def to_row(self, coach):
        pass