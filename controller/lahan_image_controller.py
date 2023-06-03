from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify

from util.db import db
from google.cloud import storage

from service.lahan_image_service import LahanImageService

lahan_image_blp = Blueprint(
    "lahan_image", __name__, url_prefix="/api/v1", description="Option in lahan image"
)


@lahan_image_blp.route("/lahan-image")
class LahanImage(MethodView):
    def get(self):
        return LahanImageService().get_image_urls("flask-api-bucket", "lahan_image")
        # return LahanImageService().get_lahan_image()

    def post(self):
        return LahanImageService().post_lahan_image()


@lahan_image_blp.route("/get-image")
class GetImage(MethodView):
    def get(self):
        return LahanImageService().post_image()
