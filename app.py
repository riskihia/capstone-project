from flask import Flask, jsonify
from datetime import datetime, timedelta
import pytz

from util.blocklist import BLOCKLIST
from flask_migrate import Migrate

# from util.db import db, getconn

from util.db import engine_uri, db


from flask_jwt_extended import JWTManager
from model import models
from flask_smorest import Api

from controller.pengguna_controller import pengguna_blp
from controller.lahan_controller import lahan_blp
from controller.upload import upload_blp
from controller.user_controller import user_blp
from controller.lahan_image_controller import lahan_image_blp

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
    app.config["UPLOAD_FOLDER"] = "static"

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Capstone REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api/v1/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-key-bucket.json"

    # ini untuk development
    app.config["SQLALCHEMY_DATABASE_URI"] = engine_uri

    # ini untuk dpeloy
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://"
    # app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"creator": getconn}

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["TIMEZONE"] = "Asia/Jakarta"

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

    @app.before_request
    def set_timezone():
        # Mengubah zona waktu pada setiap permintaan sebelum diproses
        timezone = pytz.timezone(app.config["TIMEZONE"])
        datetime.now(timezone)

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "283674515990178098796700912839185640515"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "message": "Token expired",
                    "error": True,
                    "data": None,
                }
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Invalid token",
                    "error": True,
                    "data": None,
                }
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api.register_blueprint(pengguna_blp)
    api.register_blueprint(lahan_blp)
    api.register_blueprint(upload_blp)
    api.register_blueprint(user_blp)
    api.register_blueprint(lahan_image_blp)

    return app
