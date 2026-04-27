from pkg.adapter.generic_team_adapter import GenericTeamAdapter
from pkg.adapter.generic_coach_adapter import GenericCoachAdapter
from pkg.adapter.generic_match_adapter import GenericMatchAdapter
from pkg.adapter.generic_player_adapter import GenericPlayerAdapter

class DatasetConfiguration:
    def __init__(self, dataset_path, dataset_sep, adapter):
        self.dataset_path = dataset_path
        self.dataset_sep = dataset_sep
        self.adapter = adapter

# 1. VOLLEYBALL
volley_match_men_config = DatasetConfiguration(
    dataset_path="data/volleyball/match_men.csv", dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="date", col_team1="country_code_1", col_team2="country_code_2", col_score1="set_country_1", col_score2="set_country_2")
)
volley_player_men_config = DatasetConfiguration(
    dataset_path="data/volleyball/player_men.csv", dataset_sep=",",
    adapter=GenericPlayerAdapter(col_name="name", col_country="country_code", col_height="height", col_birthdate="birth_date")
)

# 2. FOOTBALL
football_match_v1_config = DatasetConfiguration(
    dataset_path="data/match.csv", dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="date", col_team1="team_home", col_team2="team_away", col_score1="score_team_home", col_score2="score_team_away")
)
football_match_v2_config = DatasetConfiguration(
    dataset_path="data/match.csv", dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="date", col_team1="home_team_api_id", col_team2="away_team_api_id", col_score1="home_team_goal", col_score2="away_team_goal")
)
football_player_config = DatasetConfiguration(
    dataset_path="data/player.csv", dataset_sep=",",
    adapter=GenericPlayerAdapter(col_name="player_name", col_country="club") 
)

team_football_config = DatasetConfiguration(
    dataset_path="data/team.csv", dataset_sep=",",
    adapter=GenericTeamAdapter(col_id="id", col_name="full_name", col_abbr="short_name", col_loc="city")
)

# 3. TENNIS (ATP & WTA)
tennis_atp_match_config = DatasetConfiguration(
    dataset_path="data/atp_matches_2024.csv", dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="tourney_date", col_team1="vainqueur_id", col_team2="loser_id", col_score1="w_1stWon", col_score2="l_1stWon")
)
tennis_atp_player_config = DatasetConfiguration(
    dataset_path="data/atp_players_2024.csv", dataset_sep=",",
    adapter=GenericPlayerAdapter(col_name="name_last", col_country="ioc", col_height="height", col_birthdate="dob")
)
tennis_wta_match_config = DatasetConfiguration(
    dataset_path="data/wta_matches_2024.csv", dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="tourney_date", col_team1="vainqueur_id", col_team2="loser_id", col_score1="w_1stWon", col_score2="l_1stWon")
)
tennis_wta_player_config = DatasetConfiguration(
    dataset_path="data/wta_players_2024.csv", dataset_sep=",",
    adapter=GenericPlayerAdapter(col_name="name_last", col_country="ioc", col_height="height", col_birthdate="dob")
)



# 4. BASKET
basket_match_config = DatasetConfiguration(
    dataset_path="Données/Basket/game.csv",
    dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="game_date", col_team1 ="team_id_home",col_team2="team_id_away", col_score1="pts_home", col_score2="pts_away")
)

basket_team_config = DatasetConfiguration(
    dataset_path="Données/Basket/team.csv",
    dataset_sep=",",
    adapter=GenericTeamAdapter(
        col_id="id",
        col_name="full_name",
        col_abbr="abbreviation", 
        col_loc="city", 
        col_reg="state"
    )
)
# 5. BADMINTON
badminton_match_config = DatasetConfiguration(
    dataset_path="Données/Badminton/matchs.csv",
    dataset_sep=",",
    adapter=GenericMatchAdapter(col_date="date", col_team1="player_1", col_team2="player_2", col_score1="score_1", col_score2="score_2")
)

# --- CONFIGURATIONS COACHS ---
coach_men_config = DatasetConfiguration(
    dataset_path="data/coach (1).csv", dataset_sep=",",
    adapter=GenericCoachAdapter(col_name="name", col_pseudo="pseudo", col_country="nationality", col_team="team")
)