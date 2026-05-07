class ServiceAnnuaireJoueurs:
    """Service gérant l'annuaire et les caractéristiques des joueurs."""

    def __init__(self):
        self.annuaire = {}

    def obtenir_pays_disponibles(self):
        """
        Parcourt l'annuaire pour extraire tous les codes pays (IOC) uniques.

        Retourne une liste triée par ordre alphabétique.
        """
        pays = set()  # Le "set" empêche automatiquement les doublons

        for joueur in self.annuaire.values():
            code_pays = getattr(joueur, "pays_ioc", None) or getattr(joueur, "ioc", None)
            if code_pays and str(code_pays).lower() != "nan":
                pays.add(code_pays)

        return sorted(list(pays))

    def obtenir_joueurs_par_pays(self, code_pays):
        """Retourne une liste de joueurs filtrée selon le code pays (IOC) demandé."""
        joueurs_filtres = []
        code_pays = code_pays.upper()

        for joueur in self.annuaire.values():
            pays_joueur = getattr(joueur, "pays_ioc", None) or getattr(joueur, "ioc", None)
            if pays_joueur == code_pays:
                joueurs_filtres.append(joueur)

        return sorted(joueurs_filtres, key=lambda j: j.nom_complet)

    def _convertir_poids_en_kg(self, poids_lbs):
        """Outil interne : Convertit un poids de livres (lbs) en kilogrammes (kg)."""
        try:
            poids_propre = str(poids_lbs).lower().replace("lbs", "").strip()
            valeur_lbs = float(poids_propre)
            valeur_kg = valeur_lbs * 0.453592

            return f"{round(valeur_kg, 1)} kg"
        except (ValueError, TypeError):
            return poids_lbs if poids_lbs else "N/A"

    def charger_joueurs(self, liste_joueurs):
        """Remplit l'annuaire avec la liste chargée par le DataRepository."""
        for joueur in liste_joueurs:
            if hasattr(joueur, "poids") and joueur.poids:
                if "kg" not in str(joueur.poids):
                    joueur.poids = self._convertir_poids_en_kg(joueur.poids)
            self.annuaire[str(joueur.id)] = joueur

    def obtenir_joueur(self, joueur_id):
        """Retourne les caractéristiques d'un joueur précis via son ID."""
        return self.annuaire.get(str(joueur_id))

    def obtenir_joueurs_par_affiliation(self, affiliation_id):
        """Retourne la liste des joueurs appartenant à une équipe (Basket) ou un pays (Tennis)."""
        joueurs_trouves = []
        for joueur in self.annuaire.values():
            if hasattr(joueur, "equipe_id") and str(joueur.equipe_id) == str(affiliation_id):
                joueurs_trouves.append(joueur)
        return joueurs_trouves
