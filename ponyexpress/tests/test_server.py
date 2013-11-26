# -*- coding: utf-8 -*-

import unittest
from ponyexpress import *
from ponyexpress.api.lib import *

#=================================
# TODO, we will stub this for now
#=================================


class TestServerBase(unittest.TestCase):

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

    DATA3 = {
        "node": "node3",
        "packages": [
            {
                "name": "openstack-deploy",
                "uri": "http://mirror1/packages/openstack-deploy.2.0.deb",
                "version": "2.0",
                "summary": "OpenStack deployment package",
                "sha": "aaed26cf3b18b0d9988be08da9086f180f3f01fb",
                "provider": "apt",
                "architecture": "amd64",
            },
            {
                "name": "openstack-nova",
                "uri": "http://mirror1/packages/openstack-nova.2013.2.0.deb",
                "version": "2013.2.0",
                "summary": "OpenStack nova package",
                "sha": "bbec2e82794591f1ec04d4a31df860390a688fd8",
                "provider": "apt",
                "architecture": "amd64",
            }
        ]
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

        # Add some sample data
        process_node_info(self.DATA1)

        process_node_info(self.DATA3)

        process_node_info(node_dict)
