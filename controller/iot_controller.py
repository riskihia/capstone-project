from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import PostIotSchema, PostIotResetSchema
from service.iot_service import IotService
from flask_jwt_extended import jwt_required
from util.example_response import UserAuthExample

iot_blp = Blueprint("iot", __name__, url_prefix="/api/v1", description="Option in iot")


@iot_blp.route("/iot/<iot_id>")
class GetIot(MethodView):
    @jwt_required()
    def get(self, iot_id):
        return IotService().get_iot(iot_id)


@iot_blp.route("/iot")
class PostIot(MethodView):
    @jwt_required()
    @iot_blp.arguments(PostIotSchema)
    def post(self, data_id):
        return IotService().post_iot(data_id)


@iot_blp.route("/iot/reset")
class PostIotReset(MethodView):
    @jwt_required()
    @iot_blp.arguments(PostIotResetSchema)
    def post(self, iot_id):
        return IotService().post_iot_reset(iot_id)
