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
    colors_row = "<div style='display: flex; justify-content: center;'>"
    for i, color in enumerate(palette):
        color_hex = "#{:02X}{:02X}{:02X}".format(color[0], color[1], color[2])
        colors_row += f"<div style='background-color: {color_hex}; width: 70px; height: 70px; margin: 10px;'></div>"
    colors_row += "</div>"

    # ----- Se muestran los colores del a paleta obtenidos
    st.markdown(colors_row, unsafe_allow_html=True)