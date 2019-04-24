from http import HTTPStatus
import pytest
from tests.factories import ConnectionFactory
from connections.models.connection import Connection


@pytest.fixture
def connection_payload():
    return {
        'connection_type': 'coworker'
    }


def test_can_patch_connection(db, testapp, connection_payload):
    testConnection = ConnectionFactory()
    db.session.commit()

    res = testapp.patch('/connections/{}'.format(testConnection.id), json=connection_payload)

    assert res.status_code == HTTPStatus.OK
    assert res.json['connection_type'] == connection_payload['connection_type']

    modConnect = Connection.query.get(res.json['id'])
    assert modConnect is not None
    assert getattr(modConnect, 'connection_type').value == connection_payload['connection_type']


@pytest.mark.parametrize('field, value, error_message', [
    pytest.param('connection_type',
                 None,
                 "Field may not be null.",
                 id='missing type'),
    pytest.param('connection_type',
                 "elephant",
                 "Invalid connection type: elephant",
                 id='invalid type')
])
def test_patch_validations(db, testapp, connection_payload, field, value, error_message):
    connection_payload[field] = value
    testConnection = ConnectionFactory()
    db.session.commit()

    res = testapp.patch('connections/{}'.format(testConnection.id), json=connection_payload)

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']

    # This is kind of hacky
    if(connection_payload[field] is None):
        assert error_message in errors[field]
    else:
        assert error_message in errors
