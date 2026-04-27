class Team:
    """Modèle représentant une équipe participant à la compétition."""
    # NOUVEAU : Ajout du paramètre id
    def __init__(self, id, name, abbreviation=None, location=None, region=None):
        self.id = id
        self.name = name
        self.abbreviation = abbreviation or name
        self.location = location
        self.region = region
        self.players = []  
        self.coach = None

    def add_player(self, player):
        """Ajoute un joueur à l'effectif de l'équipe."""
        if player not in self.players:
            self.players.append(player)

    def assign_coach(self, coach):
        """Assigne un entraîneur à l'équipe."""
        self.coach = coach

    def get_average_height(self):
        """Calcule la taille moyenne des joueurs de l'équipe."""
        if not self.players:
            return 0
        
        # On filtre les joueurs qui ont une taille > 0 (pour éviter de fausser la moyenne)
        valid_heights = [p.height for p in self.players if p.height > 0]
        
        if not valid_heights:
            return 0
            
        return sum(valid_heights) / len(valid_heights)

    # --- MÉTHODES FONCTIONNELLES DE TRAITEMENT ---

    def get_roster_size(self):
        """Retourne le nombre de joueurs dans l'effectif."""
        return len(self.players)

    def get_players_by_nationality(self, nationality_code):
        """
        Filtre et retourne la liste des joueurs ayant une nationalité spécifique.
        Utile pour vérifier les quotas de joueurs étrangers dans certaines ligues.
        """
        return [player for player in self.players if player.country_code == nationality_code]

    def has_minimum_roster(self, minimum_required=5):
        """
        Vérifie si l'équipe a suffisamment de joueurs pour participer à un match.
        """
        return len(self.players) >= minimum_required

    def __str__(self):
        return f"Équipe: {self.name} ({self.location or 'Global'})"