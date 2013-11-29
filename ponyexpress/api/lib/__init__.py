from ponyexpress.database import db
from ponyexpress.models.package import Package
from ponyexpress.models.node import Node


def process_node_info(request_json):
    node = Node.query.filter_by(name=request_json['node']).first()

    if not node:
        # Add node
        node = Node(request_json['node'])
        db.session.add(node)
        db.session.commit()

        #add the packages
        if request_json['packages']:
            for package in request_json['packages']:
                if 'sha256' in package.keys():
                    # Package sha must be uniqe, so fetch the first object
                    p = Package.query.filter_by(sha=package['sha256']).first()
                    if p:
                        node.packages.append(p)
                        db.session.commit()
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
    else:
        #prepare sha dict
        pp = {}

        for p in request_json['packages']:
            if 'sha256' in p.keys():
                sha = p['sha256']
                pp[sha] = p

        for package in node.packages:
            if package.sha in pp.keys():
                pp.pop(package.sha)
            else:
                node.packages.remove(package)
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


