from pymongo import MongoClient

class MongoDBManager:
    uri="mongodb://localhost:27017/"
    def __init__(self, db_name="chess_db"):
        self.client = MongoClient(self.uri)
        self.db = self.client[db_name]

    def insert_document(self, collection_name, document_data):
        collection = self.db[collection_name]
        collection.insert_one(document_data)

    def drop_database_if_exists(self, db_name: str):
        if db_name in self.client.list_database_names():
            self.client.drop_database(db_name)

    def insert_many_documents(self, collection_name, documents):
        collection = self.db[collection_name]
        collection.insert_many(documents)

    def get_all_documents(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find(query)

    def get_distinct_field_values(self, collection_name: str, field_name: str) -> list:
        """ Devuelve un determinado atributo de todos los documentos de una colección"""
        collection = self.db[collection_name]
        return collection.distinct(field_name)

    def list_available_dbs(self, prefix="ChessDB"):
        all_dbs = self.client.list_database_names()
        return [db for db in all_dbs if db.startswith(prefix)]

    def drop_collection(self, collection_name):
        self.db[collection_name].drop()

    def close_connection(self):
        self.client.close()