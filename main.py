from pkg.repository.data_repository import DataRepository
from pkg.config.dataset_configuration import basket_match_config, basket_equipe_config, basket_joueur_config
from pkg.services.service_statistiques import ServiceStatistiques
from pkg.services.service_statistiques import ServiceStatistiquesBasket
from pkg.services.service_annuaire_joueur import ServiceAnnuaireJoueurs

def charger_dictionnaire_noms(config_donnees):
    repo = DataRepository(
        file=config_donnees.dataset_path,
        adapter=config_donnees.adapter,
        sep=config_donnees.dataset_sep
    )
    elements = repo.load()
    return {str(e.id): e.nom for e in elements}

# ==========================================
# 2. SCÉNARIOS D'ANALYSE
# ==========================================
def afficher_statistiques_basket():
    print("\n" + "="*90)
    print("🏀 CLASSEMENT ET STATISTIQUES AVANCÉES NBA 2022/2023")
    print("="*90)
    
    noms_equipes = charger_dictionnaire_noms(basket_equipe_config)
    
    repo_matchs = DataRepository(
        file=basket_match_config.dataset_path,
        adapter=basket_match_config.adapter,
        sep=basket_match_config.dataset_sep
    )
    
    # Utilisation du service spécialisé
    service = ServiceStatistiquesBasket()
    service.charger_matchs(repo_matchs.load())
    classement = service.obtenir_classement_global()
    
    # Entête du tableau
    print(f"{'#':<3} | {'Équipe':<22} | {'Vic':<4} | {'Pts':<5} | {'Enc':<5} | {'Reb':<4} | {'Ast':<4} | {'Stl':<4} | {'Blk':<4} | {'2P%':<5} | {'3P%':<5} | {'LF%':<5}")
    print("-" * 90)
    
    for i, (equipe_id, stats_base) in enumerate(classement[:15], start=1): # Top 15 (Une conférence)
        nom = noms_equipes.get(str(equipe_id), f"ID:{equipe_id}")
        victoires = stats_base['victoires']
        moy = service.obtenir_moyennes(equipe_id)
        
        if moy:
            print(f"{i:<3} | {nom:<22} | {victoires:<4} | {moy['pts_pour']:<5} | {moy['pts_contre']:<5} | {moy['rebonds']:<4} | {moy['passes']:<4} | {moy['interceptions']:<4} | {moy['contres']:<4} | {moy['pct_2pts']:<5} | {moy['pct_3pts']:<5} | {moy['pct_lf']:<5}")


