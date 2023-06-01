from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
import uuid, datetime

from util.db import db
from model.models import PenggunaModel
from schemas import PenggunaSchema
from schemas import AuthPenggunaSchema
from schemas import AuthLogoutSchema

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from service.pengguna_service import PenggunaService
from service.auth_service import AuthService

from flask_jwt_extended import jwt_required

pengguna_blp = Blueprint(
    "pengguna", __name__, url_prefix="/api/v1", description="Option in pengguna"
)


@pengguna_blp.route("/auth/logout")
class PenggunaAuthLogout(MethodView):
    @jwt_required()
    @pengguna_blp.arguments(AuthLogoutSchema)
    @pengguna_blp.response(200, AuthLogoutSchema)
    def post(self, store_data):
        return AuthService().pengguna_logout(store_data)


@pengguna_blp.route("/auth")
class PenggunaAuth(MethodView):
    @pengguna_blp.response(200, PenggunaSchema(many=True))
    def get(self):
        return jsonify(PenggunaService().get_all_pengguna()), 200

    @pengguna_blp.arguments(AuthPenggunaSchema)
    # @pengguna_blp.response(200, PenggunaSchema)
    @pengguna_blp.response(
        202,
        description="Berhasil upload data.",
        example={
            "data": {
                "email": "user5@example.com",
                "id": "daaa2c25-3550-47fa-869d-f5bcc0b5e675",
                "photo": None,
                "premium": False,
                "terakhir_login": "Wed, 31 May 2023 07:26:54 GMT",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NTQ5MjgxNCwianRpIjoiMWRkMzUwYmUtNWRmMC00MWQzLWE2NzItOGE5MTNhMzRlZjM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRhYWEyYzI1LTM1NTAtNDdmYS04NjlkLWY1YmNjMGI1ZTY3NSIsIm5iZiI6MTY4NTQ5MjgxNCwiZXhwIjoxNjg1NDkzNzE0fQ.DmD_Cq74ualPQGYKtQp9aM2Mq16L3ukDFYsC50YUX0g",
                "username": "user5",
            },
            "error": False,
            "message": "User successfully registered",
        },
    )
    def post(self, store_data):
        return AuthService().tambah_pengguna(store_data)


@pengguna_blp.route("/pengguna")
class Pengguna(MethodView):
    # decorator untuk documentation
    @pengguna_blp.response(200, PenggunaSchema(many=True))
    def get(self):
        return jsonify(PenggunaService().get_all_pengguna()), 200

    @jwt_required(optional=True)
    @pengguna_blp.arguments(PenggunaSchema)
    @pengguna_blp.response(200, PenggunaSchema)
    def post(self, store_data):
        return PenggunaService().tambah_pengguna(store_data)
