from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from service.bibit_service import BibitService

hasil_iot_blp = Blueprint(
    "hasil_iot", __name__, url_prefix="/api/v1", description="Option in hasil iot"
)


@hasil_iot_blp.route("/hasil-iot")
class GetBibit(MethodView):
    @jwt_required()
    def get(self):
        return BibitService().get_all_bibit()
