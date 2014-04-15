from ponyexpress.database import db


class PackageHistory(db.Model):
    __tablename__ = 'packagehistory'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    #node
    nodename = db.Column(db.String(255))

    #package
    pkgsha = db.Column(db.String(255))
    pkgname = db.Column(db.String(255))
    pkgversion = db.Column(db.String(64))
    pkgsource = db.Column(db.Text)
    pkgarch = db.Column(db.String(16))

    # date installed
    installed = db.Column(db.DATE)

    upstream_version = []

    provider = ''
    summary = ''

    sha = db.synonym('pkgsha')
    name = db.synonym('pkgname')
    version = db.synonym('pkgversion')
    uri = db.synonym('pkgsource')
    architecture = db.synonym('pkgarch')

    def __init__(self, nodename, pkgsha, pkgname, pkgversion, pkgsource, installdate):
        self.nodename = nodename

        self.pkgsha = pkgsha
        self.pkgname = pkgname
        self.pkgversion = pkgversion
        self.pkgsource = pkgsource

        self.installed = installdate

    def __repr__(self):
        return '<PackageHistory %r>' % self.pkgname
