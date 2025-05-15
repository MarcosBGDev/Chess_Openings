import streamlit as st
import matplotlib.pyplot as plt

class Visualization:
    def __init__(self, data):
        self.data = data
    @staticmethod
    def show():
        st.markdown("### Visualizaciones")

    def show_opening_graph(self, modality, year, player):
        df = self.data

        if modality != "Todas":
            df = df[df["time_class"] == modality]

        if year != "Todos":
            df = df[df["end_date"].str[:4] == str(year)]

        if player != "Todos":
            df = df[df["associated_username"] == player]

        if df.empty:
            st.warning("No hay datos disponibles con los filtros seleccionados.")
            return

        aggregated = df["opening_name"].value_counts().head(10)

        st.markdown("#### Aperturas más jugadas")

        fig, ax = plt.subplots()
        aggregated.sort_values().plot(kind='barh', ax=ax, color='skyblue')  # barras horizontales
        ax.set_xlabel("Número de partidas")
        ax.set_ylabel("Apertura")
        ax.set_title("Top 10 aperturas más jugadas")

        st.pyplot(fig)

