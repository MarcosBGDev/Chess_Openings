from src import MongoDBManager
from src.storage.DatabaseUtils import DatabaseUtils
from streamlit_app.core.DatasetSelector import DatasetSelector
from streamlit_app.core.InitialParams import InitialParams
from streamlit_app.core.Segmentation import Segmentation
from streamlit_app.core.Visualization import Visualization
import streamlit as st

class Processor:
    def __init__(self):
        self.visualization = None
        self.segmentation = None
        self.dataset_selector = DatasetSelector()
        self.parameters = InitialParams()
        self.modalities = ["live_blitz", "live_bullet", "live_rapid"]
        self.database_utils= DatabaseUtils()
        self.db_manager= None

    def ejecutar(self):
        st.set_page_config(layout="wide")

        # Dividir pantalla en 2 columnas
        col_left, col_right = st.columns([1, 2], gap="large")

        # --- Izquierda ---
        with col_left:
            # Fila superior: Parámetros iniciales (crear sesión, procesar)
            with st.container():
                params = self.parameters.show()

            # Fila inferior: Selección de base de datos
            with st.container():

                selected_db = self.dataset_selector.show()

        # --- Derecha ---
        with col_right:
            if selected_db:
                # Fila superior: Segmentación según datos de BD
                with st.container():
                    self.db_manager= MongoDBManager(selected_db)
                    players_list = self.db_manager.get_distinct_field_values("players","username")
                    self.segmentation = Segmentation(selected_db, players_list)
                    modality, year, player = self.segmentation.show()

                # Fila inferior: Visualizaciones basadas en segmentación
                with st.container():
                    df = self.database_utils.get_dataframe_from_collection(selected_db, "clean_games")
                    visualization = Visualization(df)
                    visualization.show()
                    visualization.show_opening_graph(modality, year, player)
            else:
                with st.container():
                    st.info("Selecciona una base de datos para visualizar los datos.")



