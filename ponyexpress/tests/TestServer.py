# -*- coding: utf-8 -*-

import unittest
import ponyexpress

#=================================
# TODO, we will stub this for now
#=================================

class TestServer:

    def setUp(self):
        # TODO: configure database        
        self.app = ponyexpress.app.test_client()

    def tearDown(self):
        # TODO: cleanup
        pass

    def app(self):
        return self.app