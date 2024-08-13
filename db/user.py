from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField(unique=True, index=True)
    language_code = fields.TextField(null=True)

    registration_date = fields.DatetimeField(null=True)
    creation_date = fields.DatetimeField(auto_now_add=True)

    username = fields.TextField(null=True)
    first_name = fields.TextField(null=True)
    last_name = fields.TextField(null=True)

    is_bot_blocked: bool = fields.BooleanField(default=False)
