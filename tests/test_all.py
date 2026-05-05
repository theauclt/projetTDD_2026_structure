"""
Tests unitaires complets pour le projet de traitement de données sportives.
Couverture : models, adapters, services, repository
"""

import pytest
from unittest.mock import MagicMock, patch, mock_open
from collections import defaultdict
import io

from pkg.services.services_matchs import ServiceMatchs


# ==============================================================================
# TESTS — MODÈLES
# ==============================================================================

class TestJoueur:
    """Tests pour la classe de base Joueur."""

    def setup_method(self):
        from pkg.models.joueur import Joueur
        self.joueur = Joueur(
            id=1, prenom="LeBron", nom="James",
            taille=206, date_naissance="1984-12-30"
        )

    def test_attributs_de_base(self):
        assert self.joueur.id == 1
        assert self.joueur.prenom == "LeBron"
        assert self.joueur.nom == "James"
        assert self.joueur.taille == 206
        assert self.joueur.date_naissance == "1984-12-30"

    def test_nom_complet_construit_correctement(self):
        assert self.joueur.nom_complet == "LeBron James"

    def test_nom_complet_prenom_vide(self):
        from pkg.models.joueur import Joueur
        j = Joueur(id=2, prenom="", nom="James", taille=200, date_naissance="1990-01-01")
        assert j.nom_complet == "James"

    def test_nom_complet_nom_vide(self):
        from pkg.models.joueur import Joueur
        j = Joueur(id=3, prenom="LeBron", nom="", taille=200, date_naissance="1990-01-01")
        assert j.nom_complet == "LeBron"


class TestJoueurBasket:
    """Tests pour la spécialisation JoueurBasket."""

    def setup_method(self):
        from pkg.models.joueur import JoueurBasket
        self.joueur = JoueurBasket(
            id=23, prenom="LeBron", nom="James",
            taille=206, date_naissance="1984-12-30",
            equipe_id=1610612747, numero="23",
            position="F", poids="250"
        )

    def test_heritage_joueur(self):
        from pkg.models.joueur import Joueur
        assert isinstance(self.joueur, Joueur)

    def test_attributs_specifiques_basket(self):
        assert self.joueur.equipe_id == 1610612747
        assert self.joueur.numero == "23"
        assert self.joueur.position == "F"
        assert self.joueur.poids == "250"

    def test_nom_complet_herite(self):
        assert self.joueur.nom_complet == "LeBron James"


class TestJoueurTennis:
    """Tests pour la spécialisation JoueurTennis."""

    def setup_method(self):
        from pkg.models.joueur import JoueurTennis
        self.joueur = JoueurTennis(
            id=101, prenom="Rafael", nom="Nadal",
            taille=185, date_naissance="1986-06-03",
            pays_ioc="ESP", main_forte="L"
        )

    def test_heritage_joueur(self):
        from pkg.models.joueur import Joueur
        assert isinstance(self.joueur, Joueur)

    def test_attributs_specifiques_tennis(self):
        assert self.joueur.pays_ioc == "ESP"
        assert self.joueur.main_forte == "L"

    def test_nom_complet(self):
        assert self.joueur.nom_complet == "Rafael Nadal"