def explorer_annuaire_basket():
    """Menu interactif pour naviguer des équipes vers les joueurs spécifiques."""
    
    print("\n⏳ Chargement de la base de données des joueurs...")
    
    # 1. On charge le dictionnaire des équipes {id: nom}
    noms_equipes = charger_dictionnaire_noms(basket_equipe_config)
    
    # 2. On charge l'annuaire des joueurs avec notre super adaptateur
    repo_joueurs = DataRepository(
        file=basket_joueur_config.dataset_path,
        adapter=basket_joueur_config.adapter,
        sep=basket_joueur_config.dataset_sep
    )
    annuaire = ServiceAnnuaireJoueurs()
    annuaire.charger_joueurs(repo_joueurs.load())

    # --- NIVEAU 1 : CHOIX DE L'ÉQUIPE ---
    while True:
        print("\n" + "="*40)
        print("🏢 ANNUAIRE DES ÉQUIPES NBA")
        print("="*40)
        
        # On transforme le dictionnaire en liste pour pouvoir utiliser des numéros
        liste_ids_equipes = list(noms_equipes.keys())
        
        for idx, equipe_id in enumerate(liste_ids_equipes, start=1):
            print(f"{idx:2}. {noms_equipes[equipe_id]}")
        
        print("-" * 40)
        print(f"{len(liste_ids_equipes) + 1}. 🔙 Retour au menu principal")
        
        choix_eq = input("\n👉 Choisissez une équipe (numéro) : ")
        
        # Si l'utilisateur choisit le dernier numéro (Retour)
        if choix_eq == str(len(liste_ids_equipes) + 1):
            break
            
        try:
            # On récupère l'ID de l'équipe choisie
            idx_choisi = int(choix_eq) - 1
            equipe_id = liste_ids_equipes[idx_choisi]
            nom_equipe = noms_equipes[equipe_id]
            
            # --- NIVEAU 2 : CHOIX DU JOUEUR ---
            while True:
                effectif = annuaire.obtenir_joueurs_par_affiliation(equipe_id)
                
                # Tri de l'effectif par numéro de maillot pour faire propre
                def tri_numero(j):
                    try: return int(j.numero)
                    except: return 999
                effectif_trie = sorted(effectif, key=tri_numero)
                
                print("\n" + "="*45)
                print(f"📋 EFFECTIF : {nom_equipe.upper()}")
                print("="*45)
                
                if not effectif_trie:
                    print("⚠️ Aucun joueur trouvé pour cette équipe.")
                    break
                    
                for idx, joueur in enumerate(effectif_trie, start=1):
                    print(f"{idx:2}. #{joueur.numero:<2} - {joueur.nom_complet} ({joueur.position})")
                    
                print("-" * 45)
                print(f"{len(effectif_trie) + 1}. 🔙 Choisir une autre équipe")
                
                choix_joueur = input("\n👉 Choisissez un joueur pour voir son profil : ")
                
                if choix_joueur == str(len(effectif_trie) + 1):
                    break # Remonte au menu des équipes
                    
                try:
                    idx_j = int(choix_joueur) - 1
                    joueur_choisi = effectif_trie[idx_j]
                    
                    # --- NIVEAU 3 : PROFIL DU JOUEUR ---
                    print("\n" + "★"*40)
                    print(f" 👤 CARTE JOUEUR : {joueur_choisi.nom_complet.upper()}")
                    print("★"*40)
                    print(f"  Équipe    : {nom_equipe}")
                    print(f"  Maillot   : #{joueur_choisi.numero}")
                    print(f"  Position  : {joueur_choisi.position}")
                    print(f"  Taille    : {joueur_choisi.taille}")
                    print(f"  Poids     : {joueur_choisi.poids}")
                    print(f"  Naissance : {joueur_choisi.date_naissance}")
                    print("★"*40)
                    
                    input("\nAppuyez sur Entrée pour revenir à l'effectif...")
                    
                except (ValueError, IndexError):
                    print("⚠️ Numéro de joueur invalide. Veuillez réessayer.")
                    
        except (ValueError, IndexError):
            print("⚠️ Numéro d'équipe invalide. Veuillez réessayer.")

def lancer_application():
    while True:
        print("\n" + "*"*50)
        print(" 🏆 TABLEAU DE BORD MULTISPORTS 2026")
        print("*"*50)
        print("1. 🏀 NBA : Classement et Statistiques")
        print("2. 🏀 NBA : Explorer les Effectifs (Joueurs)") # <-- La nouvelle option !
        print("3. 🎾 TENNIS ATP (Classement Hommes)")
        print("4. 🎾 TENNIS WTA (Classement Femmes)")
        print("5. ❌ Quitter")
        
        choix = input("\n👉 Entrez votre choix (1-5) : ")
        
        if choix == '1':
            afficher_statistiques_basket()
        elif choix == '2':
            explorer_annuaire_basket() # <-- Appel de notre nouvelle fonction
        elif choix == '3':
            afficher_statistiques_tennis(tennis_atp_match_config, tennis_atp_joueur_config, "ATP")
        elif choix == '4':
            afficher_statistiques_tennis(tennis_wta_match_config, tennis_wta_joueur_config, "WTA")
        elif choix == '5':
            print("\nFermeture du logiciel. À bientôt ! 👋\n")
            break
        else:
            print("\n⚠️ Choix invalide, veuillez réessayer.")


if __name__ == "__main__":
    lancer_application()
