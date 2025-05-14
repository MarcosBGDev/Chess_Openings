#from .Processor import Processor

import streamlit as st
from src.etl.FetchData import FetchData
from src.utils.Helpers import Helpers

class InitialParams:
    def __init__(self):
        self.modalities = ["live_blitz", "live_bullet", "live_rapid"]
        self.clean_modalities = ["blitz", "bullet", "rapid"]
        self.fetch_data_client = FetchData()
        self.helper = Helpers()
        self.processor = Processor(
            self.modalities,
            self.clean_modalities,
            self.fetch_data_client,
            self.helper
        )

    def show(self):
        # Estado de desactivación tras procesamiento
        if "procesado" not in st.session_state:
            st.session_state.procesado = False

        st.markdown("### Parámetros iniciales")
        st.write("Indica qué datos son los de tu preferencia.")

        disabled = st.session_state.procesado

        n_players = st.slider(
            "Número de jugadores:",
            1, 50, 6,
            disabled=disabled
        )
        if n_players > 30:
            st.warning("Un gran número de jugadores tardará más tiempo en procesarse")

        start_year = st.slider(
            "Año inicial:",
            2008, 2025, 2016,
            disabled=disabled
        )
        end_year = st.slider(
            "Año final:",
            2008, 2025, 2016,
            disabled=disabled
        )

        valid = end_year >= start_year
        if not valid:
            st.error("El año final no puede ser menor que el inicial.")

        # Botón de procesar
        if not valid:
            st.button("Procesar", disabled=True)
        else:
            if st.button("Procesar", disabled=disabled):
                self.processor.run(n_players, start_year, end_year)
                st.session_state.procesado = True
                st.success("Parámetros procesados correctamente")

        return {
            "n_players": n_players,
            "start_year": start_year,
            "end_year": end_year,
            "valid": valid,
            "procesado": st.session_state.procesado
        }