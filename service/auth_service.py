from model.models import PenggunaModel
from schemas import PenggunaSchema
from util.db import db

from sqlalchemy import Null
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from flask_jwt_extended import create_access_token, decode_token
import uuid
import datetime
import re
from werkzeug.utils import secure_filename

import os
from flask import jsonify, request, current_app


class AuthService:
    def __init__(self):
        pass

    def tambah_pengguna(self, store_data):
        file = request.files["file"]
        filename = secure_filename(file.filename)
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        file.save(os.path.join((upload_folder + "/" + filename)))

        username = store_data["username"]
        email = store_data["email"]

        def validate_email(email):
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            return re.match(pattern, email)

        if not validate_email(email):
            abort(400, message="Invalid email")

        store_data["id"] = str(uuid.uuid4())
        store_data["photo"] = filename
        store_data["premium"] = False
        store_data["terakhir_login"] = datetime.datetime.now()
        store_data["token"] = "hai"

        # Cek apakah pengguna sudah ada di database
        user = PenggunaModel.query.filter(
            PenggunaModel.email == store_data["email"]
        ).first()

        if user is None:
            # Buat pengguna baru dan simpan ke database
            new_user = PenggunaModel(**store_data)
            db.session.add(new_user)
            db.session.commit()

            user = PenggunaModel.query.filter(
                PenggunaModel.username == store_data["username"]
            ).first()
            # Perbarui nilai store_data["token"] dengan token baru yang dibuat
            store_data["token"] = create_access_token(identity=user.id)
            new_token = store_data["token"]
            user.token = new_token
            db.session.commit()

            response = {
                "error": False,
                "message": "User successfully registered",
                "data": store_data,
            }
            return jsonify(response)
        else:
            store_data["token"] = create_access_token(identity=user.id)

            user.terakhir_login = datetime.datetime.now()
            user.token = store_data["token"]
            db.session.commit()

            response = {
                "error": False,
                "message": "User successfully logged in",
                "data": store_data,
            }
            return jsonify(response)
