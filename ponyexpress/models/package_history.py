from ponyexpress.database import db


class PackageHistory(db.Model):
    __tablename__ = 'packagehistory'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    #node
    nodename = db.Column(db.String(255))

    #package
    pkgsha = db.Column(db.String(64))
    pkgname = db.Column(db.String(255))
    pkgversion = db.Column(db.String(64))
    pkgsource = db.Column(db.TEXT)

    # date installed
    installed = db.Column(db.DATE)

    def __init__(self, nodename, pkgsha, pkgname, pkgversion, pkgsource, installdate):
        self.nodename = nodename

        self.pkgsha = pkgsha
        self.pkgname = pkgname
        self.pkgversion = pkgversion
        self.pkgsource = pkgsource

        self.installed = installdate

    def __repr__(self):
        return '<PackageHistory %r>' % self.pkgname
