import uuid
from flask import jsonify
from model.models import IotModel, HasilIotModel, BaseDataIotModel
from schemas import UserLahanSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_smorest import abort
from util.config import db

from flask_jwt_extended import get_jwt_identity


class HasilIotService:
    def __init__(self):
        pass

    def tambah_hasil_iot(self, suhu, kelembaban_udara, iot_id):
        iot = (
            IotModel.query.filter_by(id=iot_id)
            .filter(IotModel.deleted_at.is_(None))
            .first()
        )
        print(iot)
        if iot is None:
            return jsonify({"error": True, "message": "IoT ID tidak ditemukan"}), 404

        try:
            hasil_iot = HasilIotModel(
                id=uuid.uuid4(),
                iot_id=iot_id,
                kelembaban_udara=kelembaban_udara,
                suhu=suhu,
            )
            db.session.add(hasil_iot)
            db.session.commit()

            data = {"error": False, "message": "Data IoT berhasil ditambahkan"}
            return jsonify(data), 202
        except SQLAlchemyError:
            # Kesalahan umum saat menyisipkan item
            abort(500, message="An error occurred while inserting item")
