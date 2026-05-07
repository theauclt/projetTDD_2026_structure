class Joueur:
    """Classe de base pour tous les athlètes."""

    def __init__(self, id, prenom, nom, taille, date_naissance):
        self.id = id
        self.prenom = prenom
        self.nom = nom
        self.nom_complet = f"{prenom} {nom}".strip()
        self.taille = taille
        self.date_naissance = date_naissance


class JoueurBasket(Joueur):
    """Spécialisation pour le Basket."""

    def __init__(
        self,
        id,
        prenom,
        nom,
        taille,
        date_naissance,
        equipe_id,
        numero,
        position,
        poids,
    ):
        # On appelle le constructeur de la classe mère pour remplir les bases
        super().__init__(id, prenom, nom, taille, date_naissance)
        # On ajoute les spécificités du basket
        self.equipe_id = equipe_id
        self.numero = numero
        self.position = position
        self.poids = poids


class JoueurTennis(Joueur):
    """Spécialisation pour le Tennis."""

    def __init__(self, id, prenom, nom, taille, date_naissance, pays_ioc, main_forte):
        super().__init__(id, prenom, nom, taille, date_naissance)
        self.pays_ioc = pays_ioc
        self.main_forte = main_forte
