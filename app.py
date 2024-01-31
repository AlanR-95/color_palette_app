####################################################
#   _____ __  __ _____   ____  _____ _______ _____ 
#  |_   _|  \/  |  __ \ / __ \|  __ \__   __/ ____|
#    | | | \  / | |__) | |  | | |__) | | | | (___  
#    | | | |\/| |  ___/| |  | |  _  /  | |  \___ \ 
#   _| |_| |  | | |    | |__| | | \ \  | |  ____) |
#  |_____|_|  |_|_|     \____/|_|  \_\ |_| |_____/ 
####################################################
                                      
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

###############################
#    _____ ____  _____  ______ 
#   / ____/ __ \|  __ \|  ____|
#  | |   | |  | | |  | | |__   
#  | |   | |  | | |  | |  __|  
#  | |___| |__| | |__| | |____ 
#   \_____\____/|_____/|______|
###############################

html_custom_2 = """
    <style>
    .st-emotion-cache-1r4qj8v {
    position: absolute;
    background: #3E3E3E;
    color: rgb(49, 51, 63);
    inset: 0px;
    color-scheme: light;
    overflow: hidden;}

    .st-emotion-cache-18ni7ap {
    position: fixed;
    top: 0px;
    left: 0px;
    right: 0px;
    height: 2.875rem;
    background: #505050;
    outline: none;
    z-index: 999990;
    display: block;}

    .st-emotion-cache-16idsys p {
    font-size: 14px;
    color: #ffffff;}

    .st-emotion-cache-1uixxvy {
    color:#ffffff;}

    .st-emotion-cache-1gulkj5 {
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    padding: 1rem;
    background-color: #505050;
    border-radius: 0.5rem;
    color: #ffffff;}

    .st-emotion-cache-1aehpvj {
    color: #ffffff;
    font-size: 14px;
    line-height: 1.25;}


    .st-emotion-cache-7ym5gk {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 38.4px;
    margin: 0px;
    line-height: 1.6;
    color: #FFFFFF;
    width: auto;
    user-select: none;
    background-color: #747474;
    border: 1px solid #3E3E3E;}
    
    .st-emotion-cache-5rimss {
    font-family: "Source Sans Pro", sans-serif;
    margin-bottom: -1rem;
    color: #FFFFFF
    }
    

    .st-emotion-cache-1dp5vir {
    position: absolute;
    top: 0px;
    right: 0px;
    left: 0px;
    height: 0.125rem;
    background-image: linear-gradient(90deg, rgb(0, 0, 0), rgb(0, 0, 0));
    z-index: 999990;}

    .st-emotion-cache-zbmw0q:hover:enabled, .st-emotion-cache-zbmw0q:focus:enabled {
    color: rgb(255, 255, 255);
    background-color: #000000;
    transition: none 0s ease 0s;

    .st-emotion-cache-kskxxl {
    background-color: #000000;}

    </style>
    """

def main():

    # ----- Seteos de página
    st.set_page_config(
        page_title="Color Palette",
        page_icon="🎨",
        layout="centered",
        initial_sidebar_state="auto",
    )

    st.write(
        html_custom_2,
        unsafe_allow_html=True
    )

    # ----- Diccionario para gestionar el estado (si se cargó o no la imagen)
    if "image_url" not in st.session_state:
        st.session_state.image_url = None

    # ----- Carga de la imagen
    uploaded_file = st.file_uploader("Seleccione una imagen:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen cargada", use_column_width=True)

        # ----- Se obtiene como sample_size el total de píxeles de la imagen
        width, height = image.size
        total_pixels = width * height
        sample_size = total_pixels

        # ----- Se genera el dataframe con los valores RGB de cada píxel
        r, g, b = np.array(image).reshape(-1, 3).T
        df_rgb = pd.DataFrame({"R": r, "G": g, "B": b}).sample(n=sample_size)

        st.markdown(
            """
            <style>
                div[data-baseweb="input"] .streamlit-NumberInputUpButton:hover,
                div[data-baseweb="input"] .streamlit-NumberInputDownButton:hover {
                    background-color: #666666 !important; /* Cambia #666666 al color gris oscuro que prefieras */
                    color: white !important; /* Cambia "white" al color de texto que prefieras */
                }
            </style>
            """, 
            unsafe_allow_html=True
        )

        # ----- Se clusteriza para obtener los valores promedios RGB de la paleta de colores
        palette_size = st.number_input("palette size", 
                                                min_value=1, 
                                                max_value=20, 
                                            value=5, 
                                                step=1, 
                                                help="Number of colors to infer from the image.")

        model = KMeans(n_clusters=palette_size)
        clusters = model.fit_predict(df_rgb)
        palette = model.cluster_centers_.astype(int).tolist()

        # ----- Se crea la fila de colores con formato personalizado
        colors_row = "<div style='display: flex; justify-content: center; flex-wrap: wrap;'>"
        for i, color in enumerate(palette):
            color_hex = "#{:02X}{:02X}{:02X}".format(color[0], color[1], color[2])
            colors_row += f"<div style='text-align: center; margin: 10px;'><div style='background-color: {color_hex}; width: 70px; height: 70px;'></div>{color_hex}</div>"
        colors_row += "</div>"

        # ----- Se muestran los colores de la paleta obtenidos
        st.markdown(colors_row, unsafe_allow_html=True)

if __name__ == '__main__':
    main()