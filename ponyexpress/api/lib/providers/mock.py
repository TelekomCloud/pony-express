
from ponyexpress.api.lib.providers import Provider


class MockRepository(Provider):
    data = {'5d8e40ce35ea30f621573d40b17dcd21e3b974f2dd5e096c6c10701af8cdc5d0': {
            "package": "accountsservice",
            "filename": "http://us.archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_0.6.15-2ubuntu9_amd64.deb",
            "description": "query and manipulate user account information",
            "version": "0.6.15-2ubuntu9",
            "architecture": "amd64",
            "sha256": "5d8e40ce35ea30f621573d40b17dcd21e3b974f2dd5e096c6c10701af8cdc5d0"
        },
    }

    #
    def __init__(self, data=None):
        if data is not None:
            self.data = data

    def set_url(self, url):
        pass

    def fetch_metadata(self):
        return self.data