class TestEquipe:
    """Tests pour le modèle Equipe."""

    def setup_method(self):
        from pkg.models.equipe import Equipe
        self.equipe = Equipe(
            id=1, nom="Los Angeles Lakers",
            abreviation="LAL", lieu="Los Angeles", region="California"
        )

    def test_attributs_de_base(self):
        assert self.equipe.id == 1
        assert self.equipe.nom == "Los Angeles Lakers"
        assert self.equipe.abreviation == "LAL"
        assert self.equipe.lieu == "Los Angeles"
        assert self.equipe.region == "California"

    def test_abreviation_par_defaut_est_le_nom(self):
        from pkg.models.equipe import Equipe
        e = Equipe(id=2, nom="Boston Celtics")
        assert e.abreviation == "Boston Celtics"

    def test_liste_joueurs_vide_par_defaut(self):
        assert self.equipe.joueurs == []

    def test_entraineur_none_par_defaut(self):
        assert self.equipe.entraineur is None

    def test_ajouter_joueur(self):
        from pkg.models.joueur import JoueurBasket
        j = JoueurBasket(23, "LeBron", "James", 206, "1984-12-30", 1, "23", "F", "250")
        self.equipe.ajouter_joueur(j)
        assert j in self.equipe.joueurs

    def test_ajouter_joueur_pas_de_doublon(self):
        from pkg.models.joueur import JoueurBasket
        j = JoueurBasket(23, "LeBron", "James", 206, "1984-12-30", 1, "23", "F", "250")
        self.equipe.ajouter_joueur(j)
        self.equipe.ajouter_joueur(j)  # second ajout identique
        assert len(self.equipe.joueurs) == 1

    def test_assigner_entraineur(self):
        entraineur = MagicMock()
        self.equipe.assigner_entraineur(entraineur)
        assert self.equipe.entraineur == entraineur

    def test_obtenir_taille_effectif(self):
        from pkg.models.joueur import JoueurBasket
        j1 = JoueurBasket(1, "A", "B", 200, "1990-01-01", 1, "1", "G", "200")
        j2 = JoueurBasket(2, "C", "D", 210, "1991-01-01", 1, "2", "F", "220")
        self.equipe.ajouter_joueur(j1)
        self.equipe.ajouter_joueur(j2)
        assert self.equipe.obtenir_taille_effectif() == 2

    def test_obtenir_taille_moyenne(self):
        from pkg.models.joueur import JoueurBasket
        j1 = JoueurBasket(1, "A", "B", 200, "1990-01-01", 1, "1", "G", "200")
        j2 = JoueurBasket(2, "C", "D", 210, "1991-01-01", 1, "2", "F", "220")
        self.equipe.ajouter_joueur(j1)
        self.equipe.ajouter_joueur(j2)
        assert self.equipe.obtenir_taille_moyenne() == 205.0

    def test_obtenir_taille_moyenne_equipe_vide(self):
        assert self.equipe.obtenir_taille_moyenne() == 0

    def test_obtenir_taille_moyenne_ignore_taille_zero(self):
        from pkg.models.joueur import JoueurBasket
        j1 = JoueurBasket(1, "A", "B", 200, "1990-01-01", 1, "1", "G", "200")
        j2 = JoueurBasket(2, "C", "D", 0, "1991-01-01", 1, "2", "F", "220")  # taille invalide
        self.equipe.ajouter_joueur(j1)
        self.equipe.ajouter_joueur(j2)
        assert self.equipe.obtenir_taille_moyenne() == 200.0

    def test_a_effectif_minimum_vrai(self):
        from pkg.models.joueur import JoueurBasket
        for i in range(5):
            j = JoueurBasket(i, "A", "B", 200, "1990-01-01", 1, str(i), "G", "200")
            self.equipe.ajouter_joueur(j)
        assert self.equipe.a_effectif_minimum(5) is True

    def test_a_effectif_minimum_faux(self):
        assert self.equipe.a_effectif_minimum(5) is False

    def test_str_avec_lieu(self):
        assert "Los Angeles Lakers" in str(self.equipe)
        assert "Los Angeles" in str(self.equipe)

    def test_str_sans_lieu(self):
        from pkg.models.equipe import Equipe
        e = Equipe(id=99, nom="Team X")
        assert "Global" in str(e)


