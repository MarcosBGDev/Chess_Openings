import streamlit as st

# Configurar ancho completo
st.set_page_config(layout="wide")
# Espacio arriba
st.markdown("<br>", unsafe_allow_html=True)
# Crear dos columnas con separación proporcional
col1, col2 = st.columns([1, 2], gap="large")  # 1:2 relación

# Contenedor izquierdo
with col1:
    modalities = ["live_blitz", "live_bullet", "live_rapid"]
    clean_modalities = ["blitz", "bullet", "rapid"]

    st.markdown("### Parámetros iniciales")
    st.write("Indica que datos son los de tu preferencia.")
    n_players = st.slider(
        "Indica cuantos jugadores del ranking quieres de cada modalidad de juego:",
        min_value = 1,
        max_value = 50,
        value = 6,
        step = 1
    )
    if n_players > 30:
        st.warning("Un gran número de jugadores tardará más tiempo en procesarse")
    start_year = st.slider(
        "Indica un año inicial para el analisis:",
        min_value=2008,
        max_value=2025,
        value=2016,
        step=1
    )
    end_year = st.slider(
        "Indica un año final para el analisis:",
        min_value=2008,
        max_value=2025,
        value=2016,
        step=1
    )

# Contenedor derecho con margen superior simulado
with col2:
    st.markdown("### Panel derecho")

    # Subcontenedor arriba para segmentaciones
    with st.container():
        st.markdown("#### Segmentación")

        # Distribuir en 3 columnas para limitar el ancho
        col1, col2, _ = st.columns([1, 1, 3])  # Deja espacio al final con "_"

        with col1:
            player = st.selectbox("Jugador", ["Jugador A", "Jugador B"])

        with col2:
            year = st.selectbox("Año", [2023, 2024])
    if end_year < start_year:
        st.error("El año final no puede ser menor que el año inicial.")
        disable_button = True
    else:
        disable_button = False
    # Otro contenido debajo
    st.markdown("---")
    st.markdown("#### Visualizaciones")
    st.write("Aquí irían los gráficos")

    # Botón para realizar acción solo si la validación es correcta
    if disable_button:
        st.button("Procesar", disabled=True)
    else:
        st.button("Procesar")