from util.db import db
import datetime
import uuid
from sqlalchemy import (
    Column,
    Double,
    ForeignKey,
    Null,
    DateTime,
    Integer,
    String,
    Text,
    text,
)


class TimeStamp:
    created_at = Column(DateTime, server_default=db.func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


class PenggunaModel(db.Model, TimeStamp):
    __tablename__ = "pengguna"
    id = Column(String(250), nullable=False, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    photo = Column(String(250), unique=True)
    premium = Column(String(250), nullable=True)
    token = Column(String(250), nullable=True, unique=True)
    terakhir_login = Column(DateTime, nullable=False)


class LahanModel(db.Model, TimeStamp):
    __tablename__ = "lahan"
    id = Column(String(250), nullable=False, primary_key=True)
    user_id = Column(String(250), ForeignKey("pengguna.id"))
    nama = Column(String(250), nullable=False)
    luas = Column(Double, nullable=False)
    alamat = Column(String(250), nullable=True)
    lat = Column(Double, default=Null)
    lon = Column(Double, default=Null)