class TestMatch:
    """Tests pour le modèle Match."""

    def setup_method(self):
        from pkg.models.match import Match
        self.match = Match(
            id=1, date="2024-01-15",
            equipe1="Lakers", equipe2="Celtics",
            score1=110, score2=95
        )

    def test_attributs_de_base(self):
        assert self.match.id == 1
        assert self.match.date == "2024-01-15"
        assert self.match.equipe1 == "Lakers"
        assert self.match.equipe2 == "Celtics"
        assert self.match.score1 == 110
        assert self.match.score2 == 95

    def test_stats_vide_par_defaut(self):
        assert self.match.stats == {}

    def test_stats_custom(self):
        from pkg.models.match import Match
        m = Match(1, "2024-01-01", "A", "B", 10, 5, stats={"type": "Playoffs"})
        assert m.stats["type"] == "Playoffs"

    def test_vainqueur_equipe1(self):
        assert self.match.vainqueur() == "Lakers"

    def test_vainqueur_equipe2(self):
        from pkg.models.match import Match
        m = Match(2, "2024-01-16", "Lakers", "Celtics", 90, 105)
        assert m.vainqueur() == "Celtics"

    def test_vainqueur_nul(self):
        from pkg.models.match import Match
        m = Match(3, "2024-01-17", "Lakers", "Celtics", 100, 100)
        assert m.vainqueur() is None

    def test_perdant_equipe2(self):
        assert self.match.perdant() == "Celtics"

    def test_perdant_equipe1(self):
        from pkg.models.match import Match
        m = Match(2, "2024-01-16", "Lakers", "Celtics", 90, 105)
        assert m.perdant() == "Lakers"

    def test_perdant_nul(self):
        from pkg.models.match import Match
        m = Match(3, "2024-01-17", "Lakers", "Celtics", 100, 100)
        assert m.perdant() is None

    def test_obtenir_total_points(self):
        assert self.match.obtenir_total_points() == 205

    def test_obtenir_points_pour_equipe1(self):
        assert self.match.obtenir_points_pour("Lakers") == 110

    def test_obtenir_points_pour_equipe2(self):
        assert self.match.obtenir_points_pour("Celtics") == 95

    def test_obtenir_points_pour_equipe_inconnue(self):
        assert self.match.obtenir_points_pour("Warriors") == 0

    def test_obtenir_points_contre_equipe1(self):
        assert self.match.obtenir_points_contre("Lakers") == 95

    def test_obtenir_points_contre_equipe2(self):
        assert self.match.obtenir_points_contre("Celtics") == 110

    def test_obtenir_points_contre_equipe_inconnue(self):
        assert self.match.obtenir_points_contre("Warriors") == 0

    def test_implique_equipe_vrai(self):
        assert self.match.implique_equipe("Lakers") is True
        assert self.match.implique_equipe("Celtics") is True

    def test_implique_equipe_faux(self):
        assert self.match.implique_equipe("Warriors") is False

    def test_obtenir_difference_points(self):
        assert self.match.obtenir_difference_points() == 15

    def test_obtenir_difference_points_nul(self):
        from pkg.models.match import Match
        m = Match(3, "2024-01-17", "Lakers", "Celtics", 100, 100)
        assert m.obtenir_difference_points() == 0

    def test_str(self):
        s = str(self.match)
        assert "Lakers" in s
        assert "Celtics" in s
        assert "110" in s
        assert "95" in s

    def test_repr(self):
        r = repr(self.match)
        assert "Lakers" in r
        assert "2024-01-15" in r


class TestStatistiqueJoueur:
    """Tests pour le modèle StatistiqueJoueur."""

    def setup_method(self):
        from pkg.models.stats_joueur_basket import StatistiqueJoueur
        self.stat = StatistiqueJoueur(
            match_id=1, joueur_id=23, nom_joueur="LeBron James",
            equipe_id=1610612747, pts=30, reb=8, ast=10, blk=1, stl=2
        )

    def test_attributs_de_base(self):
        assert self.stat.match_id == 1
        assert self.stat.joueur_id == 23
        assert self.stat.nom_joueur == "LeBron James"
        assert self.stat.equipe_id == 1610612747

    def test_conversion_en_float(self):
        assert isinstance(self.stat.pts, float)
        assert self.stat.pts == 30.0
        assert self.stat.reb == 8.0
        assert self.stat.ast == 10.0

    def test_valeurs_vides_deviennent_zero(self):
        from pkg.models.stats_joueur_basket import StatistiqueJoueur
        s = StatistiqueJoueur(1, 1, "X", 1, pts=None, reb="", ast=0, blk=None, stl=None)
        assert s.pts == 0.0
        assert s.reb == 0.0
        assert s.blk == 0.0


# ==============================================================================
# TESTS — ADAPTERS
# ==============================================================================

