from pkg.repository.data_repository import DataRepository
from pkg.config.dataset_configuration import (
    basket_match_config, 
    basket_equipe_config, 
    basket_joueur_config,
    tennis_atp_match_config,
    tennis_atp_joueur_config,
    tennis_wta_match_config,  
    tennis_wta_joueur_config
)
from pkg.services.service_statistiques import ServiceStatistiquesTennis
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
def determiner_conference_nba(nom_equipe):
    """Détermine si une équipe est à l'Est ou à l'Ouest en fonction de son nom."""
    mots_cles_est = [
        "Boston", "Celtics", "Brooklyn", "Nets", "New York", "Knicks", 
        "Philadelphia", "76ers", "Toronto", "Raptors", "Chicago", "Bulls", 
        "Cleveland", "Cavaliers", "Detroit", "Pistons", "Indiana", "Pacers", 
        "Milwaukee", "Bucks", "Atlanta", "Hawks", "Charlotte", "Hornets", 
        "Miami", "Heat", "Orlando", "Magic", "Washington", "Wizards"
    ]
    
    # Si on trouve un de ces mots dans le nom de l'équipe, c'est l'Est
    for mot in mots_cles_est:
        if mot.lower() in nom_equipe.lower():
            return "Est"
            
    # Sinon, c'est forcément l'Ouest
    return "Ouest"

def afficher_statistiques_basket():
    print("\n" + "="*90)
    print("🏀 CLASSEMENT ET STATISTIQUES AVANCÉES NBA 2022/2023")
    print("="*90)
    
    # --- CHOIX DE LA PHASE ---
    print("Quelle phase souhaitez-vous analyser ?")
    print("1. Saison Régulière")
    print("2. Playoffs")
    choix_phase = input("\n👉 Votre choix (1-2) : ")
    
    nom_phase = "Playoffs" if choix_phase == '2' else "Regular Season"
    
    # --- NOUVEAU : CHOIX DE LA CONFÉRENCE ---
    print("\nQuelle conférence souhaitez-vous afficher ?")
    print("1. 🔵 Conférence Est")
    print("2. 🔴 Conférence Ouest")
    print("3. 🌍 Les deux (Classement Global)")
    choix_conf = input("\n👉 Votre choix (1-3) : ")
    
    noms_equipes = charger_dictionnaire_noms(basket_equipe_config)
    
    repo_matchs = DataRepository(
        file=basket_match_config.dataset_path,
        adapter=basket_match_config.adapter,
        sep=basket_match_config.dataset_sep
    )
    
    service = ServiceStatistiquesBasket()
    service.charger_matchs(repo_matchs.load())
    
    # On récupère le classement de TOUTES les équipes pour la phase choisie
    classement_complet = service.obtenir_classement_global(phase=nom_phase)
    
    # --- FILTRAGE PAR CONFÉRENCE ---
    classement_filtre = []
    nom_affichage_conf = "GLOBALE"
    
    for equipe_id, stats_base in classement_complet:
        nom_eq = noms_equipes.get(str(equipe_id), f"ID:{equipe_id}")
        conference_eq = determiner_conference_nba(nom_eq) # On utilise notre détecteur
        
        # On range l'équipe dans la liste finale seulement si elle correspond au choix
        if choix_conf == '1' and conference_eq == "Est":
            classement_filtre.append((equipe_id, stats_base, nom_eq))
            nom_affichage_conf = "CONFÉRENCE EST"
        elif choix_conf == '2' and conference_eq == "Ouest":
            classement_filtre.append((equipe_id, stats_base, nom_eq))
            nom_affichage_conf = "CONFÉRENCE OUEST"
        elif choix_conf == '3' or choix_conf not in ['1', '2']: # Par défaut : on garde tout
            classement_filtre.append((equipe_id, stats_base, nom_eq))
            nom_affichage_conf = "GLOBALE"

    # --- AFFICHAGE DU TABLEAU ---
    print(f"\n--- RÉSULTATS POUR : {nom_phase.upper()} | {nom_affichage_conf} ---")
    print(f"{'#':<3} | {'Équipe':<22} | {'Vic':<4} | {'Pts':<5} | {'Enc':<5} | {'Reb':<4} | {'Ast':<4} | {'Stl':<4} | {'Blk':<4} | {'2P%':<5} | {'3P%':<5} | {'LF%':<5}")
    print("-" * 105)
    
    if not classement_filtre:
        print(f"⚠️ Aucune donnée trouvée pour cette sélection.")
    
    # On affiche notre liste filtrée, l'énumération refera un beau top 1 à 15 (ou 30) !
    for i, (equipe_id, stats_base, nom) in enumerate(classement_filtre, start=1):
        victoires = stats_base['victoires']
        moy = service.obtenir_moyennes(equipe_id, phase=nom_phase)
        
        if moy:
            print(f"{i:<3} | {nom:<22} | {victoires:<4} | {moy.get('pts_pour','N/A'):<5} | {moy.get('pts_contre','N/A'):<5} | {moy.get('rebonds','N/A'):<4} | {moy.get('passes','N/A'):<4} | {moy.get('interceptions','N/A'):<4} | {moy.get('contres','N/A'):<4} | {moy.get('pct_2pts','N/A'):<5} | {moy.get('pct_3pts','N/A'):<5} | {moy.get('pct_lf','N/A'):<5}")

    input("\nAppuyez sur Entrée pour revenir au menu...")

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
    while True:
        print("\n" + "="*40)
        print("🏢 ANNUAIRE DES ÉQUIPES NBA")
        print("="*40)
        
        # 1. On sépare les IDs en deux groupes
        equipes_est = []
        equipes_ouest = []
        
        for eq_id, nom in noms_equipes.items():
            if determiner_conference_nba(nom) == "Est":
                equipes_est.append(eq_id)
            else:
                equipes_ouest.append(eq_id)
                
        # 2. On rassemble la liste dans un ordre précis (Est d'abord, puis Ouest)
        liste_ids_equipes = equipes_est + equipes_ouest
        
        # 3. Affichage personnalisé
        for idx, equipe_id in enumerate(liste_ids_equipes, start=1):
            # On ajoute des titres de section dynamiques
            if idx == 1:
                print("\n🔵 --- CONFÉRENCE EST ---")
            elif idx == len(equipes_est) + 1:
                print("\n🔴 --- CONFÉRENCE OUEST ---")
                
            print(f"{idx:2}. {noms_equipes[equipe_id]}")
        
        print("\n" + "-" * 40)
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

