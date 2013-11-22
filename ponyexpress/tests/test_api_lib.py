import json
import nose
from nose.tools import *

from .test_server import *

from ponyexpress.api.lib import *

from ponyexpress.models.node import Node
from ponyexpress.models.package import Package

DATA = {
    "node": "<nodename>",
    "packages": [
        {
            "name": "<packagename>",
            "uri": "<uri>",
            "version": "<version>",
            "summary": "<summary>",
            "sha": "<sha256>",
            "provider": "[apt|pip|gem|...]",
            "archive": "<precise|...>",
            "architecture": "<i386|amd64>",
        }
    ]
}


class TestAPILibrary(TestServerBase):
    def test_node_import_empty(self):
        """Test importing a new node"""

        process_node_info(DATA)

        assert Node.query.count() == 1
        assert Package.query.count() == 1

    def test_node_import(self):
        """Test importing a node which exists in the db"""

        process_node_info(DATA)

        process_node_info(DATA)

        assert Node.query.count() == 1
        assert Package.query.count() == 1

        node = Node.query.first()

        assert node.packages.count() == 1


if __name__ == '__main__':
    unittest.main()
