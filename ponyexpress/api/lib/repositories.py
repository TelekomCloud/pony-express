## Handle configured repositores and query for outdated package data
from datetime import date
import re

from ponyexpress.database import db
from ponyexpress.api.lib.providers import *
from ponyexpress.models.repository import Repository
from ponyexpress.models.repo_history import RepoHistory
from ponyexpress.models.package_history import PackageHistory


class Repositories:
    provider = None

    pattern = None  # store the compiled regex pattern

    def __init__(self):
        pass

    @staticmethod
    def create_repository(repodata):
        # name, uri, label, provider   +   id

        # skip checking for the existance of a repo
        # could be done via URI only at this step
        new_repo = Repository()
        new_repo.name = repodata['name']
        new_repo.label = repodata['label']
        new_repo.uri = repodata['uri']
        new_repo.provider = repodata['provider']

        db.session.add(new_repo)
        db.session.commit()

        # return the new object's id
        return new_repo.id

    @staticmethod
    def update_repository_info(repository, repodata):
        # update all known fields
        if 'name' in repodata:
            repository.name = repodata['name']
        if 'uri' in repodata:
            repository.uri = repodata['uri']
        if 'label' in repodata:
            repository.label = repodata['label']
        if 'provider' in repodata:
            repository.provider = repodata['provider']

        # update the database
        db.session.commit()

    @staticmethod
    def delete_repository(repository):
        # remove the entry
        db.session.delete(repository)
        db.session.commit()

    def select_provider(self, repo):
        if repo.provider == 'apt':
            self.provider = AptRepository(repo.uri)
        else:
            raise NotImplementedError()

    def update_repository(self, repository):
        if self.provider is not None:
            metadata = self.provider.fetch_metadata()
        else:
            raise Exception()

        if metadata is not None:

            try:
                mvals = metadata.itervalues()
            except:
                mvals = metadata.values()

            for m in mvals:
                hist = RepoHistory(repository, m['sha256'], m['package'], m['version'], m['filename'], date.today())

                db.session.add(hist)
            db.session.commit()

    def get_outdated_packages(self, node_filter, repo_list):
        """Compare packages available on the repository server with those available on a set of nodes"""

        outdated_packages = {}

        if not isinstance(repo_list, list):
            return []

        # get packages from selected nodes
        if node_filter != '':
            node_filter_expression = ('%%%s%%' % node_filter)

            packages_history = PackageHistory.query.filter(PackageHistory.nodename.like(node_filter_expression)).all()
        else:
            packages_history = PackageHistory.query.all()

        if packages_history is not None:
            for package in packages_history:
                #try:
                if repo_list is not []:
                    rl = []
                    for repo in repo_list:
                        rl.append(repo.id)

                    mp = RepoHistory.query.filter(RepoHistory.pkgname == package.pkgname) \
                                          .filter(RepoHistory.repo_id.in_(rl)).all()

                    if mp is not None:
                        upstream_version = []
                        for p in mp:
                            # compare versions
                            res = self.ver_cmp(package.pkgversion, p.pkgversion)

                            if res < 0:
                                # repository is newer
                                upstream_version.append(p.pkgversion)

                        package.upstream_version = upstream_version

                        if package.pkgname not in outdated_packages:
                            outdated_packages[package.pkgname] = package
                else:
                    return []
                #except Exception as e:
                #    # Catch exceptions and move on to the next object
                #    print(e)
                #    #next()

            return list(outdated_packages.values())
        else:
            return []

    def get_repositories(self, expression):
        #check if expression is an integer or a comma separated list of values

        repo_list = []

        if expression is not None and (isinstance(expression, int) or expression.isdigit()):
            repo_id = int(expression)
            if repo_id > 0:
                repo = Repository.query.filter_by(id=repo_id).first()
                if repo is not None:
                    repo_list.append(repo)
        else:
            # assume expression is a list of repository numeric identifiers
            split = expression.split(',')

            if split is None:
                return []

            expression_list = [s for s in split if s.isdigit()]

            if expression_list is not None and isinstance(expression_list, list):
                repos = Repository.query.filter(Repository.id.in_(expression_list)).all()
                if repos is not None:
                    repo_list = repos

        return repo_list

    def get_repositories_by_label(self, label):
        #check if expression is an integer or a comma separated list of values

        if label is not None and label != '':
            repo_list = Repository.query.filter_by(label=label).all()
            if repo_list is not None:
                return repo_list

        return []

    def _ver_tuple(self, z):
        """Parse debian/ubuntu style version strings and return a tuple containing only numbers"""

        if self.pattern is None:
            self.pattern = re.compile('/(?<=\d)(?=\D)|(?<=\D)(?=\d)/')

        a = self.pattern.split(z)

        if a is not None and len(a) > 0:
            return tuple([str(x) for x in a[0] if x.isdigit()])

        return None

    def ver_cmp(self, a, b):
        """Compare two version tuples"""

        # TODO: handle different length versions
        va = self._ver_tuple(a)
        vb = self._ver_tuple(b)

        # When the second tuple is longer we assume it's a newer version
        #if len(va) != len(vb):
        #    return -1

        #return va < vb
        if va < vb:
            return -1
        elif va == vb:
            return 0
        elif va > vb:
            return 1
