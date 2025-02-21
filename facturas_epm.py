import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.add_vertical_space import add_vertical_space
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import sqlite3
import requests
import altair as alt
import os

# URL del archivo SQL en GitHub (reemplaza con tu enlace)
GITHUB_SQL_URL = "https://raw.githubusercontent.com/EduardoMG9906/Facturas_epm/refs/heads/main/proyecto.sql"

# Función para descargar y guardar el archivo SQL
def descargar_sql(url, filename="database.sql"):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        return filename
    else:
        st.error("⚠️ Error al descargar el archivo SQL desde GitHub.")
        return None

# Descargar el archivo SQL
sql_file = descargar_sql(GITHUB_SQL_URL)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 1. Configuración inicial de la aplicación
st.set_page_config(
    page_title="Dashboard Interactivo",
    page_icon="📊",
    layout="wide"
)

st.title("📄 Proyecto Analisis de Facturas EPM")
# st.sidebar.title("🔍 Paginas")

# # 3. Implementación de la Barra de Navegación
# menu = st.sidebar.radio(
#     "",
#     ["Introducción","Visualización", "Datos"]
# )

Introduccion, Visualizacion, Datos = st.tabs(["Introducción","Visualización", "Datos"])

if sql_file:
    
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Leer el contenido del archivo SQL
    with open(sql_file, "r", encoding="utf-8") as file:
        sql_script = file.read()

    # Ejecutar las sentencias SQL
    cursor.executescript(sql_script)
    conn.commit()

    # Obtener nombres de las tablas
    #tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
    df = pd.read_sql(f"SELECT * FROM tarifas_epm_limpio", conn)
    
    df['Año'] = df['Año'].astype(int)
    df["Rango de Consumo"] = df["Rango de Consumo"].replace('0-CS','Rango 0 - CS')
    df["Rango de Consumo"] = df["Rango de Consumo"].replace('Mayor CS','Rango > CS')
    
    with Introduccion:
        st.markdown("""
            <h1 style="text-align: center; font-size: 36px;">Introducción</h1>
            <p style="font-size: 20px; text-align: justify; margin-bottom: 50px;">
            El costo de la energía eléctrica es un factor determinante en la planificación financiera de hogares y empresas. 
            Sin embargo, la variabilidad de las tarifas según el tipo de cliente, el consumo y otros factores puede dificultar la toma de decisiones informadas. 
            Este proyecto tiene como objetivo analizar las tarifas eléctricas de EPM en el área metropolitana entre 2016 y 2022, identificando patrones y tendencias que permitan optimizar el consumo energético. 
            A través del desarrollo de una herramienta de visualización, se busca brindar información clara y accesible para que los usuarios comprendan sus costos y tomen decisiones más eficientes en el uso de la energía.
            </p>
        """, unsafe_allow_html=True)

        # Agregar espacio adicional
        st.markdown("", unsafe_allow_html=True)

        lottie_book = load_lottieurl("https://lottie.host/8acb477f-bcc4-4098-ab27-39a9a5cda7f1/Y7lK81s2RL.json")
        st_lottie(lottie_book, speed=1, height=300, key="initial")    

    with Datos:
        
        st.write("# Datos")
        
        st.write(f"### 📊 Datos de la tabla `")        
        st.dataframe(df)

        # Opción para descargar los datos en CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv, "datos.csv", "text/csv")
    
    # filtered_data = df
    
    with Visualizacion:
        st.subheader("📊 Visualización de Datos")
        # Agregar opción "Todos" a la lista de categorías
        categorias = ["Todos"] + list(df["Tipo de Dato"].unique())
        
        categoria = st.selectbox("Selecciona una categoría", categorias)
        
        # Filtrar datos si se selecciona una categoría específica
        if categoria == "Todos":
            filtered_data = df.copy()  # No aplicar filtro
        else:
            filtered_data = df[df["Tipo de Dato"] == categoria]

        filtered_data["Año"] = pd.to_numeric(filtered_data["Año"], errors="coerce")
        filtered_data["Compartido"] = pd.to_numeric(filtered_data["Compartido"], errors="coerce")
        
        st.write("## Gráficos")
        
        col1, col2 = st.columns(2)
        with col1: 
            st.write(f"### Gráfico de barras para el valor de la tarifa promedio por año para {categoria}")

            # Calcular el promedio por año
            df_mean = filtered_data.groupby("Año", as_index=False)["Compartido"].mean()
            

            # Crear el gráfico
            fig = px.box(
                filtered_data, 
                x="Año", 
                y="Compartido", 
                labels={"Compartido": "Tarifa Promedio", "Año": "Año"},
                color_discrete_sequence=["#3498db"]
            )
            
            st.plotly_chart(fig)

            st.write(f"### Histograma para ver el comportamiento del valor de la energia por estrato y año para {categoria}")

            # Crear el gráfico de líneas con Plotly
            fig_2 = px.histogram(
                filtered_data, 
                x="Tipo de Dato", 
                y="Compartido", 
                color="Año",  # Equivalente a hue en Seaborn
                barmode= "group",  # Añade puntos en las líneas
                #labels={"Tipo de Dato": "Categoría", "Compartido": "Tarifa Promedio", "Año": "Año"}
            )
            st.plotly_chart(fig_2)
        
        with col2:
            st.write(f"### Gráfico de dispersión para los rangos del valor de la tarifa  por año para {categoria}")
            fig_3 = px.scatter(
                filtered_data, 
                x="Rango de Consumo",
                y="Tipo de Dato",  
                color="Tipo de Información",  # Equivalente a hue en Seaborn
                size = "Compartido",  
                #title=f"  {categoria}",
                #labels={"Tipo de Dato": "Categoría", "Compartido": "Tarifa Promedio", "Año": "Año"}
            )
            st.plotly_chart(fig_3)

    conn.close()


  
        


  