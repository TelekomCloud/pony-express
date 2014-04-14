import os

from .test_server import *

from ponyexpress.api.lib.repositories import Repositories
from ponyexpress.models.repository import Repository
from ponyexpress.api.lib.package_import import PackageImport

from ponyexpress.models.repo_history import RepoHistory


class TestRepository(TestServerBase):

    def test_update_repository(self):
        """Test package list downloading"""

        self.repositories = Repositories()

        repo = Repository()
        repo.id = 1
        repo.provider = 'apt'
        repo.name = 'Test'
        repo.uri = 'http://de.archive.ubuntu.com/ubuntu/dists/precise/main/binary-amd64/Packages.gz'
        repo.label = 'Test'

        path = os.path.dirname(__file__)
        datafile = os.path.join(path, 'data/install_tiny.txt')
        data_install = self.process_data(datafile)

        test_importer = PackageImport()
        test_importer.process_node_info(data_install)

        self.repositories.select_provider(repo)
        self.repositories.update_repository(repo)

        self.assertGreater(RepoHistory.query.count(), 1)

    def test_get_outdated_packages(self):
        self.repositories = Repositories()

        # create the demo repo
        data = {}
        data['name'] = 'Repo1'
        data['label'] = 'main'
        data['uri'] = 'http://de.archive.ubuntu.com/ubuntu/dists/precise/main/binary-amd64/Packages.gz'
        data['provider'] = 'apt'

        repo_id = self.repositories.create_repository(data)
        repo = Repository.query.filter_by(id=repo_id).first()

        path = os.path.dirname(__file__)
        datafile = os.path.join(path, 'data/install_tiny.txt')
        data_install = self.process_data(datafile)

        test_importer = PackageImport()
        test_importer.process_node_info(data_install)

        self.repositories.select_provider(repo)
        self.repositories.update_repository(repo)

        self.assertGreater(RepoHistory.query.count(), 5000)

        packages = self.repositories.get_outdated_packages('ponyexpress', [repo])

        self.assertIsNotNone(packages)
        #self.assertNotEqual(packages, [])

        self.assertIsInstance(packages[0].upstream_version, list)
        #self.assertGreaterEqual(len(packages[0].upstream_version), 1)

    def test_get_outdated_packages_multi(self):
        self.repositories = Repositories()

        # create the demo repo
        data = {}
        data['name'] = 'Repo1'
        data['label'] = 'main'
        data['uri'] = 'http://de.archive.ubuntu.com/ubuntu/dists/precise/main/binary-amd64/Packages.gz'
        data['provider'] = 'apt'

        repo_id = self.repositories.create_repository(data)
        repo1 = Repository.query.filter_by(id=repo_id).first()

        data = {}
        data['name'] = 'Repo2'
        data['label'] = 'beta'
        data['uri'] = 'http://de.archive.ubuntu.com/ubuntu/dists/trusty/main/binary-amd64/Packages.gz'
        data['provider'] = 'apt'

        repo_id = self.repositories.create_repository(data)
        repo2 = Repository.query.filter_by(id=repo_id).first()

        path = os.path.dirname(__file__)
        datafile = os.path.join(path, 'data/install_tiny.txt')
        data_install = self.process_data(datafile)

        test_importer = PackageImport()
        test_importer.process_node_info(data_install)

        self.repositories.select_provider(repo1)
        self.repositories.update_repository(repo1)

        self.repositories.select_provider(repo2)
        self.repositories.update_repository(repo2)

        self.assertGreater(RepoHistory.query.count(), 5000)

        packages = self.repositories.get_outdated_packages('ponyexpress', [repo1, repo2])

        self.assertIsNotNone(packages)
        self.assertNotEqual(packages, [])

        self.assertIsInstance(packages[0].upstream_version, list)
        #self.assertGreaterEqual(len(packages[0].upstream_version), 1)

    def test_version_compare(self):
        self.repositories = Repositories()

        vers = ['1.0.0', '1.0.1',
                '0.5.7', '0.20',
                '0.6.15-2ubuntu9', '0.6.15-2ubuntu10',
                '0.6.15-2ubuntu9', '0.6.17-2ubuntu9',
                '0.1.1-1ubuntu1'
        ]

        # first two
        self.assertEqual(self.repositories.ver_cmp(vers[0], vers[1]), -1)

        # third and fourth
        self.assertEqual(self.repositories.ver_cmp(vers[2], vers[3]), 1)

        # with ubuntu string
        self.assertEqual(self.repositories.ver_cmp(vers[4], vers[5]), 1)

        #with ubuntu, upstream version change
        self.assertEqual(self.repositories.ver_cmp(vers[6], vers[7]), -1)

        #
        self.assertEqual(self.repositories.ver_cmp(vers[8], vers[8]), 0)

    def test_get_repositories(self):
        self.repositories = Repositories()

        # create the demo repo
        data = {}
        data['name'] = 'Repo1'
        data['label'] = 'main'
        data['uri'] = 'http://www.software.repo'
        data['provider'] = 'apt'
        repo_id = self.repositories.create_repository(data)

        expression = '1,2,3'

        repo_list = self.repositories.get_repositories(expression)
        self.assertIsInstance(repo_list, list)
        self.assertEqual(repo_list[0].id, repo_id)

if __name__ == '__main__':
    unittest.main()

