from marshmallow import Schema, fields, post_dump


class TimeStampSchema(Schema):
    # created_at = fields.DateTime(required=True, dump_only=False)
    # updated_at = fields.DateTime(required=True, dump_only=False)
    # deleted_at = fields.DateTime(required=True, dump_only=True)
    pass


class AuthLogoutSchema(TimeStampSchema):
    email = fields.Str(required=True, load_only=True)


class AuthPenggunaSchema(TimeStampSchema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)


class UserPenggunaSchema(AuthPenggunaSchema):
    id = fields.Str(dump_only=True)
    email = fields.Str(required=True)
    photo = fields.Str()
    premium = fields.Boolean(required=False)
    terakhir_login = fields.DateTime(dump_only=True)


class PlainPenggunaSchema(AuthPenggunaSchema):
    id = fields.Str(dump_only=True)
    photo = fields.Str()
    premium = fields.Boolean(required=False)
    token = fields.Str(required=False)
    terakhir_login = fields.DateTime(dump_only=True)


class LahanImageSchema(TimeStampSchema):
    nama = fields.Str(dump_only=True)
    photo = fields.Str(dump_only=True)


class GetLahanSchema(TimeStampSchema):
    id = fields.Str()
    nama = fields.Str(required=True)
    image = fields.Str(dump_only=True)
    luas = fields.Float(required=True)
    alamat = fields.Str(required=False)
    lat = fields.Float(required=False, allow_none=True)
    lon = fields.Float(required=False, allow_none=True)


class PostLahanSchema(TimeStampSchema):
    user_id = fields.Str()
    nama = fields.Str(required=True)
    image = fields.Str(dump_only=True)
    luas = fields.Float(required=True)
    alamat = fields.Str(required=False)
    lat = fields.Float(required=False, allow_none=True)
    lon = fields.Float(required=False, allow_none=True)


class PlainLahanSchema(TimeStampSchema):
    id = fields.Str(required=True, load_only=True)
    nama = fields.Str(required=True)
    photo = fields.Str()
    luas = fields.Float(required=True)
    alamat = fields.Str(required=False)
    lat = fields.Float(required=False)
    lon = fields.Float(required=False)


class UploadSchema(TimeStampSchema):
    nama = fields.Str(required=True, load_only=True)


class PenggunaSchema(PlainPenggunaSchema):
    lahan = fields.List(fields.Nested(PlainLahanSchema()), dump_only=True)


class LahanSchema(PlainLahanSchema):
    pengguna = fields.Nested(PlainPenggunaSchema(), dump_only=True)


class UserLahanSchema(UserPenggunaSchema):
    lahan = fields.List(fields.Nested(PlainLahanSchema()), dump_only=True)

    @post_dump(pass_many=True)
    def limit_lahan(self, data, many, **kwargs):
        # Batasi jumlah lahan menjadi 5 data
        if many:
            for item in data:
                item["lahan"] = item["lahan"][:5] if item["lahan"] else []
        else:
            data["lahan"] = data["lahan"][:5] if data["lahan"] else []
        return data
