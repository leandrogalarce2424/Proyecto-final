from flask import Blueprint, render_template,url_for,redirect,flash,request
from app.conecion_bd import obtener_conexion
from .main import role_required
consulta_bp = Blueprint("consulta", __name__)

@consulta_bp.route("/consulta/registro", methods=["POST"])

def registro():
    if request.method == 'POST':
        # Capturar datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        celular = request.form.get('celular')
        correo = request.form.get('correo')
        ciudad = request.form.get('ciudad')
        detalles = request.form.get('detalles')
       

        # Validar datos
        if not (nombre and apellido and correo and ciudad and detalles):
            flash('Por favor, completa todos los campos requeridos.', 'error')
            return redirect(url_for('registro'))

        # Guardar datos en la base de datos
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO consultas (nombre, apellido, celular, email, ciudad, detalle_consulta)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (nombre, apellido, celular, correo, ciudad, detalles))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Consulta registrada exitosamente.', 'success')
        except Exception as err:
            flash(f'Error al guardar la consulta: {err}', 'error')

        return render_template('consulta.html')

    return render_template('consulta.html')  # Usa tu archivo HTML aquí


@consulta_bp.route("/consulta/ver_consultas", methods=["POST","GET"])
@role_required("admin")
def ver_consultas(): 
    try:
        # Conexión a la base de datos
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)  # `dictionary=True` para obtener resultados como diccionarios
        # Consulta para obtener todos los registros
        cursor.execute("SELECT * FROM consultas")
        consultas = cursor.fetchall()
        cursor.close()
        conn.close()
        # Renderizar plantilla con los datos obtenidos
        return render_template('ver_consultas.html', consultas=consultas)
    except Exception as err:
        return f"Error al conectar con la base de datos: {err}"

@consulta_bp.route('/consulta/eliminar/<int:id>', methods=['POST'])
@role_required("admin")
def eliminar_consulta(id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        # Eliminar la consulta de la base de datos
        cursor.execute("DELETE FROM consultas WHERE idconsultas = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('consulta.ver_consultas'))  # Redirige a la página de consultas
    except Exception as err:
        return f"Error al eliminar la consulta: {err}"
    
@consulta_bp.route('/consulta/actualizar_estado/<int:id>', methods=['POST'])
def actualizar_estado(id):
    try:
        # Obtener el nuevo estado desde el formulario
        nuevo_estado = request.form['estado']
        
        # Conexión a la base de datos
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Actualizar el estado de la consulta
        cursor.execute('''
            UPDATE consultas
            SET estado = %s
            WHERE idconsultas = %s
        ''', (nuevo_estado, id))

        conn.commit()  # Guardar los cambios
        cursor.close()
        conn.close()

        flash('Estado actualizado exitosamente.', 'success')
        return redirect(url_for('consulta.ver_consultas'))  # Redirigir a la página de consultas

    except Exception as err:
        flash(f'Error al actualizar el estado: {err}', 'error')
        return redirect(url_for('consulta.ver_consultas'))  # Redirigir en caso de error

