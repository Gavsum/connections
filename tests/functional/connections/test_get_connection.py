from http import HTTPStatus
from tests.factories import PersonFactory, ConnectionFactory
from connections.models.connection import Connection
from connections.models.person import Person
EXPECTED_FIELDS = [
    'connection_type',
    'from_person',
    'from_person_id',
    'to_person',
    'to_person_id',
    'id'
]


def test_can_get_connections(db, testapp):
    ConnectionFactory.create_batch(10)
    db.session.commit()

    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for connection in res.json:
        for field in EXPECTED_FIELDS:
            assert field in connection
