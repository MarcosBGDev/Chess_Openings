import streamlit as st
from src.etl.FetchData import FetchData
from src.etl.CleanConfig import CleanConfig
from src.etl.CleanData import CleanData
from src.utils.Helpers import Helpers

class InitialParams:
    def __init__(self):
        self.modalities = ["live_blitz", "live_bullet", "live_rapid"]
        self.clean_modalities = ["blitz", "bullet", "rapid"]
        self.fetch_data_client = FetchData()
        self.clean_data_client = None
        self.helper = Helpers()

    def show(self):
        if "procesado" not in st.session_state:
            st.session_state.procesado = False

        st.markdown("### Parámetros iniciales")
        st.write("Indica qué datos son los de tu preferencia.")

        n_players = st.slider(
            "Número de jugadores:",
            1, 50, 6
        )
        if n_players > 30:
            st.warning("Un gran número de jugadores tardará más tiempo en procesarse")

        start_year = st.slider(
            "Año inicial:",
            2008, 2025, 2016
        )
        end_year = st.slider(
            "Año final:",
            2008, 2025, 2016
        )

        valid = end_year >= start_year
        if not valid:
            st.error("El año final no puede ser menor que el inicial.")

        # Botón de procesar
        if valid:
            if st.button("Procesar"):
                st.session_state.procesado = True
                players_data = self.fetch_data_client.get_all_top_players(self.modalities, n_players)
                self.fetch_data_client.store_players_data(players_data, start_year, end_year, n_players)

                self.fetch_data_client.fetch_and_store_games(start_year, end_year, n_players)
                config = CleanConfig(start_year, end_year, n_players, self.clean_modalities, "white")
                clean_data_client = CleanData(config)
                clean_data_client.clean()

                st.success("Parámetros procesados correctamente")
        else:
            st.button("Procesar", disabled=True)

        return {
            "valid": valid,
            "procesado": st.session_state.procesado
        }