class TestGenericEquipeAdapter:
    """Tests pour GenericEquipeAdapter."""

    def setup_method(self):
        from pkg.adapter.generic_equipe_adapter import GenericEquipeAdapter
        self.adapter = GenericEquipeAdapter(
            col_id="id", col_nom="full_name",
            col_abbr="abbreviation", col_loc="city", col_reg="state"
        )

    def test_adapt_cree_equipe(self):
        from pkg.models.equipe import Equipe
        row = {"id": 1, "full_name": "Los Angeles Lakers", "abbreviation": "LAL", "city": "Los Angeles", "state": "California"}
        equipe = self.adapter.adapt(row)
        assert isinstance(equipe, Equipe)

    def test_adapt_remplit_attributs(self):
        row = {"id": 1, "full_name": "Los Angeles Lakers", "abbreviation": "LAL", "city": "Los Angeles", "state": "California"}
        equipe = self.adapter.adapt(row)
        assert equipe.id == 1
        assert equipe.nom == "Los Angeles Lakers"
        assert equipe.abreviation == "LAL"
        assert equipe.lieu == "Los Angeles"
        assert equipe.region == "California"

    def test_adapt_sans_colonnes_optionnelles(self):
        from pkg.adapter.generic_equipe_adapter import GenericEquipeAdapter
        adapter = GenericEquipeAdapter(col_id="id", col_nom="full_name")
        row = {"id": 2, "full_name": "Boston Celtics"}
        equipe = adapter.adapt(row)
        assert equipe.abreviation == "Boston Celtics"  # valeur par défaut
        assert equipe.lieu is None
        assert equipe.region is None

    def test_to_row_retourne_none(self):
        result = self.adapter.to_row(MagicMock())
        assert result is None


class TestBasketJoueurAdapter:
    """Tests pour BasketJoueurAdapter."""

    def setup_method(self):
        from pkg.adapter.generic_joueur_adapter import BasketJoueurAdapter
        self.adapter = BasketJoueurAdapter(
            col_id="person_id", col_prenom="first_name", col_nom="last_name",
            col_taille="height", col_date_naissance="birthdate",
            col_equipe="team_id", col_numero="jersey",
            col_position="position", col_poids="weight"
        )
        self.row = {
            "person_id": 2544, "first_name": "LeBron", "last_name": "James",
            "height": "6-8", "birthdate": "1984-12-30",
            "team_id": 1610612747, "jersey": "23",
            "position": "Forward", "weight": "250"
        }

    def test_adapt_cree_joueur_basket(self):
        from pkg.models.joueur import JoueurBasket
        joueur = self.adapter.adapt(self.row)
        assert isinstance(joueur, JoueurBasket)

    def test_adapt_remplit_attributs_base(self):
        joueur = self.adapter.adapt(self.row)
        assert joueur.id == 2544
        assert joueur.prenom == "LeBron"
        assert joueur.nom == "James"

    def test_adapt_remplit_attributs_basket(self):
        joueur = self.adapter.adapt(self.row)
        assert joueur.equipe_id == 1610612747
        assert joueur.numero == "23"
        assert joueur.position == "Forward"
        assert joueur.poids == "250"

    def test_adapt_valeurs_manquantes(self):
        row_partiel = {"person_id": 99}
        joueur = self.adapter.adapt(row_partiel)
        assert joueur.prenom == ""
        assert joueur.nom == ""
        assert joueur.equipe_id == "Inconnu"


class TestTennisJoueurAdapter:
    """Tests pour TennisJoueurAdapter."""

    def setup_method(self):
        from pkg.adapter.generic_joueur_adapter import TennisJoueurAdapter
        self.adapter = TennisJoueurAdapter(
            col_id="player_id", col_prenom="name_first", col_nom="name_last",
            col_taille="height", col_date_naissance="dob",
            col_pays="ioc", col_main="hand"
        )

    def test_adapt_cree_joueur_tennis(self):
        from pkg.models.joueur import JoueurTennis
        row = {
            "player_id": 101, "name_first": "Rafael", "name_last": "Nadal",
            "height": 185, "dob": "19860603", "ioc": "ESP", "hand": "L"
        }
        joueur = self.adapter.adapt(row)
        assert isinstance(joueur, JoueurTennis)
        assert joueur.pays_ioc == "ESP"
        assert joueur.main_forte == "L"

    def test_adapt_valeurs_manquantes(self):
        row = {"player_id": 200}
        joueur = self.adapter.adapt(row)
        assert joueur.pays_ioc == "Inconnu"
        assert joueur.main_forte == "N/A"


