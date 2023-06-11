from flask import jsonify
from model.models import LahanModel, PenggunaModel
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
                    jsonify({"error": True, "message": "User not found", "data": None}),
                    404,
                )
            else:
                lahan = (
                    LahanModel.query.filter_by(user_id=current_user)
                    .filter(LahanModel.deleted_at.is_(None))
                    .all()
                )

                lahans_list = []

                if lahan is None:
                    lahan = {}
                else:
                    for lahans_item in lahan:
                        lahan = {
                            "id": lahans_item.id,
                            "nama": lahans_item.nama,
                            "photo": lahans_item.photo,
                            "luas": lahans_item.luas,
                            "alamat": lahans_item.alamat,
                            "lat": lahans_item.lat,
                            "lon": lahans_item.lon,
                        }
                        lahans_list.append(lahan)

                pengguna = {
                    "id": data.id,
                    "username": data.username,
                    "email": data.email,
                    "photo": data.photo,
                    "premium": data.premium,
                    "terakhir_login": data.terakhir_login,
                    "lahan": lahans_list,
                }
            # pengguna_schema = UserLahanSchema()

            response_data = {
                "error": False,
                "message": "User data fetched successfully",
                "data": pengguna,
            }
            return jsonify(response_data), 200
        except Exception as e:
            print(e)
