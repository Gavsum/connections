from marshmallow import fields
from marshmallow_enum import EnumField

from connections.extensions import ma
from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person


class BaseModelSchema(ma.ModelSchema):
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)


class PersonSchema(BaseModelSchema):
    first_name = fields.Str(required=True)
    last_name = fields.Str()
    email = fields.Email(required=True)

    # Two way nesting https://bit.ly/2XCnWM6
    # connections = fields.Nested(
    #     'ConnectionSchema',
    #     many=True,
    #     only=['connection_type', 'id', 'to_person_id']
    # )

    class Meta:
        model = Person


class ConnectionSchema(BaseModelSchema):
    from_person_id = fields.Integer(required=True)
    to_person_id = fields.Integer(required=True)
    connection_type = EnumField(ConnectionType)
    from_person = fields.Nested(PersonSchema, only=['email', 'first_name', 'last_name'])
    to_person = fields.Nested(PersonSchema, only=['email', 'first_name', 'last_name'])

    class Meta:
        model = Connection
