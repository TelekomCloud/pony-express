from ponyexpress.database import db


class Node(db.Model):
    __tablename__ = 'nodes'

    name = db.Column(db.String(255), primary_key=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Node %r>' % (self.name)
