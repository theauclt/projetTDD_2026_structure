from src.repository.data_repository import DataRepository
from src.dataset_configuration import volleyball_player_men_configuration

def test_load_players():
    print("--- Test du chargement des joueurs ---")
    
    # 1. On initialise le Repository avec la config des joueurs
    repo = DataRepository(
        file=volleyball_player_men_configuration.dataset_path,
        adapter=volleyball_player_men_configuration.adapter,
        sep=volleyball_player_men_configuration.dataset_sep
    )

    # 2. On charge les données
    players = repo.load()

    # 3. On affiche le résultat
    print(f"Nombre de joueurs chargés : {len(players)}")
    
    if players:
        print("Aperçu des 3 premiers joueurs :")
        for player in players[:3]:
            print(f" - {player}")
            print(f"   Détails : Lieu de naissance: {player.birth_place}, Taille: {player.height}cm")

if __name__ == "__main__":
    test_load_players()