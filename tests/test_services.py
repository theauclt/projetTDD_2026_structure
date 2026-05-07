"""
Tests unitaires — SERVICES
Vérifie la logique métier : calcul des statistiques, classements,
moyennes, annuaire des joueurs et gestion des matchs.
"""

import pytest
from unittest.mock import MagicMock


# ==============================================================================
# TESTS — SERVICE STATISTIQUES (générique)
# ==============================================================================

class TestServiceStatistiques:
    """Tests pour ServiceStatistiques générique."""

    def setup_method(self):
        from pkg.services.service_statistiques import ServiceStatistiques
        from pkg.models.match import Match
        self.service = ServiceStatistiques()
        self.match1 = Match(1, "2024-01-01", "Lakers", "Celtics", 110, 95)
        self.match2 = Match(2, "2024-01-02", "Lakers", "Warriors", 90, 105)
        self.match_nul = Match(3, "2024-01-03", "Celtics", "Warriors", 100, 100)

    def test_charger_matchs(self):
        self.service.charger_matchs([self.match1, self.match2])
        assert len(self.service.matchs) == 2

    def test_ajouter_match_incremente_joues(self):
        self.service.ajouter_match(self.match1)
        assert self.service.stats["Lakers"]["joues"] == 1
        assert self.service.stats["Celtics"]["joues"] == 1

    def test_ajouter_match_victoire_equipe1(self):
        self.service.ajouter_match(self.match1)
        assert self.service.stats["Lakers"]["victoires"] == 1
        assert self.service.stats["Celtics"]["defaites"] == 1

    def test_ajouter_match_victoire_equipe2(self):
        self.service.ajouter_match(self.match2)
        assert self.service.stats["Warriors"]["victoires"] == 1
        assert self.service.stats["Lakers"]["defaites"] == 1

    def test_ajouter_match_nul(self):
        self.service.ajouter_match(self.match_nul)
        assert self.service.stats["Celtics"]["nuls"] == 1
        assert self.service.stats["Warriors"]["nuls"] == 1

    def test_points_marques(self):
        self.service.ajouter_match(self.match1)
        assert self.service.stats["Lakers"]["points_marques"] == 110
        assert self.service.stats["Celtics"]["points_marques"] == 95

    def test_obtenir_classement_global_ordre(self):
        self.service.charger_matchs([self.match1, self.match2])
        classement = self.service.obtenir_classement_global()
        noms = [nom for nom, _ in classement]
        assert len(noms) == 3

    def test_obtenir_stats_entite_existante(self):
        self.service.ajouter_match(self.match1)
        stats = self.service.obtenir_stats_entite("Lakers")
        assert stats is not None
        assert stats["victoires"] == 1

    def test_obtenir_stats_entite_inconnue(self):
        stats = self.service.obtenir_stats_entite("Inconnue")
        assert stats is None

    def test_obtenir_historique_equipe(self):
        self.service.charger_matchs([self.match1, self.match2, self.match_nul])
        historique = self.service.obtenir_historique_equipe("Lakers")
        assert len(historique) == 2

    def test_obtenir_historique_equipe_inconnue(self):
        historique = self.service.obtenir_historique_equipe("Inconnue")
        assert historique == []

    def test_calculer_classement_championnat(self):
        self.service.charger_matchs([self.match1, self.match2])
        classement = self.service.calculer_classement_championnat()
        noms_points = {nom: stats["points"] for nom, stats in classement}
        assert noms_points["Warriors"] == 3
        assert noms_points["Lakers"] == 3
        assert noms_points["Celtics"] == 0

    def test_calculer_classement_avec_nul(self):
        self.service.ajouter_match(self.match_nul)
        classement = self.service.calculer_classement_championnat()
        noms_points = {nom: stats["points"] for nom, stats in classement}
        assert noms_points["Celtics"] == 1
        assert noms_points["Warriors"] == 1

    def test_calculer_classement_points_custom(self):
        self.service.ajouter_match(self.match1)
        classement = self.service.calculer_classement_championnat(pts_victoire=2, pts_defaite=1)
        noms_points = {nom: stats["points"] for nom, stats in classement}
        assert noms_points["Lakers"] == 2
        assert noms_points["Celtics"] == 1

    def test_calculer_classement_difference_buts(self):
        self.service.ajouter_match(self.match1)
        classement = self.service.calculer_classement_championnat()
        noms_diff = {nom: stats["diff"] for nom, stats in classement}
        assert noms_diff["Lakers"] == 15
        assert noms_diff["Celtics"] == -15


