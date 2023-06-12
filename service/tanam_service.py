from flask import jsonify
from model.models import BibitModel, PenggunaModel, TanamModel, LahanModel
from schemas import UserLahanSchema
from util.config import db
import uuid, datetime
from flask_jwt_extended import get_jwt_identity


class TanamService:
    def __init__(self):
        pass
    
    def rekomendasi_tanam(self, data_image):
        pass

    def delete_tanam(self, id):
        tanam = (
            TanamModel.query.filter_by(id=id)
            .filter(TanamModel.deleted_at.is_(None))
            .first()
        )

        if tanam is None:
            return (
                jsonify(
                    {
                        "error": True,
                        "message": "Data tanam tidak ditemukan atau sudah dihapus",
                    }
                ),
                404,
            )
        print(tanam)
        print(tanam.deleted_at)
        try:
            tanam.deleted_at = datetime.datetime.now()
            db.session.commit()
        except Exception as e:
            print(e)

        return jsonify({"error": False, "message": "Data tanam berhasil dihapus"})

    def get_close_tanam(self, lahan_id):
        tanam = (
            TanamModel.query.filter_by(lahan_id=lahan_id)
            .filter(TanamModel.deleted_at.is_(None))
            .first()
        )
        # print(tanam)
        if not tanam:
            return (
                jsonify(
                    {"error": True, "message": "Lahan id pada Tanam tidak ditemukan"}
                ),
                404,
            )
        # tanam = TanamModel.query.filter_by(lahan_id=lahan_id, status="close").first()
        tanams = (
            TanamModel.query.filter_by(lahan_id=lahan_id, status="close")
            .filter(TanamModel.deleted_at.is_(None))
            .all()
        )
        print(tanams)
        if not tanams:
            return (
                jsonify(
                    {
                        "error": True,
                        "message": "Tanam tidak ditemukan / blm ada tanaman yg panen",
                    }
                ),
                404,
            )

        # return "hai"
        tanam_list = []
        for tanam_item in tanams:
            bibit = (
                BibitModel.query.filter_by(id=tanam_item.bibit_id)
                .filter(BibitModel.deleted_at.is_(None))
                .first()
            )
            tanam = {
                "id": tanam_item.id,
                "bibit_nama": bibit.nama,
                "jarak": tanam_item.jarak,
                "status": tanam_item.status,
                "tanggal_tanam": tanam_item.tanggal_tanam,
                "tanggal_panen": tanam_item.tanggal_panen,
                "jumlah_panen": tanam_item.jumlah_panen,
                "harga_panen": tanam_item.harga_panen,
            }
            tanam_list.append(tanam)
        response_data = {
            "error": False,
            "message": "Data tanam berhasil diambil",
            "data": tanam_list,
        }
        return jsonify(response_data), 200

    def close_post_tanam(self, data_tanam):
        id = data_tanam["id"]
        tanggal_panen = data_tanam["tanggal_panen"]
        jumlah_panen = data_tanam["jumlah_panen"]
        harga_panen = data_tanam["harga_panen"]

        tanam = (
            TanamModel.query.filter_by(id=id)
            .filter(TanamModel.deleted_at.is_(None))
            .first()
        )
        # print(tanam)
        if tanam is None:
            return (
                jsonify(
                    {
                        "error": True,
                        "message": "Data tanam tidak ditemukan atau status bukan 'exec'",
                    }
                ),
                404,
            )

        if tanam.status != "exec":
            return (
                jsonify(
                    {
                        "error": True,
                        "message": "Data tanam tidak ditemukan atau status bukan 'exec'",
                    }
                ),
                404,
            )

        tanam.status = "close"
        tanam.tanggal_panen = tanggal_panen
        tanam.jumlah_panen = jumlah_panen
        tanam.harga_panen = harga_panen

        db.session.commit()
        return jsonify(
            {"error": False, "message": "Status tanam berhasil diubah menjadi 'close'"}
        )

    def exec_post_tanam(self, data_tanam):
        id = data_tanam["id"]
        jarak = data_tanam["jarak"]
        tanggal_tanam = data_tanam["tanggal_tanam"]
        tanam = (
            TanamModel.query.filter_by(id=id)
            .filter(TanamModel.deleted_at.is_(None))
            .first()
        )

        if tanam is None:
            return (
                jsonify(
                    {
                        "error": True,
                        "message": "Data tanam tidak ditemukan atau status bukan 'plan'",
                    }
                ),
                404,
            )
        if tanam.status != "plan":
            return (
                jsonify(
                    {
                        "error": True,
                        "message": "Data tanam tidak ditemukan atau status bukan 'plan'",
                    }
                ),
                404,
            )
        tanam.status = "exec"
        tanam.jarak = jarak
        tanam.tanggal_tanam = tanggal_tanam
        db.session.commit()
        return jsonify(
            {"error": False, "message": "Status tanam berhasil diubah menjadi 'exec'"}
        )

    def post_tanam(self, data_tanam):
        bibit_id = data_tanam["bibit_id"]
        lahan_id = data_tanam["lahan_id"]

        bibit = (
            BibitModel.query.filter_by(id=bibit_id)
            .filter(BibitModel.deleted_at.is_(None))
            .first()
        )
        if bibit is None:
            return (
                jsonify({"error": True, "message": "Bibit atau lahan tidak ditemukan"}),
                404,
            )

        lahan = (
            LahanModel.query.filter_by(id=lahan_id)
            .filter(LahanModel.deleted_at.is_(None))
            .first()
        )
        if lahan is None:
            return (
                jsonify({"error": True, "message": "Bibit atau lahan tidak ditemukan"}),
                404,
            )

        tanam = (
            TanamModel.query.filter_by(lahan_id=lahan_id)
            .filter(TanamModel.deleted_at.is_(None))
            .first()
        )
        # print(tanam)
        if tanam is None or tanam.status == "close":
            data_tanam["id"] = str(uuid.uuid4())
            data_tanam["status"] = "plan"
            data_tanam["jarak"] = 30
            data_tanam["tanggal_tanam"] = datetime.datetime.now()
            new_tanam = TanamModel(**data_tanam)
            db.session.add(new_tanam)
            db.session.commit()
            response = {
                "error": False,
                "message": "Data plan tanam berhasil ditambahkan",
            }
            return jsonify(response), 201

        if tanam.status == "plan" or tanam.status == "exec":
            return (
                jsonify(
                    {
                        "error": True,
                        "message": "Lahan sudah mempunyai rencana atau proses tanam",
                    }
                ),
                404,
            )
        return (
            jsonify({"error": True, "message": "GAGAL"}),
            404,
        )
