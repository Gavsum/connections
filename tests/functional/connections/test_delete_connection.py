from http import HTTPStatus

from tests.factories import ConnectionFactory

from connections.models.connection import Connection


def test_can_delete_connection(db, testapp):
    new_connection = ConnectionFactory()
    db.session.commit()

    res = testapp.delete('connections/{}'.format(new_connection.id))

    assert res.status_code == HTTPStatus.NO_CONTENT
    assert db.session.query(Connection).get(new_connection.id) is None
