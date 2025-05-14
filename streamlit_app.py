from streamlit_app.core.InitialParams import InitialParams
from streamlit_app.core.Segmentation import Segmentation
from streamlit_app.core.Visualization import Visualization
import streamlit as st

class StreamlitApp:
    def __init__(self):
        self.visualization = None
        self.segmentation = None
        self.parameters = InitialParams()
        self.modalities = ["live_blitz", "live_bullet", "live_rapid"]

    def ejecutar(self):
        st.set_page_config(layout="wide")

        col1, col2 = st.columns([1, 2], gap="large")
        with col1:
            params = self.parameters.show()

        if params.get("selected_db"):
            # Extraer info dinámica desde la base de datos
            fetch_data_client = self.parameters.fetch_data_client.get_database_names()

            start_year, end_year = fetch_data_client.get_years_from_db_name(params["selected_db"])
            years = list(range(int(start_year), int(end_year) + 1))

            df = fetch_data_client.get_dataframe_from_db(params["selected_db"])

            self.segmentation = Segmentation(self.modalities, years)
            modality, year = self.segmentation.show()

            self.visualization = Visualization(df)
            self.visualization.show()
            self.visualization.show_opening_graph(modality, year)
        else:
            with col2:
                st.info("Selecciona una base de datos para continuar.")



if __name__ == "__main__":
    app = StreamlitApp()
    app.ejecutar()