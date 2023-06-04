from flask import Flask
from controller import *
from datetime import datetime
import pytz, os
from util.config import db, Config
from flask_smorest import Api
from util import jwt_config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-key-bucket.json"

    @app.before_request
    def set_timezone():
        timezone = pytz.timezone(app.config["TIMEZONE"])
        datetime.now(timezone)

    db.init_app(app)
    jwt_config.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    blueprints = [
        pengguna_controller.pengguna_blp,
        lahan_controller.lahan_blp,
        upload.upload_blp,
        user_controller.user_blp,
        lahan_image_controller.lahan_image_blp,
    ]

    for bp in blueprints:
        api.register_blueprint(bp)

    return app


app = create_app()
