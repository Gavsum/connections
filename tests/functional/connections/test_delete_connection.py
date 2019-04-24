from http import HTTPStatus
from tests.factories import ConnectionFactory
from connections.models.connection import Connection


def test_can_delete_connection(db, testapp):
    newConnection = ConnectionFactory()
    db.session.commit()

    res = testapp.delete('connections/{}'.format(newConnection.id))

    assert res.status_code == HTTPStatus.OK
    assert db.session.query(Connection).get(newConnection.id) is None
