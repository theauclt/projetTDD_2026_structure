from datetime import date

class Personne :

    def __init__(
        self,
        nom : str,
        prenom : str,
        dateNaissance : date,
        paysOrigine : str ) -> None:

        self.nom=nom
        self.prenom=prenom
        self.dateNaissance=dateNaissance
        self.paysOrigine=paysOrigine

    def calculer_age(self) -> int :
        date_aujourdhui=date.today()
        if (date_aujourdhui.month < self.dateNaissance.month) or (date_aujourdhui.month==self.dateNaissance.month and date_aujourdhui.day<self.dateNaissance.day) :
            age=date_aujourdhui.year - self.dateNaissance.year-1
        else :
            age=date_aujourdhui.year-self.dateNaissance.year

        return age

    def __eq__(self, autre_personne)->bool :
        if isinstance(autre_personne, Personne):
            return (self.nom.lower()==autre_personne.nom.lower() and
                    self.prenom.lower()==autre_personne.prenom.lower() and
                    self.dateNaissance==autre_personne.dateNaissance)

            return False

    def __hash__(self)->int:
        return hash((self.nom.lower(),self.prenom.lower(),self.dateNaissance))
        