from ponyexpress.database import db
from ponyexpress.api.lib.serializer import Serializer, JSONEncoder
import json

node_packages = db.Table('node_packages',
                         db.Column('node_name', db.String, db.ForeignKey('nodes.name'), primary_key=True),
                         db.Column('package_sha', db.Integer, db.ForeignKey('packages.sha'), primary_key=True)
)


class Node(db.Model, Serializer):
    __tablename__ = 'nodes'

    name = db.Column(db.String(255), primary_key=True, unique=True)

    packages = db.relationship('Package', secondary=node_packages,
                               backref=db.backref('nodes', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Node %r>' % self.name

    def as_json(self):
        return json.dumps(self.to_serializable_dict(), cls=JSONEncoder)
