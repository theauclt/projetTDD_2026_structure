class ServiceAnnuaireJoueurs:
    """Service gérant l'annuaire et les caractéristiques des joueurs."""
    
    def __init__(self):
        # Dictionnaire pour retrouver un joueur par son ID : { "123": Objet(Joueur) }
        self.annuaire = {}

    def obtenir_pays_disponibles(self):
        """
        Parcourt l'annuaire pour extraire tous les codes pays (IOC) uniques.
        Retourne une liste triée par ordre alphabétique.
        """
        pays = set() # Le "set" empêche automatiquement les doublons
        
        for joueur in self.annuaire.values():
            # On utilise getattr pour éviter les erreurs si l'attribut a un nom légèrement différent
            code_pays = getattr(joueur, 'pays_ioc', None) or getattr(joueur, 'ioc', None)
            
            # On ignore les pays vides ou les erreurs de lecture 'nan'
            if code_pays and str(code_pays).lower() != 'nan':
                pays.add(code_pays)
                
        return sorted(list(pays))

    def obtenir_joueurs_par_pays(self, code_pays):
        """
        Retourne une liste de joueurs filtrée selon le code pays (IOC) demandé.
        """
        joueurs_filtres = []
        code_pays = code_pays.upper() # On s'assure que la casse correspond
        
        for joueur in self.annuaire.values():
            pays_joueur = getattr(joueur, 'pays_ioc', None) or getattr(joueur, 'ioc', None)
            if pays_joueur == code_pays:
                joueurs_filtres.append(joueur)

        # On trie les joueurs trouvés par ordre alphabétique de leur nom complet
        return sorted(joueurs_filtres, key=lambda j: j.nom_complet)
    
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
            if hasattr(joueur, 'equipe_id') and str(joueur.equipe_id) == str(affiliation_id):
                joueurs_trouves.append(joueur)
        return joueurs_trouves