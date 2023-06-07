from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from service.bibit_service import BibitService

bibit_blp = Blueprint(
    "bibit", __name__, url_prefix="/api/v1", description="Option in bibit"
)


@bibit_blp.route("/bibit")
class GetBibit(MethodView):
    @jwt_required()
    def get(self):
        return BibitService().get_all_bibit()
