class Entraineur:
    """
    Modèle représentant un entraîneur.

    Parameters
    ----------
    nom : str
        Nom de l'entraîneur.
    prenom : str, optional
        Prénom ou pseudonyme de l'entraîneur. Par défaut None.
    pays : str, optional
        Pays d'origine ou nationalité de l'entraîneur. Par défaut None.
    date_naissance : str, optional
        Date de naissance de l'entraîneur. Par défaut None.
    role : str, optional
        Rôle précis dans le staff (ex: 'Head Entraineur', 'Assistant Entraineur'). Par défaut None.
    nom_equipe : str, optional
        Nom de l'équipe qu'il entraîne actuellement (pour faire le lien avec l'objet Equipe). Par défaut None.
    """
  
    def __init__(self, nom, prenom=None, pays=None, date_naissance=None, role=None, nom_equipe=None):
        self.nom = nom
        self.prenom = prenom
        self.pays = pays
        self.date_naissance = date_naissance
        self.role = role
        self.nom_equipe = nom_equipe # Pour faire le lien avec l'objet Equipe plus tard

    def __str__(self):
        return f"Entraîneur: {self.nom} [{self.role}]"