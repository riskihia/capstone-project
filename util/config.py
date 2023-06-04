from datetime import timedelta
import os
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()


class Config(object):
    HOST = str(os.environ.get("DB_HOST"))
    DATABASE = str(os.environ.get("DB_DATABASE"))
    USERNAME = str(os.environ.get("DB_USERNAME"))
    PASSWORD = str(os.environ.get("DB_PASSWORD"))

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://" + USERNAME + ":" + PASSWORD + "@" + HOST + "/" + DATABASE
    )
    SQLALCHEMY_TRACK_MODIFICAIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Capstone REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/api/v1/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    TIMEZONE = "Asia/Jakarta"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    JWT_SECRET_KEY = "283674515990178098796700912839185640515"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"


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
