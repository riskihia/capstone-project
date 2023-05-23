from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify

from util.db import db
from model.models import PenggunaModel
from schemas import PenggunaSchema

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from service.pengguna_service import PenggunaService

pengguna_blp = Blueprint("pengguna", __name__, description="Option in pengguna")


@pengguna_blp.route("/pengguna")
class Pengguna(MethodView):
    # decorator untuk documentation
    @pengguna_blp.response(200, PenggunaSchema(many=True))
    def get(self):
        return jsonify(PenggunaService().get_all_user()), 200

    @pengguna_blp.arguments(PenggunaSchema)
    @pengguna_blp.response(200, PenggunaSchema)
    def post(self, store_data):
        pengguna = PenggunaModel(**store_data)
        try:
            db.session.add(pengguna)
            db.session.commit()
        except IntegrityError:
            abort(400, message="a store with that name already exits")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting item")

        return pengguna
