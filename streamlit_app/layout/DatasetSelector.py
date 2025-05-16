from src.storage.DatabaseUtils import DatabaseUtils
import streamlit as st

class DatasetSelector:
    def __init__(self):
        self.database_utils = DatabaseUtils()

    def show(self):
        st.markdown("### Selección de BD")
        db_names = self.database_utils.get_database_names()
        selected_db = st.selectbox("Selecciona una base de datos:", db_names)
        return selected_db