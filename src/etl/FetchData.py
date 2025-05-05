class ChessDownloader:
    def __init__(self, modalities_list):
        print("Descargando partidas...")

    def download_raw_games(self, games, username):
        partidas_blancas = []
        for game in games:
            # Filtramos aquellas partidas donde el jugador indicado juega con blancas
            if game.get("time_class") != modality:
                continue
            jugador_blancas = game.get("white", {}).get("username", "").lower()
            if jugador_blancas == username.lower():
                partidas_blancas.append(game)
