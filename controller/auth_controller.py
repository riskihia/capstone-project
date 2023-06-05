from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from service.auth_service import AuthService
from schemas import PlainPenggunaSchema, AuthLogoutSchema, AuthPenggunaSchema
from flask import jsonify
from service.user_service import UserService
from util.example_response import GetAuthExample
from util.example_response import LogoutAuthExample

auth_blp = Blueprint(
    "auth", __name__, url_prefix="/api/v1", description="Option in pengguna"
)


@auth_blp.route("/auth/logout")
class PenggunaAuthLogout(MethodView):
    @jwt_required()
    @auth_blp.arguments(AuthLogoutSchema)
    @auth_blp.response(200, AuthLogoutSchema)
    @auth_blp.response(200, example=LogoutAuthExample)
    def post(self, store_data):
        return AuthService().pengguna_logout(store_data)


@auth_blp.route("/auth")
class PenggunaAuth(MethodView):
    @auth_blp.response(200, PlainPenggunaSchema(many=True))
    def get(self):
        # return UserService().get_all_pengguna()
        return jsonify(UserService().get_all_pengguna()), 200

    @auth_blp.arguments(AuthPenggunaSchema)
    @auth_blp.response(
        202,
        example=GetAuthExample,
    )
    def post(self, store_data):
        return AuthService().tambah_pengguna(store_data)
