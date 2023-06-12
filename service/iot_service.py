from flask import jsonify
from model.models import IotModel, HasilIotModel, LahanModel
from schemas import UserLahanSchema
from util.config import db

from flask_jwt_extended import get_jwt_identity


class IotService:
    def __init__(self):
        pass

    def post_iot_reset(self, iot_id):
        id = iot_id["id"]
        iot = (
            IotModel.query.filter_by(id=id)
            .filter(IotModel.deleted_at.is_(None))
            .first()
        )

        if iot is None:
            return (
                jsonify({"error": True, "message": "IOT tidak ditemukan"}),
                404,
            )

        iot.user_id = None
        iot.lahan_id = None
        db.session.commit()
        return (
            jsonify({"error": False, "message": "Pendaftaran IOT berhasil direset"}),
            201,
        )

    def post_iot(self, data_iot):
        iot_id = data_iot["iot_id"]
        lahan_id = data_iot["lahan_id"]
        current_user = get_jwt_identity()
        iot = (
            IotModel.query.filter_by(id=iot_id)
            .filter(IotModel.deleted_at.is_(None))
            .first()
        )

        if iot is None:
            return (
                jsonify({"error": True, "message": "IOT atau lahan tidak ditemukan"}),
                404,
            )

        lahan = (
            LahanModel.query.filter_by(id=lahan_id)
            .filter(LahanModel.deleted_at.is_(None))
            .first()
        )
        if lahan is None:
            return (
                jsonify({"error": True, "message": "IOT atau lahan tidak ditemukan"}),
                404,
            )

        if iot.user_id is not None or iot.lahan_id is not None:
            return jsonify(
                {
                    "error": True,
                    "message": f"IOT sudah terdaftar di lahan lain ({lahan.nama})",
                }
            )

        iot.user_id = current_user
        iot.lahan_id = lahan_id
        db.session.commit()

        return (
            jsonify({"error": False, "message": "IOT berhasil didaftarkan di lahan"}),
            201,
        )

    def get_iot(self, iot_id):
        hasil_iot = (
            HasilIotModel.query.filter_by(iot_id=iot_id)
            .filter(HasilIotModel.deleted_at.is_(None))
            .first()
        )
        print(hasil_iot)

        if hasil_iot is None:
            return jsonify({"error": True, "message": "Data tidak ditemukan"}), 404

        hasil_iot = {
            "suhu": hasil_iot.suhu,
            "kelembaban_udara": hasil_iot.kelembaban_udara,
        }

        data_iot = {
            "error": False,
            "message": "Data berhasil didapat",
            "data": hasil_iot,
        }

        return jsonify(data_iot), 200
