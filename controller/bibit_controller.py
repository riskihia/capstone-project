from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from service.bibit_service import BibitService
from util.example_response import GetBibit

bibit_blp = Blueprint(
    "bibit", __name__, url_prefix="/api/v1", description="Option in bibit"
)


@bibit_blp.route("/bibit")
class GetBibit(MethodView):
    @jwt_required()
    @bibit_blp.response(200, example=GetBibit)
    def get(self):
        return BibitService().get_all_bibit()
