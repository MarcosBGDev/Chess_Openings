import streamlit as st
from src.storage.DatabaseUtils import DatabaseUtils

class Segmentation:

    def __init__(self, db_name, players_list):
        self.players_list = players_list
        self.database_utils = DatabaseUtils()
        self.available_modalities = ["Todas"] + self.database_utils.get_available_modalities(db_name)

        self.start_year, self.end_year = self.database_utils.get_years_from_db_name(db_name)
        years = list(range(int(self.start_year), int(self.end_year) + 1))
        self.available_years = ["Todos"] + years
        self.available_players = ["Todos"] + players_list
        

    def show(self):
        st.markdown("#### Segmentación")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            modality = st.selectbox("Selecciona modalidad:", self.available_modalities)
        with col2:
            year = st.selectbox("Selecciona año:", self.available_years)
        with col3:
            player = st.selectbox("Selecciona jugador:", self.available_players)

        return modality, year, player


