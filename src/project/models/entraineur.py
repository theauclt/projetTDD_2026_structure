from personne import Personne

class Entraineur(Personne):
    """Classe représentant un entraineur."""
    
    def __init__(self, nom: str, prenom: str, dateNaissance: date, paysOrigine: str, 
                 role: str, anneesExperience: int) -> None:

        super().__init__(nom, prenom, dateNaissance, paysOrigine)

        self.role = role
        self.anneesExperience = anneesExperience