from ponyexpress.database import db


class Package(db.Model):
    __tablename__ = 'packages'

    sha = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(255))
    version = db.Column(db.String(64))

    def __init__(self, sha, name, version):
        self.sha = sha
        self.name = name
        self.version = version

    def __repr__(self):
        return '<Package %r>' % (self.name)
