from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify

from util.db import db
from model.models import LahanModel
from schemas import LahanSchema

lahan_blp = Blueprint("lahan", __name__, description="Option in lahan")


@lahan_blp.route("/lahan")
class Lahan(MethodView):
    @lahan_blp.response(200, LahanSchema(many=True))
    def get(self):
        data = LahanModel.query.all()
        lahan_schema = LahanSchema(many=True)
        response_data = {
            "status_code": 200,
            "msg": "Data retrieved successfully",
            "data": lahan_schema.dump(data),
        }
        return jsonify(response_data)
