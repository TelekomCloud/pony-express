# -*- coding: utf-8 -*-

import unittest
import json
from ponyexpress import create_app
from ponyexpress.database import db
from ponyexpress.api.lib.package_import import PackageImport
from ponyexpress.api.lib.repositories import Repositories

#=================================
# TODO, we will stub this for now
#=================================


class TestServerBase(unittest.TestCase):

    DATA_E = {
        "node": "node1",
        "packages": [
        ]
    }

    DATA1 = {
        "node": "node1",
        "packages": [
            {
                "name": "openstack-deploy",
                "uri": "http://mirror1/packages/openstack-deploy.1.0.deb",
                "version": "1.0",
                "summary": "OpenStack deployment package",
                "sha256": "29ed26cf3b18b0d9988be08da9086f180f3f01fb",
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
                "sha256": "29ed26cf3b18b0d9988be08da9086f180f3f01fb",
                "provider": "apt",
                "architecture": "amd64",
            },
            {
                "name": "openstack-nova",
                "uri": "http://mirror1/packages/openstack-nova.2013.1.0.deb",
                "version": "2013.1.0",
                "summary": "OpenStack nova package",
                "sha256": "f2ec2e82794591f1ec04d4a31df860390a688fd8",
                "provider": "apt",
                "architecture": "amd64",
            }
        ]
    }

    DATA3 = {
        "node": "node3",
        "packages": [
            {
                "name": "openstack-deploy",
                "uri": "http://mirror1/packages/openstack-deploy.2.0.deb",
                "version": "2.0",
                "summary": "OpenStack deployment package",
                "sha256": "aaed26cf3b18b0d9988be08da9086f180f3f01fb",
                "provider": "apt",
                "architecture": "amd64",
            },
            {
                "name": "openstack-nova",
                "uri": "http://mirror1/packages/openstack-nova.2013.2.0.deb",
                "version": "2013.2.0",
                "summary": "OpenStack nova package",
                "sha256": "bbec2e82794591f1ec04d4a31df860390a688fd8",
                "provider": "apt",
                "architecture": "amd64",
            }
        ]
    }

    MIRROR1 = {
        "name": "Magus Repository",
        "label": "live",
        "uri": "http://archive.canonical.com/ubuntu/dists/maverick/partner/i386/binary-i386/Packages.gz",
        "provider": "apt"
    }

    def setUp(self):
        """
        Set test environment and load test config
        """

        app = create_app()

        app.config['TESTING'] = True
        app.config.from_object('ponyexpress.config.configuration.TestingConfig')

        # Init the Flask test client
        # This is not the ponyexpress app object
        self.client = app.test_client()

        # Create all database tables, uses an in-memory sqlite database
        with app.app_context():
            db.app = app
            db.create_all(app=app)

    def tearDown(self):
        """
        Tear down the test case
        """

        # Clean the db sessions
        db.session.remove()

        # Drop the db
        db.drop_all()

    def addNode(self, node_dict):
        """A method to add nodes for test purposes"""

        test_import = PackageImport()
        test_import.process_node_info(node_dict)

    def addMirror(self, mirror_dict):
        """A method to add mirrors for test purposes"""

        handler = Repositories()
        return handler.create_repository( mirror_dict )

    def process_data(self, filename):
        json_data = open(filename)

        data = json.load(json_data)
        json_data.close()

        return data
