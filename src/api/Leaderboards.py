import requests


class Leaderboards:
    BASE_URL = "https://api.chess.com/pub/leaderboards"
    def __init__(self):
        self.headers = {
            #Permite simular una aplicación legítima para mandar una solicitud a la API
            #Si no se añade esta línea en cada petición, devuelve el codigo de error 403
            "User-Agent": "MiAplicacionPython/1.0 (correo@example.com)"
        }
        self.data = None

    def get_modalities_leaderboards(self):
        #Devuelve las modalidades del endpoint "Leaderboards" de chess.com
        response = requests.get(self.BASE_URL, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            modalidades = list(data.keys())
            return modalidades
        else:
            print(f"Error obteniendo modalidades: {response.status_code}")
            return []
        
    @staticmethod
    def fix_modalities(modalities):
        #Quitar el "live_" inicial de una modalidad
        fixed_modalities = []
        for modality in modalities:
            if modality.startswith("live_"):
                fixed_modalities.append(modality[5:])
            else:
                fixed_modalities.append(modality)
        return fixed_modalities 
       
    def get_players_leaderboards(self, modality): 
        #Obtener los jugadores de una modalidad
        response = requests.get(self.BASE_URL, headers=self.headers)
        if response.status_code == 200:
            top_players = [player['username'] for player in response.json()[modality][:5]] #Guarda en una lista los 5 mejores jugadores de esa modalidad
            return top_players
        else:
            print(f"Error en la petición: {response.status_code} - {response.text}")
            return None
    
    @staticmethod
    def choose_modality(modalidades):
        #Muestra el menú de modalidades disponibles para que el usuario elija una
        while True:
            print("\nElige una modalidad introduciendo el número correspondiente:")
            for i, modalidad in enumerate(modalidades, start=1):
                print(f"{i}. {modalidad}")

            opcion = input("Introduce el número de la modalidad: ")

            if opcion.isdigit():
                opcion = int(opcion)
                if 1 <= opcion <= len(modalidades):
                    print(f"Has elegido la modalidad: {modalidades[opcion - 1]}")
                    return opcion - 1
                else:
                    print("Número fuera de rango. Inténtalo de nuevo.")
            else:
                print("Entrada inválida. Introduce un número.")