class TestGenericMatchAdapter:
    """Tests pour GenericMatchAdapter."""

    def setup_method(self):
        from pkg.adapter.generic_match_adapter import GenericMatchAdapter
        self.adapter = GenericMatchAdapter(
            col_date="game_date", col_equipe1="team_id_home",
            col_equipe2="team_id_away", col_score1="pts_home",
            col_score2="pts_away"
        )
        self.row = {
            "game_date": "2024-01-15", "team_id_home": "Lakers",
            "team_id_away": "Celtics", "pts_home": 110, "pts_away": 95,
            "extra_stat": 42
        }

    def test_adapt_cree_match(self):
        from pkg.models.match import Match
        match = self.adapter.adapt(self.row)
        assert isinstance(match, Match)

    def test_adapt_remplit_champs_principaux(self):
        match = self.adapter.adapt(self.row)
        assert match.date == "2024-01-15"
        assert match.equipe1 == "Lakers"
        assert match.equipe2 == "Celtics"
        assert match.score1 == 110
        assert match.score2 == 95

    def test_adapt_type_match_defaut(self):
        match = self.adapter.adapt(self.row)
        assert match.stats["type_match"] == "Regular Season"

    def test_adapt_avec_type_match_custom(self):
        from pkg.adapter.generic_match_adapter import GenericMatchAdapter
        adapter = GenericMatchAdapter(
            col_date="game_date", col_equipe1="team_id_home",
            col_equipe2="team_id_away", col_score1="pts_home",
            col_score2="pts_away", col_type_match="season_type"
        )
        row = {**self.row, "season_type": "Playoffs"}
        match = adapter.adapt(row)
        assert match.stats["type_match"] == "Playoffs"

    def test_adapt_extra_stats_dans_stats(self):
        match = self.adapter.adapt(self.row)
        assert match.stats.get("extra_stat") == 42

    def test_to_row_reconstruit_dictionnaire(self):
        from pkg.models.match import Match
        match = Match(1, "2024-01-15", "Lakers", "Celtics", 110, 95)
        row = self.adapter.to_row(match)
        assert row["game_date"] == "2024-01-15"
        assert row["team_id_home"] == "Lakers"
        assert row["pts_home"] == 110


class TestTennisMatchAdapter:
    """Tests pour TennisMatchAdapter."""

    def setup_method(self):
        from pkg.adapter.generic_match_adapter import TennisMatchAdapter
        self.adapter = TennisMatchAdapter(
            col_id="match_num", col_date="tourney_date",
            col_vainqueur="vainqueur_id", col_perdant="loser_id"
        )
        self.row = {
            "match_num": "M001", "tourney_date": "20240115",
            "vainqueur_id": "101", "loser_id": "202",
            "minutes": 120, "w_ace": 10, "tourney_name": "Roland Garros", "round": "F"
        }

    def test_adapt_cree_match(self):
        from pkg.models.match import Match
        match = self.adapter.adapt(self.row)
        assert isinstance(match, Match)

    def test_adapt_score_tennis_fixe(self):
        match = self.adapter.adapt(self.row)
        assert match.score1 == 1
        assert match.score2 == 0

    def test_adapt_stats_tennis(self):
        match = self.adapter.adapt(self.row)
        assert match.stats["tourney_name"] == "Roland Garros"
        assert match.stats["round"] == "F"
        assert match.stats["w_ace"] == 10

    def test_to_row_reconstruit_dictionnaire(self):
        from pkg.models.match import Match
        match = Match("M001", "20240115", "101", "202", 1, 0, stats={"tourney_name": "RG"})
        row = self.adapter.to_row(match)
        assert row["match_num"] == "M001"
        assert row["vainqueur_id"] == "101"
        assert row["tourney_name"] == "RG"


# ==============================================================================
# TESTS — SERVICE STATISTIQUES
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
        # Warriors a 1 victoire, Lakers 1 victoire → tri par points_marques en cas d'égalité
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
        # Warriors : 3 pts (victoire), Lakers : 3 pts (victoire), Celtics : 0
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
        assert noms_diff["Lakers"] == 15   # 110 - 95
        assert noms_diff["Celtics"] == -15


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
        # fg3m=12, fg3a=35 → pct ≈ 34.3%
        assert moyennes["pct_3pts"] == round((12 / 35) * 100, 1)


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
        # w_bpFaced=7, w_bpSaved=5 → l_bpFaced=6, l_bpSaved=2
        # vainqueur bp_converties = l_bpFaced - l_bpSaved = 6 - 2 = 4
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
        self.j_tennis_esp = JoueurTennis(101, "Rafael", "Nadal", 185, "1986-06-03", "ESP", "L")
        self.j_tennis_sui = JoueurTennis(102, "Roger", "Federer", 185, "1981-08-08", "SUI", "R")
        self.j_tennis_esp2 = JoueurTennis(103, "Carlos", "Alcaraz", 183, "2003-05-05", "ESP", "R")
        self.j_basket = JoueurBasket(23, "LeBron", "James", 206, "1984-12-30", 1610612747, "23", "F", "250 lbs")

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
        assert j.poids == "113.4 kg"  # ne doit pas être reconverti

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
        assert len(pays) == 2  # pas de doublons

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
        assert "99.8" in resultat  # 220 * 0.453592 ≈ 99.8

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
# TESTS — DATA REPOSITORY
# ==============================================================================

