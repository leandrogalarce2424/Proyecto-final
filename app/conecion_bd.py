import mysql.connector


def obtener_conexion():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1234",
        database="listado_de_autos",
    )