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
        en temps réel. C'est l'exigence principale du cahier des charges !
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