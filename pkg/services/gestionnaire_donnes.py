class GestionnaireDonnees:
    """
    Service central pour stocker et lier toutes les entités sportives en mémoire.
    """
    
    def __init__(self):
        self.equipes = {}   # Dictionnaire {nom_equipe: objet Equipe}
        self.joueurs = []   # Liste d'objets Joueur
        self.entraineurs = [] # Liste d'objets Entraineur

    def charger_tout(self, depot_equipes, depot_joueurs, depot_entraineurs):
        """Charge toutes les données (à adapter avec notre lecteur CSV Pandas)."""
        # 1. Charger les équipes
        equipes_chargees = depot_equipes.load()
        for equipe in equipes_chargees:
            self.equipes[equipe.nom] = equipe

        # 2. Charger les joueurs
        self.joueurs = depot_joueurs.load()

        # 3. Charger les entraîneurs et les lier
        self.entraineurs = depot_entraineurs.load()
        for entraineur in self.entraineurs:
            if entraineur.nom_equipe in self.equipes:
                self.equipes[entraineur.nom_equipe].assigner_entraineur(entraineur)

    def obtenir_info_equipe(self, nom_equipe):
        """Retourne un résumé textuel d'une équipe."""
        equipe = self.equipes.get(nom_equipe)
        if equipe:
            nom_coach = equipe.entraineur.nom if equipe.entraineur else 'Aucun'
            return f"{equipe.nom} - Entraîneur: {nom_coach}"
        return "Équipe inconnue"