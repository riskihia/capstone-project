from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from schemas import UserLahanSchema
from flask import jsonify
from service.pengguna_service import PenggunaService

user_blp = Blueprint(
    "user", __name__, url_prefix="/api/v1", description="Option in user"
)


@user_blp.route("/user")
class GetUser(MethodView):
    @jwt_required()
    @user_blp.response(200, UserLahanSchema(many=True))
    def get(self):
        return PenggunaService().get_user_detail()
