from ponyexpress.database import db


class Mirror(db.Model):
    __tablename__ = 'mirrors'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    name = db.Column(db.String(255), primary_key=True)

    uri = db.Column(db.String(255))

    label = db.Column(db.String(255))

    provider = db.Column(db.String(12))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Node %r>' % self.name

