import requests

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

