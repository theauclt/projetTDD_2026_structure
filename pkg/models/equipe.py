class Equipe:
    """
    Modèle représentant une équipe ou un club.

    Parameters
    ----------
    nom : str
        Nom complet de l'équipe ou du club.
    abreviation : str, optional
        Abréviation du nom de l'équipe (ex: 'PSG', 'LAL'). Par défaut None (prendra le nom complet).
    lieu : str, optional
        Ville ou lieu de domiciliation de l'équipe. Par défaut None.
    region : str, optional
        Région ou continent de l'équipe. Par défaut None.
    """
    
    def __init__(self, id, nom, abreviation=None, lieu=None, region=None):
        self.id = id
        self.nom = nom
        self.abreviation = abreviation or nom
        self.lieu = lieu
        self.region = region
        self.joueurs = []  # Liste d'objets Joueur
        self.entraineur = None  # Objet Entraineur

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
        
        # On filtre les joueurs qui ont une taille > 0 (pour éviter de fausser la moyenne)
        tailles_valides = [j.taille for j in self.joueurs if j.taille > 0]
        
        if not tailles_valides:
            return 0
            
        return sum(tailles_valides) / len(tailles_valides)

    # --- MÉTHODES FONCTIONNELLES DE TRAITEMENT ---

    def obtenir_taille_effectif(self):
        """Retourne le nombre de joueurs dans l'effectif."""
        return len(self.joueurs)

    def obtenir_joueurs_par_nationalite(self, code_nationalite):
        """
        Filtre et retourne la liste des joueurs ayant une nationalité spécifique.
        Utile pour vérifier les quotas de joueurs étrangers dans certaines ligues.
        """
        return [joueur for joueur in self.joueurs if joueur.code_pays == code_nationalite]

    def a_effectif_minimum(self, minimum_requis=5):
        """
        Vérifie si l'équipe a suffisamment de joueurs pour participer à un match.
        """
        return len(self.joueurs) >= minimum_requis

    def __str__(self):
        return f"Équipe: {self.nom} ({self.lieu or 'Global'})"