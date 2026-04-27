class Joueur:
    """
    Représente un joueur ou une joueuse participant aux compétitions.
    """

    def __init__(self, nom, code_pays, taille, date_naissance, lieu_naissance, surnom=None):
        """
        Initialise un nouvel objet Joueur.

        Parametres:
            nom (str): Nom complet du joueur.
            code_pays (str): Code ISO du pays (ex: 'FRA', 'GER').
            taille (int): Taille en centimètres.
            date_naissance (str): Date de naissance.
            lieu_naissance (str): Lieu de naissance.
            surnom (str, optional): Surnom du joueur. Par défaut None.
        """
        self.nom = nom
        self.code_pays = code_pays
        self.taille = taille
        self.date_naissance = date_naissance
        self.lieu_naissance = lieu_naissance
        self.surnom = surnom

    def __str__(self):
        """Retourne une représentation lisible du joueur."""
        return f"{self.nom} ({self.code_pays})"

    def __repr__(self):
        """Retourne une représentation détaillée pour le débogage."""
        return (
            f"Joueur(nom='{self.nom}', code_pays='{self.code_pays}', "
            f"taille={self.taille}, date_naissance='{self.date_naissance}', "
            f"lieu_naissance='{self.lieu_naissance}', surnom='{self.surnom}')"
        )
    
    def est_grand(self, seuil=190):
        """Détermine si le joueur est considéré comme grand (utile pour le Volley ou le Basket)."""
        return self.taille >= seuil