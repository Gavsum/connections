from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email'
]


def test_can_get_mutual_friends(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()

    ConnectionFactory.create_batch(5, to_person=instance)
    ConnectionFactory.create_batch(5, to_person=target)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person=instance, to_person=f,
                          connection_type='friend')
        ConnectionFactory(from_person=target, to_person=f,
                          connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=instance, to_person=decoy,
                      connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy,
                      connection_type='coworker')

    db.session.commit()

    expected_mutual_friend_ids = [f.id for f in mutual_friends]

    res = testapp.get('/people/{}/mutual_friends?target_id={}'.format(instance.id, target.id))
    assert res.status_code == HTTPStatus.OK

    res_reverse = (testapp.get('/people/{}/mutual_friends?target_id={}'
                   .format(target.id, instance.id)))

    assert res_reverse.status_code == HTTPStatus.OK
    assert len(res.json) == 3

    for f in res.json:
        assert f['id'] in expected_mutual_friend_ids

    assert res.json == res_reverse.json

    for person in res.json:
        for field in EXPECTED_FIELDS:
            assert field in person
