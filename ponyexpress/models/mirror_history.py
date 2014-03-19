from ponyexpress.database import db


class PackageHistory(db.Model):
    __tablename__ = 'mirrorhistory'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    #node
    mirrorurl = db.Column(db.String(255))

    #package
    pkgsha = db.Column(db.String(64))
    pkgname = db.Column(db.String(255))
    pkgversion = db.Column(db.String(64))
    pkgsource = db.Column(db.text)

    # date installed
    released = db.Column(db.DATE)

    def __init__(self, sha, mirrorurl, pkgname, pkgversion, pkgsource, releasedate):
        self.sha = sha

        self.mirrorurl = mirrorurl

        self.pkgname = pkgname
        self.pkgversion = pkgversion
        self.pkgsource = pkgsource

        self.released = releasedate

    def __repr__(self):
        return '<PackageHistory %r>' % (self.name, self.version)

