from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)

    connections = db.relationship('Connection', foreign_keys='Connection.from_person_id')

    def mutual_friends(self, target):
        friend_ids = [
            i.to_person_id for i in self.connections
            if i.connection_type.value == 'friend'
        ]

        return [
            (db.session.query(Person).get(mutual))
            for mutual in friend_ids
            if mutual in ([j.to_person_id for j in target.connections])
        ]
