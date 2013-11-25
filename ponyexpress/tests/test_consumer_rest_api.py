import json
from nose.tools import *

from .test_server import *


class BasicTestCaseV1(TestServerBase):

    def content_type_must_eq(self, response, t):
        self.assertEqual(response.headers['Content-Type'], t)

    def get_json(self, path):
        r = self.client.get(path)
        self.content_type_must_eq(r, 'application/json')
        self.assertEqual(r.status_code, 200)
        return json.loads(r.data)

    def testRequestNodesEmpty(self):
        j = self.get_json('/v1/nodes')
        eq_(j, [])

    def testRequestNodesOne(self):
        self.addNode(self.DATA1)
        j = self.get_json('/v1/nodes')
        eq_(type(j[0]), dict)
        eq_(j[0]['id'], self.DATA1['node'])

    def testRequestNode(self):
        self.addNode(self.DATA1)
        j = self.get_json('/v1/node/' + self.DATA1['node'])
        eq_(type(j), dict)
        eq_(j['packages'], [])

    def testRequestNodePackages(self):
        self.addNode(self.DATA2)
        j = self.get_json('/v1/node/' + self.DATA2['node'] + '/full')
        eq_(type(j), dict)

        ps = j['packages']
        eq_(type(ps), list)
        eq_(len(ps), 2)

        package = ps[0]
        eq_(type(package), dict)
        eq_(package['id'], self.DATA2['packages'][0]['sha'])

    def testRequestPackages(self):
        self.addNode(self.DATA2)
        p = self.DATA2['packages'][0]
        j = self.get_json('/v1/packages')
        eq_(type(j), list)
        eq_(len(j), 1)
        eq_(j[0]["id"], p["sha"])

    def testRequestPackageInfo(self):
        self.addNode(self.DATA2)
        p = self.DATA2['packages'][0]
        j = self.get_json('/v1/package/' + p['sha'])
        eq_(type(j), dict)
        eq_(j["name"], p["name"])
        eq_(j["uri"], p["uri"])
        eq_(j["summary"], p["summary"])
        eq_(j["version"], p["version"])
        eq_(j["architecture"], p["architecture"])
        eq_(j["id"], p["id"])
        eq_(j["provider"], p["provider"])
        eq_(j["archive"], p["archive"])
