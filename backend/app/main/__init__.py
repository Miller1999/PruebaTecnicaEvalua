from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api  # Importaciones para Swagger
from .config import config_by_name
from .constants import ORIGINS
import os
import jinja2
from app.main.dto.inventory_dto import InventoryDto  # Importar el DTO de inventario

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
migrate = Migrate()


def create_app(config_name):
    cwd = os.getcwd()
    template_dir = os.path.abspath("../../templates")
    static_dir = os.path.abspath("../../templates/dist/static")

    app = Flask(
        __name__,
        static_folder="../../templates/dist/static",
        template_folder="../template",
    )
    app.jinja_loader = jinja2.FileSystemLoader("../files/templates")
    app.config.from_object(config_by_name[config_name])

    # Inicializa CORS
    CORS(
        app,
        origins=ORIGINS,
        supports_credentials=True,
        expose_headers="Content-Disposition",
    )

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization, Content-Disposition",
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS"
        )
        return response

    db.init_app(app)
    flask_bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Configuración de Swagger
    api = Api(
        app,
        version="1.0",
        title="API de Inventario",
        description="Documentación de la API para el sistema de inventario",
        doc="/swagger",  # URL donde se servirá la documentación Swagger
    )

    # Registrar el namespace de inventario
    api.add_namespace(InventoryDto.api)

    return app
