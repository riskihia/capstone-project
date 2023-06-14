from flask.views import MethodView
from flask_smorest import Blueprint
from model.models import LahanModel
from schemas import PostLahanSchema, GetLahanSchema, TanamSchema
from util.example_response import (
    GetLahanExample,
    PostLahanExample,
    DeleteLahanExample,
    GetLahanIdExample,
)
from service.lahan_service import LahanService
from flask_jwt_extended import jwt_required
from flask import jsonify, request

lahan_blp = Blueprint(
    "lahan", __name__, url_prefix="/api/v1", description="Option in lahan"
)


@lahan_blp.route("/lahan")
class Lahan(MethodView):
    @jwt_required()
    @lahan_blp.response(200, GetLahanSchema(many=True))
    @lahan_blp.response(200, example=GetLahanExample)
    def get(self):
        return LahanService().get_user_lahan()

    @jwt_required()
    @lahan_blp.arguments(PostLahanSchema)
    @lahan_blp.response(201, example=PostLahanExample)
    def post(self, lahan_data):
        return LahanService().post_lahan(lahan_data)


@lahan_blp.route("/lahan/<string:lahan_id>")
class DeleteLahan(MethodView):
    @jwt_required()
    @lahan_blp.response(200, example=GetLahanIdExample)
    def get(self, lahan_id):
        return LahanService().get_lahan_details(lahan_id)

    @jwt_required()
    @lahan_blp.response(200, example=DeleteLahanExample)
    def delete(self, lahan_id):
        return LahanService().delete_lahan(lahan_id)
