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


class ServiceStatistiquesBasket(ServiceStatistiques):
    """Service spécialisé pour traiter les statistiques complexes de la NBA."""
    
    def __init__(self):
        super().__init__() # Initialise les victoires/défaites du service parent
        
        # On crée un dictionnaire pour stocker les totaux de la saison
        self.stats_nba = defaultdict(lambda: {
            'matchs_joues': 0, 'points_marques': 0, 'points_encaisses': 0,
            'rebonds': 0, 'passes': 0, 'interceptions': 0, 'contres': 0,
            'fg2m': 0, 'fg2a': 0, # 2 points (réussis / tentés)
            'fg3m': 0, 'fg3a': 0, # 3 points
            'ftm': 0, 'fta': 0    # Lancers francs
        })

    def charger_matchs(self, matchs):
        # 1. On lance le calcul de base (victoires) du parent
        super().charger_matchs(matchs)
        
        # 2. On plonge dans le sac à dos pour les stats NBA
        for match in matchs:
            # === STATS POUR L'ÉQUIPE À DOMICILE (Equipe 1) ===
            d_home = self.stats_nba[match.equipe1]
            d_home['matchs_joues'] += 1
            d_home['points_marques'] += match.score1
            d_home['points_encaisses'] += match.score2
            
            # On utilise float() pour éviter les bugs si le CSV a des vides
            d_home['rebonds'] += float(match.stats.get('reb_home', 0))
            d_home['passes'] += float(match.stats.get('ast_home', 0))
            d_home['interceptions'] += float(match.stats.get('stl_home', 0))
            d_home['contres'] += float(match.stats.get('blk_home', 0))
            
            # Calcul des tirs (FGM = Field Goals Made = Total des tirs)
            fgm_h = float(match.stats.get('fgm_home', 0))
            fga_h = float(match.stats.get('fga_home', 0))
            fg3m_h = float(match.stats.get('fg3m_home', 0))
            fg3a_h = float(match.stats.get('fg3a_home', 0))
            
            d_home['fg3m'] += fg3m_h
            d_home['fg3a'] += fg3a_h
            d_home['fg2m'] += (fgm_h - fg3m_h) # 2pts = Total - 3pts
            d_home['fg2a'] += (fga_h - fg3a_h)
            d_home['ftm'] += float(match.stats.get('ftm_home', 0))
            d_home['fta'] += float(match.stats.get('fta_home', 0))

            # === STATS POUR L'ÉQUIPE À L'EXTÉRIEUR (Equipe 2) ===
            d_away = self.stats_nba[match.equipe2]
            d_away['matchs_joues'] += 1
            d_away['points_marques'] += match.score2
            d_away['points_encaisses'] += match.score1
            
            d_away['rebonds'] += float(match.stats.get('reb_away', 0))
            d_away['passes'] += float(match.stats.get('ast_away', 0))
            d_away['interceptions'] += float(match.stats.get('stl_away', 0))
            d_away['contres'] += float(match.stats.get('blk_away', 0))
            
            fgm_a = float(match.stats.get('fgm_away', 0))
            fga_a = float(match.stats.get('fga_away', 0))
            fg3m_a = float(match.stats.get('fg3m_away', 0))
            fg3a_a = float(match.stats.get('fg3a_away', 0))
            
            d_away['fg3m'] += fg3m_a
            d_away['fg3a'] += fg3a_a
            d_away['fg2m'] += (fgm_a - fg3m_a)
            d_away['fg2a'] += (fga_a - fg3a_a)
            d_away['ftm'] += float(match.stats.get('ftm_away', 0))
            d_away['fta'] += float(match.stats.get('fta_away', 0))

    def obtenir_moyennes(self, equipe_id):
        """Calcule et retourne les moyennes par match pour une équipe."""
        s = self.stats_nba.get(equipe_id)
        if not s or s['matchs_joues'] == 0:
            return None
            
        m = s['matchs_joues']
        
        # Fonction interne pour calculer les pourcentages proprement
        def pct(reussis, tentes):
            return round((reussis / tentes) * 100, 1) if tentes > 0 else 0.0

        return {
            'pts_pour': round(s['points_marques'] / m, 1),
            'pts_contre': round(s['points_encaisses'] / m, 1),
            'rebonds': round(s['rebonds'] / m, 1),
            'passes': round(s['passes'] / m, 1),
            'interceptions': round(s['interceptions'] / m, 1),
            'contres': round(s['contres'] / m, 1),
            'pct_2pts': pct(s['fg2m'], s['fg2a']),
            'pct_3pts': pct(s['fg3m'], s['fg3a']),
            'pct_lf': pct(s['ftm'], s['fta'])
        }