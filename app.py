from flask import Flask
from flask_cors import CORS

from extensions import db, migrate, ma
from api import bp as api_bp
import api.empleados  # asegura que las rutas se registren
import models  # asegura que los modelos estén visibles para Alembic/Flask-Migrate


def create_app():
    app = Flask(__name__)

    # Ajusta usuario/contraseña/host según tu entorno
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:admin@localhost/recursos_humanos_db?charset=utf8mb4"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_AS_ASCII"] = False

    # Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # CORS (abrimos para /api/*; ajusta origins según tu front)
    CORS(app, resources={r"/api/*": {"origins": "*"}}) #  r -> raw (texto crudo)

    # # CORS (útil si luego consumes desde Angular/React)
    # CORS(app, resources={r"/api/*": {"origins": [
    #     "http://localhost:4200", # angular
    #     "http://localhost:5173", # react vite
    #     "http://localhost:3001" # react
    # ]}})

    # Blueprints
    app.register_blueprint(api_bp)

    @app.get("/")
    def inicio():
        return "API de Recursos Humanos (Flask)"

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

