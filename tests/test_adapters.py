"""
Tests unitaires — ADAPTERS & REPOSITORY
Vérifie que les adaptateurs transforment bien les données CSV en objets,
gèrent les valeurs manquantes, et que le DataRepository lit/écrit correctement.
"""

import pytest
from unittest.mock import MagicMock


# ==============================================================================
# TESTS — GENERIC EQUIPE ADAPTER
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
        assert equipe.abreviation == "Boston Celtics"
        assert equipe.lieu is None
        assert equipe.region is None

    def test_to_row_retourne_none(self):
        result = self.adapter.to_row(MagicMock())
        assert result is None


# ==============================================================================
# TESTS — BASKET JOUEUR ADAPTER
# ==============================================================================

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


# ==============================================================================
# TESTS — TENNIS JOUEUR ADAPTER
# ==============================================================================

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


# ==============================================================================
# TESTS — GENERIC MATCH ADAPTER
# ==============================================================================

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


# ==============================================================================
# TESTS — TENNIS MATCH ADAPTER
# ==============================================================================

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
# TESTS — DATA REPOSITORY
# ==============================================================================

class TestDataRepository:
    """Tests pour DataRepository."""

    def setup_method(self):
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
