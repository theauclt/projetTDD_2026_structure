class StatistiqueJoueur:
    """Représente la performance d'un joueur lors d'un match spécifique.
    Inutile dans notre cas car la base de données ne contient pas de stats individuelles,
    mais conceptuellement c'est une bonne idée de les modéliser pour une future extension."""
    
    def __init__(self, match_id, joueur_id, nom_joueur, equipe_id, pts, reb, ast, blk, stl):
        self.match_id = match_id
        self.joueur_id = joueur_id
        self.nom_joueur = nom_joueur
        self.equipe_id = equipe_id
        
        # On convertit en float pour éviter les bugs si le CSV a des cases vides
        self.pts = float(pts) if pts else 0.0
        self.reb = float(reb) if reb else 0.0
        self.ast = float(ast) if ast else 0.0
        self.blk = float(blk) if blk else 0.0
        self.stl = float(stl) if stl else 0.0
        # Tu pourras ajouter les interceptions (stl), contres (blk), etc.