from flask import Flask
from util.db import engine_uri, db
from model import models
from flask_smorest import Api

from controller.pengguna_controller import pengguna_blp
from controller.lahan_controller import lahan_blp


def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Capstone REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = engine_uri

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = Api(app)
    with app.app_context():
        db.create_all()

    api.register_blueprint(pengguna_blp)
    api.register_blueprint(lahan_blp)

    return app
