from src.etl.CleanConfig import CleanConfig
from src.etl.FetchData import FetchData
from src.etl.CleanData import CleanData
from src.utils.Helpers import Helpers
from src.utils.ParameterValidator import ParameterValidator

fetchDataClient = FetchData()
helper = Helpers()

modalities = ["live_blitz", "live_bullet", "live_rapid"]
clean_modalities = ["blitz", "bullet", "rapid"]

"""
n_top=2
start_year = 2023
end_year = 2024
"""

n_top, start_year, end_year = ParameterValidator.ask_parameters()


players_data = fetchDataClient.get_all_top_players(modalities,n_top)
fetchDataClient.store_players_data(players_data,start_year, end_year, n_top)
players_list = helper.extract_unique_usernames(players_data)
fetchDataClient.fetch_and_store_games(start_year, end_year, n_top)
config = CleanConfig(start_year, end_year, n_top, clean_modalities, "white")
clean_data = CleanData(config)
clean_data.clean()


