from util.config import db
import datetime
import uuid
from sqlalchemy import (
    Column,
    Double,
    ForeignKey,
    Null,
    DateTime,
    Boolean,
    Integer,
    String,
    Text,
    Enum,
)


class TimeStamp:
    created_at = Column(DateTime, server_default=db.func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


class PenggunaModel(db.Model, TimeStamp):
    __tablename__ = "pengguna"
    id = Column(String(250), nullable=False, primary_key=True, unique=True)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    photo = Column(String(250), unique=False)
    premium = Column(Boolean, nullable=True)
    token = Column(Text, nullable=True)
    terakhir_login = Column(DateTime, nullable=False)

    lahan = db.relationship("LahanModel", back_populates="pengguna", lazy="dynamic")


class LahanModel(db.Model, TimeStamp):
    __tablename__ = "lahan"
    id = Column(String(250), nullable=False, primary_key=True)
    user_id = Column(String(250), ForeignKey("pengguna.id"))
    nama = Column(String(250), nullable=False)
    photo = Column(String(250), unique=False)
    luas = Column(Double, nullable=False)
    alamat = Column(String(250), nullable=True)
    lat = Column(Double, nullable=True)
    lon = Column(Double, nullable=True)
    pengguna = db.relationship("PenggunaModel", back_populates="lahan")
    tanam = db.relationship("TanamModel", back_populates="lahan", lazy="joined")


class TanamModel(db.Model, TimeStamp):
    __tablename__ = "tanam"
    id = Column(String(250), nullable=False, primary_key=True)
    # bibit_id = Column(String(250), ForeignKey("bibit.id"))
    lahan_id = Column(String(250), ForeignKey("lahan.id"))
    jarak = Column(Integer, server_default="30")
    status = Column(Enum("plan", "exec", "close"))
    tanggal_tanam = Column(DateTime, nullable=True)
    tanggal_panen = Column(DateTime, nullable=True)
    jumlah_panen = Column(Integer)
    harga_panen = Column(Integer)
    lahan = db.relationship("LahanModel", back_populates="tanam")


class LahanImageModel(db.Model, TimeStamp):
    __tablename__ = "lahan_image"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(250), nullable=False)
    photo = Column(String(250), unique=False)


# class BibitModel(db.Model, TimeStamp):
#     __tablename__ = "bibit"
#     id = Column(String(250), nullable=False, primary_key=True)
#     nama = Column(String(250))
#     photo = Column(String(250))
#     deskripsi = Column(Text, nullable=True)
#     harga_beli = Column(Integer)
#     jenis = Column(Enum("sayuran", "buah"))
#     link_market = Column(String(250), server_default="tani.iyabos.com/marketplace")


# class AktivitasModel(db.Model, TimeStamp):
#     __tablename__ = "aktivitas"
#     id = Column(String(250), nullable=False, primary_key=True)
#     tanam_id = Column(String(250), ForeignKey("tanam.id"))
#     nama = Column(String(250))
#     keterangan = Column(Text, nullable=True)
#     pupuk = Column(Integer)
#     tanggal_aktivitas = Column(DateTime, nullable=True)


# # Todo:: buat model tanam
# class TanamanModel(db.Model, TimeStamp):
#     __tablename__ = "Tanaman"
#     id = Column(String(250), nullable=False, primary_key=True)
#     bibit_id = Column(String(250), ForeignKey("bibit.id"))
#     lahan_id = Column(String(250), ForeignKey("lahan.id"))
#     product_id = Column(String(250), ForeignKey("produk.id"))
#     status = Column(Enum("plan", "exec", "close"), nullable=True)
#     tanggal_tanam = Column(DateTime, nullable=True)
#     tanggal_panen = Column(DateTime, nullable=True)
#     harga_panen = Column(String(250), nullable=True)


# # Todo:: buat model bibit
# class BibitModel(db.Model, TimeStamp):
#     __tablename__ = "Bibit"
#     id = Column(String(250), nullable=False, primary_key=True)
#     nama = Column(String(250), nullable=False)
#     photo = Column(String(250), nullable=False)
#     deskripsi = Column(text(250), nullable=True)
#     harga_beli = Column(Integer, nullable=False)
#     harga_panen = Column(Integer, nullable=True)
#     link_market = Column(DateTime, nullable=True)


# # Todo:: buat model produk
# class ProdukModel(db.Model, TimeStamp):
#     __tablename__ = "Produk"
#     id = Column(String(250), nullable=False, primary_key=True)
#     bibit_id = Column(String(250), ForeignKey("bibit.id"))


# # Todo:: buat model rekomendasi_tanaman
# class RekomendasiModel(db.Model, TimeStamp):
#     __tablename__ = "Rekomendasi"
#     id = Column(String(250), nullable=False, primary_key=True)
#     bibit_id = Column(String(250), ForeignKey("bibit.id"))
#     nama = Column(String(250), nullable=False)
#     deskripsi = Column(text(250), nullable=True)


# # Todo:: buat model keuangan
# class KeuanganModel(db.Model, TimeStamp):
#     __tablename__ = "Keuangan"
#     id = Column(String(250), nullable=False, primary_key=True)
#     tanaman_id = Column(String(250), ForeignKey("tanam.id"))
#     keterangan_id = Column(String(250), ForeignKey("kategori_keuangan.id"))
#     nama = Column(String(250), nullable=True)
#     unit = Column(Double, default=Null)
#     total = Column(Integer, nullable=True)
#     keterangan = Column(Double, default=Null)


# # Todo:: buat model kategori_keuangan
# class Kategori_KeuanganModel(db.Model, TimeStamp):
#     __tablename__ = "Kategori_Keuangan"
#     id = Column(String(250), nullable=False, primary_key=True)
#     nama = Column(String(250), nullable=True)
#     jenis = Column(Enum("masuk", "keluar"), nullable=True)


# # Todo:: buat model iot_tool
# class Iot_ToolModel(db.Model, TimeStamp):
#     __tablename__ = "Iot_Tool"
#     id = Column(String(250), nullable=False, primary_key=True)
#     user_id = Column(String(250), ForeignKey("pengguna.id"))


# # Todo:: buat model hasil_tool
# class Hasil_ToolModel(db.Model, TimeStamp):
#     __tablename__ = "Hasil_Tool"
#     id = Column(String(250), nullable=False, primary_key=True)
#     tool_id = Column(String(250), ForeignKey("iot_tool.id"))
#     ph = Column(Double, default=Null)
#     kelembaban_tanah = Column(Double, default=Null)
#     kelembaban_udara = Column(Double, default=Null)
#     suhu = Column(Double, default=Null)
