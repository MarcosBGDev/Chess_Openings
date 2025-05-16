from streamlit_app.layout.InterfaceManager import InterfaceManager

class StreamlitApp:
    def __init__(self):
        self.interface_manager = InterfaceManager()

if __name__ == "__main__":
    app = StreamlitApp()
    app.interface_manager.execute()