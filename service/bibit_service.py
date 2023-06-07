from model.models import BibitModel
from schemas import BibitSchema
from util.config import db
from flask import jsonify


class BibitService:
    def __init__(self):
        pass

    def get_all_bibit(self):
        try:
            bibit = BibitModel.query.filter(BibitModel.deleted_at.is_(None)).all()

            bibit_schema = BibitSchema(many=True)

            response_data = {
                "error": False,
                "message": "Data Bibi fetched successfully",
                "data": bibit_schema.dump(bibit),
            }
            return jsonify(response_data), 200
        except Exception as e:
            print(e)
