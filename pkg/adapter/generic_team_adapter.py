from pkg.adapters.base_adapter import BaseAdapter
from pkg.models.team import Team

class GenericTeamAdapter(BaseAdapter):
    def __init__(self, col_name, col_abbr=None, col_loc=None, col_reg=None):
        super().__init__()
        self.col_name = col_name
        self.col_abbr = col_abbr
        self.col_loc = col_loc
        self.col_reg = col_reg

    def adapt(self, row) -> Team:
        return Team(
            name=row[self.col_name],
            abbreviation=row[self.col_abbr] if self.col_abbr else None,
            location=row[self.col_loc] if self.col_loc else None,
            region=row[self.col_reg] if self.col_reg else None
        )

    def to_row(self, team):
        pass # Optionnel pour la sauvegarde