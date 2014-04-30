import json
import uuid
from nose.tools import *

from .test_server import *

from ponyexpress.api.lib.providers import MockRepository

class BasicTestCaseV1(TestServerBase):

    def prepare_repo_data(self, packagedata=None):
        # create the demo repo
        data = {}
        data['name'] = 'Repo1'
        data['label'] = 'main'
        data['uri'] = 'http://de.archive.ubuntu.com/ubuntu/dists/precise/main/binary-amd64/Packages.gz'
        data['provider'] = 'apt'

        repo = self.addRepository(data)
        provider = MockRepository(packagedata)

        self.updateRepository(repo, provider)

    def content_type_must_eq(self, response, t):
        self.assertEqual(response.headers['Content-Type'], t)

    def request_json(self, path, method = "get", status_code = 200, data = None ):
        # get the request method (get/post/put...) from the method string
        req = getattr(self.client, method)
        # before sending the request, determine if you add data to it
        data_methods = ["post", "put", "patch"]
        if method in data_methods:
            d = json.dumps( data )
            r = req(path, data=d, content_type='application/json')
        else:
            r = req(path)
        # assert the response code
        self.assertEqual(r.status_code, status_code)
        # assert the response type
        self.content_type_must_eq(r, 'application/json')
        # return the json response
        data = r.data.decode("utf-8")
        ret = json.loads(data) if len(data) > 0 else ''
        return ret

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
        j = self.get_json('/v1/packages')
        eq_(type(j), list)

        eq_(j[0]["name"], p["name"])
        eq_(type(j[0]["versions"]), list)
        eq_(len(j[0]["versions"]), 2)
        eq_(j[0]["versions"][0]["id"], p["sha256"])

    def testRequestPackagesWithFilter(self):
        self.addNode(self.DATA2)
        self.addNode(self.DATA3)
        p = self.DATA2['packages'][0]
        j = self.get_json('/v1/packages?filter=node2')
        eq_(type(j), list)

        eq_(j[0]["name"], p["name"])
        eq_(type(j[0]["versions"]), list)
        eq_(len(j[0]["versions"]), 2)
        eq_(j[0]["versions"][0]["id"], p["sha256"])

    def testRequestPackagesWithMultipleRepos(self):
        self.addNode(self.DATA1)

        data = {'29ed26cf3b18b0d9988be08da9086f180f3f01fb': {
                "package": "openstack-deploy",
                "filename": "http://repo/pool/main/o/openstack-deploy/openstack-deploy.deb",
                "description": "query and manipulate user account information",
                "version": "2.0",
                "architecture": "amd64",
                "sha256": "29ed26cf3b18b0d9988be08da9086f180f3f01fb"
            },
        }

        self.prepare_repo_data(data)

        j = self.get_json('/v1/packages?outdated=true&repo=1,2')
        self.assertIsInstance(j, list)

        self.assertIsInstance(j[0]['versions'], list)
        self.assertEqual(j[0]["upstream"][0], '2.0')

    def testRequestPackagesWithLabel(self):
        self.addNode(self.DATA1)

        data = {'29ed26cf3b18b0d9988be08da9086f180f3f01fc': {
                "package": "openstack-deploy",
                "filename": "http://repo/pool/main/o/openstack-deploy/openstack-deploy.deb",
                "description": "query and manipulate user account information",
                "version": "2.0",
                "architecture": "amd64",
                "sha256": "29ed26cf3b18b0d9988be08da9086f180f3f01fc"
            },
        }

        self.prepare_repo_data(data)

        j = self.get_json('/v1/packages?outdated=true&repolabel=main')
        self.assertIsInstance(j, list)

        self.assertIsInstance(j[0]['versions'], list)
        self.assertEqual(j[0]["upstream"][0], '2.0')

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

    def testCreateRepository(self):
        m = self.REPO1
        j = self.request_json('/v1/repositories', 'post', data = m, status_code = 201)

        self.assertNotEqual(j["id"], None)
        eq_(j["uri"], m["uri"])
        eq_(j["label"], m["label"])

    def testReadRepositoriesEmpty(self):
        j = self.get_json('/v1/repositories')
        eq_(type(j), list)

    def testReadRepositories(self):
        id = self.addRepository(self.REPO1)

        m = self.REPO1
        j = self.get_json('/v1/repositories')
        eq_(type(j), list)
        eq_(len(j), 1)

        eq_(j[0]["id"], id.id)
        eq_(j[0]["name"], m["name"])
        eq_(j[0]["uri"], m["uri"])
        eq_(j[0]["label"], m["label"])
        eq_(j[0]["provider"], m["provider"])

    def testUpdateRepository(self):
        id = self.addRepository(self.REPO1)
        m = self.REPO1

        # create a new random label
        label = str(uuid.uuid4())
        update_data = {
            "label": label
        }

        # send the request to update this repository with the new data
        j = self.request_json('/v1/repositories/'+str(id.id), 'patch', data=update_data, status_code=200)

        # check if the response of this update has the new data
        eq_(j["id"], id.id)
        eq_(j["label"], label)

        # check if the get requests also have the update
        j = self.get_json('/v1/repositories')
        eq_(type(j), list)
        eq_(len(j), 1)
        eq_(j[0]["id"], id.id)
        eq_(j[0]["name"], m["name"])
        eq_(j[0]["uri"], m["uri"])
        eq_(j[0]["label"], label)
        eq_(j[0]["provider"], m["provider"])

    def testDeleteRepository(self):
        id = self.addRepository(self.REPO1)
        # send the request to remove this repository
        j = self.request_json('/v1/repositories/'+str(id.id), 'delete', status_code = 204)

    def testUpdateRepositoryMetadata(self):
        id = self.addRepository(self.REPO1)
        m = self.REPO1

        # create a new random label
        repo_data = {
            "repolist": id.id
        }

        # send the request to update this repository with the new data
        j = self.request_json('/v1/updater', 'post', data=repo_data, status_code=200)

        # check if the response of this update has the new data
        self.assertEqual(j["repositories"][0], m['name'])

    def testUpdateRepositoryMetadataLabel(self):
        id = self.addRepository(self.REPO1)
        m = self.REPO1

        # send the request to update this repository with the new data
        j = self.request_json('/v1/updater', 'post', status_code=200)

        # check if the response of this update has the new data
        self.assertEqual(j["repositories"][0], m['name'])
