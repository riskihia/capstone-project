from flask.views import MethodView
from flask_smorest import Blueprint
from service.tanam_service import TanamService
from schemas import PostTanamSchema, ExecTanamSchema
from flask_jwt_extended import jwt_required
from flask import jsonify

tanam_blp = Blueprint(
    "tanam", __name__, url_prefix="/api/v1", description="Option in tanam"
)


@tanam_blp.route("/tanam/plan")
class AddTanam(MethodView):
    @jwt_required()
    @tanam_blp.arguments(PostTanamSchema)
    def post(self, data_tanam):
        return TanamService().post_tanam(data_tanam)


@tanam_blp.route("/tanam/exec")
class ExecTanam(MethodView):
    @jwt_required()
    @tanam_blp.arguments(ExecTanamSchema)
    def post(self, data_tanam):
        return TanamService().exec_post_tanam(data_tanam)
