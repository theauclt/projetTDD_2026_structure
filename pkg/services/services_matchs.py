from pkg.models.match import Match


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
        nouveau_match = Match(
            id_match=id_match,
            date=date,
            equipe1=equipe1,
            equipe2=equipe2,
            score1=score1,
            score2=score2,
        )

        self.matchs.append(nouveau_match)
        return nouveau_match

    def afficher_matchs(self):
        """Affiche tous les matchs dans la console."""
        for match in self.matchs:
            print(match)
