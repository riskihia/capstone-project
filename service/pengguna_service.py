from model.models import PenggunaModel
from schemas import PenggunaSchema
from util.db import db

from flask_smorest import abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class PenggunaService:
    def __init__(self):
        pass

    def get_all_pengguna(self):
        data = PenggunaModel.query.all()
        pengguna_schema = PenggunaSchema(many=True)
        response_data = {
            "status_code": 200,
            "msg": "Data retrieved successfully",
            "data": pengguna_schema.dump(data),
        }
        return response_data

    def tambah_pengguna(self, store_data):
        id = store_data["id"]
        token = store_data["token"]
        photo = store_data["photo"]
        email = store_data["email"]

        # Pemeriksaan keunikan nama
        pengguna_id = PenggunaModel.query.filter_by(id=id).first()
        if pengguna_id:
            abort(400, message="A user with the same id already exists")

        pengguna_token = PenggunaModel.query.filter_by(token=token).first()
        if pengguna_token:
            abort(400, message="A user with the same token already exists")

        # Pemeriksaan keunikan username
        pengguna_foto = PenggunaModel.query.filter_by(photo=photo).first()
        if pengguna_foto:
            abort(400, message="A user with the same photo already exists")

        pengguna_email = PenggunaModel.query.filter_by(email=email).first()
        if pengguna_email:
            abort(400, message="A user with the same email already exists")

        pengguna = PenggunaModel(**store_data)

        try:
            db.session.add(pengguna)
            db.session.commit()
        except IntegrityError as e:
            # error_message = str(e.orig) if e.orig else "An integrity error occurred"
            # abort(400, message=error_message)
            abort(400, message="error")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting item")

        return pengguna
