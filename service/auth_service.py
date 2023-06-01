from model.models import PenggunaModel
from schemas import PenggunaSchema
from util.db import db

from flask_jwt_extended.exceptions import JWTDecodeError

from sqlalchemy import Null
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from flask_jwt_extended import create_access_token, create_access_token, get_jwt
import uuid
import datetime
import re
from werkzeug.utils import secure_filename
from google.cloud import storage

from util.blocklist import BLOCKLIST
import os
from flask import jsonify, request, current_app


class AuthService:
    def __init__(self):
        pass

    def get_image_urls(self):
        storage_client = storage.Client()
        bucket_name = "flask-api-bucket"
        folder_name = "profile"
        image_filename = "default_profile.png"
        image_path = f"{folder_name}/{image_filename}"

        # Mendapatkan URL gambar dari cloud storage bucket
        def get_image_url(bucket_name, image_path):
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(image_path)
            return blob.public_url

        # Mengambil link gambar
        image_url = get_image_url(bucket_name, image_path)
        return image_url

    def get_unique_filename(username, filename):
        unique_id = str(uuid.uuid4().hex)  # Generate unique ID
        prefix = f"{username}_"
        secure_filename_str = secure_filename(filename)
        unique_filename = f"{prefix}{unique_id}_{secure_filename_str}"
        return unique_filename

    def tambah_pengguna(self, store_data):
        username = store_data["username"]
        email = store_data["email"]

        def validate_email(email):
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            return re.match(pattern, email)

        if not validate_email(email):
            abort(400, message="Invalid email")

        store_data["id"] = str(uuid.uuid4())
        store_data["photo"] = self.get_image_urls()
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

    def pengguna_logout(self, store_data):
        if not store_data or "email" not in store_data:
            response = {"error": True, "message": "Logout failed. Invalid request."}
            return jsonify(response), 400

        email = store_data["email"]
        user = PenggunaModel.query.filter(PenggunaModel.email == email).first()

        if user:
            user.token = None
            db.session.commit()
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            response = {
                "error": False,
                "message": "User has been successfully logged out.",
            }
            return jsonify(response), 200
        else:
            abort(404, message="User not found.")
