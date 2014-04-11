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

    def create_repository(self, repodata):
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

    def update_repository_info(self, repository, repodata):
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

    def delete_repository(self, repository):
        # remove the entry
        db.session.delete(repository)
        db.session.commit()

    def update_repository(self, repository):

        # TODO: replace with better class selection
        if repository.provider == 'apt':
            m = AptRepository(repository.uri)

            metadata = m.fetch_metadata()
        else:
            raise NotImplementedError()

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

        outdated_packages = []

        if not isinstance(repo_list, list):
            return []

        # get packages from selected nodes
        node_filter_expression = ('%%%s%%' % node_filter)

        packages_history = PackageHistory.query.filter(PackageHistory.nodename.like(node_filter_expression)).all()

        # get packages from selected set of repositories, filter by label
        #repo_list = self.get_repositories(repository)

        if packages_history is not None:

            for package in packages_history:
                try:
                    if repo_list is not []:
                        for repo in repo_list:
                            mp = RepoHistory.query.filter(RepoHistory.pkgname == package.pkgname,
                                                          RepoHistory.repo_id == repo.id). \
                                order_by(RepoHistory.pkgversion).first()

                        if mp is not None:
                            # compare versions
                            res = self.ver_cmp(package.pkgversion, mp.pkgversion)

                            if res < 0:
                                # repository is newer
                                package.upstream_version = mp.pkgversion
                                outdated_packages.append(package)
                    else:
                        return []
                except Exception as e:
                    # Catch exceptions and move on to the next object
                    print(e)
                    #next()

            return outdated_packages
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

    def _ver_tuple(self, z):
        """Parse debian/ubuntu style version strings and return a tuple containing only numbers"""

        if self.pattern is None:
            self.pattern = re.compile("([0-9]+)\.([0-9]+)\.?([0-9]*)[\-\+\~]?([0-9]|[\+\-\~a-z0-9]*)[a-z]*([0-9]+)")

        a = self.pattern.findall(z)

        if a is not None and len(a) > 0:
            return tuple([str(x) for x in a[0] if x.isdigit()])

        # TODO: fallback, simply return not-equal!!
        #tup = tuple([str(x) for x in z.split('.')])

        return None

    def ver_cmp(self, a, b):
        """Compare two version tuples"""

        # TODO: handle different length versions
        va = self._ver_tuple(a)
        vb = self._ver_tuple(b)

        if len(va) != len(vb):
            return -1

        #return va < vb
        if va < vb:
            return -1
        elif va == vb:
            return 0
        elif va > vb:
            return 1
