import os
import io

from .test_server import *

from ponyexpress.api.lib.repositories import Repositories
from ponyexpress.api.lib.providers import MockRepository
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

        self.repositories.provider = MockRepository()

        self.repositories.update_repository(repo)

        self.assertEqual(RepoHistory.query.count(), 1)

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

        data = {'75da5ca65e2160e994c33d1006046c2be954efe804a24d34628d0c4cac791ce4': {
                "package": "accountsservice",
                "filename": "http://us.archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_0.6.21-6ubuntu5.1_amd64.deb",
                "description": "query and manipulate user account information",
                "version": "0.6.21-6ubuntu5.1",
                "architecture": "amd64",
                "sha256": "75da5ca65e2160e994c33d1006046c2be954efe804a24d34628d0c4cac791ce4"
            },
        }

        self.repositories.provider = MockRepository(data)

        self.repositories.update_repository(repo)

        self.assertEqual(RepoHistory.query.count(), 1)

        packages = self.repositories.get_outdated_packages('ponyexpress', [repo])

        self.assertIsNotNone(packages)
        #self.assertNotEqual(packages, [])

        self.assertIsInstance(packages[0].upstream_version, list)
        self.assertEqual(len(packages[0].upstream_version), 1)

        self.assertEqual(packages[0].pkgversion, '0.6.15-2ubuntu9')
        self.assertEqual(packages[0].upstream_version, ['0.6.21-6ubuntu5.1'])

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

        data1 = {'75da5ca65e2160e994c33d1006046c2be954efe804a24d34628d0c4cac791ce4': {
                "package": "accountsservice",
                "filename": "http://us.archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_0.6.21-6ubuntu5.1_amd64.deb",
                "description": "query and manipulate user account information",
                "version": "0.6.21-6ubuntu5.1",
                "architecture": "amd64",
                "sha256": "75da5ca65e2160e994c33d1006046c2be954efe804a24d34628d0c4cac791ce4"
            },
        }

        #self.repositories.select_provider(repo1)
        self.repositories.provider = MockRepository(data1)

        self.repositories.update_repository(repo1)

        data2 = {'2ea5cb960f976935484eff2a2f4f642a991c2af7a88d08b7731dfcd3e3cc3b20': {
                "package": "accountsservice",
                "filename": "http://us.archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_0.6.35-0ubuntu7_amd64.deb",
                "description": "query and manipulate user account information",
                "version": "0.6.35-0ubuntu7",
                "architecture": "amd64",
                "sha256": "2ea5cb960f976935484eff2a2f4f642a991c2af7a88d08b7731dfcd3e3cc3b20"
            },
        }

        #self.repositories.select_provider(repo2)
        self.repositories.provider = MockRepository(data2)
        self.repositories.update_repository(repo2)

        self.assertEqual(RepoHistory.query.count(), 2)

        packages = self.repositories.get_outdated_packages('ponyexpress', [repo1, repo2])

        self.assertIsNotNone(packages)
        self.assertNotEqual(packages, [])

        self.assertIsInstance(packages[0].upstream_version, list)
        self.assertGreaterEqual(len(packages[0].upstream_version), 2)

        self.assertEqual(packages[0].pkgversion, '0.6.15-2ubuntu9')
        self.assertEqual(packages[0].upstream_version, ['0.6.21-6ubuntu5.1', '0.6.35-0ubuntu7'])

    def test_version_compare(self):
        self.repositories = Repositories()

        vers = ['1.0.0', '1.0.1',
                '0.5.7', '0.20',
                '0.6.15-2ubuntu9', '0.6.15-2ubuntu10',
                '0.6.15-2ubuntu9', '0.6.17-2ubuntu9',
                '2.2.3.dfsg.1-2build1', '2.2.3.dfsg.1-2build2',
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

        self.assertEqual(self.repositories.ver_cmp(vers[8], vers[9]), -1)
        #
        self.assertEqual(self.repositories.ver_cmp(vers[10], vers[10]), 0)

    def test_version_parsing(self):
        self.repositories = Repositories()

        vers = [
            "1.024~beta1+svn234",
            "1",
            "0.6.15-2ubuntu9",
            "0.6.15-2ubuntu9.1",
            "0.20",
            "0.21.1",
            "0.1.1-1ubuntu2.1212",
            "3.113+nmu3ubuntu3",
            "1:2.0.18-1ubuntu1",
            "20100513-3.1ubuntu1",
            "1.20120910-2",
            "2.2.3.dfsg.1-2build1",
            "0.3.1~ubuntu4",
            "0.9.0-3+wheezy1",
            "0.9.7.7ubuntu4",
            "1.2.10~pre3-2",
            ]

        # first two
        for i in vers:
            self.assertEqual(self.repositories.ver_cmp(i, i), 0)

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

    def test_get_repositories_by_label(self):
        self.repositories = Repositories()

        # create the demo repo
        data = {}
        data['name'] = 'Repo1'
        data['label'] = 'main'
        data['uri'] = 'http://www.software.repo'
        data['provider'] = 'apt'
        repo_id = self.repositories.create_repository(data)

        data = {}
        data['name'] = 'Repo2'
        data['label'] = 'main'
        data['uri'] = 'http://www.software.repo'
        data['provider'] = 'apt'
        repo_id = self.repositories.create_repository(data)

        data = {}
        data['name'] = 'Repo3'
        data['label'] = 'mirror'
        data['uri'] = 'http://mirror.repo'
        data['provider'] = 'apt'
        repo_id = self.repositories.create_repository(data)

        repo_list = self.repositories.get_repositories_by_label('main')

        self.assertIsInstance(repo_list, list)
        self.assertEqual(len(repo_list), 2)
        self.assertEqual(repo_list[0].name, 'Repo1')

    def test_load_config(self):
        yml = """
        repositories:
          - name: Ubuntu
            url: http://de.archive.ubuntu.com/ubuntu/dists/precise/main/binary-amd64/Packages.gz
            label: ubuntu
            provider: apt
          - name: Cloud
            url: http://ubuntu-cloud.archive.canonical.com/ubuntu/dists/precise-proposed/icehouse/main/binary-amd64/Packages.gz
            label: mirror
            provider: apt
        """

        config = io.StringIO(initial_value=yml)

        repoyaml = Repositories.load_config(stream=config)

        self.assertIsNotNone(repoyaml)
        self.assertIsInstance(repoyaml, list)

        self.assertEqual(len(repoyaml), 2)

if __name__ == '__main__':
    unittest.main()

