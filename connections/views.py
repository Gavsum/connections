from http import HTTPStatus
from flask import Blueprint
from webargs.flaskparser import use_args
from webargs import fields
from connections.models.person import Person
from connections.models.connection import Connection, ConnectionType
from connections.schemas import ConnectionSchema, PersonSchema

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
@use_args({"sort": fields.Str(location="query")})
def get_people(args):
    people_schema = PersonSchema(many=True)
    order_by = None

    if(args):
        if(args['sort'] == '-created_at'):
            order_by = Person.created_at.desc()
        elif(args['sort'] == 'created_at'):
            order_by = Person.created_at
        elif(args['sort'] == '-name'):
            order_by = Person.first_name.desc()
        elif(args['sort'] == 'name'):
            order_by = Person.first_name

    people = (Person.query
              .order_by(order_by)
              .all())

    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/people/<person_id>/mutual_friends', methods=['GET'])
@use_args({"target_id": fields.Integer(location="query", required=True)})
def get_mutual_friends(args, person_id):
    source = Person.query.get_or_404(person_id)
    target = Person.query.get_or_404(args['target_id'])
    people_schema = PersonSchema(many=True)

    mutuals = source.mutual_friends(target)

    return people_schema.jsonify(mutuals), HTTPStatus.OK


@blueprint.route('/connections', methods=['GET'])
def get_connections():
    connection_schema = ConnectionSchema(many=True)
    connections = Connection.query.all()

    return connection_schema.jsonify(connections), HTTPStatus.OK


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections/<connection_id>', methods=['PATCH'])
@use_args({"connection_type": fields.Str(
    location="json",
    validate=lambda x: ConnectionType.has_type(x)
)})
def patch_connection(args, connection_id):
    Connection.query.get_or_404(connection_id)
    (Connection.query
        .filter_by(id=connection_id)
        .update({"connection_type": args['connection_type']}))

    return ConnectionSchema().jsonify(Connection.query.get(connection_id)), HTTPStatus.OK


@blueprint.route('/connections/<connection_id>', methods=['DELETE'])
def delete_connection(connection_id):
    connectionToDelete = Connection.query.get_or_404(connection_id)
    connectionToDelete.delete()
    return '', HTTPStatus.NO_CONTENT
