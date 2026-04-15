class Coach:
    """Modèle représentant un entraîneur."""
    def __init__(self, name, pseudo=None, country=None, birthdate=None, role=None, team_name=None):
        self.name = name
        self.pseudo = pseudo
        self.country = country
        self.birthdate = birthdate
        self.role = role
        self.team_name = team_name # Pour faire le lien avec l'objet Team plus tard

    def __str__(self):
        return f"Coach: {self.name} [{self.role}]"