from http import HTTPStatus
import json
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from webargs.flaskparser import use_args
from webargs import fields
from connections.models.person import Person
from connections.models.connection import Connection
from connections.schemas import ConnectionSchema, PersonSchema

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
@use_args({"sort": fields.Str(location="query")})
def get_people(args):
    people_schema = PersonSchema(many=True)

    if(args):
        if(args['sort'] == '-created_at'):
            people = Person.query.order_by(Person.created_at.desc()).all()
        elif(args['sort'] == 'created_at'):
            people = Person.query.order_by(Person.created_at).all()
        elif(args['sort'] == '-name'):
            people = Person.query.order_by(Person.first_name.desc()).all()
        elif(args['sort'] == 'name'):
            people = Person.query.order_by(Person.first_name).all()
        else:
            people = Person.query.options(joinedload(Person.connections)).all()

    else:
        people = Person.query.options(joinedload(Person.connections)).all()

    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


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
