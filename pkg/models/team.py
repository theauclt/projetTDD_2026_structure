class Team:
    """Modèle représentant une équipe ou un club."""
    def __init__(self, name, abbreviation=None, location=None, region=None):
        self.name = name
        self.abbreviation = abbreviation or name
        self.location = location
        self.region = region
        self.players = []  # Liste d'objets Player
        self.coach = None  # Objet Coach

    def __str__(self):
        return f"Équipe: {self.name} ({self.location or 'Global'})"