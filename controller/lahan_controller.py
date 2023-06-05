from flask.views import MethodView
from flask_smorest import Blueprint
from model.models import LahanModel
from schemas import PostLahanSchema

from service.lahan_service import LahanService
from flask_jwt_extended import jwt_required
from flask import jsonify, request

lahan_blp = Blueprint(
    "lahan", __name__, url_prefix="/api/v1", description="Option in lahan"
)


@lahan_blp.route("/lahan")
class Lahan(MethodView):
    @jwt_required()
    @lahan_blp.response(200, PostLahanSchema(many=True))
    def get(self):
        return LahanService().get_user_lahan()

    @jwt_required()
    @lahan_blp.arguments(PostLahanSchema)
    def post(self, lahan_data):
        return LahanService().post_lahan(lahan_data)


@lahan_blp.route("/lahan/<lahan_id>")
class DeleteLahan(MethodView):
    @jwt_required()
    def delete(self, lahan_id):
        # lahan = LahanModel.query.get_or_404(lahan_id)
        # return lahan
        # lahan = lahan_id
        print(str(lahan_id))
        return jsonify({"hai": "hai"})
        # return LahanService().delete_lahan(lahan_id)