# ==============================================================================
# TESTS — SERVICE STATISTIQUES BASKET
# ==============================================================================

class TestServiceStatistiquesBasket:
    """Tests pour ServiceStatistiquesBasket."""

    def setup_method(self):
        from pkg.services.service_statistiques import ServiceStatistiquesBasket
        from pkg.models.match import Match
        self.service = ServiceStatistiquesBasket()
        self.match_regular = Match(
            id=1, date="2024-01-01",
            equipe1="Lakers", equipe2="Celtics",
            score1=110, score2=95,
            stats={
                "type_match": "Regular Season",
                "reb_home": 40, "ast_home": 25, "stl_home": 8, "blk_home": 5,
                "fgm_home": 42, "fga_home": 90, "fg3m_home": 12, "fg3a_home": 35,
                "ftm_home": 14, "fta_home": 18,
                "reb_away": 35, "ast_away": 22, "stl_away": 6, "blk_away": 4,
                "fgm_away": 38, "fga_away": 88, "fg3m_away": 10, "fg3a_away": 30,
                "ftm_away": 9, "fta_away": 12
            }
        )
        self.match_playoffs = Match(
            id=2, date="2024-04-01",
            equipe1="Lakers", equipe2="Warriors",
            score1=105, score2=98,
            stats={"type_match": "Playoffs"}
        )

    def test_charger_matchs_remplit_stats_par_phase(self):
        self.service.charger_matchs([self.match_regular])
        assert "Regular Season" in self.service.stats_par_phase

    def test_stats_par_phase_victoires(self):
        self.service.charger_matchs([self.match_regular])
        stats_lakers = self.service.stats_par_phase["Regular Season"]["Lakers"]
        assert stats_lakers["victoires"] == 1
        assert stats_lakers["defaites"] == 0

    def test_stats_par_phase_defaite(self):
        self.service.charger_matchs([self.match_regular])
        stats_celtics = self.service.stats_par_phase["Regular Season"]["Celtics"]
        assert stats_celtics["victoires"] == 0
        assert stats_celtics["defaites"] == 1

    def test_stats_par_phase_points(self):
        self.service.charger_matchs([self.match_regular])
        stats_lakers = self.service.stats_par_phase["Regular Season"]["Lakers"]
        assert stats_lakers["points_marques"] == 110
        assert stats_lakers["points_encaisses"] == 95

    def test_obtenir_classement_global_par_phase(self):
        self.service.charger_matchs([self.match_regular, self.match_playoffs])
        classement_regular = self.service.obtenir_classement_global("Regular Season")
        noms = [nom for nom, _ in classement_regular]
        assert "Lakers" in noms
        assert "Celtics" in noms

    def test_obtenir_classement_phase_inconnue(self):
        classement = self.service.obtenir_classement_global("Phase Inconnue")
        assert classement == []

    def test_obtenir_moyennes_calcul(self):
        self.service.charger_matchs([self.match_regular])
        moyennes = self.service.obtenir_moyennes("Lakers", "Regular Season")
        assert moyennes is not None
        assert moyennes["pts_pour"] == 110.0
        assert moyennes["pts_contre"] == 95.0

    def test_obtenir_moyennes_equipe_inconnue(self):
        self.service.charger_matchs([self.match_regular])
        moyennes = self.service.obtenir_moyennes("Inconnue", "Regular Season")
        assert moyennes is None

    def test_obtenir_moyennes_phase_inconnue(self):
        self.service.charger_matchs([self.match_regular])
        moyennes = self.service.obtenir_moyennes("Lakers", "Phase Inconnue")
        assert moyennes is None

    def test_obtenir_moyennes_pourcentages_tirs(self):
        self.service.charger_matchs([self.match_regular])
        moyennes = self.service.obtenir_moyennes("Lakers", "Regular Season")
        assert moyennes["pct_3pts"] == round((12 / 35) * 100, 1)


# ==============================================================================
# TESTS — SERVICE STATISTIQUES TENNIS
# ==============================================================================

