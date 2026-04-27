from pkg.repository.data_repository import DataRepository
from pkg.config.dataset_configuration import basket_match_config, basket_team_config
from pkg.services.stats_service import StatsService

def demo():
    print("=== DÉMONSTRATION : ANALYSE NBA AVEC JOINTS ===\n")
    
    # --- ÉTAPE 1 : Charger les noms des équipes ---
    repo_teams = DataRepository(
        file=basket_team_config.dataset_path,
        adapter=basket_team_config.adapter,
        sep=basket_team_config.dataset_sep
    )
    # On charge les objets Team. 
    # Supposons que ton GenericTeamAdapter stocke l'ID dans l'objet Team.
    teams_list = repo_teams.load()
    
    # On crée le dictionnaire de traduction { "ID": "Nom" }
    # Note : Adapte 'team.name' selon les attributs de ton modèle Team
    team_map = {str(t.id): t.name for t in teams_list} 
    
    print(f"[Config] {len(team_map)} noms d'équipes chargés depuis team.csv.")

    # --- ÉTAPE 2 : Charger les matchs (comme avant) ---
    repo_matches = DataRepository(
        file=basket_match_config.dataset_path,
        adapter=basket_match_config.adapter,
        sep=basket_match_config.dataset_sep
    )
    matchs_basket = repo_matches.load()
    
    service = StatsService()
    service.load_matches(matchs_basket)

    # --- ÉTAPE 3 : Affichage avec les vrais noms ---
    print("\n[Analyse] Classement Final :")
    leaderboard = service.get_leaderboard()
    
    for i, (team_id, stats) in enumerate(leaderboard[:10], start=1):
        # On cherche le nom dans notre map, sinon on garde l'ID
        name = team_map.get(str(team_id), f"Inconnu ({team_id})")
        print(f"  {i:2}. {name:<25} | Victoires: {stats['wins']} | Points: {stats['points_scored']}")

    # --- ÉTAPE 4 : Détails du match ---
    premier_match = matchs_basket[0]
    home_name = team_map.get(str(premier_match.team1), premier_match.team1)
    away_name = team_map.get(str(premier_match.team2), premier_match.team2)
    
    print(f"\n[Détails] Match du {premier_match.date} :")
    print(f"  {home_name} vs {away_name}")
    print(f"  Paniers à 3 pts (Home) : {premier_match.stats.get('fg3m_home', 'N/A')}")

if __name__ == "__main__":
    demo()