from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify, request, send_from_directory
import uuid, datetime

from util.config import db
from flask import current_app
import os
from google.cloud import storage
from schemas import UploadSchema

from flask_jwt_extended import jwt_required

from werkzeug.utils import secure_filename

upload_blp = Blueprint(
    "upload", __name__, url_prefix="/api/v1", description="Option in upload"
)


def get_unique_filename(username, filename):
    unique_id = str(uuid.uuid4().hex)  # Generate unique ID
    prefix = f"{username}_"
    secure_filename_str = secure_filename(filename)
    unique_filename = f"{prefix}{unique_id}_{secure_filename_str}"
    return unique_filename


@upload_blp.route("/image")
class Image(MethodView):
    def get(self):
        storage_client = storage.Client()
        bucket_name = "flask-api-bucket"
        folder_name = "profile"
        image_filename = "riski_a032b4c4190e4e6f8540033be4ac57ea_x.PNG"
        image_path = f"{folder_name}/{image_filename}"

        # Mendapatkan URL gambar dari cloud storage bucket
        def get_image_url(bucket_name, image_path):
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(image_path)
            return blob.public_url

        # Mengambil link gambar
        image_url = get_image_url(bucket_name, image_path)
        return jsonify(image_url)


@upload_blp.route("/upload")
class Pengguna(MethodView):
    # decorator untuk documentation
    # @upload_blp.response(200)
    def get(self):
        image_filename = "Capture.PNG"
        image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_filename)
        return image_path

    # @upload_blp.arguments(UploadSchema)
    def post(self):
        storage_client = storage.Client()
        bucket_name = "flask-api-bucket"
        folder_name = "profile"

        file = request.files["file"]
        # filename = secure_filename(file.filename)
        username = "riski"
        filename = get_unique_filename(username, file.filename)
        destination_blob_name = f"{folder_name}/{filename}"

        # Upload file directly to the cloud storage bucket
        try:
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_file(file)
            return jsonify(message="File uploaded successfully.")
        except Exception as e:
            print(e)
            return jsonify(message="Failed to upload file."), 500

        # file = request.files["file"]
        # filename = secure_filename(file.filename)
        # upload_folder = current_app.config["UPLOAD_FOLDER"]
        # file.save(os.path.join((upload_folder + "/" + filename)))

        # return jsonify("berhasil")