class TestServiceStatistiquesTennis:
    """Tests pour ServiceStatistiquesTennis."""

    def setup_method(self):
        from pkg.services.service_statistiques import ServiceStatistiquesTennis
        from pkg.models.match import Match
        self.service = ServiceStatistiquesTennis()
        self.match_finale = Match(
            id="M001", date="20240115",
            equipe1="101", equipe2="202",
            score1=1, score2=0,
            stats={
                "round": "F", "tourney_name": "Roland Garros",
                "minutes": 180, "w_ace": 8, "w_df": 3,
                "w_bpSaved": 5, "w_bpFaced": 7,
                "l_ace": 4, "l_df": 5,
                "l_bpSaved": 2, "l_bpFaced": 6
            }
        )
        self.match_normal = Match(
            id="M002", date="20240116",
            equipe1="101", equipe2="303",
            score1=1, score2=0,
            stats={
                "round": "QF", "tourney_name": "Wimbledon",
                "minutes": 120, "w_ace": 6, "w_df": 2,
                "w_bpSaved": 3, "w_bpFaced": 5,
                "l_ace": 2, "l_df": 3,
                "l_bpSaved": 1, "l_bpFaced": 4
            }
        )

    def test_charger_matchs_cree_stats_joueur(self):
        self.service.charger_matchs([self.match_finale])
        assert "101" in self.service.stats_joueurs
        assert "202" in self.service.stats_joueurs

    def test_victoire_perdant_incrementes(self):
        self.service.charger_matchs([self.match_finale])
        assert self.service.stats_joueurs["101"]["victoires"] == 1
        assert self.service.stats_joueurs["202"]["defaites"] == 1

    def test_palmares_finale(self):
        self.service.charger_matchs([self.match_finale])
        assert "Roland Garros" in self.service.stats_joueurs["101"]["palmares"]

    def test_palmares_pas_finale(self):
        self.service.charger_matchs([self.match_normal])
        assert len(self.service.stats_joueurs["101"]["palmares"]) == 0

    def test_aces_comptabilises(self):
        self.service.charger_matchs([self.match_finale])
        assert self.service.stats_joueurs["101"]["total_aces"] == 8.0
        assert self.service.stats_joueurs["202"]["total_aces"] == 4.0

    def test_obtenir_moyennes_joueur(self):
        self.service.charger_matchs([self.match_finale])
        moyennes = self.service.obtenir_moyennes_joueur("101")
        assert moyennes is not None
        assert moyennes["victoires"] == 1
        assert moyennes["aces_par_match"] == 8.0

    def test_obtenir_moyennes_joueur_inconnu(self):
        moyennes = self.service.obtenir_moyennes_joueur("999")
        assert moyennes is None

    def test_nettoyer_valeur_nan(self):
        assert self.service.nettoyer_valeur("nan") == 0.0

    def test_nettoyer_valeur_vide(self):
        assert self.service.nettoyer_valeur("") == 0.0
        assert self.service.nettoyer_valeur(None) == 0.0

    def test_nettoyer_valeur_valide(self):
        assert self.service.nettoyer_valeur("12.5") == 12.5
        assert self.service.nettoyer_valeur(7) == 7.0

    def test_balles_de_break(self):
        self.service.charger_matchs([self.match_finale])
        assert self.service.stats_joueurs["101"]["bp_converties"] == 4.0


# ==============================================================================
# TESTS — SERVICE ANNUAIRE JOUEURS
# ==============================================================================

