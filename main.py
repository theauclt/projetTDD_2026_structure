from pkg.repository.data_repository import DataRepository
from pkg.config.dataset_configuration import basket_match_config, basket_equipe_config
from pkg.services.service_statistiques import ServiceStatistiques

def charger_noms_equipes():
    """Charge le dictionnaire de correspondance ID -> Nom."""
    repo = DataRepository(
        file=basket_equipe_config.dataset_path,
        adapter=basket_equipe_config.adapter,
        sep=basket_equipe_config.dataset_sep
    )
    equipes = repo.load()
    # On crée le dictionnaire { id: nom }
    return {str(e.id): e.nom for e in equipes}

def afficher_classement_basket():
    """Logique complète pour le calcul et l'affichage du classement NBA."""
    print("=== ANALYSE : CLASSEMENT NBA ===")
    
    # 1. Préparation des données de traduction
    noms_equipes = charger_noms_equipes()
    
    # 2. Chargement des matchs
    repo_matchs = DataRepository(
        file=basket_match_config.dataset_path,
        adapter=basket_match_config.adapter,
        sep=basket_match_config.dataset_sep
    )
    liste_matchs = repo_matchs.load()
    
    # 3. Calcul des statistiques
    service = ServiceStatistiques()
    service.charger_matchs(liste_matchs)
    classement = service.obtenir_classement_global()
    
    # 4. Affichage propre
    for i, (equipe_id, stats) in enumerate(classement[:10], start=1):
        nom = noms_equipes.get(str(equipe_id), f"Inconnu ({equipe_id})")
        print(f"  {i:2}. {nom:<25} | Victoires: {stats['victoires']} | Points: {stats['points_marques']}")

def afficher_detail_match_nba(index_match=0):
    """Affiche les détails (sac à dos) d'un match spécifique."""
    noms_equipes = charger_noms_equipes()
    repo_matchs = DataRepository(
        file=basket_match_config.dataset_path, 
        adapter=basket_match_config.adapter,
        sep=basket_match_config.dataset_sep)
    liste_matchs = repo_matchs.load()
    
    match = liste_matchs[index_match]
    nom_dom = noms_equipes.get(str(match.equipe1), match.equipe1)
    nom_ext = noms_equipes.get(str(match.equipe2), match.equipe2)
    
    print(f"\n[Détails Match] {nom_dom} vs {nom_ext} ({match.date})")
    # On affiche une stat spécifique du sac à dos
    tirs_3pts = match.stats.get('fg3m_home', 'N/A')
    print(f" -> Paniers à 3 pts réussis par l'équipe à domicile : {tirs_3pts}")
    

if __name__ == "__main__":
    print("Logiciel d'Analyse Multisports 2026")
    choix = input("Tapez '1' pour le classement NBA, '2' pour les détails : ")
    
    if choix == '1':
        afficher_classement_basket()
    elif choix == '2':
        afficher_detail_match_nba()
    else:
        print("Choix invalide.")