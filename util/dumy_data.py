import datetime
import uuid
from util.config import db
from model.models import PenggunaModel, LahanModel, LahanImageModel
from sqlalchemy import inspect
import random


def has_data(model):
    count = db.session.query(db.func.count()).select_from(model).scalar()
    return count > 0


def CekTabel(nama_table):
    inspector = inspect(db.engine)
    return inspector.has_table(nama_table)


def populate_data():
    if CekTabel("pengguna") and not has_data(PenggunaModel):
        insert_pengguna()
    if CekTabel("lahan_image") and not has_data(LahanImageModel):
        insert_lahan_image()

    db.session.commit()


def get_photo_list():
    list_photo = [
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/a1.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/a2.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/a3.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/a4.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/b1.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/b2.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/b3.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/b4.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/c1.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/c2.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/c3.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/c4.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/d1.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/d2.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/d3.png",
        "https://storage.googleapis.com/flask-api-bucket/lahan_image/d4.png",
    ]

    return list_photo


def insert_pengguna():
    user_data = []
    for i in range(1, 6):
        user = {
            "username": f"user{i}",
            "email": f"user{i}@gmail.com",
        }
        user_data.append(user)

    for item in user_data:
        user_id = uuid.uuid4()
        pengguna = PenggunaModel(
            id=user_id,
            username=item["username"],
            email=item["email"],
            photo="https://storage.googleapis.com/flask-api-bucket/profile/default_profile.png",
            premium=False,
            terakhir_login=db.func.now(),
            updated_at=db.func.now(),
        )
        db.session.add(pengguna)

        lahan_data = []
        num_iterations = random.randint(1, 10)  # Jumlah iterasi acak antara 1 dan 10

        for i in range(1, num_iterations + 1):
            photo = random.choice(get_photo_list())
            lahan = {
                "nama": f"Lahan {i}",
                "luas": i * 100.0,
                "alamat": f"Alamat {i}",
                "photo": photo,
                "lat": i * 1.1,
                "lon": i * 1.1,
            }
            lahan_data.append(lahan)

        for lahanx in lahan_data:
            lahan_id = uuid.uuid4()
            lahan = LahanModel(
                id=lahan_id,
                user_id=user_id,
                nama=lahanx["nama"],
                photo=lahanx["photo"],
                luas=lahanx["luas"],
                alamat=lahanx["alamat"],
                lat=lahanx["lat"],
                lon=lahanx["lon"],
                updated_at=db.func.now(),
            )
            db.session.add(lahan)

    db.session.commit()


def insert_lahan_image():
    photos = get_photo_list()
    for i, photo in enumerate(photos):
        lahan_image = LahanImageModel(
            nama=f"Image {i+1}",
            photo=photo,
            updated_at=db.func.now(),
        )
        db.session.add(lahan_image)
    db.session.commit()
