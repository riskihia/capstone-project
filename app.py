from flask import Flask
from controller import *
from datetime import datetime
import pytz, os
from util.config import db, Config
from flask_smorest import Api
from util import jwt_config
from util.dumy_data import populate_data


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
        populate_data()

    blueprints = [
        user_controller.user_blp,
        lahan_controller.lahan_blp,
        auth_controller.auth_blp,
    ]

    for bp in blueprints:
        api.register_blueprint(bp)

    return app


app = create_app()
