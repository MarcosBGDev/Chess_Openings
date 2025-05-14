from src.api.Chesscom import Chesscom
from src.utils.Helpers import Helpers
from src.storage.MongoDBManager import MongoDBManager

class FetchData:
    chesscom_client = Chesscom()
    helper = Helpers()

    #||||||||||||||||Obtener jugadores de la API|||||||||||||||||||||||||||

    def extract_top_players_data(self, leaderboard_data, modality, top_n):
        """ Devuelve una lista de datos de jugadores (username, score, etc.) de una modalidad concreta. """
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
        """ Construye un diccionario con la información de un jugador. """
        return {
            "username": player.get("username"),
            "modality": modality,
            "score": player.get("score"),  # o "rating"
            "country": player.get("country"),
        }

    def get_all_top_players(self, modalities, top_n):
        """ Obtiene una lista de datos de jugadores """
        leaderboard_data = self.chesscom_client.send_leaderboards_request()
        if not leaderboard_data:
            return []

        top_players = []
        for modality in modalities:
            players = self.extract_top_players_data(leaderboard_data, modality, top_n)
            top_players.extend(players)
        return top_players

    #||||||||||||||||||||||||||||||||||||||||||||||||

    #||||||||||||||||Obtener partidas de la API||||||||||||||||||||||||||

    def get_all_games(self, player, year):
        """
        Devuelve una lista de partidas jugadas por un jugador durante un año.
        Hace uso de un generador (yield) para no cargar todas las partidas en memoria.
        """
        month_list = self.helper.get_months()
        year = str(year)
        for month in month_list:
            games = self.chesscom_client.send_games_request(player, month, year)
            for game in games:
                yield game

    def fetch_and_store_games(self, players_list, start_year, end_year, n_top):
        """
        Recopila y guarda todas las partidas de todos los jugadores en un periodo de tiempo
        """
        db_name = f"ChessDB_{start_year}-{end_year}_Top_{n_top}"
        db_manager = MongoDBManager(db_name)

        for player in players_list:
            self.process_player_games(player, start_year, end_year, db_manager)

        db_manager.close_connection()

    def process_player_games(self, player, start_year, end_year, db_manager):
        """
        Comprueba que las partidas de un jugador son válidas y las guarda.
        """
        for year in range(start_year, end_year + 1):
            print(f"Buscando partidas para jugador {player} en el año {year}")
            games = self.get_all_games(player, year)
            for game in games:
                if self.is_valid_game(game):
                    new_game = self.prepare_game_for_insert(game, player)
                    db_manager.insert_game("raw_games", new_game)

    @staticmethod
    def is_valid_game(game):
        """
        Comprueba si una partida contiene el campo "PNG" necesario para el análisis
        """
        pgn = game.get("pgn")
        return isinstance(pgn, str) and pgn.strip()

    @staticmethod
    def prepare_game_for_insert(game, player):
        return {
            "associated_username": player,
            "time_class": game.get("time_class"),
            "time_control": game.get("time_control"),
            "rules": game.get("rules"),
            "white_result": game.get("white", {}).get("result"),
            "white_username": game.get("white", {}).get("username"),
            "black_result": game.get("black", {}).get("result"),
            "black_username": game.get("black", {}).get("username"),
            "end_time": game.get("end_time"),
            "pgn": FetchData.strip_pgn_moves(game.get("pgn"))
        }

    @staticmethod
    def strip_pgn_moves(pgn: str) -> str:
        """
        Recorta la parte innecesaria del campo "PGN" de una partida.
        """
        if isinstance(pgn, str):
            return pgn.split("\n\n")[0]
        return ""