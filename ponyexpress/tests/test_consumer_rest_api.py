import json
import nose
from nose.tools import *

from .test_server import *


class BasicTestCaseV1(TestServerBase):
    DATA = {
        'node1': {
            'id': 'my1.full.fqdn',
            'packages': []
        },
        'node2': {
            'id': 'my2.full.fqdn',
            'packages': [
                {
                    "name": "accountsservice",
                    "uri": "http://us.archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_0.6.15-2ubuntu9_amd64.deb",
                    "summary": "query and manipulate user account information",
                    "version": "0.6.15-2ubuntu9",
                    "architecture": "amd64",
                    "sha256": "5d8e40ce35ea30f621573d40b17dcd21e3b974f2dd5e096c6c10701af8cdc5d0",
                    "provider": "apt",
                    "archive": "precise"
                }
            ]
        }
    }

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
        self.addNode(self.DATA['node1'])
        j = self.get_json('/v1/nodes')
        eq_(type(j['node1']), dict)

    def testRequestNode(self):
        self.addNode(self.DATA['node1'])
        j = self.get_json('/v1/node/' + self.DATA['node1']['id'])
        eq_(type(j), dict)
        eq_(j['packages'], [])

    def testRequestNodePackages(self):
        self.addNode(self.DATA['node2'])
        j = self.get_json('/v1/node/' + self.DATA['node2']['id'])
        eq_(type(j), dict)

        ps = j['packages']
        eq_(type(ps), list)
        eq_(len(ps), 1)

        package = ps[0]
        eq_(type(package), dict)
        eq_(package['id'], self.DATA['node2']['packages'][0]['sha256'])

    def testRequestPackages(self):
        self.addNode(self.DATA['node2'])
        p = self.DATA['node2']['packages'][0]
        j = self.get_json('/v1/packages')
        eq_(type(j), list)
        eq_(len(j), 1)
        eq_(j[0]["id"], p["sha256"])

    def testRequestPackageInfo(self):
        self.addNode(self.DATA['node2'])
        p = self.DATA['node2']['packages'][0]
        j = self.get_json('/v1/package/' + p['sha256'])
        eq_(type(j), dict)
        eq_(j["name"], p["name"])
        eq_(j["uri"], p["uri"])
        eq_(j["summary"], p["summary"])
        eq_(j["version"], p["version"])
        eq_(j["architecture"], p["architecture"])
        eq_(j["sha256"], p["sha256"])
        eq_(j["provider"], p["provider"])
        eq_(j["archive"], p["archive"])
