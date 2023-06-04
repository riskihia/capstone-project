from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import PostLahanSchema

from service.lahan_service import LahanService
from flask_jwt_extended import jwt_required

lahan_blp = Blueprint(
    "lahan", __name__, url_prefix="/api/v1", description="Option in lahan"
)


@lahan_blp.route("/lahan")
class Lahan(MethodView):
    @jwt_required()
    @lahan_blp.response(200, PostLahanSchema(many=True))
    def get(self):
        return LahanService().get_all_lahan()

    @jwt_required()
    @lahan_blp.arguments(PostLahanSchema)
    def post(self, lahan_data):
        return LahanService().post_lahan(lahan_data)
