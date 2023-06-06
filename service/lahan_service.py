import datetime
import random
import uuid
from sqlalchemy import text
import traceback

from model.models import LahanImageModel, LahanModel, TanamModel
from util.config import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_smorest import abort
from schemas import GetLahanSchema, TanamGetLahanSchema, TanamSchema
from flask import jsonify
from flask_jwt_extended import get_jwt_identity


class LahanService:
    def __init__(self):
        pass

    def get_tanam_detail(self, lahan_id):
        try:
            tanam = TanamModel.query.filter_by(lahan_id=lahan_id).first()
            tanam_schema = TanamSchema()
            response_data = {
                "error": False,
                "message": "Lahan fetched successfully",
                "data": tanam_schema.dump(tanam),
            }
            return jsonify(response_data), 200
        except Exception as e:
            print(e)

    def get_lahan_detail(self, lahan_id):
        try:
            data = (
                LahanModel.query.filter_by(id=lahan_id)
                .filter(LahanModel.deleted_at.is_(None))
                .first()
            )

            lahan_schema = TanamGetLahanSchema()
            response_data = {
                "error": False,
                "message": "Lahan fetched successfully",
                "data": lahan_schema.dump(data),
            }
            return jsonify(response_data), 200

        except Exception as e:
            error_message = str(e)  # Get the error message as a string
            response_data = {
                "error": True,
                "message": "An error occurred: " + error_message,
            }
            return jsonify(response_data), 500

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
        lahan = LahanModel.query.filter_by(id=lahan_id).first()

        if lahan is None:
            return jsonify({"error": True, "message": "Lahan not found"})
        else:
            is_deleted = LahanModel.query.filter(
                LahanModel.deleted_at.is_(None), LahanModel.id == lahan_id
            ).first()
            if is_deleted is None:
                return jsonify({"error": True, "message": "Lahan Already Deleted"})
            else:
                try:
                    lahan.deleted_at = datetime.datetime.now()
                    db.session.commit()
                except Exception as e:
                    print(e)
                return jsonify(
                    {"error": False, "message": "Lahan deleted successfully"}
                )
