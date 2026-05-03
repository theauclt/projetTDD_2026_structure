from pkg.repository.data_repository import DataRepository
from pkg.config.dataset_configuration import basket_match_config, basket_equipe_config
from pkg.services.service_statistiques import ServiceStatistiques

# --- NIVEAU 2 : CHOIX DE L'ENTITÉ ---
def menu_basket():
    print("\n[BASKET] Que voulez-vous analyser ?")
    print("1. Statistiques des Équipes")
    print("2. Statistiques des Joueurs")
    choix = input("Votre choix (1 ou 2) : ")
    
    if choix == '1':
        afficher_stats_equipes_basket()
    elif choix == '2':
        afficher_stats_joueurs_basket()
    else:
        print("Retour au menu principal.")

def menu_tennis():
    print("\n[TENNIS] Que voulez-vous analyser ?")
    print("1. Statistiques des Équipes (Nations)")
    print("2. Statistiques des Joueurs (Classement ATP)")
    choix = input("Votre choix (1 ou 2) : ")
    
    if choix == '2':
        # Exemple rapide pour le tennis
        print("\nChargement du classement ATP 2026...")
        # ... logique similaire au basket ...
    else:
        print("Option non disponible ou retour.")

# --- NIVEAU 1 : CHOIX DU SPORT ---
if __name__ == "__main__":
    while True: # Boucle pour revenir au menu après une analyse
        print("\n========================================")
        print("   LOGICIEL D'ANALYSE MULTISPORTS 2026  ")
        print("========================================")
        print("1. Basket-ball")
        print("2. Tennis")
        print("q. Quitter")
        
        choix_sport = input("\nChoisissez un sport : ").lower()

        if choix_sport == '1':
            menu_basket()
        elif choix_sport == '2':
            menu_tennis()
        elif choix_sport == 'q':
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")