from datetime import datetime
import random
import uuid
from sqlalchemy import text
import traceback

from model.models import (
    LahanImageModel,
    LahanModel,
    TanamModel,
    BibitModel,
    AktivitasModel,
)
from util.config import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_smorest import abort
from schemas import GetLahanSchema, TanamGetLahanSchema, TanamSchema
from flask import jsonify
from flask_jwt_extended import get_jwt_identity


class LahanService:
    def __init__(self):
        pass

    def get_lahan_details(self, lahan_id):
        try:
            lahan = (
                LahanModel.query.filter_by(id=lahan_id)
                .filter(LahanModel.deleted_at.is_(None))
                .first()
            )
            if lahan is None:
                return jsonify({"error": True, "message": "Lahan not found"})

            tanam = (
                TanamModel.query.filter_by(lahan_id=lahan_id)
                .filter(TanamModel.deleted_at.is_(None))
                .first()
            )
            if tanam is None:
                tanam = {}
                # return jsonify({"error": True, "message": "Tanam not found"})
            else:
                aktivitas = (
                    AktivitasModel.query.filter_by(tanam_id=tanam.id)
                    .filter(BibitModel.deleted_at.is_(None))
                    .limit(5)
                    .all()
                )
                if lahan is None:
                    return jsonify({"error": True, "message": "aktivitas not found"})

                aktivitas_list = []

                for aktivitas_item in aktivitas:
                    aktivitas_dict = {
                        "id": aktivitas_item.id,
                        "nama": aktivitas_item.nama,
                        "keterangan": aktivitas_item.keterangan,
                        "pupuk": aktivitas_item.pupuk,
                        "tanggal_aktivitas": aktivitas_item.tanggal_aktivitas
                        # tambahkan atribut-atribut lain yang diperlukan
                    }
                    aktivitas_list.append(aktivitas_dict)

                tanggal_tanam = tanam.tanggal_tanam  # Hapus pemanggilan ke strptime
                tanggal_hari_ini = datetime.now()
                selisih = tanggal_hari_ini - tanggal_tanam

                # Menghitung selisih dalam bentuk hari, jam, dan menit
                selisih_hari = selisih.days
                selisih_jam = selisih.seconds // 3600
                selisih_menit = (selisih.seconds // 60) % 60

                # Menyusun hasil selisih menjadi sebuah string yang lebih detail
                selisih_detail = (
                    f"{selisih_hari} hari, {selisih_jam} jam, {selisih_menit} menit"
                )
                bibit = (
                    BibitModel.query.filter_by(id=tanam.bibit_id)
                    .filter(BibitModel.deleted_at.is_(None))
                    .first()
                )
                if bibit is None:
                    bibit = {}
                    # return jsonify({"error": True, "message": "Bibit not found"})
                else:
                    bibit = {
                        "id": bibit.id,
                        "nama": bibit.nama,
                        "photo": bibit.photo,
                        "deskripsi": bibit.deskripsi,
                        "harga_beli": bibit.harga_beli,
                        "jenis": bibit.jenis,
                        "link_market": bibit.link_market,
                    }
                tanam = {
                    "id": tanam.id,
                    "jarak": tanam.jarak,
                    "status": tanam.status,
                    "tanggal_tanam": tanam.tanggal_tanam,
                    "tanggal_panen": tanam.tanggal_panen,
                    "jumlah_panen": tanam.jumlah_panen,
                    "harga_panen": tanam.harga_panen,
                    "umur": selisih_detail,
                    "bibit": bibit,
                    "aktivitas": aktivitas_list,
                }

            lahan = {
                "id": lahan.id,
                "user_id": lahan.user_id,
                "nama": lahan.nama,
                "photo": lahan.photo,
                "luas": lahan.luas,
                "alamat": lahan.alamat,
                "lat": lahan.lat,
                "lon": lahan.lon,
                "tanam": tanam,
            }
            response_data = {
                "error": False,
                "message": "Lahan fetched successfullys",
                "data": lahan,
            }
            return jsonify(response_data), 200
        except Exception as e:
            print(e)
            return jsonify({"gagal": "gagal"}), 200

    def get_lahan_detail(self, lahan_id):
        try:
            data = (
                LahanModel.query.filter_by(id=lahan_id)
                .filter(LahanModel.deleted_at.is_(None))
                .first()
            )

            lahan_schema = TanamGetLahanSchema()
            response_data = {
                "error": False,
                "message": "Lahan fetched successfully",
                "data": lahan_schema.dump(data),
            }
            return jsonify(response_data), 200

        except Exception as e:
            error_message = str(e)  # Get the error message as a string
            response_data = {
                "error": True,
                "message": "An error occurred: " + error_message,
            }
            return jsonify(response_data), 500

    def get_user_lahan(self):
        current_user = get_jwt_identity()

        try:
            # data = LahanModel.query.filter(LahanModel.deleted_at.is_(None)).all()
            data = (
                LahanModel.query.filter_by(user_id=current_user)
                .filter(LahanModel.deleted_at.is_(None))
                .all()
            )
            lahan_schema = GetLahanSchema(many=True)

            response_data = {
                "error": False,
                "message": "Lahan fetched successfully",
                "data": lahan_schema.dump(data),
            }
            return jsonify(response_data), 200
        except Exception as e:
            print(e)

    def post_lahan(self, lahan_data):
        try:
            lahan = LahanImageModel.query.filter(
                LahanImageModel.deleted_at.is_(None)
            ).all()
            lahan_data["id"] = str(uuid.uuid4())
            random_photo = random.choice([l.photo for l in lahan])
            lahan_data["photo"] = random_photo

            new_lahan = LahanModel(**lahan_data)
            db.session.add(new_lahan)
            db.session.commit()

            return {"error": False, "message": "Lahan added successfully"}
        except IntegrityError:
            # Jika user_id tidak valid
            abort(400, message="User id not valid")
        except SQLAlchemyError:
            # Kesalahan umum saat menyisipkan item
            abort(500, message="An error occurred while inserting item")

    def delete_lahan(self, lahan_id):
        lahan = LahanModel.query.filter_by(id=lahan_id).first()

        if lahan is None:
            return jsonify({"error": True, "message": "Lahan not found"})
        else:
            is_deleted = LahanModel.query.filter(
                LahanModel.deleted_at.is_(None), LahanModel.id == lahan_id
            ).first()
            if is_deleted is None:
                return jsonify({"error": True, "message": "Lahan Already Deleted"})
            else:
                try:
                    lahan.deleted_at = datetime.datetime.now()
                    db.session.commit()
                except Exception as e:
                    print(e)
                return jsonify(
                    {"error": False, "message": "Lahan deleted successfully"}
                )
