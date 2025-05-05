from src.api.Chesscom import Chesscom
from src.utils.Helpers import Helpers
from src.storage.MongoDBManager import MongoDBManager

import re

class FetchData:
    chesscom_client = Chesscom()
    helper = Helpers()
    def __init__(self):
        print("Descargando partidas...")

    #||||||||||||||||Obtener jugadores|||||||||||||||||||||||||||

    def extract_top_players(self, leaderboard_data, modality, top_n=5):
        # Devuelve una lista de  datos de jugadores (username, score, etc.) de una modalidad concreta.
        if modality not in leaderboard_data:
            print(f"Modalidad '{modality}' no encontrada en el leaderboard.")
            return []
        players = []
        for player in leaderboard_data[modality][:top_n]:
            entry = self.build_player_entry(player, modality)
            players.append(entry)

        return players

    @staticmethod
    def build_player_entry(player, modality):
        # Construye un diccionario con la información de un jugador.
        return {
            "username": player.get("username"),
            "modality": modality,
            "score": player.get("score"),  # o "rating"
            "country": player.get("country"),
        }

    def get_all_top_players(self, modalities, top_n=5):
        # Obtiene el JSON de la petición al endpoint y devuelve una lista de datos de jugadores
        leaderboard_data = self.chesscom_client.send_leaderboards_request()
        if not leaderboard_data:
            return []

        top_players = []
        for modality in modalities:
            players = self.extract_top_players(leaderboard_data, modality, top_n)
            top_players.extend(players)
        return top_players

    #||||||||||||||||||||||||||||||||||||||||||||||||

    #||||||||||||||||Obtener partidas||||||||||||||||||||||||||

    def get_filtered_games(self, username, year, modalities):
        month_list = self.helper.get_months()
        year = str(year)
        for month in month_list:
            games = self.chesscom_client.send_games_request(username, month, year)
            for game in games:
                if game.get("time_class") in modalities and game.get("white", {}).get("username","").lower() == username.lower():
                    yield game

    def fetch_and_store_games(self, players_list, start_year, end_year, modalities, n_top):
        db_name = f"ChessDB_{start_year}-{end_year}_Top_{n_top}"
        db_manager = MongoDBManager(db_name)

        for player in players_list:
            for year in range(start_year, end_year + 1):
                print(f"Buscando partidas para jugador {player} en el año {year}")
                games = self.get_filtered_games(player, year, modalities)
                for game in games:
                    db_manager.insert_game("games", {
                        "username_asociated": player,
                        "white_player": game.get("white", {}).get("result"),
                        "black_player": game.get("black", {}).get("result"),
                        "end_time": game.get("end_time"),
                        "pgn": game.get("pgn")
                    })
        db_manager.close_connection()