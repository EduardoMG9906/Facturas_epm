import streamlit as st

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from tarifas_energia;', ttl=600)

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
    st.dataframe(df)
