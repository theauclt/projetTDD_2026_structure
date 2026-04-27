from collections import defaultdict
from pkg.models.match import Match


class StatsService:
    """
    Service responsable de l'analyse et de la manipulation des données.
    Fonctionne indépendamment du sport grâce aux modèles génériques.
    """

    def __init__(self):
        self.matches = []
        # defaultdict permet d'initialiser automatiquement les stats à 0 
        # pour une équipe ou un joueur dès qu'on le rencontre pour la première fois.
        self.stats = defaultdict(lambda: {
            'played': 0, 
            'wins': 0, 
            'losses': 0, 
            'draws': 0, 
            'points_scored': 0
        })

    def load_matches(self, matches: list[Match]):
        """Charge un historique complet de matchs et met à jour les statistiques."""
        for match in matches:
            self.add_match(match)

    def add_match(self, match: Match):
        """
        Ajoute un nouveau match et met à jour les caractéristiques des équipes/joueurs
        en temps réel.
        """
        self.matches.append(match)

        # 1. Mise à jour des matchs joués
        self.stats[match.team1]['played'] += 1
        self.stats[match.team2]['played'] += 1

        # 2. Mise à jour des points marqués (ou buts, ou kills)
        self.stats[match.team1]['points_scored'] += match.score1
        self.stats[match.team2]['points_scored'] += match.score2

        # 3. Détermination du gagnant et mise à jour du palmarès
        if match.score1 > match.score2:
            self.stats[match.team1]['wins'] += 1
            self.stats[match.team2]['losses'] += 1
        elif match.score2 > match.score1:
            self.stats[match.team2]['wins'] += 1
            self.stats[match.team1]['losses'] += 1
        else:
            self.stats[match.team1]['draws'] += 1
            self.stats[match.team2]['draws'] += 1

    def get_leaderboard(self):
        """
        Génère un classement global trié.
        Critère 1 : Nombre de victoires
        Critère 2 : Nombre de points marqués
        """
        # On trie le dictionnaire de stats. item[1] correspond au sous-dictionnaire de stats.
        leaderboard = sorted(
            self.stats.items(),
            key=lambda item: (item[1]['wins'], item[1]['points_scored']),
            reverse=True # Ordre décroissant (du meilleur au pire)
        )
        return leaderboard
    
    def get_entity_stats(self, entity_name: str):
        """Récupère les statistiques détaillées d'une équipe ou d'un joueur spécifique."""
        if entity_name in self.stats:
            return self.stats[entity_name]
        return None
    
    # --- MÉTHODES DE MANIPULATION COMPLEXES ---

    def get_team_history(self, team_name):
        """
        Filtre la base de données de matchs pour ne ressortir que l'historique d'une équipe.
        Utilise la nouvelle méthode `involves_team` du modèle Match.
        """
        return [match for match in self.matches if match.involves_team(team_name)]

    def calculate_standings(self, points_for_win=3, points_for_draw=1, points_for_loss=0):
        """
        Calcule le classement générique d'un tournoi (type championnat).
        Retourne un dictionnaire complexe avec toutes les stats agrégées.
        """
        standings = defaultdict(lambda: {'played': 0, 'points': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'pf': 0, 'pa': 0, 'diff': 0})

        for match in self.matches:
            t1, t2 = match.team1, match.team2
            
            standings[t1]['played'] += 1
            standings[t2]['played'] += 1
            
            # Utilisation des méthodes intelligentes du modèle Match
            standings[t1]['pf'] += match.get_points_for(t1)
            standings[t1]['pa'] += match.get_points_against(t1)
            standings[t2]['pf'] += match.get_points_for(t2)
            standings[t2]['pa'] += match.get_points_against(t2)

            winner = match.get_winner()
            if winner == t1:
                standings[t1]['wins'] += 1
                standings[t1]['points'] += points_for_win
                standings[t2]['losses'] += 1
                standings[t2]['points'] += points_for_loss
            elif winner == t2:
                standings[t2]['wins'] += 1
                standings[t2]['points'] += points_for_win
                standings[t1]['losses'] += 1
                standings[t1]['points'] += points_for_loss
            else:
                standings[t1]['draws'] += 1
                standings[t2]['draws'] += 1
                standings[t1]['points'] += points_for_draw
                standings[t2]['points'] += points_for_draw

        # Calcul de la différence de points finale
        for team, stats in standings.items():
            stats['diff'] = stats['pf'] - stats['pa']

        # Tri : Points > Différence de points > Points marqués
        return sorted(standings.items(), key=lambda x: (x[1]['points'], x[1]['diff'], x[1]['pf']), reverse=True)