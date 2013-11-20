from Helper import *

class BasicTestCase(unittest.TestCase, TestServer):

    def testSuccess(self): 
        self.failUnlessEqual(1,1)