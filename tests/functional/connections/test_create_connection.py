from http import HTTPStatus

import pytest
from tests.factories import PersonFactory

from connections.models.connection import Connection


@pytest.fixture
def connection_payload():
    return {
        'from_person_id': 1,
        'to_person_id': 2,
        'connection_type': 'mother',
    }


def test_can_create_connection(db, testapp):
    person_from = PersonFactory(first_name='Diana')
    person_to = PersonFactory(first_name='Harry')
    db.session.commit()
    payload = {
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,
        'connection_type': 'mother',
    }
    res = testapp.post('/connections', json=payload)

    assert res.status_code == HTTPStatus.CREATED

    assert 'id' in res.json

    connection = Connection.query.get(res.json['id'])

    assert connection is not None
    assert connection.from_person_id == person_from.id
    assert connection.to_person_id == person_to.id
    assert connection.connection_type.value == 'mother'


@pytest.mark.parametrize('field, value, error_message', [
    pytest.param('from_person_id', None, 'Field may not be null.', id='missing from_person_id'),
    pytest.param('from_person_id', 'blue', 'Not a valid integer.',  id='invalid from id'),
    pytest.param('to_person_id', None, 'Field may not be null', id='missing to_person_id'),
    pytest.param('to_person_id', 'blue', 'Not a valid integer.', id='invalid to id'),
    pytest.param('connection_type', None, 'Field may not be null', id='missing connection_type'),
    pytest.param(
        'connection_type',
        'doppelganger',
        'Invalid enum member doppelganger',
        id='invalid connection type')
])
def test_create_person_validations(db, testapp, connection_payload, field, value, error_message):
    connection_payload[field] = value

    res = testapp.post('/connections', json=connection_payload)
    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']
    assert error_message in errors[field][0]
