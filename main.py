from pkg.repository.data_repository import DataRepository
from pkg.config.dataset_configuration import basket_match_config, basket_equipe_config
from pkg.services.service_statistiques import ServiceStatistiques

def demo():
    print("=== DÉMONSTRATION : ANALYSE NBA AVEC JOINTS ===\n")
    
    # --- ÉTAPE 1 : Charger les noms des équipes ---
    repo_equipes = DataRepository(
        file=basket_equipe_config.dataset_path,
        adapter=basket_equipe_config.adapter,
        sep=basket_equipe_config.dataset_sep
    )
    # On charge les objets Equipe. 
    # Supposons que ton GenericEquipeAdapter stocke l'ID dans l'objet Equipe.
    equipes_list = repo_equipes.load()
    
    # On crée le dictionnaire de traduction { "ID": "Nom" }
    # Note : Adapte 'equipe.nom' selon les attributs de ton modèle Equipe
    equipe_map = {str(t.id): t.nom for t in equipes_list} 
    
    print(f"[Config] {len(equipe_map)} noms d'équipes chargés depuis equipe.csv.")

    # --- ÉTAPE 2 : Charger les matchs (comme avant) ---
    repo_matches = DataRepository(
        file=basket_match_config.dataset_path,
        adapter=basket_match_config.adapter,
        sep=basket_match_config.dataset_sep
    )
    matchs_basket = repo_matches.load()
    
    service = ServiceStatistiques()
    service.charger_matchs(matchs_basket)

    # --- ÉTAPE 3 : Affichage avec les vrais noms ---
    print("\n[Analyse] Classement Final :")
    leaderboard = service.obtenir_classement_global()
    
    for i, (equipe_id, stats) in enumerate(leaderboard[:10], start=1):
        # On cherche le nom dans notre map, sinon on garde l'ID
        nom = equipe_map.get(str(equipe_id), f"Inconnu ({equipe_id})")
        print(f"  {i:2}. {nom:<25} | Victoires: {stats['victoires']} | Points: {stats['points_marques']}")

    # --- ÉTAPE 4 : Détails du match ---
    premier_match = matchs_basket[0]
    home_nom = equipe_map.get(str(premier_match.equipe1), premier_match.equipe1)
    away_nom = equipe_map.get(str(premier_match.equipe2), premier_match.equipe2)
    
    print(f"\n[Détails] Match du {premier_match.date} :")
    print(f"  {home_nom} vs {away_nom}")
    print(f"  Paniers à 3 pts (Home) : {premier_match.stats.get('fg3m_home', 'N/A')}")


if __name__ == "__main__":
    demo()