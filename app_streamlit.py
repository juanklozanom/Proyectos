import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static

# URL de la API FastAPI
API_URL = "http://127.0.0.1:8000"

# Título de la aplicación
st.title("Gestión de Proyectos y Predios")

# Sidebar con opciones
menu = st.sidebar.selectbox("Menú", ["Agregar Proyecto", "Ver Proyectos", "Ver Predios en Mapa"])


# Función para obtener proyectos
def obtener_proyectos():
    response = requests.get(f"{API_URL}/proyectos")
    return response.json() if response.status_code == 200 else []


# Función para obtener predios
def obtener_predios():
    response = requests.get(f"{API_URL}/predios")
    return response.json() if response.status_code == 200 else []


# 1️⃣ Agregar Proyecto
if menu == "Agregar Proyecto":
    st.subheader("Agregar Nuevo Proyecto")

    with st.form("proyecto_form"):
        nombre = st.text_input("Nombre del Proyecto")
        entidad = st.text_input("Entidad Responsable")
        priorizacion = st.selectbox("Priorización", ["Alta", "Media", "Baja"])
        localidad = st.text_input("Localidad")
        upl = st.text_input("UPL")
        numero_predios = st.number_input("Número de Predios", min_value=1, step=1)
        enviado = st.form_submit_button("Guardar Proyecto")

    if enviado:
        datos = {
            "nombre_proyecto": nombre,
            "entidad": entidad,
            "priorizacion": priorizacion,
            "localidad": localidad,
            "UPL": upl,
            "numero_predios": numero_predios
        }
        response = requests.post(f"{API_URL}/proyectos", json=datos)
        if response.status_code == 200:
            st.success("Proyecto agregado exitosamente!")
        else:
            st.error("Error al agregar el proyecto")

# 2️⃣ Ver Proyectos
elif menu == "Ver Proyectos":
    st.subheader("Lista de Proyectos")
    proyectos = obtener_proyectos()
    if proyectos:
        df = pd.DataFrame(proyectos)
        st.dataframe(df)
    else:
        st.warning("No hay proyectos disponibles")

# 3️⃣ Ver Predios en Mapa
elif menu == "Ver Predios en Mapa":
    st.subheader("Mapa de Predios")
    predios = obtener_predios()

    if predios:
        mapa = folium.Map(location=[4.6097, -74.0817], zoom_start=12)
        for predio in predios:
            lat, lon = predio["latitud"], predio["longitud"]
            if lat and lon:
                folium.Marker([lat, lon], popup=predio["direccion"]).add_to(mapa)
        folium_static(mapa)
    else:
        st.warning("No hay predios con coordenadas registradas")
