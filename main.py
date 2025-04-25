from src.api.Leaderboards import Leaderboards
from src.api.Games import Games
import time
import pandas as pd
import os

leaderboard_client= Leaderboards()

modalities = leaderboard_client.get_modalities_leaderboards() #Obtiene los diferentes modos de juego

chosen_modality = leaderboard_client.choose_modality(modalities) #Devuelve la posición de la modalidad elegida

time.sleep(1) #Pequeña pausa para que no falle la API

players_list = leaderboard_client.get_players_leaderboards(modalities[chosen_modality])

print("Jugadores de la categoría ", modalities[chosen_modality], ":\n ",players_list)

games_client = Games()

months = games_client.get_months() #Devuelve la sucesuón de los meses en formato String ("01","02",...)

clean_modalities = leaderboard_client.fix_modalities(modalities) #Estandariza los nombres de los modos de juego

year="2024"
csv_name = "Partidas_" + clean_modalities[chosen_modality]+"_"+year+".csv"

if not os.path.exists(csv_name):
    #Crear el archivo CSV
    df = pd.DataFrame(columns=["Jugador", "Fecha", "Modalidad", "Resultado Blancas", "Resultado Negras", "Apertura"])
    df.to_csv(csv_name, index=False)

for player in range(len(players_list)):
    print("Buscando partidas del jugador ", players_list[player])
    for month in months:
        games_client.get_games_games(players_list[player], month, year, clean_modalities[chosen_modality])