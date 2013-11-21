# -*- coding: utf-8 -*-

import unittest
import ponyexpress

#=================================
# TODO, we will stub this for now
#=================================

class TestServerBase(unittest.TestCase):

    def setUp(self):
        # TODO: configure database        
        self.app = ponyexpress.app.test_client()

    def tearDown(self):
        # TODO: cleanup
        pass

    def addNode(self, node_dict):
        # TODO: a method to add nodes for test purposes
        pass