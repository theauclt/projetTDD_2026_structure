"""
Tests unitaires — MODÈLES
Vérifie que les classes (Joueur, Match, Equipe, StatistiqueJoueur)
s'instancient correctement et que leurs méthodes de base fonctionnent.
"""

import pytest
from unittest.mock import MagicMock


# ==============================================================================
# TESTS — JOUEUR
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


# ==============================================================================
# TESTS — EQUIPE
# ==============================================================================

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
        self.equipe.ajouter_joueur(j)
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
        j2 = JoueurBasket(2, "C", "D", 0, "1991-01-01", 1, "2", "F", "220")
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


# ==============================================================================
# TESTS — MATCH
# ==============================================================================

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