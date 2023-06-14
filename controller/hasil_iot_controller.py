from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from service.bibit_service import BibitService
from service.hasil_iot_service import HasilIotService
from util.example_response import GetHasilIot

hasil_iot_blp = Blueprint(
    "hasil_iot", __name__, url_prefix="/api/v1", description="Option in hasil iot"
)


@hasil_iot_blp.route("/hasil-iot")
class GetBibit(MethodView):
    @hasil_iot_blp.response(201, example=GetHasilIot)
    def get(self):
        suhu = request.args.get("suhu")
        kelembaban_udara = request.args.get("kelembaban_udara")
        iot_id = request.args.get("iot_id")

        return HasilIotService().tambah_hasil_iot(suhu, kelembaban_udara, iot_id)
