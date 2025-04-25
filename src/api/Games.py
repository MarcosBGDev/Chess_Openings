import requests
from datetime import datetime, timezone
import pandas as pd
import re
class Games:
    def __init__(self): 
        self.headers = {
            "User-Agent": "MiAplicacionPython/1.0 (correo@example.com)" #
        }
        self.data = None
        
    def get_months(self):
        #Devuelve los meses en formato de dos dígitos
        months=["01","02","03","04","05","06","07","08","09","10","11","12"]
        return months
    
    def limpiar_apertura(self, apertura):
        #Eliminar la parte de las aperturas que varía
        apertura_base = apertura.split("...")[0]
        apertura_base = re.split(r"\d+\.", apertura_base)[0].rstrip("-")
        if "-with" in apertura_base:
            apertura_base = "-".join(apertura_base.split("-with")[:-1])
        apertura_base = re.sub(r"-\d+$", "", apertura_base)
        return apertura_base
    
    def get_games_games(self, username,month, year, modality):
        #Devuelve las partidas de una modalidad de un jugador en un mes y año concretos
        url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            partidas = response.json().get("games", [])
            
            partidas_blancas = []
            
            csv_name="Partidas_" + modality+"_"+year+".csv"
            with open(csv_name, mode="a", newline='', encoding="utf-8") as f: #Abrimos el archivo CSV
                
                for partida in partidas:
                    #Filtramos aquellas partidas donde el jugador indicado juega con blancas
                    if partida.get("time_class") != modality:
                        continue
                    jugador_blancas = partida.get("white", {}).get("username", "").lower()
                    if jugador_blancas == username.lower():
                        partidas_blancas.append(partida)

                if partidas_blancas:
                    for partida in partidas_blancas:
                        fecha_partida = datetime.fromtimestamp(partida['end_time'], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                        resultado_blancas = partida.get("white", {}).get("result", "Desconocido")
                        resultado_negras = partida.get("black", {}).get("result", "Desconocido")
                        apertura = partida.get("eco", "Desconocido").split("/")[-1]
                        
                        apertura_base = self.limpiar_apertura(apertura)
                        
                        df_partida = pd.DataFrame([[username, fecha_partida, modality, resultado_blancas, resultado_negras, apertura_base]],
                                    columns=["Jugador", "Fecha","Modalidad", "Resultado Blancas", "Resultado Negras", "Apertura"])
                        df_partida.to_csv(f, index=False, header=False)
                else:
                    print(f"No se encontraron partidas '{modality}' con blancas para {username} en {year}/{month}.")
        else:
            print(f"Error al obtener las partidas. Código de estado: {response.status_code}")
        