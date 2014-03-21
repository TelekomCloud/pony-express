import json
import uuid
from nose.tools import *

from .test_server import *


class BasicTestCaseV1(TestServerBase):

    def content_type_must_eq(self, response, t):
        self.assertEqual(response.headers['Content-Type'], t)

    def request_json(self, path, method = "get", status_code = 200, data = None ):
        # get the request method (get/post/put...) from the method string
        req = getattr(self.client, method)
        # before sending the request, determine if you add data to it
        data_methods = ["post", "put", "patch"]
        if method in data_methods:
            r = req(path, data=data)
        else:
            r = req(path)
        # assert the response code
        self.assertEqual(r.status_code, status_code)
        # assert the response type
        self.content_type_must_eq(r, 'application/json')
        # return the json response
        return json.loads(r.data.decode("utf-8"))

    def get_json(self, path):
        return self.request_json(path, "get", 200)

    def testRequestNodesEmpty(self):
        j = self.get_json('/v1/nodes')
        eq_(j, [])

    def testRequestNodesOne(self):
        self.addNode(self.DATA1)
        j = self.get_json('/v1/nodes')
        eq_(type(j[0]), dict)
        eq_(j[0]['id'], self.DATA1['node'])

    def testRequestNode(self):
        self.addNode(self.DATA_E)
        j = self.get_json('/v1/node/' + self.DATA_E['node'])
        eq_(type(j), dict)
        eq_(j['packages'], [])

    def testRequestNodePackages(self):
        self.addNode(self.DATA2)
        j = self.get_json('/v1/node/' + self.DATA2['node'])
        eq_(type(j), dict)

        ps = j['packages']
        eq_(type(ps), list)
        eq_(len(ps), 2)

        package = ps[0]
        eq_(type(package), dict)
        eq_(package['id'], self.DATA2['packages'][0]['sha256'])

    def testRequestPackages(self):
        self.addNode(self.DATA2)
        self.addNode(self.DATA3)
        p = self.DATA2['packages'][0]
        j = self.get_json('/v1/packages?filter=node2')
        eq_(type(j), list)
        #eq_(len(j), 2)

        eq_(j[0]["name"], p["name"])
        eq_(type(j[0]["versions"]), list)
        eq_(len(j[0]["versions"]), 2)
        eq_(j[0]["versions"][0]["id"], p["sha256"])

    def testRequestPackageInfo(self):
        self.addNode(self.DATA2)
        p = self.DATA2['packages'][0]
        j = self.get_json('/v1/package/' + p['sha256'])
        eq_(type(j), dict)

        eq_(j["name"], p["name"])
        eq_(j["uri"], p["uri"])
        eq_(j["summary"], p["summary"])
        eq_(j["version"], p["version"])
        eq_(j["architecture"], p["architecture"])
        eq_(j["id"], p["sha256"])
        eq_(j["provider"], p["provider"])

        eq_(type(j['nodes']), list)
        eq_(len(j['nodes']), 1)
        eq_(type(j['nodes'][0]), dict)
        eq_(j['nodes'][0]['id'], 'node2')

    def testCreateMirror(self):
        m = self.MIRROR1
        j = self.request_json('/v1/mirrors', 'post', data = m, status_code = 201)

        eq_(j["id"], m["id"])
        eq_(j["url"], m["url"])
        eq_(j["label"], m["label"])

    def testReadMirrorsEmpty(self):
        j = self.get_json('/v1/mirrors')
        eq_(type(j), list)

    def testReadMirrors(self):
        self.addMirror(self.MIRROR1)
        m = self.MIRROR1
        j = self.get_json('/v1/mirrors')
        eq_(type(j), list)
        eq_(len(j), 1)

        eq_(j[0]["id"], m["id"])
        eq_(j[0]["url"], m["url"])
        eq_(j[0]["label"], m["label"])

    def testUpdateMirror(self):
        self.addMirror(self.MIRROR1)
        m = self.MIRROR1
        # create a new random label
        label = str(uuid.uuid4())
        update_data = {
            "id" : m["id"],
            "label" : label
        }
        # send the request to update this mirror with the new data
        j = self.request_json('/v1/mirrors', 'patch', data = update_data, status_code = 200)

        # check if the response of this update has the new data
        eq_(j["id"], m["id"])
        eq_(j["label"], label)

        # check if the get requests also have the update
        j = self.get_json('/v1/mirrors')
        eq_(type(j), list)
        eq_(len(j), 1)
        eq_(j[0]["id"], m["id"])
        eq_(j[0]["url"], m["url"])
        eq_(j[0]["label"], label)

    def testDeleteMirror(self):
        self.addMirror(self.MIRROR1)
        m = self.MIRROR1
        # send the request to remove this mirror
        j = self.request_json('/v1/mirror/'+m["id"], 'delete', status_code = 204)
