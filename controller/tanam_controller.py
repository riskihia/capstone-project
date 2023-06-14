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
from util.example_response import (
    PostTanamPlan,
    PostTanamPlanAlready,
    PostTanamPlanNotfound,
    DeleteTanam,
    DeleteTanamNotfound,
    PostTanamExec,
    PostTanamExecNotfound,
    GetTanamClose,
    GetTanamCloseNotfound,
    PostTanamClose,
    PostTanamCloseNotfound,
    PostTanamRekomendasi,
    PostTanamRekomendasiNot,
    PostRekomendasiIot,
    PostRekomendasiIotNotvalid,
)

tanam_blp = Blueprint(
    "tanam", __name__, url_prefix="/api/v1", description="Option in tanam"
)


@tanam_blp.route("/tanam/plan")
class AddTanam(MethodView):
    @jwt_required()
    @tanam_blp.arguments(PostTanamSchema)
    @tanam_blp.response(201, example=PostTanamPlan)
    @tanam_blp.alt_response(
        404, example=PostTanamPlanNotfound, description="Bibit or Tanam not found."
    )
    @tanam_blp.alt_response(
        400,
        example=PostTanamPlanAlready,
        description="Already have plan.",
    )
    def post(self, data_tanam):
        return TanamService().post_tanam(data_tanam)


@tanam_blp.route("/tanam/<id>")
class DelTanam(MethodView):
    @jwt_required()
    @tanam_blp.response(201, example=DeleteTanam)
    @tanam_blp.alt_response(
        404, example=DeleteTanamNotfound, description="Data Tanam tidak ditemukan"
    )
    def delete(self, id):
        return TanamService().delete_tanam(id)


@tanam_blp.route("/tanam/exec")
class ExecTanam(MethodView):
    @jwt_required()
    @tanam_blp.arguments(ExecTanamSchema)
    @tanam_blp.response(200, example=PostTanamExec)
    @tanam_blp.alt_response(
        404, example=PostTanamExecNotfound, description="Tanam or status not valid"
    )
    def post(self, data_tanam):
        return TanamService().exec_post_tanam(data_tanam)


@tanam_blp.route("/tanam/close")
class CloseTanam(MethodView):
    @jwt_required()
    @tanam_blp.response(200, example=GetTanamClose)
    @tanam_blp.alt_response(
        404, example=GetTanamCloseNotfound, description="Tanam Not Found"
    )
    def get(self):
        lahan_id = request.args.get("lahan_id")
        return TanamService().get_close_tanam(lahan_id)

    @jwt_required()
    @tanam_blp.arguments(CloseTanamSchema)
    @tanam_blp.response(200, example=PostTanamClose)
    @tanam_blp.alt_response(
        404, example=PostTanamCloseNotfound, description="Tanam Not Found"
    )
    def post(self, data_tanam):
        return TanamService().close_post_tanam(data_tanam)


@tanam_blp.route("/tanam/rekomendasi/gambar")
class RekomendasiTanam(MethodView):
    @jwt_required()
    @tanam_blp.arguments(RekomendasiTanamSchema)
    @tanam_blp.response(200, example=PostTanamRekomendasi)
    @tanam_blp.alt_response(
        404, example=PostTanamRekomendasiNot, description="Data tidak valid"
    )
    def post(self, data_image):
        return TanamService().rekomendasi_tanam(data_image)


@tanam_blp.route("/tanam/rekomendasi/iot")
class RekomendasiIotTanam(MethodView):
    @jwt_required()
    @tanam_blp.arguments(RekomendasiTanamIotSchema)
    @tanam_blp.response(200, example=PostRekomendasiIot)
    @tanam_blp.alt_response(
        404, example=PostRekomendasiIotNotvalid, description="Data Not Valid"
    )
    def post(self, iot_id):
        return TanamService().rekomendasi_tanam_iot(iot_id)
