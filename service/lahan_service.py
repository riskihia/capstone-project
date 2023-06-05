import datetime
import random
import uuid
from sqlalchemy import text

from model.models import LahanImageModel, LahanModel
from util.config import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_smorest import abort
from schemas import GetLahanSchema
from flask import jsonify
from flask_jwt_extended import get_jwt_identity


class LahanService:
    def __init__(self):
        pass

    def get_user_lahan(self):
        current_user = get_jwt_identity()

        try:
            # data = LahanModel.query.filter(LahanModel.deleted_at.is_(None)).all()
            data = (
                LahanModel.query.filter_by(user_id=current_user)
                .filter(LahanModel.deleted_at.is_(None))
                .all()
            )
            lahan_schema = GetLahanSchema(many=True)

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

    def delete_lahan(self, lahan_id):
        # lahan = LahanModel.query.filter_by(id=lahan_id).first()
        # is_deleted = LahanModel.query.filter(
        #     LahanModel.deleted_at.is_(None), LahanModel.id == lahan_id
        # ).first()
        print(lahan_id)
        return jsonify({"hai": "hai"})
