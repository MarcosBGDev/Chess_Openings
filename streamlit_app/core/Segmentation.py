import streamlit as st

class Segmentation:

    def __init__(self, modalities, years, players):
        self.available_modalities = ["Todas"] + modalities
        self.available_years = ["Todos"] + years
        self.available_players = ["Todos"] + players

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
