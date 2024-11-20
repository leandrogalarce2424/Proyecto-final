from flask import Blueprint, render_template,url_for,redirect,flash,session
from app.conecion_bd import obtener_conexion

listar_bp = Blueprint("listar", __name__)
editar_bp = Blueprint("editar", __name__)


@listar_bp.route("/listar")
def listar():
   # Verificar si el usuario está autenticado
    if "idusuarios" not in session:
        flash("Por favor, inicia sesión primero.", "danger")
        return redirect(url_for("main.login"))  # Redirigir a la página de login si no está autenticado

    # Obtener la información del usuario de la sesión
 
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM autos")
    autos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("listar.html")
@editar_bp.route("/editar")
def editar():
    pass    
@listar_bp.route("/listar/fiat")
def listar_fiat():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM autos")
    autos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("modelos.html",autos=autos)

@listar_bp.route("/consulta")
def consulta():
    return render_template("Consulta.html")