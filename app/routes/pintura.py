from flask import Blueprint, render_template,url_for,redirect
from app.conecion_bd import obtener_conexion

pintura_bp = Blueprint("pintura", __name__)

@pintura_bp.route("/pintura")
def pintura():
    try:
        # Conexión a la base de datos
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)  # `dictionary=True` para obtener resultados como diccionarios
        # Consulta para obtener todos los registros
        cursor.execute("SELECT * FROM pintura")
        pinturas = cursor.fetchall()
        cursor.close()
        conn.close()
        # Renderizar plantilla con los datos obtenidos
        return render_template('pintura.html', pinturas=pinturas)
    except Exception as err:
        return f"Error al conectar con la base de datos: {err}"