def explorer_annuaire_tennis(config_joueurs, config_matchs, nom_circuit):
    """Menu interactif pour explorer les statistiques des joueurs de Tennis par pays."""
    
    print(f"\n⏳ Chargement de la base de données {nom_circuit}...")
    
    # 1. Chargement de l'annuaire (les joueurs)
    repo_joueurs = DataRepository(
        file=config_joueurs.dataset_path, adapter=config_joueurs.adapter, sep=config_joueurs.dataset_sep)
    annuaire = ServiceAnnuaireJoueurs()
    annuaire.charger_joueurs(repo_joueurs.load())
    
    # 2. Chargement des matchs (pour les stats)
    repo_matchs = DataRepository(
        file=config_matchs.dataset_path, adapter=config_matchs.adapter, sep=config_matchs.dataset_sep)
    service_stats = ServiceStatistiquesTennis()
    service_stats.charger_matchs(repo_matchs.load())

    # --- ÉTAPE 3 : RECHERCHE PAR PAYS ---
    while True:
        print("\n" + "="*60)
        print(f"🌍 EXPLORATEUR INTERNATIONAL - CIRCUIT {nom_circuit}")
        print("="*60)
        
        liste_pays = annuaire.obtenir_pays_disponibles()
        
        print("📍 Codes pays disponibles :")
        # --- NOUVEAU SYSTÈME D'AFFICHAGE DE LA LISTE ---
        # On parcourt la liste de 0 jusqu'à la fin, en faisant des sauts de 5
        for i in range(0, len(liste_pays), 7):
            # On prend une tranche de 5 pays (ex: de l'index 0 à 5, puis 5 à 10, etc.)
            tranche = liste_pays[i:i+7]
            # On affiche cette tranche séparée par des virgules
            print(", ".join(tranche))
        # -----------------------------------------------
        print("-" * 60)
        
        choix_pays = input("\n👉 Tapez le code à 3 lettres d'un pays (ou 'Q' pour quitter) : ").upper().strip()
        
        if choix_pays == 'Q':
            break # Retourne au menu précédent (Choix ATP/WTA)
            
        if choix_pays not in liste_pays:
            print(f"⚠️ Aucun joueur trouvé pour le code '{choix_pays}'. Vérifiez l'orthographe.")
            continue
            
        # --- ÉTAPE 4 : SÉLECTION DU JOUEUR ---
        while True:
            joueurs_du_pays = annuaire.obtenir_joueurs_par_pays(choix_pays)
            
            print("\n" + "="*50)
            print(f"🎾 JOUEURS REPRÉSENTANT : {choix_pays} ({len(joueurs_du_pays)} trouvés)")
            print("="*50)
            
            for idx, joueur in enumerate(joueurs_du_pays, start=1):
                print(f"{idx:2}. {joueur.nom_complet}")
                
            print("-" * 50)
            print(f"{len(joueurs_du_pays) + 1}. 🔙 Chercher un autre pays")
            
            choix_j = input("\n👉 Choisissez un joueur (numéro) pour voir ses stats : ")
            
            if choix_j == str(len(joueurs_du_pays) + 1):
                break # Remonte au choix du pays
                
            try:
                idx_choisi = int(choix_j) - 1
                joueur = joueurs_du_pays[idx_choisi]
                
                # --- ÉTAPE 5 : AFFICHAGE DES STATISTIQUES ---
                stats = service_stats.obtenir_moyennes_joueur(joueur.id)
                
                print("\n" + "★"*45)
                print(f" 👤 PROFIL ET STATS : {joueur.nom_complet.upper()}")
                print("★"*45)
                print(f"  Taille       : {joueur.taille} cm")
                print(f"  Main forte   : {getattr(joueur, 'main_forte', 'N/A')}")
                print(f"  Pays         : {getattr(joueur, 'pays_ioc', getattr(joueur, 'ioc', 'N/A'))}")
                print("-" * 45)
                
                if stats:
                    print(f"  Victoires    : {stats['victoires']}")
                    print(f"  Défaites     : {stats['defaites']}")
                    print(f"  Aces / match : {stats['aces_par_match']}")
                    print(f"  DF / match   : {stats['df_par_match']}")
                    print(f"  Temps moyen  : {stats['minutes_moyennes']} minutes")
                    print("-" * 45)
                    print("  🔥 STATISTIQUES DE BREAK :")
                    print(f"  Défense (Sauvées)    : {stats['bp_sauvees']} / {stats['bp_concedees']}")
                    print(f"  Attaque (Converties) : {stats['bp_converties']} / {stats['bp_obtenues']}")
                    print("-" * 45)
                    
                    # On affiche le palmarès s'il y a des titres, sinon on met "Aucun"
                    titres = stats['palmares']
                    print(f"  🏆 PALMARÈS ({len(titres)} titres) :")
                    if titres:
                        # On parcourt la liste de 0 à la fin, en faisant des sauts de 3
                        for i in range(0, len(titres), 3):
                            # On découpe une tranche de 3 titres maximum
                            tranche_titres = titres[i:i+3]
                            # On les affiche séparés par une virgule, avec un petit espace au début pour l'alignement
                            print("    " + ", ".join(tranche_titres))
                    else:
                        print("  Aucun titre répertorié dans la base.")
                else:
                    print("  ⚠️ Aucune donnée de match trouvée pour ce joueur.")
                print("★"*45)
                
                input("\nAppuyez sur Entrée pour revenir à la liste des joueurs...")
                
            except (ValueError, IndexError):
                print("⚠️ Choix invalide. Veuillez entrer un numéro valide.")


