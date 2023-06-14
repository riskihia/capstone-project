from flask.views import MethodView
from flask_smorest import Blueprint
from service.plant_recomendation_service import PlantRecomendationService
from flask_jwt_extended import jwt_required
from flask import request


plant_recomendation_blp = Blueprint(
    "plant_recomendation",
    __name__,
    url_prefix="/api/v1",
    description="Option in plant recomendation",
)


@plant_recomendation_blp.route("/plant_recomendation")
class Plant_recomendation(MethodView):
    @jwt_required()
    @plant_recomendation_blp.response(200)
    def get(self):
        return PlantRecomendationService().get_plant_recomendation()

    @jwt_required()
    # @plant_recomendation_blp.arguments(PostLahanSchema)
    def post(self):
        data = request.get_json()
        humidity = data.get("humidity")
        temperature = data.get("temperature")
        return PlantRecomendationService().predict(humidity, temperature)
