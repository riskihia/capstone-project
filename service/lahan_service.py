import random
import uuid

from model.models import LahanImageModel, LahanModel
from util.db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_smorest import abort
from schemas import PostLahanSchema
from flask import jsonify


class LahanService:
    def __init__(self):
        pass

    def get_all_lahan(self):
        try:
            data = LahanModel.query.filter(LahanModel.deleted_at.is_(None)).all()

            lahan_schema = PostLahanSchema(many=True)

            response_data = {
                "error": False,
                "message": "Lahan fetched successfully",
                "data": lahan_schema.dump(data),
            }
            return jsonify(response_data), 200
        except Exception as e:
            print(e)

    def post_lahan(self, lahan_data):
        try:
            lahan = LahanImageModel.query.filter(
                LahanImageModel.deleted_at.is_(None)
            ).all()
            lahan_data["id"] = str(uuid.uuid4())
            random_photo = random.choice([l.photo for l in lahan])
            lahan_data["photo"] = random_photo

            new_lahan = LahanModel(**lahan_data)
            db.session.add(new_lahan)
            db.session.commit()

            return {"error": False, "message": "Lahan added successfully"}
        except IntegrityError:
            # Jika user_id tidak valid
            abort(400, message="User id not valid")
        except SQLAlchemyError:
            # Kesalahan umum saat menyisipkan item
            abort(500, message="An error occurred while inserting item")
