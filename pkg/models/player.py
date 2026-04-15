class Player:
    """
    Représente un joueur ou une joueuse participant aux compétitions.
    """

    def __init__(self, name, country_code, height, birth_date, birth_place, nickname=None):
        """
        Initialise un nouvel objet Player.

        Args:
            name (str): Nom complet du joueur.
            country_code (str): Code ISO du pays (ex: 'FRA', 'GER').
            height (int): Taille en centimètres.
            birth_date (str): Date de naissance.
            birth_place (str): Lieu de naissance.
            nickname (str, optional): Surnom du joueur. Par défaut None.
        """
        self.name = name
        self.country_code = country_code
        self.height = height
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.nickname = nickname

    def __str__(self):
        """Retourne une représentation lisible du joueur."""
        return f"{self.name} ({self.country_code})"

    def __repr__(self):
        """Retourne une représentation détaillée pour le débogage."""
        return (
            f"Player(name='{self.name}', country_code='{self.country_code}', "
            f"height={self.height}, birth_date='{self.birth_date}', "
            f"birth_place='{self.birth_place}', nickname='{self.nickname}')"
        )
    
    def is_tall(self, threshold=190):
        """Détermine si le joueur est considéré comme grand (utile pour le Volley ou le Basket)."""
        return self.height >= threshold