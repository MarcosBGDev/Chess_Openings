from datetime import datetime
from src.storage.MongoDBManager import MongoDBManager
import re

class CleanData:
    def __init__(self):
        print("Limpiando datos...")

    def clean(self):
        print("Datos limpios")

    def limpiar_apertura(self, apertura):
        #Eliminar la parte de las aperturas que varía
        apertura_base = apertura.split("...")[0]
        apertura_base = re.split(r"\d+\.", apertura_base)[0].rstrip("-")
        if "-with" in apertura_base:
            apertura_base = "-".join(apertura_base.split("-with")[:-1])
        apertura_base = re.sub(r"-\d+$", "", apertura_base)
        return apertura_base

    @staticmethod
    def clean_time_format(game):
        # Convierte el campo end_time de una partida a una fecha
        timestamp = game.get("end_time")
        if isinstance(timestamp, int):
            game["end_date"] = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            game["end_date"] = "Unknown"
        return game

    @staticmethod
    def filter_by_color(games, username, color="white"):
        for game in games:
            player_info = game.get(color, {})
            if player_info.get("username", "").lower() == username.lower():
                yield game