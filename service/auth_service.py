from model.models import PenggunaModel
from util.config import db
from flask_smorest import abort
from flask_jwt_extended import create_access_token, create_access_token, get_jwt
import uuid, datetime, re
from google.cloud import storage
from schemas import PlainPenggunaSchema

from util.blocklist import BLOCKLIST
from flask import jsonify


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

    def get_all_pengguna(self):
        try:
            data = PenggunaModel.query.filter(PenggunaModel.deleted_at.is_(None)).all()

            pengguna_schema = PlainPenggunaSchema(many=True)

            response_data = {
                "error": False,
                "message": "User data fetched ssuccessfully",
                "data": pengguna_schema.dump(data),
            }
            return jsonify(response_data), 200
        except Exception as e:
            print(e)

    def tambah_pengguna(self, store_data):
        username = store_data["username"]
        email = store_data["email"]

        def validate_email(email):
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            return re.match(pattern, email)

        if not validate_email(email):
            abort(400, message="Invalid email")

        store_data["photo"] = self.get_image_urls()
        store_data["premium"] = False
        store_data["terakhir_login"] = datetime.datetime.now()
        store_data["token"] = "hai"

        # Cek apakah pengguna sudah ada di database
        user = (
            PenggunaModel.query.filter(PenggunaModel.email == store_data["email"])
            .filter(PenggunaModel.deleted_at.is_(None))
            .first()
        )

        if user is None:
            # Buat pengguna baru dan simpan ke database
            store_data["id"] = str(uuid.uuid4())
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
            return jsonify(response), 201
        else:
            store_data["token"] = create_access_token(identity=user.id)

            user.terakhir_login = datetime.datetime.now()
            user.token = store_data["token"]
            db.session.commit()

            store_data["id"] = user.id
            response = {
                "error": False,
                "message": "User successfully logged in",
                "data": store_data,
            }
            return jsonify(response), 200

    def pengguna_logout(self, store_data):
        if not store_data or "email" not in store_data:
            response = {"error": True, "message": "Logout failed. Invalid request."}
            return jsonify(response), 400

        email = store_data["email"]
        user = (
            PenggunaModel.query.filter(PenggunaModel.email == email)
            .filter(PenggunaModel.deleted_at.is_(None))
            .first()
        )

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
