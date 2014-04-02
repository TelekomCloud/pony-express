import hashlib
from datetime import date
from ponyexpress.database import db
from ponyexpress.models.package import Package
from ponyexpress.models.node import Node
from ponyexpress.models.package_history import PackageHistory


class PackageImport:

    def __init__(self):
        pass

    def store_history(self, node, package):
        # track package installation time separately
        hist = PackageHistory(node.name, package.sha, package.name, package.version, package.uri,
                              date.today())
        db.session.add(hist)
        db.session.commit()

    def create_package(self, node, package):
        p = Package.query.filter_by(sha=package['sha256']).first()
        if p:
            node.packages.append(p)
            db.session.commit()

            self.store_history(node, p)
        else:
            new_package = Package(package['sha256'], package['name'], package['version'])

            # Set extended attributes as well
            new_package.uri = package['uri']
            new_package.architecture = package['architecture']
            new_package.provider = package['provider']
            new_package.summary = package['summary']

            node.packages.append(new_package)

            db.session.add(new_package)
            db.session.commit()

            self.store_history(node, new_package)

    def process_node_info(self, request_json):
        node = Node.query.filter_by(name=request_json['node']).first()

        if not node:
            # Add node
            node = Node(request_json['node'])
            db.session.add(node)
            db.session.commit()

            #add the packages
            if request_json['packages']:
                for package in request_json['packages']:
                    if 'sha256' in package.keys() and package['sha256'] != '':
                        # Package sha must be uniqe, so fetch the first object
                        self.create_package(node, package)
                    else:
                        if 'name' in package.keys() and 'version' in package.keys():
                            hash_contents = ( package['name'] + package['version'] ).encode('utf-8')
                            sha = hashlib.sha256(hash_contents)
                            package['sha256'] = sha.hexdigest()
                            self.create_package(node, package)
        else:
            #prepare sha dict
            pp = {}

            for p in request_json['packages']:
                if 'sha256' in p.keys():
                    sha = p['sha256']
                    pp[sha] = p

            to_remove = []
            for package in node.packages:
                if package.sha in pp.keys():
                    pp.pop(package.sha)
                else:
                    # Remove the association
                    to_remove.append(package)

            if to_remove:
                for r in to_remove:
                    node.packages.remove(r)
                db.session.commit()

            # Now we have a list of packages which have been updated
            # Figure out if we need to update
            for p in pp:
                np = pp[p]

                new_package = Package(p, np['name'], np['version'])

                # Set extended attributes as well
                new_package.uri = np['uri']
                new_package.architecture = np['architecture']
                new_package.provider = np['provider']
                new_package.summary = np['summary']

                node.packages.append(new_package)
                db.session.commit()

                self.store_history(node, new_package) # pass in the dict and not the node object
