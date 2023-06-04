from flask import Flask, jsonify
from datetime import datetime, timedelta
import pytz

from util.blocklist import BLOCKLIST

from util.config import db, Config


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
from util import jwt_config


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

    app.config.from_object(Config)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-key-bucket.json"

    @app.before_request
    def set_timezone():
        # Mengubah zona waktu pada setiap permintaan sebelum diproses
        timezone = pytz.timezone(app.config["TIMEZONE"])
        datetime.now(timezone)

    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    app.config["JWT_SECRET_KEY"] = "283674515990178098796700912839185640515"
    jwt = JWTManager(app)
    api.register_blueprint(pengguna_blp)
    api.register_blueprint(lahan_blp)
    api.register_blueprint(upload_blp)
    api.register_blueprint(user_blp)
    api.register_blueprint(lahan_image_blp)

    jwt_config.init_app(app)

    return app


app = create_app()
