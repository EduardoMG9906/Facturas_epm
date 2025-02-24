import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import requests


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
    df_bienestar = pd.read_csv("df (1).csv")
    
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
        
        st.write(f"### 📊 Datos de la tabla 'Facturas EPM 2016-2024'")        
        st.dataframe(df)

        # Opción para descargar los datos en CSV
        
        df_bienestar = pd.read_csv("df (1).csv")
        st.write(f"### 📊 Datos de la tabla `Indicador de Bienestar hasta 2021`")
        st.dataframe(df_bienestar)
        
        df_bienestar_2024 = pd.read_csv("df_bienestar_2024.csv")
        st.write(f"### 📊 Datos de la tabla `Indicador de Bienestar hasta 2024`")
        st.dataframe(df_bienestar_2024)        
    # filtered_data = df
    
    with Visualizacion:
        
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
        
        if st.button ("Gráfico de barras para el valor de la tarifa promedio por año"):
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

        if st.button ("Histograma energia con el paso de los años"):
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
        
        if st.button ("Grafico de dispersion de los rangos respecto al año"):
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
        
        
            st.write("### Promedio de tarifa en los rangos de consumo de Punta y Fuera de Punta y Rango Monomia") 
            df_avg = filtered_data[filtered_data['Rango de Consumo'].isin(['Punta', 'Fuera de Punta', 'Rango monomia'])].groupby('Rango de Consumo', as_index=False)['Compartido'].mean()
            # Crear la figura
            fig_4 = go.Figure()

            # Agregar cada trazo a la gráfica
            fig_4.add_trace(go.Bar(
                x=df_avg['Rango de Consumo'], 
                y=df_avg['Compartido'], 
                name='Tarifa Promedio',
                text=df_avg['Compartido'],  # Agregar los valores encima de las barras
                textposition='auto',  # Posicionar el texto automáticamente sobre las barras
                marker_color='blue'
            ))

            # Personalizar la gráfica
            fig_4.update_layout(
                title='Promedio de Tarifa Punta y Fuera de Punta',
                xaxis_title='Tipo de Información',
                yaxis_title='Tarifa Promedio',
                legend_title='Variables',
                template='plotly_white'
            )

            # Mostrar la gráfica
            st.plotly_chart(fig_4)
            
        if st.button ("Indicador de Bienestar hasta el 2021"):
            st.write("### Variacion del indicador de bienestar a lo largo del tiempo hasta 2021")
            fig_3 = go.Figure()

            # Agregar cada trazo a la gráfica
            fig_3.add_trace(go.Scatter(x=df_bienestar['año'], y=df_bienestar['Variacion_Porcentual_IPC'], mode='lines+markers', name='Variación Porcentual IPC', marker=dict(symbol='circle')))
            fig_3.add_trace(go.Scatter(x=df_bienestar['año'], y=df_bienestar['variacion porcentual_Salario'], mode='lines+markers', name='Variación Porcentual Salario', marker=dict(symbol='square')))
            fig_3.add_trace(go.Scatter(x=df_bienestar['año'], y=df_bienestar['Variacion_Porcentual_Kw/h'], mode='lines+markers', name='Variación Porcentual Kw/h', marker=dict(symbol='x')))
            fig_3.add_trace(go.Scatter(x=df_bienestar['año'], y=df_bienestar['indicador_bienestar'], mode='lines+markers', name='Indicador de Bienestar', marker=dict(symbol='triangle-up')))

            # Personalizar la gráfica
            fig_3.update_layout(
                title='Comparación de Variables a lo Largo del Tiempo',
                xaxis_title='Año',
                yaxis_title='Porcentaje de bienestar',
                legend_title='Variables',
                template='plotly_white'
            )
            # Mostrar la gráfica
            st.plotly_chart(fig_3)
        
        
            
        if st.button ("Proyeccion de bienestar hasta 2024"):
            st.write("### Variacion del indicador de bienestar a lo largo del tiempo hasta 2024")
            st.write("# R^2 = 0.72")
            fig_3 = go.Figure()

            # Agregar cada trazo a la gráfica
            fig_3.add_trace(go.Scatter(x=df_bienestar_2024['año'], y=df_bienestar_2024['Variacion_Porcentual_IPC'], mode='lines+markers', name='Variación Porcentual IPC', marker=dict(symbol='circle')))
            fig_3.add_trace(go.Scatter(x=df_bienestar_2024['año'], y=df_bienestar_2024['variacion_porcentual_Salario'], mode='lines+markers', name='Variación Porcentual Salario', marker=dict(symbol='square')))
            fig_3.add_trace(go.Scatter(x=df_bienestar['año'], y=df_bienestar['Variacion_Porcentual_Kw/h'], mode='lines+markers', name='Variación Porcentual Kw/h', marker=dict(symbol='x')))
            fig_3.add_trace(go.Scatter(x=df_bienestar_2024['año'], y=df_bienestar_2024['indicador_bienestar'], mode='lines+markers', name='Indicador de Bienestar', marker=dict(symbol='triangle-up')))

            # Personalizar la gráfica
            fig_3.update_layout(
                title='Comparación de Variables a lo Largo del Tiempo',
                xaxis_title='Año',
                yaxis_title='Porcentaje de bienestar',
                legend_title='Variables',
                template='plotly_white'
            )
            # Mostrar la gráfica
            st.plotly_chart(fig_3)
            


    conn.close()


  
        


  