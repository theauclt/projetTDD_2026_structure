class Equipe:
    """Modèle représentant une équipe ou un club."""

    def __init__(self, id, nom, abreviation=None, lieu=None, region=None):
        self.id = id
        self.nom = nom
        self.abreviation = abreviation or nom
        self.lieu = lieu
        self.region = region
        self.joueurs = []
        self.entraineur = None

    def ajouter_joueur(self, joueur):
        """Ajoute un joueur à l'effectif de l'équipe."""
        if joueur not in self.joueurs:
            self.joueurs.append(joueur)

    def assigner_entraineur(self, entraineur):
        """Assigne un entraîneur à l'équipe."""
        self.entraineur = entraineur

    def obtenir_taille_moyenne(self):
        """Calcule la taille moyenne des joueurs de l'équipe."""
        if not self.joueurs:
            return 0

        tailles_valides = [j.taille for j in self.joueurs if j.taille > 0]

        if not tailles_valides:
            return 0

        return sum(tailles_valides) / len(tailles_valides)

    # --- MÉTHODES FONCTIONNELLES DE TRAITEMENT ---

    def obtenir_taille_effectif(self):
        """Retourne le nombre de joueurs dans l'effectif."""
        return len(self.joueurs)

    def obtenir_joueurs_par_nationalite(self, code_nationalite):
        """Filtre et retourne la liste des joueurs ayant une nationalité spécifique."""
        return [joueur for joueur in self.joueurs if joueur.code_pays == code_nationalite]

    def a_effectif_minimum(self, minimum_requis=5):
        """Vérifie si l'équipe a suffisamment de joueurs pour participer à un match."""
        return len(self.joueurs) >= minimum_requis

    def __str__(self):
        """Fournir une représentation textuelle courte de l'équipe."""
        return f"Équipe: {self.nom} ({self.lieu or 'Global'})"
