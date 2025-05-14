import streamlit as st

class Visualization:
    def __init__(self, data):
        self.data = data
    @staticmethod
    def show(params, segmentation):
        st.markdown("#### Visualizaciones")

    def show_opening_graph(self, modality, year):
        df = self.data

        if modality != "General":
            df = df[df["modality"] == modality]

        if year != "General":
            df = df[df["year"] == year]

        # Agrupamos y visualizamos
        aggregated = df.groupby("opening")["score"].mean().sort_values(ascending=False).head(10)

        st.markdown(f"### Mejores aperturas {'(general)' if modality == 'General' else f'para {modality}'}")
        st.bar_chart(aggregated)