class TestServiceAnnuaireJoueurs:
    """Tests pour ServiceAnnuaireJoueurs."""

    def setup_method(self):
        from pkg.services.service_annuaire_joueur import ServiceAnnuaireJoueurs
        from pkg.models.joueur import JoueurTennis, JoueurBasket
        self.service = ServiceAnnuaireJoueurs()
        self.j_tennis_esp  = JoueurTennis(101, "Rafael", "Nadal", 185, "1986-06-03", "ESP", "L")
        self.j_tennis_sui  = JoueurTennis(102, "Roger", "Federer", 185, "1981-08-08", "SUI", "R")
        self.j_tennis_esp2 = JoueurTennis(103, "Carlos", "Alcaraz", 183, "2003-05-05", "ESP", "R")
        self.j_basket      = JoueurBasket(23, "LeBron", "James", 206, "1984-12-30", 1610612747, "23", "F", "250 lbs")

    def test_charger_joueurs_remplit_annuaire(self):
        self.service.charger_joueurs([self.j_tennis_esp, self.j_tennis_sui])
        assert len(self.service.annuaire) == 2

    def test_charger_joueurs_cle_est_string(self):
        self.service.charger_joueurs([self.j_tennis_esp])
        assert "101" in self.service.annuaire

    def test_charger_joueurs_convertit_poids_basket(self):
        self.service.charger_joueurs([self.j_basket])
        assert "kg" in self.j_basket.poids

    def test_charger_joueurs_poids_deja_kg(self):
        from pkg.models.joueur import JoueurBasket
        j = JoueurBasket(99, "A", "B", 200, "1990-01-01", 1, "1", "G", "113.4 kg")
        self.service.charger_joueurs([j])
        assert j.poids == "113.4 kg"

    def test_obtenir_joueur_existant(self):
        self.service.charger_joueurs([self.j_tennis_esp])
        joueur = self.service.obtenir_joueur(101)
        assert joueur == self.j_tennis_esp

    def test_obtenir_joueur_inexistant(self):
        joueur = self.service.obtenir_joueur(9999)
        assert joueur is None

    def test_obtenir_pays_disponibles(self):
        self.service.charger_joueurs([self.j_tennis_esp, self.j_tennis_sui, self.j_tennis_esp2])
        pays = self.service.obtenir_pays_disponibles()
        assert "ESP" in pays
        assert "SUI" in pays
        assert len(pays) == 2

    def test_obtenir_pays_disponibles_trie(self):
        self.service.charger_joueurs([self.j_tennis_sui, self.j_tennis_esp])
        pays = self.service.obtenir_pays_disponibles()
        assert pays == sorted(pays)

    def test_obtenir_pays_disponibles_ignore_nan(self):
        from pkg.models.joueur import JoueurTennis
        j_nan = JoueurTennis(200, "X", "Y", 180, "2000-01-01", "nan", "R")
        self.service.charger_joueurs([j_nan, self.j_tennis_esp])
        pays = self.service.obtenir_pays_disponibles()
        assert "nan" not in pays

    def test_obtenir_joueurs_par_pays_filtre(self):
        self.service.charger_joueurs([self.j_tennis_esp, self.j_tennis_sui, self.j_tennis_esp2])
        joueurs_esp = self.service.obtenir_joueurs_par_pays("ESP")
        assert len(joueurs_esp) == 2

    def test_obtenir_joueurs_par_pays_insensible_casse(self):
        self.service.charger_joueurs([self.j_tennis_esp])
        joueurs = self.service.obtenir_joueurs_par_pays("esp")
        assert len(joueurs) == 1

    def test_obtenir_joueurs_par_pays_trie_alphabetiquement(self):
        self.service.charger_joueurs([self.j_tennis_esp, self.j_tennis_esp2])
        joueurs = self.service.obtenir_joueurs_par_pays("ESP")
        noms = [j.nom_complet for j in joueurs]
        assert noms == sorted(noms)

    def test_obtenir_joueurs_par_pays_inconnu(self):
        self.service.charger_joueurs([self.j_tennis_esp])
        joueurs = self.service.obtenir_joueurs_par_pays("ZZZ")
        assert joueurs == []

    def test_obtenir_joueurs_par_affiliation(self):
        self.service.charger_joueurs([self.j_basket])
        joueurs = self.service.obtenir_joueurs_par_affiliation(1610612747)
        assert len(joueurs) == 1
        assert joueurs[0] == self.j_basket

    def test_obtenir_joueurs_par_affiliation_inconnue(self):
        self.service.charger_joueurs([self.j_basket])
        joueurs = self.service.obtenir_joueurs_par_affiliation(9999)
        assert joueurs == []

    def test_convertir_poids_en_kg(self):
        resultat = self.service._convertir_poids_en_kg("220")
        assert "kg" in resultat
        assert "99.8" in resultat

    def test_convertir_poids_en_kg_avec_lbs(self):
        resultat = self.service._convertir_poids_en_kg("220 lbs")
        assert "kg" in resultat

    def test_convertir_poids_invalide(self):
        resultat = self.service._convertir_poids_en_kg("N/A")
        assert resultat == "N/A"

    def test_convertir_poids_none(self):
        resultat = self.service._convertir_poids_en_kg(None)
        assert resultat == "N/A"


# ==============================================================================
# TESTS — SERVICE MATCHS
# ==============================================================================

class TestServiceMatchs:
    """Tests pour ServiceMatchs."""

    def test_init_vide_par_defaut(self):
        from pkg.services.services_matchs import ServiceMatchs
        s = ServiceMatchs()
        assert s.matchs == []

    def test_init_avec_liste(self):
        from pkg.services.services_matchs import ServiceMatchs
        from pkg.models.match import Match
        m = Match(1, "2024-01-01", "A", "B", 10, 5)
        s = ServiceMatchs([m])
        assert len(s.matchs) == 1

    def test_afficher_matchs_ne_plante_pas(self, capsys):
        from pkg.services.services_matchs import ServiceMatchs
        from pkg.models.match import Match
        m = Match(1, "2024-01-01", "A", "B", 10, 5)
        s = ServiceMatchs([m])
        s.afficher_matchs()
        captured = capsys.readouterr()
        assert "A" in captured.out
