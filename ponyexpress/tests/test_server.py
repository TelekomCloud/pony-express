# -*- coding: utf-8 -*-

import unittest
from ponyexpress import *
from ponyexpress.database import db

#from ponyexpress.models.package import Package
#from ponyexpress.models.node import Node

#=================================
# TODO, we will stub this for now
#=================================


class TestServerBase(unittest.TestCase):

    def setUp(self):
        # Set test environment and load test config

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
        # Clean the db sessions
        db.session.remove()

        # Drop the db
        db.drop_all()
        pass

    def addNode(self, node_dict):
        # TODO: a method to add nodes for test purposes
        #ponyexpress.api.lib.process_node_import(node_dict)
        pass
