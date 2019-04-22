from http import HTTPStatus

from tests.factories import PersonFactory, ConnectionFactory


# Expected Fields

def test_can_get_connections(db, testapp):
    # Make some Connections

    # Commit the connections to the db

    # call the endpoint with testapp.get('/connectoins')

    # assert responsecode ok

    # assert # of responded connections == number of created

    # assert that all connections contain the expected fields specified above