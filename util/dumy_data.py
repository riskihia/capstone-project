import datetime
import uuid
from util.config import db
from model.models import (
    PenggunaModel,
    LahanModel,
    LahanImageModel,
    TanamModel,
    AktivitasModel,
    BibitModel,
)
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
    if CekTabel("bibit") and not has_data(BibitModel):
        insert_bibit()
    if CekTabel("tanam") and not has_data(TanamModel):
        insert_tanam()

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
                "lat": None,
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


def insert_bibit():
    for dabit in data_bibit:
        bibit = BibitModel(
            id=dabit["id"],
            nama=dabit["nama"],
            photo=dabit["photo"],
            deskripsi=dabit["deskripsi"],
            harga_beli=dabit["harga_beli"],
            jenis=dabit["jenis"],
            link_market=dabit["link_market"],
        )
        db.session.add(bibit)
    db.session.commit()
    return bibit


def insert_tanam():
    bibits = BibitModel.query.filter(BibitModel.deleted_at.is_(None)).limit(3).all()
    lahans = LahanModel.query.filter(LahanModel.deleted_at.is_(None)).limit(3).all()
    lahan_ids = []
    bibit_ids = []
    for lahan in lahans:
        lahan_ids.append(lahan.id)
    for bibit in bibits:
        bibit_ids.append(bibit.id)

    for i in range(3):
        id = uuid.uuid4()
        tanggal_tanam = datetime.datetime.now() - datetime.timedelta(days=7)
        tanam = TanamModel(
            id=id,
            bibit_id=bibit_ids[i],
            lahan_id=lahan_ids[i],
            jarak=50,
            status="plan",
            tanggal_tanam=tanggal_tanam,
        )
        db.session.add(tanam)
    db.session.commit()

    tanams = TanamModel.query.filter(TanamModel.deleted_at.is_(None)).limit(3).all()
    tanam_ids = []
    for tanam in tanams:
        tanam_ids.append(tanam.id)

    for i in range(3):
        id = uuid.uuid4()
        aktivitas = AktivitasModel(
            id=id,
            tanam_id=tanam_ids[i],
            nama="Pemupukan",
            keterangan="Pemupukan tahap 1",
            pupuk=1,
            tanggal_aktivitas=db.func.now(),
        )
        db.session.add(aktivitas)

    db.session.commit()

    return tanam


data_bibit = [
    {
        "id": uuid.uuid4(),
        "link_market": "https://shp.ee/7xmce7t",
        "nama": "Buncis",
        "photo": "https://abahtani.com/wp-content/uploads/2019/03/Mengenal-Tanaman-Buncis.jpg",
        "deskripsi": "random cok ocom jajaj nanan yuman",
        "harga_beli": 9.000,
        "jenis": "Sayuran",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shopee.co.id/infarmofficialshop",
        "nama": "Jagung",
        "photo": "https://cdn1-production-images-kly.akamaized.net/BrN3h8F6j4I3DCkZUbYi5ZB8jV8=/1200x900/smart/filters:quality(75):strip_icc():format(jpeg)/kly-media-production/medias/939191/original/097414500_1438079406-20150728-Jagung.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 9.000,
        "jenis": "Sayuran",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shopee.co.id/infarmofficialshop",
        "nama": "Kacang Panjang",
        "photo": "https://img.iproperty.com.my/angel-legacy/1110x624-crop/static/2021/05/1.-MANFAAT-KACANG-PANJANG.png",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 9.000,
        "jenis": "Sayuran",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shopee.co.id/pusatbibitagrari",
        "nama": "Mangga",
        "photo": "https://nourishindonesia.com/image/cache/catalog/5370-550x550.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 22.380,
        "jenis": "Buah",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shp.ee/zvhiqtr",
        "nama": "Kacang Merah",
        "photo": "https://www.andrafarm.co.id/_andra_farm/gambar_kelompok/a102-3.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 5.499,
        "jenis": "Sayuran",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shopee.co.id/infarmofficialshop",
        "nama": "Kacang hijau",
        "photo": "https://www.swadayaonline.com/images/view/-IMG_20200225_45990.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 9.000,
        "jenis": "Buah",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shopee.co.id/littleindia1",
        "nama": "Lentil Hitam",
        "photo": "https://cairofood.id/wp-content/uploads/kupas-tuntas-mengenai-lentil-serta-manfaatnya-bagi-tubuh-lentil-hitam.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 46.000,
        "jenis": "Sayuran",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shopee.co.id/hera_vernando",
        "nama": "Delima",
        "photo": "https://id-test-11.slatic.net/p/c80a914de9b80835a386f668691ab940.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 3.000,
        "jenis": "Buah",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shp.ee/6qcyaf2",
        "nama": "Kacang Polong",
        "photo": "https://agrotek.id/wp-content/uploads/2020/06/Klasifikasi-Dan-Morfologi-Tanaman-Kacang-Polong.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 4.250,
        "jenis": "Sayuran",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shopee.co.id/elsa_bibit_tanaman",
        "nama": "Anggur",
        "photo": "https://images.tokopedia.net/img/cache/850/BgtCLw/2022/4/25/da432308-88b2-4a3f-9743-0081a7b788f9.jpg?ect=4g",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 4.000,
        "jenis": "Buah",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shp.ee/w39kamh",
        "nama": "Semangka",
        "photo": "https://www.budidayapetani.com/wp-content/uploads/2020/07/Tabulampot-Semangka.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 15.000,
        "jenis": "Buah",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shopee.co.id/infarmofficialshop",
        "nama": "Melon",
        "photo": "https://i0.wp.com/agrotek.id/wp-content/uploads/2020/03/Klasifikasi-dan-Morfologi-Tanaman-Melon.jpg?fit=640%2C467&ssl=1",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 9.000,
        "jenis": "Buah",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shopee.co.id/hudabibittanaman",
        "nama": "Apel",
        "photo": "https://cdn-brilio-net.akamaized.net/community/2018/09/12/13793/ayo-nikmati-apel-rebus-yang-ternyata-sangat-baik-untuk-kesehatan.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 15.000,
        "jenis": "Buah",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shp.ee/t8d3u8k",
        "nama": "Jeruk",
        "photo": "https://www.lubera.com/images/400/Ovale-Kumquat_5.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 10.800,
        "jenis": "Buah",
    },
    {
        "id": uuid.uuid4(),
        "link_market": "https://shopee.co.id/bibit_nusantara01",
        "nama": "Kelapa",
        "photo": "https://imgx.sonora.id/crop/0x0:0x0/700x465/photo/2023/04/10/istockphoto-1277125141-170667aj-20230410030406.jpg",
        "deskripsi": "random sas cok osasa sa com jajaj nanan yuman",
        "harga_beli": 9.000,
        "jenis": "Buah",
    },
]
