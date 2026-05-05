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
from pkg.services.service_statistiques import ServiceStatistiquesTennis, ServiceStatistiquesBasket
from pkg.services.service_annuaire_joueur import ServiceAnnuaireJoueurs

class ServiceApplication:
    """Service principal qui gère l'interface utilisateur, la navigation et l'affichage."""

    def __init__(self):
        # On pourrait initialiser ici des paramètres globaux de l'application si besoin
        pass

    # ==========================================
    # OUTILS GÉNERAUX
    # ==========================================

    def charger_dictionnaire_noms(self, config_donnees):
        """Outil interne pour charger rapidement un dictionnaire d'IDs et de noms."""
        repo = DataRepository(
            file=config_donnees.dataset_path,
            adapter=config_donnees.adapter,
            sep=config_donnees.dataset_sep
        )
        elements = repo.load()
        return {str(e.id): e.nom for e in elements}

    # ==========================================
    # MODULE BASKET (NBA)
    # ==========================================

    def determiner_conference_nba(self, nom_equipe):
        """Détermine si une équipe est à l'Est ou à l'Ouest en fonction de son nom."""
        mots_cles_est = [
            "Boston", "Celtics", "Brooklyn", "Nets", "New York", "Knicks", 
            "Philadelphia", "76ers", "Toronto", "Raptors", "Chicago", "Bulls", 
            "Cleveland", "Cavaliers", "Detroit", "Pistons", "Indiana", "Pacers", 
            "Milwaukee", "Bucks", "Atlanta", "Hawks", "Charlotte", "Hornets", 
            "Miami", "Heat", "Orlando", "Magic", "Washington", "Wizards"
        ]
        
        for mot in mots_cles_est:
            if mot.lower() in nom_equipe.lower():
                return "Est"
        return "Ouest"

    def afficher_statistiques_basket(self):
        """Affiche le classement et les statistiques des équipes NBA."""
        print("\n" + "="*90)
        print("🏀 CLASSEMENT ET STATISTIQUES AVANCÉES NBA 2022/2023")
        print("="*90)
        
        print("Quelle phase souhaitez-vous analyser ?")
        print("1. Saison Régulière")
        print("2. Playoffs")
        choix_phase = input("\n👉 Votre choix (1-2) : ")
        nom_phase = "Playoffs" if choix_phase == '2' else "Regular Season"
        
        print("\nQuelle conférence souhaitez-vous afficher ?")
        print("1. 🔵 Conférence Est")
        print("2. 🔴 Conférence Ouest")
        print("3. 🌍 Les deux (Classement Global)")
        choix_conf = input("\n👉 Votre choix (1-3) : ")
        
        noms_equipes = self.charger_dictionnaire_noms(basket_equipe_config)
        
        repo_matchs = DataRepository(
            file=basket_match_config.dataset_path,
            adapter=basket_match_config.adapter,
            sep=basket_match_config.dataset_sep
        )
        
        service = ServiceStatistiquesBasket()
        service.charger_matchs(repo_matchs.load())
        classement_complet = service.obtenir_classement_global(phase=nom_phase)
        
        classement_filtre = []
        nom_affichage_conf = "GLOBALE"
        
        for equipe_id, stats_base in classement_complet:
            nom_eq = noms_equipes.get(str(equipe_id), f"ID:{equipe_id}")
            conference_eq = self.determiner_conference_nba(nom_eq)
            
            if choix_conf == '1' and conference_eq == "Est":
                classement_filtre.append((equipe_id, stats_base, nom_eq))
                nom_affichage_conf = "CONFÉRENCE EST"
            elif choix_conf == '2' and conference_eq == "Ouest":
                classement_filtre.append((equipe_id, stats_base, nom_eq))
                nom_affichage_conf = "CONFÉRENCE OUEST"
            elif choix_conf == '3' or choix_conf not in ['1', '2']:
                classement_filtre.append((equipe_id, stats_base, nom_eq))
                nom_affichage_conf = "GLOBALE"

        print(f"\n--- RÉSULTATS POUR : {nom_phase.upper()} | {nom_affichage_conf} ---")
        print(f"{'#':<3} | {'Équipe':<22} | {'Vic':<4} | {'Pts':<5} | {'Enc':<5} | {'Reb':<4} | {'Ast':<4} | {'Stl':<4} | {'Blk':<4} | {'2P%':<5} | {'3P%':<5} | {'LF%':<5}")
        print("-" * 105)
        
        if not classement_filtre:
            print(f"⚠️ Aucune donnée trouvée pour cette sélection.")
        
        for i, (equipe_id, stats_base, nom) in enumerate(classement_filtre, start=1):
            victoires = stats_base['victoires']
            moy = service.obtenir_moyennes(equipe_id, phase=nom_phase)
            
            if moy:
                print(f"{i:<3} | {nom:<22} | {victoires:<4} | {moy.get('pts_pour','N/A'):<5} | {moy.get('pts_contre','N/A'):<5} | {moy.get('rebonds','N/A'):<4} | {moy.get('passes','N/A'):<4} | {moy.get('interceptions','N/A'):<4} | {moy.get('contres','N/A'):<4} | {moy.get('pct_2pts','N/A'):<5} | {moy.get('pct_3pts','N/A'):<5} | {moy.get('pct_lf','N/A'):<5}")

        input("\nAppuyez sur Entrée pour revenir au menu...")

    def explorer_annuaire_basket(self):
        """Menu interactif pour naviguer des équipes vers les joueurs spécifiques."""
        print("\n⏳ Chargement de la base de données des joueurs...")
        noms_equipes = self.charger_dictionnaire_noms(basket_equipe_config)
        
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
            
            equipes_est = []
            equipes_ouest = []
            
            for eq_id, nom in noms_equipes.items():
                if self.determiner_conference_nba(nom) == "Est":
                    equipes_est.append(eq_id)
                else:
                    equipes_ouest.append(eq_id)
                    
            liste_ids_equipes = equipes_est + equipes_ouest
            
            for idx, equipe_id in enumerate(liste_ids_equipes, start=1):
                if idx == 1:
                    print("\n🔵 --- CONFÉRENCE EST ---")
                elif idx == len(equipes_est) + 1:
                    print("\n🔴 --- CONFÉRENCE OUEST ---")
                print(f"{idx:2}. {noms_equipes[equipe_id]}")
            
            print("\n" + "-" * 40)
            print(f"0. 🔙 Retour au menu principal")
            
            choix_eq = input("\n👉 Choisissez une équipe (numéro) : ")
        
            if choix_eq == str(0):
                break
                
            try:
                idx_choisi = int(choix_eq) - 1
                equipe_id = liste_ids_equipes[idx_choisi]
                nom_equipe = noms_equipes[equipe_id]
                
                while True:
                    effectif = annuaire.obtenir_joueurs_par_affiliation(equipe_id)
                    
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
                    print(f"0. 🔙 Choisir une autre équipe")
                    
                    choix_joueur = input("\n👉 Choisissez un joueur pour voir son profil : ")
                    
                    if choix_joueur == str(0):
                        break 
                        
                    try:
                        idx_j = int(choix_joueur) - 1
                        joueur_choisi = effectif_trie[idx_j]
                        
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

    def menu_basket(self):
        """Le menu principal d'entrée pour la section NBA."""
        while True:
            print("\n" + "*"*50)
            print(" 🏆 TABLEAU DE BORD NBA 🏆")
            print("*"*50)
            print("1. 🏀 NBA : Classement et Statistiques par équipes")
            print("2. 🏀 NBA : Explorer les Effectifs")
            print("0. 🔙 Retour au menu principal")
            
            choix = input("\n👉 Entrez votre choix (1-3) : ")
            
            if choix == '1':
                self.afficher_statistiques_basket()
            elif choix == '2':
                self.explorer_annuaire_basket()
            elif choix == '0':
                break
            else:
                print("\n⚠️ Choix invalide, veuillez réessayer.")

    # ==========================================
    # MODULE TENNIS
    # ==========================================

    def explorer_annuaire_tennis(self, config_joueurs, config_matchs, nom_circuit):
        """Menu interactif pour explorer les statistiques des joueurs de Tennis par pays."""
        print(f"\n⏳ Chargement de la base de données {nom_circuit}...")
        
        repo_joueurs = DataRepository(
            file=config_joueurs.dataset_path, adapter=config_joueurs.adapter, sep=config_joueurs.dataset_sep)
        annuaire = ServiceAnnuaireJoueurs()
        annuaire.charger_joueurs(repo_joueurs.load())
        
        repo_matchs = DataRepository(
            file=config_matchs.dataset_path, adapter=config_matchs.adapter, sep=config_matchs.dataset_sep)
        service_stats = ServiceStatistiquesTennis()
        service_stats.charger_matchs(repo_matchs.load())

        while True:
            print("\n" + "="*60)
            print(f"🌍 EXPLORATEUR INTERNATIONAL - CIRCUIT {nom_circuit}")
            print("="*60)
            
            liste_pays = annuaire.obtenir_pays_disponibles()
            
            print("📍 Codes pays disponibles :")
            for i in range(0, len(liste_pays), 7):
                tranche = liste_pays[i:i+7]
                print(", ".join(tranche))
            print("-" * 60)
            
            choix_pays = input("\n👉 Tapez le code à 3 lettres d'un pays (ou '0' pour quitter) : ").upper().strip()
            
            if choix_pays == str(0):
                break 
                
            if choix_pays not in liste_pays:
                print(f"⚠️ Aucun joueur trouvé pour le code '{choix_pays}'. Vérifiez l'orthographe.")
                continue
                
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
                
                if choix_j == str(0):
                    break 
                    
                try:
                    idx_choisi = int(choix_j) - 1
                    joueur = joueurs_du_pays[idx_choisi]
                    
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
                        
                        titres = stats['palmares']
                        print(f"  🏆 PALMARÈS ({len(titres)} titres) :")
                        if titres:
                            for i in range(0, len(titres), 3):
                                tranche_titres = titres[i:i+3]
                                print("    " + ", ".join(tranche_titres))
                        else:
                            print("  Aucun titre répertorié dans la base.")
                    else:
                        print("  ⚠️ Aucune donnée de match trouvée pour ce joueur.")
                    print("★"*45)
                    
                    input("\nAppuyez sur Entrée pour revenir à la liste des joueurs...")
                    
                except (ValueError, IndexError):
                    print("⚠️ Choix invalide. Veuillez entrer un numéro valide.")

    def menu_tennis(self):
        """Le menu principal d'entrée pour la section Tennis."""
        while True:
            print("\n" + "*"*50)
            print(" 🏆 TABLEAU DE BORD TENNIS 🏆")
            print("*"*50)
            print("1. 🎾 ATP : Circuit Masculin")
            print("2. 🎾 WTA : Circuit Féminin")
            print("0. 🔙 Retour au menu principal")
            
            choix = input("\n👉 Entrez votre choix (1-3) : ")
            
            if choix == '1':
                self.explorer_annuaire_tennis(tennis_atp_joueur_config, tennis_atp_match_config, "ATP")
            elif choix == '2':
                self.explorer_annuaire_tennis(tennis_wta_joueur_config, tennis_wta_match_config, "WTA")
            elif choix == str(0):
                break
            else:
                print("\n⚠️ Choix invalide, veuillez réessayer.")

    # ==========================================
    # LANCEMENT GLOBAL
    # ==========================================

    def lancer(self):
        """Boucle principale de lancement de l'application multisports."""
        while True:
            print("\n" + "*"*50)
            print(" 🏆 TABLEAU DE BORD MULTISPORTS 2026")
            print("*"*50)
            print("CHOIX DU SPORT :")
            print("1. 🏀 NBA 🏀")
            print("2. 🎾 TENNIS 🎾")
            print("0. ❌ Quitter")
            
            choix = input("\n👉 Entrez votre choix (1-3) : ")
            
            if choix == '1':
                self.menu_basket()
            elif choix == '2':
                self.menu_tennis()
            elif choix == str(0):
                print("\nFermeture du logiciel. À bientôt ! 👋\n")
                break
            else:
                print("\n⚠️ Choix invalide, veuillez réessayer.")