from flask import Blueprint, render_template,url_for,redirect
from app.conecion_bd import obtener_conexion

ruedas_bp = Blueprint("ruedas", __name__)

@ruedas_bp.route("/ruedas")
def ruedas():
    try:
        # Conexión a la base de datos
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)  # `dictionary=True` para obtener resultados como diccionarios
        # Consulta para obtener todos los registros
        cursor.execute("SELECT * FROM ruedas")
        ruedas = cursor.fetchall()
        cursor.close()
        conn.close()
        # Renderizar plantilla con los datos obtenidos
        return render_template('ruedas.html', ruedas=ruedas)
    except Exception as err:
        return f"Error al conectar con la base de datos: {err}"


