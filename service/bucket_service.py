from flask import jsonify, request
from google.cloud import storage
import uuid
from werkzeug.utils import secure_filename


def get_unique_filename(username, filename):
    unique_id = str(uuid.uuid4().hex)  # Generate unique ID
    prefix = f"{username}_"
    secure_filename_str = secure_filename(filename)
    unique_filename = f"{prefix}{unique_id}_{secure_filename_str}"
    return unique_filename


def UploadImage(bucket_name_param, folder_name_param):
    storage_client = storage.Client()
    bucket_name = bucket_name_param
    folder_name = folder_name_param

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


def GetImage(bucket_name_param, folder_name_param, file_name_param):
    storage_client = storage.Client()
    bucket_name = bucket_name_param
    folder_name = folder_name_param
    image_filename = file_name_param
    image_path = f"{folder_name}/{image_filename}"

    # Mendapatkan URL gambar dari cloud storage bucket
    def get_image_url(bucket_name, image_path):
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(image_path)
        return blob.public_url

    # Mengambil link gambar
    image_url = get_image_url(bucket_name, image_path)
    return jsonify(image_url)
