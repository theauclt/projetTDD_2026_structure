from pkg.adapter.generic_equipe_adapter import GenericEquipeAdapter
from pkg.adapter.generic_entraineur_adapter import GenericEntraineurAdapter
from pkg.adapter.generic_match_adapter import GenericMatchAdapter
from pkg.adapter.generic_joueur_adapter import GenericJoueurAdapter

class DatasetConfiguration:
    def __init__(self, dataset_path, dataset_sep, adapter):
        self.dataset_path = dataset_path
        self.dataset_sep = dataset_sep
        self.adapter = adapter


# 1. TENNIS (ATP & WTA)
tennis_atp_match_config = DatasetConfiguration(
    dataset_path="data/atp_matches_2024.csv", 
    dataset_sep=",",
    adapter=GenericMatchAdapter(
        col_date="tourney_date", 
        col_equipe1="winner_id", 
        col_equipe2="loser_id", 
        col_score1="w_1stWon", 
        col_score2="l_1stWon")
)
tennis_atp_joueur_config = DatasetConfiguration(
    dataset_path="data/atp_players_2024.csv", 
    dataset_sep=",",
    adapter=GenericJoueurAdapter(
        col_nom="name_last", 
        col_pays="ioc", 
        col_taille="height", 
        col_date_naissance="dob")
)
tennis_wta_match_config = DatasetConfiguration(
    dataset_path="data/wta_matches_2024.csv", 
    dataset_sep=",",
    adapter=GenericMatchAdapter(
        col_date="tourney_date", 
        col_equipe1="winner_id", 
        col_equipe2="loser_id", 
        col_score1="w_1stWon", 
        col_score2="l_1stWon")
)
tennis_wta_joueur_config = DatasetConfiguration(
    dataset_path="data/wta_players_2024.csv", 
    dataset_sep=",",
    adapter=GenericJoueurAdapter(
        col_nom="name_last", 
        col_pays="ioc", 
        col_taille="height", 
        col_date_naissance="dob")
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
        col_score2="pts_away")
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


"""
# 1. VOLLEYBALL
volley_match_men_config = DatasetConfiguration(
    dataset_path="data/volleyball/match_men.csv", dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="date", col_equipe1="code_country_1", col_equipe2="code_country_2", col_score1="set_country_1", col_score2="set_country_2")
)
volley_joueur_men_config = DatasetConfiguration(
    dataset_path="data/volleyball/player_men.csv", dataset_sep=",",
    adapter=GenericJoueurAdapter(col_nom="name", col_pays="code_country", col_taille="height", col_date_naissance="birth_date")
)

# 2. FOOTBALL
football_match_v1_config = DatasetConfiguration(
    dataset_path="data/match.csv", dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="date", col_equipe1="team_home", col_equipe2="team_away", col_score1="score_team_home", col_score2="score_team_away")
)
football_match_v2_config = DatasetConfiguration(
    dataset_path="data/match.csv", dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="date", col_equipe1="home_team_api_id", col_equipe2="away_team_api_id", col_score1="home_team_goal", col_score2="away_team_goal")
)
football_joueur_config = DatasetConfiguration(
    dataset_path="data/joueur.csv", dataset_sep=",",
    adapter=GenericJoueurAdapter(col_nom="player_name", col_pays="club") 
)

equipe_football_config = DatasetConfiguration(
    dataset_path="data/equipe.csv", dataset_sep=",",
    adapter=GenericEquipeAdapter(col_id="id", col_nom="full_name", col_abbr="short_name", col_loc="city")
)

# 5. BADMINTON
badminton_match_config = DatasetConfiguration(
    dataset_path="Données/Badminton/matchs.csv",
    dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="date", col_equipe1="joueur_1", col_equipe2="joueur_2", col_score1="score_1", col_score2="score_2")
)

# --- CONFIGURATIONS COACHS ---
entraineur_men_config = DatasetConfiguration(
    dataset_path="data/entraineur (1).csv", dataset_sep=",",
    adapter=GenericEntraineurAdapter(col_nom="nom", col_pseudo="pseudo", col_pays="nationality", col_equipe="equipe")
)
"""