import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import sqlite3
import requests
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


# 1. Configuración inicial de la aplicación
st.set_page_config(
    page_title="Dashboard Interactivo",
    page_icon="📊",
    layout="wide"
)

st.title("📄 Proyecto Analisis de Facturas EPM")
st.sidebar.title("🔍 Navegación")

# 3. Implementación de la Barra de Navegación
menu = st.sidebar.radio(
    "Selecciona una opción:",
    ["Visualización", "Introducción", "Datos",]
)

if menu == "Inicio":
    st.write("""
             
    # Introducción
         
    El costo de la energía eléctrica es un factor determinante en la planificación financiera de hogares y empresas. 
    Sin embargo, la variabilidad de las tarifas según el tipo de cliente, el consumo y otros factores puede dificultar la toma de decisiones informadas. 
    Este proyecto tiene como objetivo analizar las tarifas eléctricas de EPM en el área metropolitana entre 2016 y 2022, identificando patrones y tendencias que permitan optimizar el consumo energético. 
    A través del desarrollo de una herramienta de visualización, se busca brindar información clara y accesible para que los usuarios comprendan sus costos y tomen decisiones más eficientes en el uso de la energía.
    """)    

if sql_file:
    if menu == "Datos":
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        # Leer el contenido del archivo SQL
        with open(sql_file, "r", encoding="utf-8") as file:
            sql_script = file.read()

        # Ejecutar las sentencias SQL
        cursor.executescript(sql_script)
        conn.commit()

        # Obtener nombres de las tablas
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
        st.write("### 📌 Tablas disponibles en la base de datos:")
        st.write(tables)

        # Selección de tabla para visualizar
        table_name = st.selectbox("Selecciona una tabla para ver los datos:", tables["name"])

        if table_name:
            # Cargar los datos en un DataFrame
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            st.write(f"### 📊 Datos de la tabla `{table_name}`")
            st.dataframe(df)

            # Opción para descargar los datos en CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descargar CSV", csv, "datos.csv", "text/csv")

        # Cerrar la conexión
        conn.close()

filtered_data = df
if menu == "Visualización":
    st.subheader("📊 Visualización de Datos")
    categoria = st.sidebar.selectbox("Selecciona una categoría", df["Tipo de Dato"].unique())
    filtered_data = df[df["Tipo de Dato"] == categoria]
    st.write(f"Mostrando datos para la categoría {categoria}")
    st.dataframe(filtered_data)
  
        


  