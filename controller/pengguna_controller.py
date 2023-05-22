from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify

from util.db import db
from model.models import PenggunaModel
from schemas import PenggunaSchema

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

pengguna_blp = Blueprint("pengguna", __name__, description="Option in pengguna")


@pengguna_blp.route("/pengguna")
class Pengguna(MethodView):
    # decorator untuk documentation
    @pengguna_blp.response(200, PenggunaSchema(many=True))
    def get(self):
        data = PenggunaModel.query.all()
        pengguna_schema = PenggunaSchema(many=True)
        response_data = {
            "status_code": 200,
            "msg": "Data retrieved successfully",
            "data": pengguna_schema.dump(data),
        }
        return jsonify(response_data)

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