def menu_tennis():
    """Le premier menu du Tennis qui gère l'étape 2 (Choix du circuit)"""
    while True:
        print("\n" + "*"*50)
        print(" 🏆 TABLEAU DE BORD TENNIS 🏆")
        print("*"*50)
        print("1. 🎾 ATP : Circuit Masculin")
        print("2. 🎾 WTA : Circuit Féminin")
        print("3. 🔙 Retour au menu principal")
        
        choix = input("\n👉 Entrez votre choix (1-3) : ")
        
        if choix == '1':
            # On envoie l'utilisateur vers la recherche avec les données ATP
            explorer_annuaire_tennis(tennis_atp_joueur_config, tennis_atp_match_config, "ATP")
        elif choix == '2':
            # On envoie l'utilisateur vers la recherche avec les données WTA
            explorer_annuaire_tennis(tennis_wta_joueur_config, tennis_wta_match_config, "WTA")
        elif choix == '3':
            break
        else:
            print("\n⚠️ Choix invalide, veuillez réessayer.")


def menu_basket():
    while True:
        print("\n" + "*"*50)
        print(" 🏆 TABLEAU DE BORD NBA 🏆")
        print("*"*50)
        print("1. 🏀 NBA : Classement et Statistiques par équipes")
        print("2. 🏀 NBA : Explorer les Effectifs")
        print("3. 🔙 Retour au menu principal")
        
        choix = input("\n👉 Entrez votre choix (1-3) : ")
        
        if choix == '1':
            afficher_statistiques_basket()
        elif choix == '2':
            explorer_annuaire_basket()
        elif choix == '3':
            break
        else:
            print("\n⚠️ Choix invalide, veuillez réessayer.")


def lancer_application():

    while True:
        print("\n" + "*"*50)
        print(" 🏆 TABLEAU DE BORD MULTISPORTS 2026")
        print("*"*50)
        print("CHOIX DU SPORT :")
        print("1. 🏀 NBA 🏀")
        print("2. 🎾 TENNIS 🎾")
        print("3. ❌ Quitter")
        
        choix = input("\n👉 Entrez votre choix (1-3) : ")
        
        if choix == '1':
            menu_basket()
        elif choix == '2':
            menu_tennis()
        elif choix == '3':
            print("\nFermeture du logiciel. À bientôt ! 👋\n")
            break
        else:
            print("\n⚠️ Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    lancer_application()
