from flask.views import MethodView
from flask_smorest import Blueprint
from service.soil_prediction_service import SoilPredictionService
from flask_jwt_extended import jwt_required
from flask import request


soil_prediction_blp = Blueprint(
    "soil_prediction", __name__, url_prefix="/api/v1", description="Option in soil prediction"
)


@soil_prediction_blp.route("/soil_prediction")
class Soil_prediction(MethodView):
    # @jwt_required()
    @soil_prediction_blp.response(200)
    def get(self):
        return SoilPredictionService().get_soil_class()

    # @jwt_required()
    # @plant_recomendation_blp.arguments(PostLahanSchema)
    def post(self):
        image = request.files["image"]
        return SoilPredictionService().predict(image)
