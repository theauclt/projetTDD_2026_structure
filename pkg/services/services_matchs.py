from pkg.adapter.base_adapter import BaseAdapter
from pkg.models.match import Match
from pkg.repository.data_repository import DataRepository


class ServiceMatchs:
    """
    Service responsable de la gestion basique de la liste des matchs.
    
    Parameters
    ----------
    liste_matchs_initiale : list, optional
        Une liste d'objets Match pour initialiser le service. Par défaut vide.
    """

    def __init__(self, liste_matchs_initiale=None):
        self.matchs = liste_matchs_initiale if liste_matchs_initiale else []

    def creer_match(self, id_match, date, equipe1, equipe2, score1, score2):
        """Crée un nouveau match et l'ajoute à la base de données en mémoire."""
        from modeles import Match # Assure-toi que l'import correspond à ton fichier
        
        nouveau_match = Match(
            id_match=id_match,
            date=date,
            equipe1=equipe1,
            equipe2=equipe2,
            score1=score1,
            score2=score2
        )

        self.matchs.append(nouveau_match)
        return nouveau_match

    def afficher_matchs(self):
        """Affiche tous les matchs dans la console."""
        for match in self.matchs:
            print(match)
