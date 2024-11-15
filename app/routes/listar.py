from flask import Blueprint, render_template,url_for
from app.conecion_bd import obtener_conexion
from .main import role_required
listar_bp = Blueprint("listar", __name__)
editar_bp = Blueprint("editar", __name__)


@listar_bp.route("/listar")
@role_required("admin")
def listar():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM autos")
    autos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("listar.html", autos=autos)
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