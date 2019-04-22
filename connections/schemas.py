from marshmallow import fields
from marshmallow_enum import EnumField

from connections.extensions import ma
from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person


class BaseModelSchema(ma.ModelSchema):
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)


class PersonSchema(BaseModelSchema):
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()

    class Meta:
        model = Person


class ConnectionSchema(BaseModelSchema):
    from_person_id = fields.Integer()
    to_person_id = fields.Integer()
    connection_type = EnumField(ConnectionType)
    from_person = fields.Nested(PersonSchema, only=["email", "first_name", "last_name"])
    to_person = fields.Nested(PersonSchema, only=["email", "first_name", "last_name"])
    # from_person = fields.Nested(PersonSchema)

    class Meta:
        model = Connection
