from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify
from util.example_response import UserAuthExample

base_blp = Blueprint("base", __name__, url_prefix="", description="Option in BASE")


@base_blp.route("/")
class Base(MethodView):
    def get(self):
        return jsonify(
            {
                "status": "ok",
                "Application Nama": "TaniLand",
                "Team": [
                    "Khazim Fikri Al-Fadhli",
                    "Nabillah Griselda Ghinafauz",
                    "Riski Rahmat Hia",
                    "Mohammad Nizar Ardansyah",
                    "Salsabila Tjahya Kusuma Putri",
                    "Syafira Alifah",
                ],
                "Description": "TaniLand : Aplikasi Manajemen Lahan Tani Berbasis Teknologi",
                "Api Prefix": "/api/v1",
                "Api Documentation": "https://cicd-qkb7fzajaq-uc.a.run.app/api/v1/swagger-ui",
                "Api Repository": "https://github.com/riskihia/capstone-project.git",
            }
        )
