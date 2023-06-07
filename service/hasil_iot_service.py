from flask import jsonify
from model.models import PenggunaModel
from schemas import UserLahanSchema
from util.config import db

from flask_jwt_extended import get_jwt_identity


class HasilIotService:
    def __init__(self):
        pass

    def get_hasil_iot(self):
        pass
