from src.repository.data_repository import DataRepository
from src.dataset_configuration import volleyball_joueur_men_configuration

def test_load_joueurs():
    print("--- Test du chargement des joueurs ---")
    
    # 1. On initialise le Repository avec la config des joueurs
    repo = DataRepository(
        file=volleyball_joueur_men_configuration.dataset_path,
        adapter=volleyball_joueur_men_configuration.adapter,
        sep=volleyball_joueur_men_configuration.dataset_sep
    )

    # 2. On charge les données
    joueurs = repo.load()

    # 3. On affiche le résultat
    print(f"Nombre de joueurs chargés : {len(joueurs)}")
    
    if joueurs:
        print("Aperçu des 3 premiers joueurs :")
        for joueur in joueurs[:3]:
            print(f" - {joueur}")
            print(f"   Détails : Lieu de naissance: {joueur.birth_place}, Taille: {joueur.height}cm")

if __name__ == "__main__":
    test_load_joueurs()