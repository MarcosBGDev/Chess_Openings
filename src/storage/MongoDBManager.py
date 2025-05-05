from pymongo import MongoClient

class MongoDBManager:
    uri="mongodb://localhost:27017/"
    def __init__(self, db_name="chess_db"):
        self.client = MongoClient(self.uri)
        self.db = self.client[db_name]

    def insert_game(self, collection_name, game_data):
        collection = self.db[collection_name]
        collection.insert_one(game_data)

    def insert_many_games(self, collection_name, games):
        collection = self.db[collection_name]
        collection.insert_many(games)

    def find_games(self, collection_name, query={}):
        collection = self.db[collection_name]
        return list(collection.find(query))

    def drop_collection(self, collection_name):
        self.db[collection_name].drop()

    def close_connection(self):
        self.client.close()