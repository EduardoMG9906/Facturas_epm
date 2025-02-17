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
