from ponyexpress.database import db


class RepoHistory(db.Model):
    __tablename__ = 'repohistory'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    #node
    repo_id = db.Column(db.Integer, db.ForeignKey('repositories.id'))
    repository = db.relationship("Repository")

    #package
    pkgsha = db.Column(db.String(255))
    pkgname = db.Column(db.String(255))
    pkgversion = db.Column(db.String(64))
    pkgsource = db.Column(db.Text)

    # date installed
    released = db.Column(db.DATE)

    def __init__(self, repository, pkgsha, pkgname, pkgversion, pkgsource, releasedate):
        self.repository = repository

        self.pkgsha = pkgsha
        self.pkgname = pkgname
        self.pkgversion = pkgversion
        self.pkgsource = pkgsource

        self.released = releasedate

    def __repr__(self):
        return '<RepoHistory %r>' % (self.pkgname)

