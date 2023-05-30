from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
import uuid, datetime

from util.db import db
from model.models import PenggunaModel
from schemas import PenggunaSchema
from schemas import AuthPenggunaSchema

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from service.pengguna_service import PenggunaService
from service.auth_service import AuthService

from flask_jwt_extended import jwt_required

pengguna_blp = Blueprint(
    "pengguna", __name__, url_prefix="/api/v1", description="Option in pengguna"
)


@pengguna_blp.route("/auth")
class PenggunaAuth(MethodView):
    @pengguna_blp.response(200, PenggunaSchema(many=True))
    def get(self):
        return jsonify(PenggunaService().get_all_pengguna()), 200

    @pengguna_blp.arguments(AuthPenggunaSchema)
    @pengguna_blp.response(200, PenggunaSchema)
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
