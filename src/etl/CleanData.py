from datetime import datetime, timezone
from src.storage.MongoDBManager import MongoDBManager
from src.etl.CleanConfig import CleanConfig
import re

from src.storage.QueryBuilder import QueryBuilder

class CleanData:
    RESULT_NORMALIZATION = {
        "win": "win",
        "checkmated": "loss",
        "timeout": "loss",
        "resigned": "loss",
        "agreed": "draw",
        "stalemate": "draw",
        "insufficient": "draw",
        "50move": "draw",
        "timevsinsufficient": "draw",
        "repetition": "draw",
    }
    def __init__(self, config: CleanConfig):
        self.config = config
        self.query_builder = QueryBuilder()

    def clean(self):
        db_name = f"ChessDB_{self.config.start_year}-{self.config.end_year}_Top_{self.config.n_top}"
        db_manager = MongoDBManager(db_name)

        filtered_games = self.get_filtered_games(db_manager)

        for game in filtered_games:
            cleaned_game = self.build_cleaned_game(game)
            db_manager.insert_game("clean_games", cleaned_game)

        db_manager.close_connection()

    @staticmethod
    def get_time_from_timestamp(timestamp):
        if isinstance(timestamp, int):
            return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%H:%M:%S')
        return "Unknown"

    @staticmethod
    def get_date_from_timestamp(timestamp):
        if isinstance(timestamp, int):
            return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d')
        return "Unknown"

    @staticmethod
    def extract_opening_from_pgn(pgn: str) -> str:
        if not pgn or not isinstance(pgn, str):
            return "Unknown"
        if "[ECOUrl \"" in pgn:
            try:
                start = pgn.index("[ECOUrl \"") + len("[ECOUrl \"")
                end = pgn.index("\"]", start)
                url = pgn[start:end]
                parts = url.split("/")
                if parts:
                    raw_name = parts[-1]
                    name = raw_name.replace("-", " ")
                    name = re.split(r"\s\d+.*", name)[0].strip()  # Eliminar el texto después del primer número
                    name = re.sub(r"\swith.*$", "", name).strip()  # Eliminar cualquier cosa después de "with"
                    return name
            except ValueError:
                pass
        return "Unknown"

    @staticmethod
    def extract_start_time_from_pgn(pgn: str) -> str:
        # Extrae el StartTime de un string PGN
        if not isinstance(pgn, str):
            return "Unknown"

        match = re.search(r'\[StartTime\s+"(\d{2}:\d{2}:\d{2})"]', pgn)
        if match:
            return match.group(1)

        return "Unknown"

    @staticmethod
    def normalize_result(result: str) -> str:
        return CleanData.RESULT_NORMALIZATION.get(result.lower(), "unknown")

    def get_filtered_games(self, db_manager):
        query = {}
        query.update(self.query_builder.filter_by_modality(self.config.modalities))
        query.update(self.query_builder.filter_white_games())
        return db_manager.get_all_documents("raw_games", query)

    def build_cleaned_game(self, game):
        return {
            "associated_username": game.get("associated_username"),
            "time_class": game.get("time_class"),
            "time_control": game.get("time_control"),
            "rules": game.get("rules"),
            "white_username": game.get("white_username", {}),
            "white_result": self.normalize_result(game.get("white_result")),
            "black_username": game.get("black_username"),
            "black_result": self.normalize_result(game.get("black_result")),
            "start_time": self.extract_start_time_from_pgn(game.get("pgn", "")),
            "end_date": self.get_date_from_timestamp(game.get("end_time")),
            "end_time": self.get_time_from_timestamp(game.get("end_time")),
            "opening_name": self.extract_opening_from_pgn(game.get("pgn", ""))
        }