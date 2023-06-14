from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from service.auth_service import AuthService
from schemas import (
    AuthLogoutSchema,
    AuthPenggunaSchema,
    UserLahanSchema,
)
from util.example_response import GetAuthExample, UserAuthExample, LogoutAuthExample

auth_blp = Blueprint(
    "auth", __name__, url_prefix="/api/v1", description="Option in pengguna"
)


@auth_blp.route("/user")
class GetUser(MethodView):
    @jwt_required()
    @auth_blp.response(200, UserLahanSchema(many=True))
    @auth_blp.response(200, example=UserAuthExample)
    def get(self):
        return AuthService().get_user_detail()


@auth_blp.route("/logout")
class PenggunaAuthLogout(MethodView):
    @jwt_required()
    @auth_blp.arguments(AuthLogoutSchema)
    @auth_blp.response(200, AuthLogoutSchema)
    @auth_blp.response(200, example=LogoutAuthExample)
    def post(self, store_data):
        return AuthService().pengguna_logout(store_data)


@auth_blp.route("/auth")
class PenggunaAuth(MethodView):
    @auth_blp.arguments(AuthPenggunaSchema)
    @auth_blp.response(
        202,
        example=GetAuthExample,
    )
    def post(self, store_data):
        return AuthService().tambah_pengguna(store_data)
