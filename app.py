from flask import Flask
from datetime import datetime
import pytz


from util.db import engine_uri, db, getconn

# from util.db import engine_uri, db


from flask_jwt_extended import JWTManager
from model import models
from flask_smorest import Api

from controller.pengguna_controller import pengguna_blp
from controller.lahan_controller import lahan_blp

from google.cloud.sql.connector import Connector, IPTypes
import pymysql, sqlalchemy, os


def getconn():
    with Connector() as connector:
        conn = connector.connect(
            "testing-flask-api:asia-southeast2:flask-api-db-instance",  # Cloud SQL Instance Connection Name
            "pymysql",
            user="riski-db",
            password="riski123",
            db="tani_aid",
            ip_type=IPTypes.PUBLIC,  # IPTypes.PRIVATE for private IP
        )
        return conn


def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Capstone REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api/v1/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # ini untuk development
    # app.config["SQLALCHEMY_DATABASE_URI"] = engine_uri

    # ini untuk dpeloy
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"creator": getconn}

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["TIMEZONE"] = "Asia/Jakarta"

    @app.before_request
    def set_timezone():
        # Mengubah zona waktu pada setiap permintaan sebelum diproses
        timezone = pytz.timezone(app.config["TIMEZONE"])
        datetime.now(timezone)

    db.init_app(app)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "283674515990178098796700912839185640515"
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(pengguna_blp)
    api.register_blueprint(lahan_blp)

    return app
