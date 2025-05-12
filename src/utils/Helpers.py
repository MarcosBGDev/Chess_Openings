import datetime

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
    def get_current_year() -> int:
        """ Devuelve el año actual"""
        return datetime.datetime.now().year