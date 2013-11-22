from ponyexpress.database import db
from ponyexpress.models.package import Package
from ponyexpress.models.node import Node


def process_node_info(request_json):
    node = Node.query.filter_by(name=request_json['node']).first()

    if not node:
        # Add node
        node = Node(request_json['node'])
        db.session.add(node)

        #add the packages
        for package in request_json['packages']:
            if 'sha' in package.keys():
                new_package = Package(package['sha'], package['name'], package['version'])

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
            if 'sha' in p.keys():
                sha = p['sha']
                pp[sha] = p

        # Verify package version
        for package in node.packages:
            if package.sha in pp.keys():
                # we already know the sha, so same package
                # verify if this packages
                pass
            else:
                pass
