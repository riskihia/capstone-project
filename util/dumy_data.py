import datetime
import uuid
from util.config import db
from model.models import PenggunaModel, LahanModel, LahanImageModel
from sqlalchemy import inspect


def has_data(model):
    count = db.session.query(db.func.count()).select_from(model).scalar()
    return count > 0


def CekTabel(nama_table):
    inspector = inspect(db.engine)
    return inspector.has_table(nama_table)


def populate_data():
    if CekTabel("pengguna") and not has_data(PenggunaModel):
        insert_pengguna()
    if CekTabel("lahan") and not has_data(LahanModel):
        insert_lahan()
    if CekTabel("lahan_image") and not has_data(LahanImageModel):
        insert_lahan_image()

    db.session.commit()


def insert_pengguna():
    user_id = []
    for _ in range(5):
        user_id.append(uuid.uuid4())
    data_user = [
        {
            "id": user_id[0],
            "username": "user1",
            "email": "user1@gmail.com",
            "photo": "https://storage.googleapis.com/flask-api-bucket/profile/default_profile.png",
            "premium": False,
            "terakhir_login": datetime.datetime.utcnow(),
        },
        {
            "id": user_id[1],
            "username": "user2",
            "email": "user2@gmail.com",
            "photo": "https://storage.googleapis.com/flask-api-bucket/profile/default_profile.png",
            "premium": False,
            "terakhir_login": datetime.datetime.utcnow(),
        },
        {
            "id": user_id[2],
            "username": "user3",
            "email": "user3@gmail.com",
            "photo": "https://storage.googleapis.com/flask-api-bucket/profile/default_profile.png",
            "premium": False,
            "terakhir_login": datetime.datetime.utcnow(),
        },
        {
            "id": user_id[3],
            "username": "user4",
            "email": "user4@gmail.com",
            "photo": "https://storage.googleapis.com/flask-api-bucket/profile/default_profile.png",
            "premium": False,
            "terakhir_login": datetime.datetime.utcnow(),
        },
        {
            "id": user_id[4],
            "username": "user5",
            "email": "user5@gmail.com",
            "photo": "https://storage.googleapis.com/flask-api-bucket/profile/default_profile.png",
            "premium": False,
            "terakhir_login": datetime.datetime.utcnow(),
        },
    ]

    for item in data_user:
        pengguna = PenggunaModel(
            id=item["id"],
            username=item["username"],
            email=item["email"],
            photo=item["photo"],
            premium=item["premium"],
            terakhir_login=item["terakhir_login"],
        )
        db.session.add(pengguna)

        lahan_id = []
        for _ in range(6):
            lahan_id.append(uuid.uuid4())

        data_lahan = [
            {
                "id": lahan_id[0],
                "user_id": item["id"],
                "nama": "Lahan 1",
                "luas": 100.0,
                "alamat": "Alamat 1",
                "lat": 0.0,
                "lon": 0.0,
            },
            {
                "id": lahan_id[1],
                "user_id": item["id"],
                "nama": "Lahan 2",
                "luas": 200.0,
                "alamat": "Alamat 2",
                "lat": 1.1,
                "lon": 1.1,
            },
            {
                "id": lahan_id[2],
                "user_id": item["id"],
                "nama": "Lahan 3",
                "luas": 300.0,
                "alamat": "Alamat 3",
                "lat": 3.3,
                "lon": 3.3,
            },
            {
                "id": lahan_id[3],
                "user_id": item["id"],
                "nama": "Lahan 4",
                "luas": 400.0,
                "alamat": "Alamat 4",
                "lat": 4.4,
                "lon": 4.4,
            },
            {
                "id": lahan_id[4],
                "user_id": item["id"],
                "nama": "Lahan 5",
                "luas": 500.0,
                "alamat": "Alamat 5",
                "lat": 5.5,
                "lon": 5.5,
            },
            {
                "id": lahan_id[5],
                "user_id": item["id"],
                "nama": "Lahan 6",
                "luas": 600.0,
                "alamat": "Alamat 6",
                "lat": 6.6,
                "lon": 6.6,
            },
        ]
        for lahanx in data_lahan:
            lahan = LahanModel(
                id=lahanx["id"],
                user_id=lahanx["user_id"],
                nama=lahanx["nama"],
                luas=lahanx["luas"],
                alamat=lahanx["alamat"],
                lat=lahanx["lat"],
                lon=lahanx["lon"],
            )
            db.session.add(lahan)

    db.session.commit()


def insert_lahan_image():
    lahan_image = LahanImageModel(nama="Image 1", photo="image1.jpg")
    db.session.add(lahan_image)
    db.session.commit()
