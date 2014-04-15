import unittest

from ponyexpress.api.lib.providers.apt import AptRepository


class TestAptRepository(unittest.TestCase):

    def setUp(self):
        """
        Set test environment and load test config
        """
        self.aptrepo = AptRepository('http://us.archive.ubuntu.com/ubuntu/dists/precise/main/binary-amd64/Packages.gz')

    def test_fetch_metadata(self):
        """Test package list downloading"""
        metadata = self.aptrepo.fetch_metadata()

        self.assertIsNotNone(metadata, 'Metadata must not be None')
        self.assertIsNot(metadata, {}, 'Metadata can not be empty')


if __name__ == '__main__':
    unittest.main()

