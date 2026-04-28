class ServiceAnnuaireJoueurs:
    """Service gérant l'annuaire et les caractéristiques des joueurs."""
    
    def __init__(self):
        # Dictionnaire pour retrouver un joueur par son ID : { "123": Objet(Joueur) }
        self.annuaire = {}

    def charger_joueurs(self, liste_joueurs):
        """Remplit l'annuaire avec la liste chargée par le DataRepository."""
        for joueur in liste_joueurs:
            self.annuaire[str(joueur.id)] = joueur

    def obtenir_joueur(self, joueur_id):
        """Retourne les caractéristiques d'un joueur précis via son ID."""
        return self.annuaire.get(str(joueur_id))

    def obtenir_joueurs_par_affiliation(self, affiliation_id):
        """Retourne la liste des joueurs appartenant à une équipe (Basket) ou un pays (Tennis)."""
        joueurs_trouves = []
        for joueur in self.annuaire.values():
            # Si le joueur a l'ID de l'équipe qu'on cherche, on l'ajoute à la liste
            # (Pour le basket, self.affiliation correspond à self.equipe_id grâce à l'héritage)
            if hasattr(joueur, 'equipe_id') and str(joueur.equipe_id) == str(affiliation_id):
                joueurs_trouves.append(joueur)
            # Pour le tennis (si on cherche par pays IOC)
            elif hasattr(joueur, 'pays_ioc') and str(joueur.pays_ioc) == str(affiliation_id):
                joueurs_trouves.append(joueur)
                
        return joueurs_trouves