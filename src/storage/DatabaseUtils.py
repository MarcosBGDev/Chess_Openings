import re
import pandas as pd
from src import MongoDBManager


class DatabaseUtils:
    pass


    @staticmethod
    def get_database_names(prefix="ChessDB"):
        db_manager = MongoDBManager()
        dbs = db_manager.list_available_dbs(prefix)
        db_manager.close_connection()
        return dbs

    @staticmethod
    def get_years_from_db_name(db_name):
        match = re.search(r'ChessDB_(\d{4})-(\d{4})', db_name)
        if match:
            start_year = match.group(1)
            end_year = match.group(2)
            return start_year, end_year
        else:
            return None, None


    def get_available_modalities(self,db_name: str) -> list[str]:
        client = MongoDBManager(db_name)
        collection = client.db["players"]
        modalities = collection.distinct("modality")
        clean_modalities = self.fix_modalities(modalities)
        return sorted(clean_modalities)

    @staticmethod
    def get_dataframe_from_collection(db_name, collection_name):
        manager = MongoDBManager(db_name)
        docs = list(manager.get_all_documents(collection_name, {}))
        df = pd.DataFrame(docs)
        columns_to_keep = ["opening_name", "white_result", "end_date", "time_class", "associated_username"]  # ajusta si usas otros nombres
        df = df[columns_to_keep]
        return df


    @staticmethod
    def fix_modalities(modalities):
        # Quitar el "live_" inicial de una modalidad
        fixed_modalities = []
        for modality in modalities:
            if modality.startswith("live_"):
                fixed_modalities.append(modality[5:])
            else:
                fixed_modalities.append(modality)
        return fixed_modalities