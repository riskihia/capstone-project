from flask import jsonify
from model.models import PenggunaModel
from schemas import UserLahanSchema
from util.config import db

from flask_jwt_extended import get_jwt_identity


class UserService:
    def __init__(self):
        pass

    def get_user_detail(self):
        current_user = get_jwt_identity()
        try:
            data = (
                PenggunaModel.query.filter_by(id=current_user)
                .filter(PenggunaModel.deleted_at.is_(None))
                .first()
            )
            if not data:
                return (
                    jsonify(
                        {"error": True, "message": "User not found", "data": None}),
                    404,
                )
            pengguna_schema = UserLahanSchema()
            response_data = {
                "error": False,
                "message": "User data fetched successfully",
                "data": pengguna_schema.dump(data),
            }
            return jsonify(response_data), 200
        except Exception as e:
            print(e)


    def get_all_pengguna(self):
        try:
            data = PenggunaModel.query.filter(
                PenggunaModel.deleted_at.is_(None)).all()

            pengguna_schema = PlainPenggunaSchema(many=True)

            response_data = {
                "error": False,
                "message": "User data fetched successfully",
                "data": pengguna_schema.dump(data),
            }
            return response_data
        except Exception as e:
            print(e)

