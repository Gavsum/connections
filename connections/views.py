from http import HTTPStatus

from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_args

from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person
from connections.schemas import ConnectionSchema, PersonSchema
from connections.extensions import cache

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
@use_args({'sort': fields.Str(location='query')})
@cache.cached(key_prefix='all_people')
def get_people(args):
    print("Cache not used?")
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
    cache.delete('all_people')
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/people/<person_id>/mutual_friends', methods=['GET'])
@use_args({'target_id': fields.Integer(location='query', required=True)})
@cache.cached()
def get_mutual_friends(args, person_id):
    source = Person.query.get_or_404(person_id)
    target = Person.query.get_or_404(args['target_id'])
    people_schema = PersonSchema(many=True)

    mutuals = source.mutual_friends(target)

    return people_schema.jsonify(mutuals), HTTPStatus.OK


@blueprint.route('/connections', methods=['GET'])
@cache.cached()
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
@use_args({'connection_type': fields.Str(
    location='json',
    validate=lambda x: ConnectionType.has_type(x)
)})
def patch_connection(args, connection_id):
    Connection.query.get_or_404(connection_id)
    (Connection.query
        .filter_by(id=connection_id)
        .update({'connection_type': args['connection_type']}))

    return ConnectionSchema().jsonify(Connection.query.get(connection_id)), HTTPStatus.OK


@blueprint.route('/connections/<connection_id>', methods=['DELETE'])
def delete_connection(connection_id):
    connection_to_delete = Connection.query.get_or_404(connection_id)
    connection_to_delete.delete()
    return '', HTTPStatus.NO_CONTENT
