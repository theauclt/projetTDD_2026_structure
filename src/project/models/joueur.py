from personne import Personne

class Joueur(Personne):
    """Classe représentant un joueur sur le terrain."""
    
    def __init__(self, nom: str, prenom: str, dateNaissance: date, paysOrigine: str, 
                 taille: float, poids: float, position: str, main_dominante: str):
        
        super().__init__(nom, prenom, dateNaissance, paysOrigine)
        
        self.taille = taille
        self.poids = poids
        self.position = position
        self.main_dominante = main_dominante

    def calculer_statistiques(self):
        pass


