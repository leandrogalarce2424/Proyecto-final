from flask import Flask


def create_app():
    app = Flask(__name__)

    app.secret_key = "tu_clave_secreta_aqui"

    from .routes.main import main
    from .routes.listar import listar_bp
    from .routes.listar import editar_bp
    app.register_blueprint(main)
    app.register_blueprint(listar_bp)
    app.register_blueprint(editar_bp)
    
    return app