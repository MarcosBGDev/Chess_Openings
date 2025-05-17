import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

class Visualization:
    def __init__(self, data):
        self.data = data
    @staticmethod
    def show():
        st.markdown("### Visualizaciones")


    def show_opening_graph(self, modality, year, player):
        df = self.filter_data(modality, year, player)

        aggregated = df["opening_name"].value_counts().head(10)
        st.markdown("#### Aperturas más jugadas")

        fig, ax = plt.subplots()
        aggregated.sort_values().plot(kind='barh', ax=ax, color='skyblue')  # barras horizontales
        ax.set_xlabel("Número de partidas")
        ax.set_ylabel("Apertura")
        ax.set_title("Top 10 aperturas más jugadas")

        st.pyplot(fig)

    def show_summary_card(self, modality, year, player):
        df = self.filter_data(modality, year, player)
        total_games = len(df)
        st.metric("Total de partidas", total_games)

    def show_activity_over_time(self, modality, year, player):
        df = self.filter_data(modality, year, player)

        if df.empty:
            st.warning("No hay datos disponibles con los filtros seleccionados.")
            return

        # Asegurar que end_date sea datetime
        df["end_date"] = pd.to_datetime(df["end_date"])

        # Agrupar por mes
        activity = df.groupby(df["end_date"].dt.to_period("M")).size().sort_index()
        activity.index = activity.index.to_timestamp()

        st.markdown("### Actividad a lo largo del tiempo")
        st.line_chart(activity)

    def filter_data(self, modality, year, player):
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

        return df