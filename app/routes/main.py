from flask import Blueprint, render_template , request , flash , redirect , url_for, session
from ..conecion_bd import obtener_conexion
from functools import wraps
def role_required(required_role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("rol") != required_role:
                flash("No tienes permisos para esa acción.", "danger")
                return redirect(
                    url_for("listar.listar")
                )  # Redirige al usuario a la página de inicio o a una página de error
            return f(*args, **kwargs)

        return decorated_function

    return wrapper
main = Blueprint("main", __name__)


@main.route("/")
def index():
    logout()
    return render_template("index.html")

@main.route("/registro")
def registro():
    return render_template("registro.html")

@main.route("/registro/add", methods=["POST"])

def add():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    usuario = request.form.get("nombre")
    mail = request.form.get("email")
    password = request.form.get("password")

    confirm_password = request.form.get("confirm-password")
    
    # Verifica que los campos requeridos estén completos
    if (
        not usuario
        or not mail
        or not password
        or not confirm_password
        
    ):
        flash("Todos los campos son requeridos", "danger")
        return redirect(url_for("main.registro"))  # Redirecciona a la página de alumnos

    # Construye la consulta SQL para insertar el nuevo alumno
    query = """
        INSERT INTO usuarios (usuario, password, mail)
        VALUES (%s, %s, %s)
    """
    values = (usuario, password, mail)

    # Ejecuta la consulta e inserta los datos en la base de datos
    try:
        cursor.execute(query, values)
        conexion.commit()

        flash(f"Alumno {usuario} {mail} agregado exitosamente", "success")
    except Exception as e:
        conexion.rollback()
        flash("Error al agregar el usuario: " + str(e), "danger")
    finally:
        cursor.close()
        conexion.close()
    return redirect(url_for("listar.listar"))  # Redirecciona a la página de alumnos
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["nombre"]
        password = request.form["password"]

        # Conectar a la base de datos
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)

        # Buscar el usuario en la base de datos
        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = %s AND password = %s",
            (username, password),
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        # Verificar usuario y contraseña
        if user:
            # Inicia sesión: almacena el id y rol en la sesión
            session["idusuarios"] = user["idusuarios"]
            session["usuario"] = user["usuario"]
            session["rol"] = user["rol"]
            

            flash("Inicio de sesión exitoso.", "success")
            return render_template("listar.html", user=user)

        else:
            flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("index.html")

@main.route("/logout")
def logout():
    session.clear()  # Limpia todos los datos de la sesión
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("main.login"))


