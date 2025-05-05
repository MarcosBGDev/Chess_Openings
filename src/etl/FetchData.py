from src.api.Chesscom import Chesscom
import re

class FetchData:

    def __init__(self):
        print("Descargando partidas...")

    def filter_raw_white_games(self, games, username):
        white_games = []
        for game in games:
            # Filtramos aquellas partidas donde el jugador indicado juega con blancas
            if game.get("time_class") not in self.modalities_list:
                continue
            white_player = game.get("white", {}).get("username", "").lower()
            if white_player == username.lower():
                white_games.append(game)
        return white_games

    @staticmethod
    def clean_opening(opening):
        #Eliminar la parte de las aperturas que varía
        apertura_base = opening.split("...")[0]
        apertura_base = re.split(r"\d+\.", apertura_base)[0].rstrip("-")
        if "-with" in apertura_base:
            apertura_base = "-".join(apertura_base.split("-with")[:-1])
        apertura_base = re.sub(r"-\d+$", "", apertura_base)
        return apertura_base