from pkg.adapter.generic_equipe_adapter import GenericEquipeAdapter
from pkg.adapter.generic_match_adapter import GenericMatchAdapter, TennisMatchAdapter
from pkg.adapter.generic_joueur_adapter import TennisJoueurAdapter, BasketJoueurAdapter


class DatasetConfiguration:
    def __init__(self, dataset_path, dataset_sep, adapter):
        self.dataset_path = dataset_path
        self.dataset_sep = dataset_sep
        self.adapter = adapter


# 1. TENNIS (ATP & WTA)
tennis_atp_match_config = DatasetConfiguration(
    dataset_path="Données/Tennis/atp_matches_2024.csv", # (Assure-toi que le chemin est bon)
    dataset_sep=",",
    adapter=TennisMatchAdapter(
        col_id="match_num",
        col_date="tourney_date",
        col_vainqueur="vainqueur_id", # Parfait, ça correspond à ton CSV !
        col_perdant="loser_id"
    )
)
tennis_wta_match_config = DatasetConfiguration(
    dataset_path="Données/Tennis/wta_matches_2024.csv", 
    dataset_sep=",",
    adapter=TennisMatchAdapter(
        col_id="match_num",
        col_date="tourney_date",
        col_vainqueur="vainqueur_id", # Parfait, ça correspond à ton CSV !
        col_perdant="loser_id"
    )
)

tennis_wta_joueur_config = DatasetConfiguration(
    dataset_path="Données/Tennis/wta_players_2024.csv", 
    dataset_sep=",",
    adapter=TennisJoueurAdapter(
        col_id="player_id", 
        col_prenom="name_first", 
        col_nom="name_last", 
        col_taille="height", 
        col_date_naissance="dob",
        col_pays="ioc", 
        col_main="hand")
)

tennis_atp_joueur_config = DatasetConfiguration(
    dataset_path="Données/Tennis/atp_players_2024.csv", 
    dataset_sep=",",
    adapter=TennisJoueurAdapter(
        col_id="player_id", 
        col_prenom="name_first", 
        col_nom="name_last", 
        col_taille="height", 
        col_date_naissance="dob",
        col_pays="ioc", 
        col_main="hand"
    )
)

# 2. BASKET
basket_match_config = DatasetConfiguration(
    dataset_path="Données/Basket/game.csv",
    dataset_sep=",",
    adapter=GenericMatchAdapter(
        col_date="game_date", 
        col_equipe1="team_id_home",
        col_equipe2="team_id_away", 
        col_score1="pts_home", 
        col_score2="pts_away",
        col_type_match="season_type")
)

basket_equipe_config = DatasetConfiguration(
    dataset_path="Données/Basket/team.csv",
    dataset_sep=",",
    adapter=GenericEquipeAdapter(
        col_id="id",
        col_nom="full_name",
        col_abbr="abbreviation", 
        col_loc="city", 
        col_reg="state"
    )
)

basket_joueur_config = DatasetConfiguration(
    dataset_path="Données/Basket/player.csv",
    dataset_sep=",",
    adapter=BasketJoueurAdapter(
        col_id="person_id",
        col_prenom="first_name",
        col_nom="last_name",
        col_taille="height",
        col_date_naissance="birthdate",
        col_equipe="team_id",
        col_numero="jersey",
        col_position="position",
        col_poids="weight"
    )
)