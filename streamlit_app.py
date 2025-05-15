from streamlit_app.core import Processor

class StreamlitApp:
    def __init__(self):
        self.processor = Processor()

if __name__ == "__main__":
    app = StreamlitApp()
    app.processor.ejecutar()