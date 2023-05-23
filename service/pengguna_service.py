from model.models import PenggunaModel
from schemas import PenggunaSchema


class PenggunaService:
    def __init__(self):
        pass

    def get_all_user(self):
        data = PenggunaModel.query.all()
        pengguna_schema = PenggunaSchema(many=True)
        response_data = {
            "status_code": 200,
            "msg": "Data retrieved successfully",
            "data": pengguna_schema.dump(data),
        }
        return response_data
