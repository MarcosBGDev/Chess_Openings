import requests
from datetime import datetime, timezone
import pandas as pd
from src.utils.Helpers import Helpers
helper = Helpers()
class Chesscom:
    URL_LEADERBOARDS = "https://api.chess.com/pub/leaderboards"
    def __init__(self):
        self.headers = {
            # Simular una aplicación legítima para mandar solicitudes
            "User-Agent": "MiAplicacionPython/1.0 (correo@example.com)"
        }
        self.data = None

    def send_leaderboards_request(self):
        #Mandar solicitud al endpoint de "Leaderboards"
        response = requests.get(self.URL_LEADERBOARDS, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en la petición: {response.status_code} - {response.text}")
            return None

    def extract_top_players(self, leaderboard_data, modality, top_n=5):
        # Extrae una lista de  datos de jugadores (username, score, etc.) para una modalidad concreta.
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
        leaderboard_data = self.send_leaderboards_request()
        if not leaderboard_data:
            return []

        top_players = []
        for modality in modalities:
            players = self.extract_top_players(leaderboard_data, modality, top_n)
            top_players.extend(players)
        return top_players

    def send_games_request(self, username, month, year):
        # Envía la petición a la API para devolver las partidas de un jugador
        url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            games = response.json().get("games", [])
            return games
        else:
            print(f"Error al obtener las partidas. Código de estado: {response.status_code}")
            return []

    def get_filtered_games(self, username, year, modalities):
        month_list = helper.get_months()
        year = str(year)
        for month in month_list:
            games = self.send_games_request(username, month, year)
            for game in games:
                if game.get("time_class") in modalities and game.get("white", {}).get("username","").lower() == username.lower():
                    yield game