class TestDataRepository:
    """Tests pour DataRepository."""

    def setup_method(self):
        from pkg.repository.data_repository import DataRepository
        from pkg.adapter.generic_match_adapter import GenericMatchAdapter
        self.adapter = GenericMatchAdapter(
            col_date="date", col_equipe1="eq1", col_equipe2="eq2",
            col_score1="s1", col_score2="s2"
        )

    def test_load_avec_csv_mock(self, tmp_path):
        from pkg.repository.data_repository import DataRepository
        csv_content = "date,eq1,eq2,s1,s2\n2024-01-01,Lakers,Celtics,110,95\n"
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        repo = DataRepository(str(csv_file), self.adapter, sep=",")
        matchs = repo.load()
        assert len(matchs) == 1
        assert matchs[0].equipe1 == "Lakers"
        assert matchs[0].score1 == 110

    def test_load_plusieurs_lignes(self, tmp_path):
        from pkg.repository.data_repository import DataRepository
        csv_content = "date,eq1,eq2,s1,s2\n2024-01-01,A,B,10,5\n2024-01-02,C,D,8,3\n"
        csv_file = tmp_path / "test2.csv"
        csv_file.write_text(csv_content)
        repo = DataRepository(str(csv_file), self.adapter, sep=",")
        matchs = repo.load()
        assert len(matchs) == 2

    def test_save_ecrit_csv(self, tmp_path):
        from pkg.repository.data_repository import DataRepository
        from pkg.models.match import Match
        csv_file = tmp_path / "output.csv"
        repo = DataRepository(str(csv_file), self.adapter, sep=",")
        match = Match(1, "2024-01-01", "Lakers", "Celtics", 110, 95)
        repo.save([match])
        contenu = csv_file.read_text()
        assert "Lakers" in contenu

    def test_separateur_personnalise(self, tmp_path):
        from pkg.repository.data_repository import DataRepository
        csv_content = "date;eq1;eq2;s1;s2\n2024-01-01;Lakers;Celtics;110;95\n"
        csv_file = tmp_path / "test_sep.csv"
        csv_file.write_text(csv_content)
        repo = DataRepository(str(csv_file), self.adapter, sep=";")
        matchs = repo.load()
        assert len(matchs) == 1


# ==============================================================================
# TESTS — DATASET CONFIGURATION
# ==============================================================================

class TestDatasetConfiguration:
    """Tests pour DatasetConfiguration."""

    def test_creation_configuration(self):
        from pkg.config.dataset_configuration import DatasetConfiguration
        adapter = MagicMock()
        config = DatasetConfiguration("chemin/fichier.csv", ",", adapter)
        assert config.dataset_path == "chemin/fichier.csv"
        assert config.dataset_sep == ","
        assert config.adapter == adapter

    def test_configurations_predefinies_existent(self):
        from pkg.config.dataset_configuration import (
            tennis_atp_match_config, tennis_wta_match_config,
            basket_match_config, basket_equipe_config, basket_joueur_config
        )
        assert tennis_atp_match_config.dataset_path is not None
        assert basket_match_config.dataset_sep == ","
        assert basket_equipe_config.adapter is not None

    def test_config_tennis_atp_joueur(self):
        from pkg.config.dataset_configuration import tennis_atp_joueur_config
        assert "atp" in tennis_atp_joueur_config.dataset_path.lower()

    def test_config_basket_match_colonnes(self):
        from pkg.config.dataset_configuration import basket_match_config
        adapter = basket_match_config.adapter
        assert adapter.col_date == "game_date"
        assert adapter.col_score1 == "pts_home"


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