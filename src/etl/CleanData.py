from src.storage.MongoDBManager import MongoDBManager
import re

class CleanData:
    def __init__(self):
        print("Limpiando datos...")

    def clean(self):
        print("Datos limpios")

    def limpiar_apertura(self, apertura):
        #Eliminar la parte de las aperturas que varía
        apertura_base = apertura.split("...")[0]
        apertura_base = re.split(r"\d+\.", apertura_base)[0].rstrip("-")
        if "-with" in apertura_base:
            apertura_base = "-".join(apertura_base.split("-with")[:-1])
        apertura_base = re.sub(r"-\d+$", "", apertura_base)
        return apertura_base