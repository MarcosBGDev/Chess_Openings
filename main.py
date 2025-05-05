from src.etl.FetchData import FetchData
from src.utils.Helpers import Helpers
import pandas as pd
import os
fetchDataClient = FetchData()

helper = Helpers()

modalities = ["live_blitz", "live_bullet", "live_rapid"]
clean_modalities = ["blitz", "bullet", "rapid"]

n_top=6
players_data = fetchDataClient.get_all_top_players(modalities,n_top)
players_list = helper.extract_unique_usernames(players_data)
print(players_list)
start_year = 2023
end_year = 2024

fetchDataClient.fetch_and_store_games(players_list, start_year, end_year, clean_modalities, n_top)





