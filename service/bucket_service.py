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


def get_image_urls(self, bucket_name, folder_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_name + "/")

    image_urls = []
    for blob in blobs:
        if (
            blob.name.endswith(".png")
            or blob.name.endswith(".jpg")
            or blob.name.endswith(".jpeg")
        ):
            url = f"https://storage.googleapis.com/{bucket_name}/{blob.name}"
            image_urls.append(url)

    return image_urls


def get_image_filename(self, url):
    return url.split("/")[-1]


def post_image(self):
    urls = self.get_image_urls("flask-api-bucket", "lahan_image")
    try:
        for url in urls:
            filename = self.get_image_filename(url)
            new_lahan_image = LahanImageModel(nama=filename, photo=url)
            db.session.add(new_lahan_image)

        db.session.commit()
        return jsonify(message="Files uploaded successfully."), 201
    except Exception as e:
        print(e)
        return jsonify(message="Failed to upload files."), 500


def get_lahan_image(self):
    try:
        data = LahanImageModel.query.filter(
            LahanImageModel.deleted_at.is_(None)).all()

        lahan_image_schema = LahanImageSchema(many=True)

        response_data = {
            "error": False,
            "message": "Lahan image fetched successfully",
            "data": lahan_image_schema.dump(data),
        }
        return response_data
    except Exception as e:
        print(e)


def post_lahan_image(self):
    storage_client = storage.Client()
    bucket_name = "flask-api-bucket"
    folder_name = "lahan_image"

    file = request.files["file"]
    filename = file.filename
    destination_blob_name = f"{folder_name}/{filename}"

    # Upload file directly to the cloud storage bucket
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_file(file, content_type="image/png")

        lahan_url = self.get_lahan_url("lahan_image", filename)
        new_lahan_image = LahanImageModel(nama=filename, photo=lahan_url)
        db.session.add(new_lahan_image)
        db.session.commit()

        return jsonify(message="File uploaded successfully."), 201
    except Exception as e:
        print(e)
        return jsonify(message="Failed to upload file."), 500
