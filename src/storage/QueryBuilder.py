from datetime import datetime

class QueryBuilder:
    @staticmethod
    def filter_by_modality(modalities):
        return {"time_class": {"$in": modalities}}

    @staticmethod
    def filter_white_games():
        # Compara que el jugador asociado sea el que juega con blancas
        return {"$expr": {"$eq": ["$associated_username", "$white_username"]}}

    @staticmethod
    def filter_by_year_range(start_year, end_year):
        return {
            "end_time": {
                "$gte": int(datetime(start_year, 1, 1).timestamp()),
                "$lte": int(datetime(end_year, 12, 31).timestamp())
            }
        }