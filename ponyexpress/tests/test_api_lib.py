import json
import nose
from nose.tools import *

from .test_server import *

from ponyexpress.api.lib import *

from ponyexpress.models.node import Node
from ponyexpress.models.package import Package

DATA1 = {
    "node": "node1",
    "packages": [
        {
            "name": "openstack-deploy",
            "uri": "http://mirror1/packages/openstack-deploy.1.0.deb",
            "version": "1.0",
            "summary": "OpenStack deployment package",
            "sha": "29ed26cf3b18b0d9988be08da9086f180f3f01fb",
            "provider": "apt",
            "architecture": "amd64",
        }
    ]
}

DATA2 = {
    "node": "node2",
    "packages": [
        {
            "name": "openstack-deploy",
            "uri": "http://mirror1/packages/openstack-deploy.1.0.deb",
            "version": "1.0",
            "summary": "OpenStack deployment package",
            "sha": "29ed26cf3b18b0d9988be08da9086f180f3f01fb",
            "provider": "apt",
            "architecture": "amd64",
        },
        {
            "name": "openstack-nova",
            "uri": "http://mirror1/packages/openstack-nova.2013.1.0.deb",
            "version": "2013.1.0",
            "summary": "OpenStack nova package",
            "sha": "f2ec2e82794591f1ec04d4a31df860390a688fd8",
            "provider": "apt",
            "architecture": "amd64",
        }
    ]
}

DATA_UPDATE1 = {
    "node": "node1",
    "packages": [
        {
            "name": "openstack-deploy",
            "uri": "http://mirror1/packages/openstack-deploy.1.0.deb",
            "version": "1.0",
            "summary": "OpenStack deployment package",
            "sha": "29ed26cf3b18b0d9988be08da9086f180f3f01fb",
            "provider": "apt",
            "architecture": "amd64",
        },
    ]
}

DATA_UPDATE2 = {
    "node": "node2",
    "packages": [
        {
            "name": "openstack-deploy",
            "uri": "http://mirror1/packages/openstack-deploy.2.0.deb",
            "version": "2.0",
            "summary": "OpenStack deployment package",
            "sha": "48a8d2c951f269661d943ed8b0ee355e42d675de",
            "provider": "apt",
            "architecture": "amd64",
        },
    ]
}

DATA_UPDATE3 = {
    "node": "node1",
    "packages": [
        {
            "name": "openstack-deploy",
            "uri": "http://mirror1/packages/openstack-deploy.1.1.deb",
            "version": "1.1",
            "summary": "OpenStack deployment package",
            "sha": "29ed26cf3b18b0d9988be08da9086f180f3f01fb",
            "provider": "apt",
            "architecture": "amd64",
        },
    ]
}

class TestAPILibrary(TestServerBase):
    def test_node_import_empty(self):
        """Test importing a new node"""

        process_node_info(DATA1)

        assert Node.query.count() == 1
        assert Package.query.count() == 1

    def test_node_import_update(self):
        """Test importing a node which exists in the db"""

        process_node_info(DATA1)

        assert Node.query.count() == 1
        assert Package.query.count() == 1

        node = Node.query.first()

        assert node.packages.count() == 1

        # Reimport data to simulate subsequent updates
        process_node_info(DATA1)

        assert Node.query.count() == 1
        assert Package.query.count() == 1

        node = Node.query.first()

        assert node.packages.count() == 1

    def test_node_import_2nodes(self):
        """Test importing a node which exists in the db"""

        process_node_info(DATA1)

        assert Node.query.count() == 1
        assert Package.query.count() == 1

        node = Node.query.first()

        assert node.packages.count() == 1

        # Reimport data to simulate subsequent updates
        process_node_info(DATA2)

        assert Node.query.count() == 2
        assert Package.query.count() == 2

        nodes = Node.query.all()

        assert len(nodes) == 2

    def test_node_import_package_update(self):
        """Test importing a node which exists in the db"""

        process_node_info(DATA_UPDATE1)

        # Reimport data to simulate subsequent updates
        process_node_info(DATA_UPDATE1)

        assert Node.query.count() == 1
        assert Package.query.count() == 1

        process_node_info(DATA_UPDATE2)

        nodes = Node.query.all()
        assert len(nodes) == 2

        packages = Package.query.all()

        # There need to be two packages stored in the db
        assert len(packages) == 2

        package = Package.query.filter_by(sha='48a8d2c951f269661d943ed8b0ee355e42d675de').first()

        assert package.name == 'openstack-deploy'
        assert package.version == '2.0'

        node = Node.query.filter_by(name='node2').first()

        assert node.name == 'node2'
        assert node.packages.count() == 1
        assert node.packages[0].version == '2.0'

        node = Node.query.filter_by(name='node1').first()

        assert node.name == 'node1'
        assert node.packages.count() == 1
        assert node.packages[0].version == '1.0'


if __name__ == '__main__':
    unittest.main()
