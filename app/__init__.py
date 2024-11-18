from flask import Flask


def create_app():
    app = Flask(__name__)

    app.secret_key = "tu_clave_secreta_aqui"

    from .routes.main import main
    from .routes.listar import listar_bp
    from .routes.listar import editar_bp
    from .routes.consultas import consulta_bp
    from .routes.pintura import pintura_bp
    from .routes.carrito import carrito_bp
    app.register_blueprint(main)
    app.register_blueprint(listar_bp)
    app.register_blueprint(editar_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(pintura_bp)
    app.register_blueprint(carrito_bp)
    return app