import json
import nose
from nose.tools import *

from .TestServer import *

class BasicTestCaseV1(TestServerBase):

    def content_type_must_eq(self, response, t):
        self.assertEqual(response.headers['Content-Type'], t)

    def testRequestNodes(self):
        r = self.app.get('/v1/nodes')
        self.content_type_must_eq(r,'application/json')
        self.assertEqual(rv.status_code,200)

        resp = json.loads(rv.data)
        self.assertEqual(resp["email"],"User1@User1.com")
        self.assertEqual(resp["first_name"],"User1First")
        self.assertEqual(resp["last_name"],"User1Last")

