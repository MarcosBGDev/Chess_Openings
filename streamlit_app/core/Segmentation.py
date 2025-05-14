import streamlit as st

class Segmentation:

    def __init__(self, available_modalities, available_years):
        self.available_modalities = ["General"] + available_modalities
        self.available_years = ["General"] + available_years


    def show(self):
        st.markdown("#### Segmentación")
        col1, col2, _ = st.columns([1, 1, 3])

        with col1:
            modality = st.selectbox("Selecciona modalidad:", self.available_modalities)
        with col2:
            year = st.selectbox("Selecciona año:", self.available_years)

        return modality, year


