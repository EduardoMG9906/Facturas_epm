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
    ["Inicio", "Datos", "Visualización", "Configuración"]
)

if menu == "Inicio":
    st.write("""
             
    # Introducción
         
    # Problematica
    - Las tarifas de energía eléctrica varían según diversos factores.
    - El impacto de estas variaciones no siempre es claro, lo que dificulta la planificación financiera y la toma de decisiones informadas por parte de los consumidores.
    
    # Interes:
    
    - El análisis de tarifas eléctricas ayudará a comprender cómo fluctúan los costos dependiendo del consumo y tipo de cliente.
    - Permitirá diseñar estrategias para optimizar el consumo, mejorar la eficiencia y reducir costos.

    # Necesidad:
    
    - Es necesario desarrollar una herramienta que brinde información clara y accesible sobre las tarifas eléctricas.
    - Esto permitirá a los consumidores conocer los factores que afectan sus costos y tomar mejores decisiones en su consumo energético.

    # Objetivo general:
    
    -Desarrollar un análisis detallado de las tarifas eléctricas de EPM del año 2016 al 2022 en el area metropolitana, identificando patrones y tendencias que promuevan la toma de decisiones informadas por parte de los usuarios y optimicen el consumo energético.

    # Objetivos especificos:
    
    - Analizar la variabilidad de tarifas según tipo de tarifa, consumo y propiedad del servicio.
    - Identificar tendencias y patrones en los cambios de tarifas a lo largo del tiempo.
    - Desarrollar una herramienta de visualización para que los usuarios comprendan sus costos de energía y cómo optimizarlos.

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


  