#services/pedidos/project/__init__.py


import os  #nuevo

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#iinstanciando la db
db = SQLAlchemy()


# new 
def create_app(script_info=None):

    # instanciamos la app
    app = Flask(__name__)

# estableciendo configuracion
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

# establecemos extensiones
    db.init_app(app);

# registrar blueprints
    from project.api.pedidos import pedidos_blueprint
    app.register_blueprint(pedidos_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app;



