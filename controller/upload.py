from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify, request, send_from_directory
import uuid, datetime

from util.db import db
from flask import current_app
import os
from google.cloud import storage

from flask_jwt_extended import jwt_required

from werkzeug.utils import secure_filename

upload_blp = Blueprint(
    "upload", __name__, url_prefix="/api/v1", description="Option in upload"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-key-bucket.json"


@upload_blp.route("/image")
class Image(MethodView):
    def get(self):
        image_url = "https://storage.googleapis.com/flask-api-bucket/Capture.PNG"
        return jsonify(image_url=image_url)


@upload_blp.route("/upload")
class Pengguna(MethodView):
    # decorator untuk documentation
    # @upload_blp.response(200)
    def get(self):
        image_filename = "Capture.PNG"
        image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_filename)
        return image_path

    def post(self):
        storage_client = storage.Client()
        bucket_name = "flask-api-bucket"
        folder_name = "profile"

        file = request.files["file"]
        filename = secure_filename(file.filename)
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
