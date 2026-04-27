from collections import defaultdict

class ServiceStatistiques:
    """
    Service responsable de l'analyse et de la manipulation des données.
    Fonctionne indépendamment du sport grâce aux modèles génériques.
    """

    def __init__(self):
        self.matchs = []
        # defaultdict initialise automatiquement les stats à 0 
        # pour une équipe ou un joueur dès qu'on le rencontre.
        self.stats = defaultdict(lambda: {
            'joues': 0, 
            'victoires': 0, 
            'defaites': 0, 
            'nuls': 0, 
            'points_marques': 0
        })

    def charger_matchs(self, liste_matchs):
        """Charge un historique complet de matchs et met à jour les statistiques."""
        for match in liste_matchs:
            self.ajouter_match(match)

    def ajouter_match(self, match):
        """Ajoute un nouveau match et met à jour les caractéristiques en temps réel."""
        self.matchs.append(match)

        # 1. Mise à jour des matchs joués
        self.stats[match.equipe1]['joues'] += 1
        self.stats[match.equipe2]['joues'] += 1

        # 2. Mise à jour des points marqués (ou buts, ou sets)
        self.stats[match.equipe1]['points_marques'] += match.score1
        self.stats[match.equipe2]['points_marques'] += match.score2

        # 3. Détermination du gagnant et mise à jour du palmarès
        if match.score1 > match.score2:
            self.stats[match.equipe1]['victoires'] += 1
            self.stats[match.equipe2]['defaites'] += 1
        elif match.score2 > match.score1:
            self.stats[match.equipe2]['victoires'] += 1
            self.stats[match.equipe1]['defaites'] += 1
        else:
            self.stats[match.equipe1]['nuls'] += 1
            self.stats[match.equipe2]['nuls'] += 1

    def obtenir_classement_global(self):
        """
        Génère un classement global trié.
        Critère 1 : Nombre de victoires
        Critère 2 : Nombre de points marqués
        """
        classement = sorted(
            self.stats.items(),
            key=lambda item: (item[1]['victoires'], item[1]['points_marques']),
            reverse=True # Ordre décroissant (du meilleur au pire)
        )
        return classement
    
    def obtenir_stats_entite(self, nom_entite):
        """Récupère les statistiques détaillées d'une équipe ou d'un joueur."""
        if nom_entite in self.stats:
            return self.stats[nom_entite]
        return None
    
    # --- MÉTHODES DE MANIPULATION COMPLEXES ---

    def obtenir_historique_equipe(self, nom_equipe):
        """Filtre la base de matchs pour ressortir l'historique d'une équipe."""
        return [match for match in self.matchs if match.implique_equipe(nom_equipe)]

    def calculer_classement_championnat(self, pts_victoire=3, pts_nul=1, pts_defaite=0):
        """
        Calcule le classement générique d'un tournoi (type championnat).
        Retourne un dictionnaire complexe avec toutes les stats agrégées.
        """
        # pm = points marqués, pe = points encaissés, diff = différence
        classement = defaultdict(lambda: {'joues': 0, 'points': 0, 'victoires': 0, 'nuls': 0, 'defaites': 0, 'pm': 0, 'pe': 0, 'diff': 0})

        for match in self.matchs:
            eq1, eq2 = match.equipe1, match.equipe2
            
            classement[eq1]['joues'] += 1
            classement[eq2]['joues'] += 1
            
            # Utilisation des méthodes de la classe Match
            classement[eq1]['pm'] += match.obtenir_points_pour(eq1)
            classement[eq1]['pe'] += match.obtenir_points_contre(eq1)
            classement[eq2]['pm'] += match.obtenir_points_pour(eq2)
            classement[eq2]['pe'] += match.obtenir_points_contre(eq2)

            vainqueur = match.vainqueur()
            if vainqueur == eq1:
                classement[eq1]['victoires'] += 1
                classement[eq1]['points'] += pts_victoire
                classement[eq2]['defaites'] += 1
                classement[eq2]['points'] += pts_defaite
            elif vainqueur == eq2:
                classement[eq2]['victoires'] += 1
                classement[eq2]['points'] += pts_victoire
                classement[eq1]['defaites'] += 1
                classement[eq1]['points'] += pts_defaite
            else:
                classement[eq1]['nuls'] += 1
                classement[eq2]['nuls'] += 1
                classement[eq1]['points'] += pts_nul
                classement[eq2]['points'] += pts_nul

        # Calcul de la différence de points finale
        for equipe, stats in classement.items():
            stats['diff'] = stats['pm'] - stats['pe']

        # Tri : Points > Différence > Points marqués
        return sorted(classement.items(), key=lambda x: (x[1]['points'], x[1]['diff'], x[1]['pm']), reverse=True)