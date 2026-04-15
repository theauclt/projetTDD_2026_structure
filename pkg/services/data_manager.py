class DataManager:
    """Service central pour charger et lier toutes les entités sportives."""
    def __init__(self):
        self.teams = {}   # Dict {nom: objet Team}
        self.players = []
        self.coaches = []

    def load_all(self, team_repo, player_repo, coach_repo):
        # 1. Charger les équipes
        loaded_teams = team_repo.load()
        for t in loaded_teams:
            self.teams[t.name] = t

        # 2. Charger les joueurs et les lier à leur équipe
        self.players = player_repo.load()
        # Ici, on pourrait ajouter une logique pour mettre les joueurs dans self.teams[p.team].players

        # 3. Charger les coachs et les lier
        self.coaches = coach_repo.load()
        for c in self.coaches:
            if c.team_name in self.teams:
                self.teams[c.team_name].coach = c

    def get_team_info(self, team_name):
        team = self.teams.get(team_name)
        if team:
            return f"{team} - Coach: {team.coach.name if team.coach else 'Aucun'}"
        return "Équipe inconnue"