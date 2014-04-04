import os

from .test_server import *

from ponyexpress.api.lib.mirrors import Mirrors
from ponyexpress.models.mirror import Mirror
from ponyexpress.api.lib.package_import import PackageImport

from ponyexpress.models.mirror_history import MirrorHistory


class TestMirrors(TestServerBase):

    def test_update_mirror(self):
        """Test package list downloading"""

        self.mirrors = Mirrors()

        mirror = Mirror()
        mirror.id = 1
        mirror.provider = 'apt'
        mirror.name = 'Test'
        mirror.uri = 'http://de.archive.ubuntu.com/ubuntu/dists/precise/main/binary-amd64/Packages.gz'
        mirror.label = 'Test'

        path = os.path.dirname(__file__)
        datafile = os.path.join(path, 'data/install_tiny.txt')
        data_install = self.process_data(datafile)

        test_importer = PackageImport()
        test_importer.process_node_info(data_install)

        self.mirrors.update_mirror(mirror)

        self.assertGreater(MirrorHistory.query.count(), 1)

    def test_get_outdated_packages(self):
        self.mirrors = Mirrors()

        mirror = Mirror()
        mirror.id = 1
        mirror.provider = 'apt'
        mirror.name = 'Test'
        mirror.uri = 'http://de.archive.ubuntu.com/ubuntu/dists/precise/main/binary-amd64/Packages.gz'
        mirror.label = 'Test'

        path = os.path.dirname(__file__)
        datafile = os.path.join(path, 'data/install_tiny.txt')
        data_install = self.process_data(datafile)

        test_importer = PackageImport()
        test_importer.process_node_info(data_install)

        self.mirrors.update_mirror(mirror)

        self.assertGreater(MirrorHistory.query.count(), 5000)

        packages = self.mirrors.get_outdated_packages('ponyexpress', mirror)

        self.assertIsNotNone(packages)
        self.assertNotEqual(packages, [])

        self.assertEqual(packages[0].pkgversion, '3.113ubuntu1')
        self.assertEqual(packages[0].upstream_version, '3.113ubuntu2')

    def test_version_compare(self):
        self.mirrors = Mirrors()

        vers = ['1.0.0', '1.0.1',
                '0.5.7', '0.20',
                '0.6.15-2ubuntu9', '0.6.15-2ubuntu10',
                '0.6.15-2ubuntu9', '0.6.17-2ubuntu9',
                '0.1.1-1ubuntu1'
        ]

        # first two
        self.assertEqual(self.mirrors.ver_cmp(vers[0], vers[1]), -1)

        # third and fourth
        self.assertEqual(self.mirrors.ver_cmp(vers[2], vers[3]), 1)

        # with ubuntu string
        self.assertEqual(self.mirrors.ver_cmp(vers[4], vers[5]), 1)

        #with ubuntu, upstream version change
        self.assertEqual(self.mirrors.ver_cmp(vers[6], vers[7]), -1)

        #
        self.assertEqual(self.mirrors.ver_cmp(vers[8], vers[8]), 0)


if __name__ == '__main__':
    unittest.main()

