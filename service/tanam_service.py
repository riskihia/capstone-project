from flask import jsonify
from model.models import PenggunaModel, TanamModel, LahanModel
from schemas import UserLahanSchema
from util.config import db

from flask_jwt_extended import get_jwt_identity


class TanamService:
    def __init__(self):
        pass

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
        tanam = (
            TanamModel.query.filter_by(bibit_id=bibit_id, lahan_id=lahan_id)
            .filter(TanamModel.deleted_at.is_(None))
            .first()
        )
        if tanam is None:
            return (
                jsonify({"error": True, "message": "Bibit atau lahan tidak ditemukan"}),
                404,
            )

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

        tanam.status = "plan"
        db.session.commit()
        return (
            jsonify(
                {"error": False, "message": "Data plan tanam berhasil ditambahkan"}
            ),
            404,
        )
