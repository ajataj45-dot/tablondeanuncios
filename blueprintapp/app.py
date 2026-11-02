import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = 'clave_secreta_anuncios'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd_anuncios.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    # Importar modelos
    from blueprintapp.usuarios.models import Usuario
    from blueprintapp.categorias.models import Categoria
    from blueprintapp.anuncios.models import Anuncio

    # Importar rutas
    from blueprintapp.core.routes import bp_core
    from blueprintapp.auth.routes import bp_auth
    from blueprintapp.usuarios.routes import bp_usuario
    from blueprintapp.categorias.routes import bp_categoria
    from blueprintapp.anuncios.routes import bp_anuncio

    # Registrar Blueprints
    app.register_blueprint(bp_core)
    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_usuario, url_prefix='/usuarios')
    app.register_blueprint(bp_categoria, url_prefix='/categorias')
    app.register_blueprint(bp_anuncio, url_prefix='/anuncios')

    return app