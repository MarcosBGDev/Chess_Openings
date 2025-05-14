import src.etl.CleanConfig
from src.etl.CleanData import CleanData
from src.etl.CleanConfig import CleanConfig
class Processor:
    def __init__(self, modalities, clean_modalities, fetch_client, helper):
        self.modalities = modalities
        self.clean_modalities = clean_modalities
        self.fetch_client = fetch_client
        self.helper = helper

    def run(self, n_top, start_year, end_year):
        players_data = self.fetch_client.get_all_top_players(self.modalities, n_top)
        players_list = self.helper.extract_unique_usernames(players_data)

        print(players_data)
        print(players_list)

        self.fetch_client.fetch_and_store_games(players_list, start_year, end_year, n_top)

        config = CleanConfig(start_year, end_year, n_top, self.clean_modalities, "white")
        clean_data = CleanData(config)
        clean_data.clean()