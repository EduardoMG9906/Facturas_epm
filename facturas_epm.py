import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import mysql.connector

def conectar():
    """Establece la conexión con la base de datos MySQL en XAMPP y devuelve el objeto de conexión."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",         # Usuario por defecto en XAMPP
        password="",         # Normalmente sin contraseña en XAMPP
        database="proyecto"  # Nombre de la base de datos
    )
    return conn

# Conectar a la base de datos
conn = conectar()

# Leer los datos en un DataFrame de Pandas
query = "SELECT * FROM tarifas_energia"
df = pd.read_sql(query, conn)
data = df.copy()

# Cerrar la conexión
conn.close()

st.set_page_config(
  page_title= "Proyecto",
  layout="wide"
)

st.title(" 📄 Facturas EPM")
st.sidebar.title("Opciones de Navegacion")

# 3. Implementación de la Barra de Navegación
menu = st.sidebar.radio(
    "Selecciona una opción:",
    ["Inicio", "Datos", "Visualización", "Configuración"]
)

# 4. Mostrar los Datos
if menu == "Datos":
  st.subheader("📂 Datos Generados")
  st.dataframe(data)
  
# # 5. Filtrar por Categoría
# filtered_data = data  # Asegurar que filtered_data esté definido en todo el script
# if menu == "Visualización":
#     st.subheader("📊 Visualización de Datos")
#     categoria = st.sidebar.selectbox("Selecciona una categoría", data["Categoría"].unique())
#     filtered_data = data[data["Categoría"] == categoria]
#     st.write(f"Mostrando datos para la categoría {categoria}")
#     st.dataframe(filtered_data)

    # # 6. Filtrar por Ventas
    # ventas_min, ventas_max = st.sidebar.slider(
    #     "Selecciona el rango de ventas:",
    #     min_value=int(data["Ventas"].min()),
    #     max_value=int(data["Ventas"].max()),
    #     value=(int(data["Ventas"].min()), int(data["Ventas"].max()))
    # )
    # filtered_data = filtered_data[(filtered_data["Ventas"] >= ventas_min) & (filtered_data["Ventas"] <= ventas_max)]

    # # 7. Filtrar por Fecha
    # fecha_inicio, fecha_fin = st.sidebar.date_input(
    #     "Selecciona el rango de fechas:",
    #     [data["Fecha"].min(), data["Fecha"].max()],
    #     min_value=data["Fecha"].min(),
    #     max_value=data["Fecha"].max()
    # )
    # filtered_data = filtered_data[(filtered_data["Fecha"] >= pd.to_datetime(fecha_inicio)) & (filtered_data["Fecha"] <= pd.to_datetime(fecha_fin))]