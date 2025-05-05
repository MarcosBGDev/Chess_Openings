from src.api.Chesscom import Chesscom
from src.storage.MongoDBManager import MongoDBManager
from src.utils.Helpers import Helpers
import pandas as pd
import os
client = Chesscom()

helper = Helpers()

modalities = ["live_blitz", "live_bullet", "live_rapid"]
clean_modalities = ["blitz", "bullet", "rapid"]
n_top=6
players_data = client.get_all_top_players(modalities,n_top)
players_list = helper.extract_unique_usernames(players_data)
print(players_list)
start_year = 2023
end_year = 2024

database_name = "ChessDB_" + str(start_year) + "-" + str(end_year) + "Top_" + str(n_top)
db_manager = MongoDBManager(database_name)

for player in players_list:
    for year in range(start_year, end_year + 1):
        games = client.get_filtered_games(player, year, clean_modalities)
        print("Buscando partidas para jugador, ", player, " en el año ", year)
        for game in games:
            db_manager.insert_game("games", {
                "username_asociated": player,
                "white_player": game.get("white",{}).get("result"),
                "black_player": game.get("black", {}).get("result"),
                "end_time": game.get("end_time"),
                "pgn": game.get("pgn")
            })



