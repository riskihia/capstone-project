from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import UserLahanSchema
from service.user_service import UserService
from flask_jwt_extended import jwt_required

user_blp = Blueprint(
    "user", __name__, url_prefix="/api/v1", description="Option in pengguna"
)


@user_blp.route("/user")
class GetUser(MethodView):
    @jwt_required()
    @user_blp.response(200, UserLahanSchema(many=True))
    def get(self):
        return UserService().get_user_detail()
