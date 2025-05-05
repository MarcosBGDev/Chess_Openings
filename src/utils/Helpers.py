from datetime import datetime
class Helpers:
    def __init__(self):
        print("")

    @staticmethod
    def get_months():
        #Devuelve los meses en formato de dos dígitos
        months=["01","02","03","04","05","06","07","08","09","10","11","12"]
        return months

    @staticmethod
    def extract_unique_usernames(players):
        return list({player["username"] for player in players})


    @staticmethod
    def convert_int_to_time(timestamp):
        date = datetime.fromtimestamp(timestamp)
        return date