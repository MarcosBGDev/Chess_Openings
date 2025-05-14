from streamlit_app.core.InitialParams import InitialParams
from streamlit_app.core.Segmentation import Segmentation
from streamlit_app.core.Visualization import Visualization
import streamlit as st

class StreamlitApp:
    def __init__(self):
        self.parameters = InitialParams()
        self.segmentation = Segmentation()
        self.visualization = Visualization()
    #
    #
    #NOTA: Hacer que haya 2 botones, uno para procesar
    #
    def ejecutar(self):
        st.set_page_config(layout="wide")

        col1, col2 = st.columns([1, 2], gap="large")
        with col1:
            params = self.parameters.show()

        with col2:
            segment = self.segmentation.show()
            self.visualization.show(params, segment)



if __name__ == "__main__":
    app = StreamlitApp()
    app.ejecutar()