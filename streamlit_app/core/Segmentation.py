import streamlit as st

class Segmentation:

    @staticmethod
    def show():
        st.markdown("#### Segmentación")
        col1, col2, _ = st.columns([1, 1, 3])

        with col1:
            player = st.selectbox("Jugador", ["Jugador A", "Jugador B"])

        with col2:
            year = st.selectbox("Año", [2023, 2024])

        return {"player": player, "year": year}