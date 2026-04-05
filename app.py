# from flask import Flask
# from flask_cors import CORS

# from extensions import db, migrate, ma
# from api import bp as api_bp
# import api.empleados  # asegura que las rutas se registren
# import models  # asegura que los modelos estén visibles para Alembic/Flask-Migrate


# def create_app():
#     app = Flask(__name__)

#     # Ajusta usuario/contraseña/host según tu entorno
#     app.config["SQLALCHEMY_DATABASE_URI"] = (
#         "mysql+pymysql://root:admin@localhost/recursos_humanos_db?charset=utf8mb4"
#     )
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config["JSON_AS_ASCII"] = False

#     # Extensiones
#     db.init_app(app)
#     migrate.init_app(app, db)
#     ma.init_app(app)

#     # CORS (abrimos para /api/*; ajusta origins según tu front)
#     CORS(app, resources={r"/api/*": {"origins": "*"}}) #  r -> raw (texto crudo)

#     # # CORS (útil si luego consumes desde Angular/React)
#     # CORS(app, resources={r"/api/*": {"origins": [
#     #     "http://localhost:4200", # angular
#     #     "http://localhost:5173", # react vite
#     #     "http://localhost:3001" # react
#     # ]}})

#     # Blueprints
#     app.register_blueprint(api_bp)

#     @app.get("/")
#     def inicio():
#         return "API de Recursos Humanos (Flask)"

#     return app


# if __name__ == "__main__":
#     create_app().run(debug=True)

# PRODUCCION

import os
from flask import Flask
from flask_cors import CORS

# Importación de tus extensiones y Blueprints existentes
from extensions import db, migrate, ma
from api import bp as api_bp
import api.empleados  # Registro de rutas
import models         # Modelos para SQLAlchemy/Alembic

def create_app():
    app = Flask(__name__)

    # --- CONFIGURACIÓN DE BASE DE DATOS ---
    # En Render, definiremos DATABASE_URL en el panel de control.
    # Si no existe, usará MySQL local por defecto.
    default_db = "mysql+pymysql://root:admin@localhost/recursos_humanos_db?charset=utf8mb4"
    database_url = os.environ.get("DATABASE_URL", default_db)

    # Corrección para PostgreSQL (Render/Neon a veces usan 'postgres://' que no es compatible con SQLAlchemy 2.0)
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_AS_ASCII"] = False

    # --- INICIALIZACIÓN DE EXTENSIONES ---
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # --- CONFIGURACIÓN DE CORS ---
    # Permitimos todos los orígenes para facilitar el despliegue inicial.
    # En un entorno real, aquí pondrías la URL de tu Vercel.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # --- REGISTRO DE BLUEPRINTS ---
    # app.register_blueprint(api_bp)

    # --- RUTA DE BIENVENIDA / TEST ---
    @app.get("/")
    def inicio():
        return {
            "mensaje": "API de Recursos Humanos funcionando",
            "estado": "Conectado",
            "base_de_datos": "Producción" if "DATABASE_URL" in os.environ else "Local"
        }

    with app.app_context():
        db.create_all()
    # -----------------------

    app.register_blueprint(api_bp)
    
    # @app.get("/")
    # def inicio():
    #     return {"mensaje": "API de Recursos Humanos funcionando"}

    return app

# Creamos la instancia global para que Gunicorn (Render) la detecte
app = create_app()

if __name__ == "__main__":
    # Render asigna dinámicamente un puerto a través de la variable PORT
    port = int(os.environ.get("PORT", 5000))
    # Usamos host 0.0.0.0 para que sea accesible externamente en la nube
    app.run(host='0.0.0.0', port=port, debug=True)