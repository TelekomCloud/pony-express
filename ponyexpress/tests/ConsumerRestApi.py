import json
import nose
from nose.tools import *

from .TestServer import *

class BasicTestCaseV1(TestServerBase):

    DATA = {
      'node1': {
        'id': 'my1.full.fqdn',
        'packages' : []
      }
    }

    def content_type_must_eq(self, response, t):
        self.assertEqual(response.headers['Content-Type'], t)

    def get_json(self, path):
        r = self.app.get(path)
        self.content_type_must_eq(r,'application/json')
        self.assertEqual(rv.status_code,200)
        return json.loads(rv.data)

    def testRequestNodesEmpty(self):
        j = self.get_json('/v1/nodes')
        eq_( j, [] )

    def testRequestNodesOne(self):
        self.addNode(self.DATA['node1'])
        j = self.get_json('/v1/nodes')
        eq_( type( j['node1'] ), dict )

    def testRequestNode(self):
        self.addNode(self.DATA['node1'])
        j = self.get_json('/v1/node/'+self.DATA['node1']['id'])
        eq_( type( j ), dict )
        eq_( r['packages'], [] )
