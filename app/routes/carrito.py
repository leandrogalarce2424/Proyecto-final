from flask import Blueprint, render_template,url_for,redirect,flash
from app.conecion_bd import obtener_conexion

carrito_bp = Blueprint("carrito", __name__)





@carrito_bp.route('/add_to_cart/<int:pintura_id>', methods=['POST',"GET"])
def add_to_cart(pintura_id):
    # Supón que el usuario ya está logueado y su id es conocido
    user_id = 1  # Cambia esto para que obtengas el id real del usuario logueado

    conexion = obtener_conexion()
    cursor = conexion.cursor()
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

    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('carrito.cart'))

@carrito_bp.route('/cart')
def cart():
    user_id = 1  # Cambia esto para que obtengas el id real del usuario logueado
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Obtén los artículos del carrito
    cursor.execute("""
        SELECT c.id, p.nombre, p.detalle, p.precio, c.cantidad, p.foto
        FROM carrito c
        JOIN pintura p ON c.pintura_id = p.idpintura
        WHERE c.user_id = %s
    """, (user_id,))
    
    cart_items = cursor.fetchall()
    total = sum(item[3] * item[4] for item in cart_items)  # Calcula el total (precio * cantidad)
    
    cursor.close()
    conexion.close()
    return render_template('carrito.html', cart=cart_items, total=total)
