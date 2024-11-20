from flask import Blueprint, render_template,url_for,redirect,flash,session,request
from app.conecion_bd import obtener_conexion

carrito_bp = Blueprint("carrito", __name__)





@carrito_bp.route('/add_to_cart', methods=['POST', "GET"])
def add_to_cart():
    # Supón que el usuario ya está logueado y su id es conocido
    user_id = session.get("idusuarios")  # Cambia esto para que obtengas el id real del usuario logueado

    # Obtener los parámetros de la solicitud
    pintura_id = request.args.get('pintura_id')  # Si se pasa pintura_id en la URL
    ruedas_id = request.args.get('ruedas_id')  # Si se pasa ruedas_id en la URL
    print(f"idpintura{pintura_id} idruedas{ruedas_id}")
    if (pintura_id and ruedas_id) or (not pintura_id and not ruedas_id):
        # Verifica que solo uno de los parámetros esté presente
        flash('Debes proporcionar solo uno de los parámetros: pintura_id o ruedas_id.', 'error')
        return redirect(url_for('carrito.cart'))

    # Conectar a la base de datos
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if pintura_id:  # Si se recibe pintura_id
        # Verifica si la pintura ya está en el carrito
        cursor.execute("SELECT id, cantidad FROM carrito WHERE user_id = %s AND pintura_id = %s", (user_id, pintura_id))
        existing_item = cursor.fetchone()

        if existing_item:
            # Si la pintura ya está en el carrito, actualiza la cantidad
            new_quantity = existing_item[1] + 1
            cursor.execute("UPDATE carrito SET cantidad = %s WHERE id = %s", (new_quantity, existing_item[0]))
            flash('Se actualizó la cantidad de la pintura en tu carrito', 'success')
        else:
            # Si la pintura no está en el carrito, agrégala
            cursor.execute("INSERT INTO carrito (user_id, pintura_id, cantidad) VALUES (%s, %s, %s)", (user_id, pintura_id, 1))
            flash('La pintura fue agregada a tu carrito', 'success')

    elif ruedas_id:  # Si se recibe ruedas_id
        # Verifica si las ruedas ya están en el carrito
        cursor.execute("SELECT id, cantidad FROM carrito WHERE user_id = %s AND ruedas_id = %s", (user_id, ruedas_id))
        existing_item = cursor.fetchone()

        if existing_item:
            # Si las ruedas ya están en el carrito, actualiza la cantidad
            new_quantity = existing_item[1] + 1
            cursor.execute("UPDATE carrito SET cantidad = %s WHERE id = %s", (new_quantity, existing_item[0]))
            flash('Se actualizó la cantidad de las ruedas en tu carrito', 'success')
        else:
            # Si las ruedas no están en el carrito, agrégalas
            cursor.execute("INSERT INTO carrito (user_id, ruedas_id, cantidad) VALUES (%s, %s, %s)", (user_id, ruedas_id, 1))
            flash('Las ruedas fueron agregadas a tu carrito', 'success')

    # Guardar cambios y cerrar la conexión
    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect(url_for('carrito.cart'))

@carrito_bp.route('/cart')
def cart():
    user_id = session["idusuarios"]  # Cambia esto para que obtengas el id real del usuario logueado
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtén los artículos del carrito (tanto pinturas como ruedas)
    cursor.execute("""
        SELECT c.id, p.nombre, p.detalle, p.precio, c.cantidad, p.foto, 'pintura' AS tipo
        FROM carrito c
        JOIN pintura p ON c.pintura_id = p.idpintura
        WHERE c.user_id = %s
        UNION
        SELECT c.id, r.nombre, r.detalle, r.precio, c.cantidad, r.foto, 'rueda' AS tipo
        FROM carrito c
        JOIN ruedas r ON c.ruedas_id = r.idruedas
        WHERE c.user_id = %s
    """, (user_id, user_id))

    cart_items = cursor.fetchall()
    total = sum(item[3] * item[4] for item in cart_items)  # Calcula el total (precio * cantidad)
    
    cursor.close()
    conexion.close()
    
    return render_template('carrito.html', cart=cart_items, total=total)


@carrito_bp.route('/vaciar_carrito', methods=['POST'])
def vaciar_carrito():
    user_id = session["idusuarios"]  # Asegúrate de que este dato está disponible en la sesión

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Eliminar todos los elementos del carrito para el usuario actual
        cursor.execute("DELETE FROM carrito WHERE user_id = %s", (user_id,))
        conexion.commit()
        flash('El carrito ha sido vaciado con éxito.', 'success')
    except Exception as e:
        conexion.rollback()
        flash('Hubo un problema al vaciar el carrito. Intenta nuevamente.', 'danger')
        print(f"Error al vaciar el carrito: {e}")
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for('carrito.cart'))

@carrito_bp.route('/eliminar_articulo/<int:item_id>', methods=['POST','GET'])
def eliminar_articulo(item_id):
    user_id = session.get("idusuarios")  # Obtén el ID del usuario logueado

    # Conectar a la base de datos
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Eliminar el artículo del carrito basado en el ID y el usuario
        cursor.execute("DELETE FROM carrito WHERE user_id = %s AND id = %s", (user_id, item_id))
        conexion.commit()
        flash('El artículo ha sido eliminado del carrito.', 'success')
    except Exception as e:
        conexion.rollback()
        flash('Hubo un problema al eliminar el artículo del carrito. Intenta nuevamente.', 'danger')
        print(f"Error al eliminar el artículo: {e}")
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for('carrito.cart'))
