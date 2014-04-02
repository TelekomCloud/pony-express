from ponyexpress.database import db

from ponyexpress.models.mirror import Mirror

# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     child_id = Column(Integer, ForeignKey('child.id'))
#     child = relationship("Child")
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)

class MirrorHistory(db.Model):
    __tablename__ = 'mirrorhistory'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    #node
    #mirror = db.Column(db.Integer)
    mirror_id = db.Column(db.Integer, db.ForeignKey('mirrors.id'))
    mirror = db.relationship("Mirror")

    #package
    pkgsha = db.Column(db.String(255))
    pkgname = db.Column(db.String(255))
    pkgversion = db.Column(db.String(64))
    pkgsource = db.Column(db.Text)

    # date installed
    released = db.Column(db.DATE)

    def __init__(self, mirror, pkgsha, pkgname, pkgversion, pkgsource, releasedate):
        self.mirror = mirror

        self.pkgsha = pkgsha
        self.pkgname = pkgname
        self.pkgversion = pkgversion
        self.pkgsource = pkgsource

        self.released = releasedate

    def __repr__(self):
        return '<MirrorHistory %r>' % (self.pkgname)

