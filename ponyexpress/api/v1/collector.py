from flask import Blueprint, request, Response
from ponyexpress.api.exceptions import *

from ponyexpress.database import db
from ponyexpress.models.package import Package
from ponyexpress.models.node import Node

collector = Blueprint('collector', __name__)

@collector.route('/v1/collector')
def default():
    raise InvalidAPIUsage('Invalid request method', status_code=400)

@collector.route('/v1/collector', methods=['POST','PUT'])
def dataimport():
    """Import json formated package information from a node.
    Store this information into a database for later querying
    """

    # Safeguard
    if request.method == 'PUT' or request.method == 'POST':

        request_json = request.get_json()

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
            # Verify package version
            for package in node.packages:
                if package in request_json.packages:
                    pass
                else:
                    pass

        #TODO: return node object?
        return Response(status=200)
    else:
        raise InvalidAPIUsage('Invalid request method', status_code=400)
