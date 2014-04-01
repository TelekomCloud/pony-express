import unittest

from ponyexpress.api.lib.providers.apt import AptMirror


class TestAptMirror(unittest.TestCase):

    def setUp(self):
        """
        Set test environment and load test config
        """
        self.aptmirror = AptMirror()
        self.aptmirror.set_url('http://us.archive.ubuntu.com/ubuntu/dists/precise/main/binary-amd64/Packages.gz')

    def test_fetch_metadata(self):
        """Test package list downloading"""
        metadata = self.aptmirror.fetch_metadata()

        self.assertIsNotNone(metadata, 'Metadata must not be None')
        self.assertIsNot(metadata, {}, 'Metadata can not be empty')


if __name__ == '__main__':
    unittest.main()

