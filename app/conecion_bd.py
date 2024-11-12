import mysql.connector


def obtener_conexion():
    return mysql.connector.connect(
        host="bbk6e0qpuaf4rjvzwlbc-mysql.services.clever-cloud.com",
        user="uejfypckzfkd1a9r",
        password="3fPKJxosLRHb18DaMG9G",
        database="bbk6e0qpuaf4rjvzwlbc",
    )