from ponyexpress.database import db


class Repository(db.Model):
    __tablename__ = 'repositories'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    name = db.Column(db.String(255))

    uri = db.Column(db.String(255))

    label = db.Column(db.String(255))

    provider = db.Column(db.String(12))

    def __init__(self):
        pass

    def __repr__(self):
        return '<Repository %r>' % self.name

