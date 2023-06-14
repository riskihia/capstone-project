from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import PostIotSchema, PostIotResetSchema
from service.iot_service import IotService
from flask_jwt_extended import jwt_required
from util.example_response import (
    UserAuthExample,
    GetIot,
    GetIotNotfound,
    PostIot,
    PostIotNotfound,
    PostIotAlready,
    PostIotReset,
    PostIotResetNotfound,
)

iot_blp = Blueprint("iot", __name__, url_prefix="/api/v1", description="Option in iot")


@iot_blp.route("/iot/<iot_id>")
class GetIot(MethodView):
    @jwt_required()
    @iot_blp.response(200, example=GetIot)
    @iot_blp.alt_response(404, example=GetIotNotfound, description="Iot not found")
    def get(self, iot_id):
        return IotService().get_iot(iot_id)


@iot_blp.route("/iot")
class PostIot(MethodView):
    @jwt_required()
    @iot_blp.arguments(PostIotSchema)
    @iot_blp.response(200, example=PostIot)
    @iot_blp.alt_response(404, example=PostIotAlready, description="Iot already used")
    @iot_blp.alt_response(404, example=PostIotNotfound, description="Iot Not Found")
    def post(self, data_id):
        return IotService().post_iot(data_id)


@iot_blp.route("/iot/reset")
class PostIotReset(MethodView):
    @jwt_required()
    @iot_blp.arguments(PostIotResetSchema)
    @iot_blp.response(200, example=PostIotReset)
    @iot_blp.response(404, example=PostIotResetNotfound, description="Iot Not Found")
    def post(self, iot_id):
        return IotService().post_iot_reset(iot_id)
