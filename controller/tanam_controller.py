from flask.views import MethodView
from flask_smorest import Blueprint
from service.tanam_service import TanamService
from schemas import (
    PostTanamSchema,
    ExecTanamSchema,
    CloseTanamSchema,
    RekomendasiTanamSchema,
    RekomendasiTanamIotSchema,
)
from flask_jwt_extended import jwt_required
from flask import jsonify, request

tanam_blp = Blueprint(
    "tanam", __name__, url_prefix="/api/v1", description="Option in tanam"
)


@tanam_blp.route("/tanam/plan")
class AddTanam(MethodView):
    @jwt_required()
    @tanam_blp.arguments(PostTanamSchema)
    def post(self, data_tanam):
        return TanamService().post_tanam(data_tanam)


@tanam_blp.route("/tanam/<id>")
class DelTanam(MethodView):
    @jwt_required()
    def delete(self, id):
        return TanamService().delete_tanam(id)


@tanam_blp.route("/tanam/exec")
class ExecTanam(MethodView):
    @jwt_required()
    @tanam_blp.arguments(ExecTanamSchema)
    def post(self, data_tanam):
        return TanamService().exec_post_tanam(data_tanam)


@tanam_blp.route("/tanam/close")
class CloseTanam(MethodView):
    @jwt_required()
    def get(self):
        lahan_id = request.args.get("lahan_id")
        return TanamService().get_close_tanam(lahan_id)

    @jwt_required()
    @tanam_blp.arguments(CloseTanamSchema)
    def post(self, data_tanam):
        return TanamService().close_post_tanam(data_tanam)


@tanam_blp.route("/tanam/rekomendasi/gambar")
class RekomendasiTanam(MethodView):
    @jwt_required()
    @tanam_blp.arguments(RekomendasiTanamSchema)
    def post(self, data_image):
        return TanamService().rekomendasi_tanam(data_image)


@tanam_blp.route("/tanam/rekomendasi/iot")
class RekomendasiIotTanam(MethodView):
    @jwt_required()
    @tanam_blp.arguments(RekomendasiTanamIotSchema)
    def post(self, iot_id):
        return TanamService().rekomendasi_tanam_iot(iot_id)
